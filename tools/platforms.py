#!/usr/bin/env python3
"""OS-first TV coverage: offline list/plan; explicit read-only inspect where supported.

Plans are not device-specific safety approvals. No cleanup, pairing or discovery is run.
"""
import argparse
import http.client
import ipaddress
import json
import re
import socket
import sys
import threading
import xml.etree.ElementTree as ET


ROKU_SOURCE = "https://developer.roku.com/docs/developer-program/dev-tools/external-control-api.md"
SAMSUNG_SOURCE = "https://github.com/Gathin23/cleanyourtv/blob/575d73f0f30c329aa7ebaea2bc863943fd9bf7f9/docs/devices/samsung-tizen.md"
# platform: (support tier, manual cleanup, control, debloat, launcher, sources)
PLATFORMS = {
    "android-tv": (
        "existing-android-tools", "Review exact-model examples; snapshot settings before manual changes.",
        "Separate existing ADB tools require explicit authorization; this CLI never invokes them.",
        "Existing disable/restore guards apply; no generic package list is safe for every model.",
        "Existing Android launcher needs SDK 26+ and confirmed Home/rollback checks.",
        ["https://developer.android.com/training/tv"]),
    "google-tv": (
        "existing-android-tools", "Review exact-model Google TV settings and existing examples.",
        "Separate existing ADB tools require explicit authorization; no automatic connection.",
        "Preserve setup/network ownership and protected packages; exact firmware matters.",
        "Existing Android launcher is conditional on Home and setupwraith safety guards.",
        ["https://support.google.com/googletv/"]),
    "fire-os": (
        "manual-guidance", "Use the Fire TV settings UI; record app and privacy settings first.",
        "ADB availability varies by device and firmware; not invoked here.",
        "Android ancestry does not validate Android TV package lists on Fire OS.",
        "No guaranteed Fire TV Home takeover; Android launcher compatibility is not established.",
        ["https://developer.amazon.com/docs/fire-tv/fire-os-overview.html"]),
    "vega-os": (
        "manual-guidance", "Use supported device settings and record original values.",
        "No Vega inspection/control adapter in this CLI.",
        "Vega is not Fire OS or Android; no Android package-disabling workflow.",
        "No system-Home replacement established here.",
        ["https://developer.amazon.com/docs/vega/latest/"]),
    "tizen": (
        "read-only-inspection-fixture-tested", "Use the Samsung UI for removable apps/privacy/startup; menus vary.",
        "Opt-in metadata GET only; no remote keys, websocket, pairing or SDB.",
        "No safe system-app disabling/removal or full restorable backup established.",
        "Custom Tizen apps are not Samsung Home replacements; Android APKs do not apply.",
        [SAMSUNG_SOURCE, "https://developer.samsung.com/smarttv/"]),
    "webos": (
        "manual-guidance", "Use LG app editing and privacy settings; record original settings first.",
        "No webOS network adapter or pairing in this CLI.",
        "No general safe system-app removal; developer mode is not root.",
        "Android launcher does not apply; custom apps do not prove Home replacement.",
        ["https://webostv.developer.lge.com/develop/getting-started/introduction"]),
    "roku": (
        "read-only-inspection-fixture-tested", "Use Roku settings for app removal/privacy; account effects need review.",
        "Opt-in ECP device-info GET only; no keys, discovery, app launch or setting changes.",
        "No shell/system-package debloat; channel management is not system-app removal.",
        "No system-Home replacement established; Android APKs do not apply.",
        [ROKU_SOURCE]),
    "vidaa": (
        "manual-guidance", "Use model/region-specific VIDAA app and privacy settings.",
        "No VIDAA network adapter; identify OS in About, not from the brand.",
        "No validated system debloat or Android package-list compatibility.",
        "No system-Home replacement established here.", ["https://www.vidaa.com/"]),
    "vizio-smartcast": (
        "manual-guidance", "Use Vizio settings and available app/customization options; menus vary.",
        "No SmartCast pairing, token exchange or control adapter here.",
        "No validated system-app disabling/removal; Android tools do not apply.",
        "No system-Home replacement established here.", ["https://support.vizio.com/"]),
    "panasonic-my-home-screen": (
        "manual-guidance", "Use the exact model's My Home Screen manual; Panasonic ships other OS families too.",
        "No My Home Screen network adapter here.",
        "No validated system-app disabling/removal; do not infer Android support.",
        "UI customization is not a system launcher replacement.", ["https://av.jpn.support.panasonic.com/support/global/cs/tv/"]),
    "tvos": (
        "manual-guidance", "Use Apple TV settings for apps/privacy; preserve original settings.",
        "No tvOS pairing or control adapter here.",
        "No system-package debloat; deleting user apps is a separate manual decision.",
        "No supported third-party system-Home replacement established here.",
        ["https://support.apple.com/guide/tv/welcome/tvos"]),
    "unknown": (
        "identification-required", "Stop and read About/model/OS before choosing a guide.",
        "No control or inspection until the OS is identified.",
        "No package lists or Android fallback for an unknown OS.",
        "No launcher recommendation until the exact OS and version are known.",
        ["https://github.com/Gathin23/cleanyourtv"]),
}


