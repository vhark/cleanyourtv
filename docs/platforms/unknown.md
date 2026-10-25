# Unknown or ambiguous OS (`unknown`)

**Coverage:** offline identification plan only. No device inspection, network discovery, pairing or changes. No hardware validation. Unknown is a deliberate stop, not shorthand for Android TV.

## Identify the thing being cleaned

1. Ask whether the owner means the television's built-in Home or an HDMI streamer. A remote's logo, retail brand or installed Apple TV/Google TV app does not establish the OS.
2. Using the physical remote, open normal **Settings > About / System Information / Device Information** or the on-device User Guide. Privately record the exact model, OS name and full firmware/software build. Do not open service/factory menus. Don't publish an About photo containing account, serial, network or device identifiers.
3. Compare those details with the manufacturer's exact regional model manual and official support pages. Hisense, TCL, Toshiba and Panasonic can ship multiple OS families. Fire TV can be Android-based Fire OS or non-Android Vega. Treat a firmware value labelled Unknown as unknown; don't substitute an API protocol version.
4. If still ambiguous, ask the owner for only the nonsensitive model/OS/software text, or the manual URL. Preserve spelling/case rather than normalizing it into another firmware family. If a panel and box are both involved, identify each separately.

```sh
python3 tools/platforms.py plan --platform unknown
```

This is offline; supplying brand/model/firmware text to `plan` does not authenticate it or trigger a connection. A missing platform must remain unknown rather than guess from the brand.

## Safe cleanup while identification is pending

With consent, use only clearly labelled on-screen **Move**, **Hide** or **Unpin** controls for shortcuts; first write down their original positions. Do not delete an app whose recovery/store availability is unknown. Keep input, tuner, remote, network and update controls unchanged. Review visible optional consents with the owner, but don't claim an unidentified menu stops all ads/tracking.

No developer permission is needed for normal Home editing. Do not enable ADB/SDB/Developer Mode, accept remote pairing, run an inspector for a guessed OS, install tools or attempt root. An open port or an Android-like interface is not OS proof.

## Undo and validation

Restore recorded tile positions/visibility through the same menus. With the physical remote verify Home/Back, required apps and normal input selection; if a menu is unclear, cancel rather than reset. No factory reset, firmware downgrade or service-menu recovery is part of this route. Once identification is established, choose the matching [platform guide](README.md) and review its specific permission and rollback boundaries before proceeding.

## Primary identification references and limits

- Amazon explicitly supports distinct Fire OS/Vega OS families: https://developer.amazon.com/docs/apps-and-games/documentation.html
- Google explains Google TV versus Android TV experiences: https://support.google.com/googletv/answer/10267283?hl=en
- Apple documents the separate HDMI-connected Apple TV box: https://support.apple.com/en-us/102451
- VIDAA directs hardware support to the actual TV manufacturer: https://www.vidaa.com/support/

No universal brand-to-OS map, cleanup API or firmware compatibility conclusion is supported without exact-device information.
