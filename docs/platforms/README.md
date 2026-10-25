# Platform guides: choose the OS, not the badge

These are **user-guided settings procedures**, not a universal debloater. This fork has not validated them on hardware. Vendor documentation establishes menu capabilities; upstream owner reports and external projects are separately attributed, not fork test results. Menu names vary by model, market and firmware. Record the exact About information privately before choosing a route.

| OS id / guide | What this fork offers | Cleanup / launcher boundary |
|---|---|---|
| [android-tv](android-tv.md) | Offline plan; existing Android tools separately | Guarded disable/restore workflow; Android launcher subject to SDK and Home checks |
| [google-tv](google-tv.md) | Offline plan; existing Android tools separately | Apps-only settings first; Android guards still apply |
| [fire-os](fire-os.md) | Offline plan; existing ADB tools conditionally | Android-based, but protected Amazon Home; no automatic takeover |
| [vega-os](vega-os.md) | Offline plan and manual guide | New non-Android Fire TV OS; no APK/ADB debloat route here |
| [tizen](tizen.md) | Offline plan; explicit read-only metadata inspection | Samsung settings, not system-app removal or Home replacement |
| [webos](webos.md) | Offline plan and manual guide | LG settings; external developer apps are not root |
| [roku](roku.md) | Offline plan; explicit read-only metadata inspection | Roku settings/app tiles; no system debloat or replacement Home |
| [vidaa](vidaa.md) | Offline plan and manual guide | Manufacturer settings and supported store apps only |
| [vizio-smartcast](vizio-smartcast.md) | Offline plan and manual guide | SmartCast / VIZIO Home settings; no arbitrary app install promise |
| [panasonic-my-home-screen](panasonic-my-home-screen.md) | Offline plan and manual guide | Home shortcuts and model-specific app controls |
| [tvos](tvos.md) | Offline plan and manual guide | Apple TV box settings, not the panel's OS |
| [unknown](unknown.md) | Offline identification plan | Stop before device commands; ask for About/model/OS |

TCL, Hisense, Toshiba, Panasonic and other brands ship multiple OS families. An Apple TV app on a Samsung TV is not tvOS. A Fire TV logo does not distinguish Fire OS from Vega OS. A streaming box and its display can need two separate guides.

## Start without contacting a TV

Run from the repository root:

```sh
python3 tools/platforms.py list
python3 tools/platforms.py plan --platform unknown
python3 tools/platforms.py plan --platform webos
```

`list` and `plan` are offline; add `--json` for structured output. `plan` optionally accepts `--brand`, `--model`, and `--firmware`, but these are user-supplied descriptions, **not verified compatibility**. A missing platform must not infer Android from the brand. No plan executes cleanup, installs software or pairs a remote.

Only `tizen` and `roku` have a separate opt-in `inspect` route, described in their guides. It reads one fixed HTTP endpoint at an explicitly supplied RFC1918 IPv4 address, not a hostname or URL. No discovery, remote keys, pairing, POSTs or mutations. Its allowlisted output omits device identifiers; raw API replies must remain private. Protocol fixtures are not hardware testing, and metadata is not a backup or cleanup success.

## Before changing settings

- Ask the owner which apps, voice features, casting, tuner, HDMI/CEC and startup behavior must stay. Manual settings need consent too.
- Privately write down each original value, tile order and change. Don't commit account information, inventories, addresses, identifiers or screenshots. No factory reset, service menu, updater blocking, root or launcher takeover is part of these guides.
- Prefer hiding/reordering to deletion. Optional vendor-menu deletion of a user-installed app is distinct from system-package debloating; it may erase app data and may not cancel a subscription. Reinstallation depends on current regional store availability. Skip deletion if recovery is uncertain.
- After each small change, use the **physical remote** to test Home/Back, required playback, inputs, tuner, volume, casting and standby/restart as applicable. Reverse the last change if something breaks. Record “not tested” for functions you cannot check; don't claim a speed or privacy improvement without evidence.
- Settings snapshots and sanitized metadata are not complete restorable backups. Privacy toggles don't remove all ads, erase all past data, or control independent streaming services.

Each guide links primary sources and flags evidence gaps. External project links are research leads only, not scripts to run as part of this release.