def safe_text(value):
    """Retain exact case/spacing but refuse control characters and unbounded metadata."""
    if not value or len(value) > 256 or not value.isprintable():
        raise argparse.ArgumentTypeError("metadata must be 1-256 printable characters")
    return value


def make_plan(platform="unknown", brand=None, model=None, firmware=None):
    tier, manual, control, debloat, launcher, sources = PLATFORMS[platform]
    return {
        "schema_version": 1, "platform": platform, "support_tier": tier,
        "brand": brand, "model": model, "firmware": firmware,
        "evidence": {"model": "user-supplied-unverified" if model else "unknown",
                     "firmware": "user-supplied-unverified" if firmware else "unknown",
                     "cleanup_verified": False, "hardware_tested": False},
        "limits": {"manual_cleanup": manual, "control": control,
                   "debloat": debloat, "launcher": launcher},
        "required_consent": ["Owner approval before any device connection or change.",
                             "Separate approval and original-settings snapshot before manual cleanup."],
        "guide": f"docs/platforms/{platform}.md", "sources": list(sources),
        "next_step": "Read About on the TV; verify exact model, OS and firmware before following the guide.",
        "network_actions": [],
    }


def local_host(value):
    """Only literal RFC1918 IPv4, not the broader ipaddress.is_private category."""
    try:
        ip = ipaddress.IPv4Address(value)
    except ipaddress.AddressValueError:
        raise argparse.ArgumentTypeError("host must be an explicit RFC1918 IPv4 literal") from None
    if str(ip) != value or not any(ip in ipaddress.IPv4Network(net) for net in
                                  ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16")):
        raise argparse.ArgumentTypeError("host must be an explicit RFC1918 IPv4 literal")
    return value


def metadata(value):
    if value is None or value == "" or (isinstance(value, str) and value.casefold() in
                                        ("unknown", "n/a", "null")):
        return None
    if not isinstance(value, str) or len(value) > 256 or not value.isprintable():
        raise ValueError("invalid metadata")
    return value


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate field")
        result[key] = value
    return result


def reject_constant(_):
    raise ValueError("non-JSON constant")


def parse_tizen(body):
    data = json.loads(body.decode("utf-8"), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)
    if not isinstance(data, dict) or not isinstance(data.get("device"), dict):
        raise ValueError("not Samsung metadata")
    device = data["device"]
    if device.get("type") != "Samsung SmartTV" or device.get("OS", "Tizen") != "Tizen":
        raise ValueError("not Samsung metadata")
    model = metadata(device.get("model"))
    if not model:
        raise ValueError("missing model")
    capabilities = {}
    if "TokenAuthSupport" in device:
        token = device["TokenAuthSupport"]
        if type(token) is not bool and (type(token) is not str or token not in ("true", "false")):
            raise ValueError("invalid capability")
        capabilities["token_auth_support"] = token is True or token == "true"
    # The top-level 'version' is the API version, NOT the TV firmware.
    return model, metadata(device.get("firmwareVersion")), capabilities


def parse_roku(body):
    # Decode FIRST: no UTF-16/32 NUL-byte trick may bypass the declaration checks.
    text = body.decode("utf-8-sig")
    if "\x00" in text or "<!DOCTYPE" in text.upper() or "<!ENTITY" in text.upper():
        raise ValueError("unsafe XML")
    declaration = re.match(r"\s*<\?xml\s+([^?]*)\?>", text)
    if declaration:
        encoding = re.search(r'''encoding\s*=\s*['"]([^'"]+)['"]''', declaration[1])
        if encoding and encoding[1].lower() not in ("utf-8", "us-ascii"):
            raise ValueError("unsupported XML encoding")
    root = ET.fromstring(text)
    if root.tag != "device-info" or root.attrib:
        raise ValueError("not Roku metadata")
    fields = {}
    for child in root:
        if child.tag in fields or len(child) or child.attrib:
            raise ValueError("invalid XML field")
        fields[child.tag] = child.text
    if fields.get("vendor-name") not in (None, "Roku"):
        raise ValueError("not Roku metadata")
    model = metadata(fields.get("model-name"))
    if not model:
        raise ValueError("missing model")
    capabilities = {}
    for key in ("is-tv", "supports-ethernet", "supports-private-listening",
                "supports-tv-power-control", "supports-audio-volume-control"):
        if key in fields:
            if fields[key] not in ("true", "false"):
                raise ValueError("invalid capability")
            capabilities[key.replace("-", "_")] = fields[key] == "true"
    return {"model": model, "model_number": metadata(fields.get("model-number")),
            "firmware": metadata(fields.get("software-version")),
            "firmware_build": metadata(fields.get("software-build")),
            "capabilities": capabilities}


def stop_read(sock):
    """A total exchange deadline, including slow-drip headers/body, not just idle timeout."""
    try:
        sock.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass


def inspect_device(platform, host):
    local_host(host)
    if platform not in ("tizen", "roku"):
        raise ValueError("inspection unsupported")
    port, path, accept = ((8001, "/api/v2/", "application/json") if platform == "tizen"
                          else (8060, "/query/device-info", "application/xml"))
    # HTTPConnection is direct: environment proxies are never consulted; redirects are not followed.
    conn = http.client.HTTPConnection(host, port, timeout=3.0)
    deadline = None
    try:
        conn.connect()  # Literal IP only, connect timeout 3s; exchange deadline another 3s.
        deadline = threading.Timer(3.0, stop_read, args=(conn.sock,))
        deadline.daemon = True
        deadline.start()
        conn.request("GET", path, headers={"Accept": accept, "Accept-Encoding": "identity"})
        response = conn.getresponse()
        if response.status != 200:
            raise ValueError("unexpected HTTP status")
        encoding = response.getheader("Content-Encoding", "identity").lower()
        content_type = response.getheader("Content-Type")
        if encoding != "identity":
            raise ValueError("unsupported content encoding")
        if content_type:
            mime = content_type.split(";", 1)[0].strip().lower()
            allowed = ("application/json",) if platform == "tizen" else ("text/xml", "application/xml")
            if mime not in allowed:
                raise ValueError("unexpected content type")
        length = response.getheader("Content-Length")
        if length is not None and (not re.fullmatch(r"[0-9]{1,5}", length) or int(length) > 65536):
            raise ValueError("invalid response size")
        body = response.read(65537)
        if len(body) > 65536 or (length is not None and len(body) != int(length)):
            raise ValueError("invalid response size")
        if platform == "tizen":
            model, firmware, capabilities = parse_tizen(body)
            fields = {"model": model, "firmware": firmware, "capabilities": capabilities}
        else:
            fields = parse_roku(body)
    finally:
        if deadline is not None:
            deadline.cancel()
            deadline.join()
        conn.close()
    return {"schema_version": 1, "platform": platform, **fields,
            "evidence": {"inspection": "protocol-fixture-tested-not-hardware-tested",
                         "model": "device-reported-unverified",
                         "firmware": "device-reported-unverified" if fields["firmware"] else "unknown",
                         "hardware_tested": False, "cleanup_verified": False},
            "guide": f"docs/platforms/{platform}.md", "sources": list(PLATFORMS[platform][5])}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    listing = sub.add_parser("list", help="offline platform coverage")
    listing.add_argument("--json", action="store_true")
    plan = sub.add_parser("plan", help="offline plan, never inferred from brand")
    plan.add_argument("--platform", choices=PLATFORMS, default="unknown")
    for name in ("brand", "model", "firmware"):
        plan.add_argument("--" + name, type=safe_text)
    plan.add_argument("--json", action="store_true")
    inspect = sub.add_parser("inspect", help="explicit read-only metadata GET; no discovery or pairing")
    inspect.add_argument("--platform", choices=("tizen", "roku"), required=True)
    inspect.add_argument("--host", type=local_host, required=True)
    inspect.add_argument("--confirm-local-device", action="store_true", required=True,
                         help="confirm this is your authorized local device")
    inspect.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "inspect":
        try:
            result = inspect_device(args.platform, args.host)
        except (ValueError, OSError, http.client.HTTPException, ET.ParseError, RecursionError):
            print("Inspection failed: refused, unavailable or invalid platform metadata; no changes made.", file=sys.stderr)
            return 2
    elif args.command == "list":
        result = {"schema_version": 1, "platforms": [make_plan(p) for p in PLATFORMS]}
    else:
        result = make_plan(args.platform, args.brand, args.model, args.firmware)
    if args.json:
        print(json.dumps(result, ensure_ascii=True))
    elif args.command == "list":
        for record in result["platforms"]:
            print(f"{record['platform']}: {record['support_tier']} — {record['guide']}")
    elif args.command == "inspect":
        print(f"{result['platform']}: model {result['model']}; firmware {result['firmware'] or 'unknown'}")
        for key, value in result["capabilities"].items():
            print(f"{key}: {value}")
        print("Evidence: device-reported, protocol fixture tested, not hardware tested; cleanup not verified.")
        print("Guide: " + result["guide"])
        print("Sources: " + " ".join(result["sources"]))
    else:
        print(f"{result['platform']}: {result['support_tier']}")
        print(result["next_step"])
        for key, value in result["limits"].items():
            print(f"{key}: {value}")
        print("Evidence: model/firmware unverified; cleanup not verified. No network actions.")
        print("Consent: " + " ".join(result["required_consent"]))
        print("Guide: " + result["guide"])
        print("Sources: " + " ".join(result["sources"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
