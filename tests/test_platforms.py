"""Offline CLI and fixture-only local metadata inspection; never contact a TV."""
import contextlib
import importlib.util
import io
import json
from unittest import mock
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "platforms.py"


def cli(*args):
    return subprocess.run([sys.executable, "-I", str(SCRIPT), *args],
                          capture_output=True, text=True, timeout=10)


class OfflineTests(unittest.TestCase):
    def test_default_plan_requires_identification_not_brand_guess(self):
        result = cli("plan", "--brand", "TCL", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = json.loads(result.stdout)
        self.assertEqual(plan["schema_version"], 1)
        self.assertEqual(plan["platform"], "unknown")
        self.assertIn("About", plan["next_step"])
        self.assertEqual(plan["network_actions"], [])

    def test_list_and_each_platform_plan_are_offline_and_evidence_limited(self):
        ids = {"android-tv", "google-tv", "fire-os", "vega-os", "tizen", "webos", "roku",
               "vidaa", "vizio-smartcast", "panasonic-my-home-screen", "tvos", "unknown"}
        result = cli("list", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        listing = json.loads(result.stdout)
        self.assertEqual(listing["schema_version"], 1)
        self.assertEqual({p["platform"] for p in listing["platforms"]}, ids)
        self.assertEqual(len(listing["platforms"]), len(ids))
        for platform in ids:
            with self.subTest(platform=platform):
                result = cli("plan", "--platform", platform, "--brand", "Hisense",
                             "--model", "MiXeD $(no shell)", "--firmware", "AbC-01", "--json")
                self.assertEqual(result.returncode, 0, result.stderr)
                plan = json.loads(result.stdout)
                self.assertEqual(plan["platform"], platform)
                self.assertEqual(plan["model"], "MiXeD $(no shell)")
                self.assertEqual(plan["firmware"], "AbC-01")
                self.assertEqual(plan["evidence"]["model"], "user-supplied-unverified")
                self.assertEqual(plan["evidence"]["firmware"], "user-supplied-unverified")
                self.assertFalse(plan["evidence"]["cleanup_verified"])
                self.assertEqual(plan["guide"], f"docs/platforms/{platform}.md")
                self.assertTrue((ROOT / plan["guide"]).is_file())
                self.assertTrue(plan["sources"])
                self.assertTrue(plan["required_consent"])
                self.assertEqual(plan["network_actions"], [])
                for field in ("manual_cleanup", "control", "debloat", "launcher"):
                    self.assertTrue(plan["limits"][field])
                self.assertTrue(plan["support_tier"])
                empty = json.loads(cli("plan", "--platform", platform, "--json").stdout)
                self.assertIsNone(empty["model"])
                self.assertIsNone(empty["firmware"])
                self.assertEqual(empty["evidence"]["firmware"], "unknown")
        self.assertIn("unknown", cli("list").stdout)
        self.assertIn("About", cli("plan").stdout)

    def test_invalid_offline_inputs_fail_without_traceback(self):
        for args in (("plan", "--platform", "Samsung"), ("plan", "--platform", "TIZEN"),
                     ("plan", "--model", "bad\nvalue"), ("plan", "--brand", "x" * 257),
                     ("plan", "--firmware", "bad\x1bvalue")):
            with self.subTest(args=args):
                result = cli(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)


class InspectTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("coverage_platforms", SCRIPT)
        assert spec is not None and spec.loader is not None
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        # Fail closed: even mistakes in the fixture harness cannot contact real devices.
        self.block_network = mock.patch("socket.socket", side_effect=AssertionError("real socket forbidden"))
        self.block_network.start()
        self.addCleanup(self.block_network.stop)

    def inspect(self, payload, platform="tizen", status=200, headers=None):
        connection = mock.MagicMock()
        response = connection.getresponse.return_value
        response.status = status
        response.getheader.side_effect = lambda key, default=None: (headers or {}).get(key, default)
        response.read.return_value = payload
        with mock.patch("http.client.HTTPConnection", return_value=connection) as factory:
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = self.module.main(["inspect", "--platform", platform, "--host", "192.168.1.50",
                                         "--confirm-local-device", "--json"])
        return code, out.getvalue(), err.getvalue(), factory, connection, response

    def test_tizen_fixture_allows_only_public_metadata_and_null_firmware(self):
        payload = json.dumps({"device": {"type": "Samsung SmartTV", "model": "MiXeD_Model",
                             "firmwareVersion": "Unknown", "TokenAuthSupport": "true",
                             "duid": "secret", "wifiMac": "secret", "ip": "secret",
                             "name": "secret"}, "version": "2.0.25"}).encode()
        code, out, err, factory, conn, response = self.inspect(payload)
        self.assertEqual(code, 0, err)
        result = json.loads(out)
        self.assertEqual(result["platform"], "tizen")
        self.assertEqual(result["model"], "MiXeD_Model")
        self.assertIsNone(result["firmware"])
        self.assertEqual(result["capabilities"], {"token_auth_support": True})
        self.assertNotIn("secret", out)
        self.assertEqual(result["evidence"]["inspection"], "protocol-fixture-tested-not-hardware-tested")
        self.assertFalse(result["evidence"]["cleanup_verified"])
        factory.assert_called_once_with("192.168.1.50", 8001, timeout=3.0)
        conn.request.assert_called_once_with("GET", "/api/v2/", headers={"Accept": "application/json", "Accept-Encoding": "identity"})
        response.read.assert_called_once_with(65537)
        conn.close.assert_called_once()

    def test_roku_fixture_endpoint_and_allowlisted_fields(self):
        body = b'''<?xml version="1.0" encoding="UTF-8"?><device-info>
          <vendor-name>Roku</vendor-name><model-name>Roku Example</model-name>
          <model-number>ExAmPlE</model-number><software-version>12.0.1</software-version>
          <software-build>00001</software-build><is-tv>true</is-tv>
          <supports-ethernet>false</supports-ethernet><serial-number>secret</serial-number>
          <user-device-name>secret</user-device-name><wifi-mac>secret</wifi-mac>
          <keyed-developer-id>secret</keyed-developer-id></device-info>'''
        code, out, err, factory, conn, _ = self.inspect(body, platform="roku")
        self.assertEqual(code, 0, err)
        result = json.loads(out)
        self.assertEqual(result["model"], "Roku Example")
        self.assertEqual(result["firmware"], "12.0.1")
        self.assertEqual(result["model_number"], "ExAmPlE")
        self.assertEqual(result["firmware_build"], "00001")
        self.assertEqual(result["capabilities"], {"is_tv": True, "supports_ethernet": False})
        self.assertNotIn("secret", out)
        factory.assert_called_once_with("192.168.1.50", 8060, timeout=3.0)
        conn.request.assert_called_once_with("GET", "/query/device-info", headers={"Accept": "application/xml", "Accept-Encoding": "identity"})
        code, out, err, *_ = self.inspect(b"<device-info><model-name>Example</model-name></device-info>", platform="roku")
        self.assertEqual(code, 0, err)
        self.assertIsNone(json.loads(out)["firmware"])

    def test_reject_hostile_or_wrong_platform_responses_without_echo(self):
        tizen = [b"not-json secret", b"[]", b'{"device":[]}',
                 b'{"device":{"type":"Roku","model":"secret"}}',
                 b'{"device":{"type":"Samsung SmartTV"}}',
                 b'{"device":{"type":"Samsung SmartTV","model":123}}',
                 b'{"device":{"type":"Samsung SmartTV","model":"bad\\u001bsecret"}}',
                 b'{"device":{"type":"Samsung SmartTV","model":"X","TokenAuthSupport":1}}',
                 b'{"device":{"type":"Samsung SmartTV","model":"A","model":"B"}}',
                 b'{"device":{"type":"Samsung SmartTV","model":"X"},"bad":NaN}',
                 b"<device-info><model-name>Roku</model-name></device-info>"]
        roku = [b'{"device":{"type":"Samsung SmartTV","model":"secret"}}',
                b"<wrong><model-name>secret</model-name></wrong>", b"<device-info/>",
                b"<device-info><model-name>A</model-name><model-name>B</model-name></device-info>",
                b"<device-info><model-name><nested>secret</nested></model-name></device-info>",
                b"<device-info><model-name>X</model-name><is-tv>secret</is-tv></device-info>",
                b'<!DOCTYPE device-info [<!ENTITY x "secret">]><device-info><model-name>&x;</model-name></device-info>',
                b'<?xml version="1.0" encoding="iso-8859-1"?><device-info><model-name>secret</model-name></device-info>',
                '<device-info><model-name>secret</model-name></device-info>'.encode("utf-16"),
                '<!DOCTYPE device-info [<!ENTITY x "secret">]><device-info><model-name>&x;</model-name></device-info>'.encode("utf-32")]
        for platform, bodies in (("tizen", tizen), ("roku", roku)):
            for body in bodies:
                with self.subTest(platform=platform, body=body[:80]):
                    code, out, err, *_ = self.inspect(body, platform)
                    self.assertEqual(code, 2)
                    self.assertEqual(out, "")
                    self.assertNotIn("secret", err)
                    self.assertNotIn("Traceback", err)

    def test_refuse_redirect_status_encoding_size_and_truncation(self):
        body = b'{"device":{"type":"Samsung SmartTV","model":"X"}}'
        cases = [(body, 302, {"Location": "http://public.example/secret"}),
                 (body, 401, {}), (body, 500, {}), (b"x" * 65537, 200, {}),
                 (body, 200, {"Content-Length": "65537"}),
                 (body, 200, {"Content-Length": "invalid"}),
                 (body, 200, {"Content-Length": "1000"}),
                 (body, 200, {"Content-Encoding": "gzip"}),
                 (body, 200, {"Content-Type": "text/html"})]
        for payload, status, headers in cases:
            with self.subTest(status=status, headers=headers):
                code, out, err, factory, conn, _ = self.inspect(payload, status=status, headers=headers)
                self.assertEqual(code, 2)
                self.assertEqual(out, "")
                self.assertNotIn("secret", err)
                self.assertEqual(factory.call_count, 1)
                self.assertEqual(conn.request.call_count, 1)
                conn.close.assert_called_once()

    def test_no_retry_and_sanitized_transport_errors(self):
        for error in (TimeoutError("secret"), OSError("secret")):
            conn = mock.MagicMock()
            conn.request.side_effect = error
            with mock.patch("http.client.HTTPConnection", return_value=conn) as factory:
                out, err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    code = self.module.main(["inspect", "--platform", "tizen", "--host", "10.0.0.50",
                                             "--confirm-local-device", "--json"])
            self.assertEqual(code, 2)
            self.assertNotIn("secret", err.getvalue())
            self.assertEqual(out.getvalue(), "")
            self.assertEqual(factory.call_count, 1)
            self.assertEqual(conn.request.call_count, 1)
            conn.close.assert_called_once()

    def test_no_network_for_offline_or_invalid_inspect_arguments(self):
        bad_hosts = ["8.8.8.8", "127.0.0.1", "169.254.1.1", "224.0.0.1", "0.0.0.0",
                     "100.64.0.1", "192.0.0.1", "172.15.0.1", "172.32.0.1", "::1",
                     "tv.local", "http://192.168.1.50", "192.168.1.50:8001", "010.0.0.1",
                     "192.168.1.50\n", "192.168.1.50/24", "192.168.1.50?secret"]
        cases = [["inspect", "--platform", "tizen", "--host", h, "--confirm-local-device"]
                 for h in bad_hosts]
        cases += [["inspect", "--platform", "tizen", "--host", "10.0.0.50"],
                  ["inspect", "--platform", "tizen", "--confirm-local-device"],
                  ["inspect", "--platform", "webos", "--host", "10.0.0.50", "--confirm-local-device"]]
        with mock.patch("http.client.HTTPConnection", side_effect=AssertionError("network forbidden")):
            for args in cases:
                with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as error:
                        self.module.main(args)
                    self.assertEqual(error.exception.code, 2)
            with contextlib.redirect_stdout(io.StringIO()):
                self.module.main(["list", "--json"])
                self.module.main(["plan", "--json"])
        for host in ("10.0.0.1", "172.16.0.1", "172.31.255.254", "192.168.255.254"):
            self.assertEqual(self.module.local_host(host), host)

    def test_tizen_explicit_os_mismatch_and_non_boolean_capability_refused(self):
        for fields in ({"OS": "Android"}, {"TokenAuthSupport": 1.0}, {"OS": []}):
            body = json.dumps({"device": {"type": "Samsung SmartTV", "model": "X", **fields}}).encode()
            code, out, _, *_ = self.inspect(body)
            self.assertEqual(code, 2)
            self.assertEqual(out, "")

    def test_inspect_readable_text(self):
        result = {"schema_version": 1, "platform": "tizen", "model": "Example",
                  "firmware": None, "capabilities": {}, "guide": "docs/platforms/tizen.md",
                  "sources": ["https://example.org/"],
                  "evidence": {"cleanup_verified": False, "hardware_tested": False}}
        with mock.patch.object(self.module, "inspect_device", return_value=result):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = self.module.main(["inspect", "--platform", "tizen", "--host", "10.0.0.50",
                                         "--confirm-local-device"])
        self.assertEqual(code, 0)
        for text in ("tizen", "Example", "unknown", "not hardware tested", "cleanup not verified"):
            self.assertIn(text, out.getvalue())

    def test_real_http_parser_with_fake_socket_ignores_proxies_and_only_sends_get(self):
        payload = b'{"device":{"type":"Samsung SmartTV","model":"Example"}}'
        fake_socket = mock.MagicMock()
        fake_socket.makefile.return_value = io.BytesIO(
            b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: " +
            str(len(payload)).encode() + b"\r\n\r\n" + payload)
        with mock.patch.dict(os.environ, {"HTTP_PROXY": "http://public.example:1", "http_proxy": "http://public.example:1",
                                          "ALL_PROXY": "http://public.example:1", "NO_PROXY": ""}), \
             mock.patch("socket.create_connection", return_value=fake_socket) as connect, \
             mock.patch("threading.Timer") as timer:
            result = self.module.inspect_device("tizen", "192.168.1.50")
        self.assertEqual(result["model"], "Example")
        self.assertEqual(connect.call_count, 1)
        self.assertEqual(connect.call_args.args[:2], (("192.168.1.50", 8001), 3.0))
        sent = b"".join(call.args[0] for call in fake_socket.sendall.call_args_list)
        self.assertTrue(sent.startswith(b"GET /api/v2/ HTTP/1.1\r\n"))
        self.assertEqual(sent.count(b"GET "), 1)
        self.assertNotIn(b"POST", sent)
        self.assertNotIn(b"public.example", sent)
        timer.assert_called_once_with(3.0, self.module.stop_read, args=(fake_socket,))
        timer.return_value.start.assert_called_once()
        timer.return_value.cancel.assert_called_once()
        timer.return_value.join.assert_called_once()
        self.module.stop_read(fake_socket)
        fake_socket.shutdown.assert_called_once_with(self.module.socket.SHUT_RDWR)

    def test_total_deadline_interrupts_a_stalled_exchange_without_real_sockets(self):
        interrupted = threading.Event()
        conn = mock.MagicMock()
        conn.sock.shutdown.side_effect = lambda _: interrupted.set()

        def stalled_headers():
            if not interrupted.wait(5):
                raise AssertionError("exchange was not interrupted by deadline")
            raise TimeoutError("sensitive server text")

        conn.getresponse.side_effect = stalled_headers
        out, err = io.StringIO(), io.StringIO()
        started = time.monotonic()
        with mock.patch("http.client.HTTPConnection", return_value=conn), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = self.module.main(["inspect", "--platform", "roku", "--host", "10.0.0.50",
                                     "--confirm-local-device", "--json"])
        self.assertEqual(code, 2)
        self.assertTrue(interrupted.is_set())
        self.assertLess(time.monotonic() - started, 5)
        self.assertNotIn("sensitive", err.getvalue())
        self.assertEqual(out.getvalue(), "")
        conn.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
