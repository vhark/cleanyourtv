# Samsung Tizen (`tizen`)

**Coverage:** offline plan, opt-in read-only HTTP metadata inspection, and manual cleanup. No Tizen system-app disable, remote key automation, SDK install, root or Home replacement is implemented. This fork has no hardware-backed cleanup result. Read the existing [Samsung note](../devices/samsung-tizen.md) as upstream owner evidence, not a universal compatibility list.

## Settings cleanup with the owner watching

1. Under the TV's About/Contact Samsung screen, privately record exact retail model and full firmware. Record app order and the original startup/privacy values before changing them. The HTTP API's `version` is not necessarily firmware; an absent/Unknown firmware stays unknown.
2. Open **Home > Apps > App Settings** (older layouts use the Apps settings gear). Select an unwanted user-installed app and **Delete** only if its data can be lost and it remains available in the regional store. Samsung says some preloaded apps cannot be removed. A grey Delete option is a boundary, not a reason to use a service menu.
3. Use the Home app row's **Move/Remove** controls to simplify shortcuts. Removing a Home shortcut is different from deleting the app. Keep required inputs and apps accessible.
4. For HDMI-first startup, locate **All Settings > General & Privacy > Start Screen Options > Start with Smart Hub Home**, or **Advanced Features > Start Screen Options** on newer layouts. Record the existing value, then switch Smart Hub startup off if desired. **Autorun Last App** is optional and not supported by every app. Neither setting replaces the physical Home button.
5. Open **Privacy Choices > Terms & Conditions, Privacy Policy** where offered. Read each optional viewing/advertising consent and withdraw only the ones the owner declines; save with OK. Names and availability depend on region/build. Do not claim that withdrawing consent removes in-app ads or all collection. Voice recording/privacy options are separate.

## Optional metadata read and permission boundary

From the repository root, the command contract is:

```sh
python3 tools/platforms.py plan --platform tizen
python3 tools/platforms.py inspect --platform tizen --host <tv-private-ipv4> --confirm-local-device
```

Replace the placeholder yourself with the explicitly approved TV's RFC1918 IPv4 literal (no angle brackets), not a URL, port or hostname. Add `--json` if needed. `inspect` sends only **GET http://host:8001/api/v2/** and displays selected sanitized fields. It does not scan, send remote keys, pair, read app lists or make a backup. Local HTTP is unencrypted; use only a trusted local network. An unreachable/refused endpoint is an inspection failure, not a reason to probe other ports or fall back to ADB.

Do not enable Developer Mode for this read. Samsung's signed-app development route uses **SDB**, certificates and on-TV Developer Mode, not Android ADB. It is separate from this fork and does not imply unrestricted shell/root. Remote-control “Allow” grants and developer certificates are also separate permissions; the inspector requests neither.

## Rollback and validation

Restore startup and privacy values and tile order through the same menus. Add a removed shortcut back with Add to Home. A deleted user app can only be reinstalled if still offered; account/data restoration is not guaranteed. Do not reset Smart Hub as routine undo: it can remove accounts/settings.

Test physical Home/Back, HDMI switching, tuner if used, streaming, volume/CEC, standby resume and a normal restart. Check whether startup returns to the intended input and whether Home still opens Samsung Home. Record those separately; standby resume is not cold-boot persistence. No performance gain or complete backup is established by metadata or app counts.

## Experimental research is outside this route

Public Samsung root projects contain genuine **other-model, exact-build reports**, not universal support. The [source-published root project](https://github.com/chris-ritsen/samsung-tv-root) and [model-specific cleanup toolkit](https://github.com/invaliddayta/samsung-tv-tools) are research leads only. Tool commands named “probe” may actually escalate privileges. Do not execute them as read-only inspection, infer support from a shared firmware number, or treat another model's root as safe cleanup compatibility. This guide supplies no exploit or root steps.

## Sources and evidence limits

- Samsung supported app management/removal limits: https://www.samsung.com/uk/support/tv-audio-video/how-do-i-manage-apps-on-my-smart-tv/
- Samsung startup/last-app caveats: https://www.samsung.com/ae/support/tv-audio-video/use-autorun-start-screen-options-on-your-samsung-tv/
- Samsung privacy controls, explicitly Hong Kong-specific: https://www.samsung.com/hk_en/support/tv-audio-video/how-to-adjust-privacy-settings-on-your-samsung-smart-tv/
- Official developer device setup: https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/tv-device.html
- HTTP endpoint evidence is [upstream reconnaissance](../devices/samsung-tizen.md), not an official stable Samsung API contract. Metadata availability and firmware reporting vary; no universal remote cleanup API was established.
