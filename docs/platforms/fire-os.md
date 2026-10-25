# Fire OS (`fire-os`)

**Coverage:** offline plan; manual Amazon settings; existing Android/ADB tools only where the actual Fire OS build permits them. No fork hardware testing, Fire remote-control implementation or automatic Home interception. **Vega OS is a different, non-Android route**: see [Vega](vega-os.md).

## Identify and simplify manually

1. In **Settings > My Fire TV** (or **Device & Software**) **> About**, privately record the model and full software build. Do not infer OS from “Fire TV” or retail Stick name alone.
2. Record current privacy settings, app order and required Alexa, casting, HDMI/tuner and streaming features.
3. Under **Settings > Preferences > Privacy Settings**, review Device Usage Data, app usage collection and Interest-based Ads where offered. Turn off only the optional processing the owner declines. Amazon says the Device Usage Data switch does not stop essential feature processing or all advertising.
4. On devices with Continue Watching, **Privacy Settings > Manage Sharing From Apps** lets you review participating apps, sharing of viewing/content information and cross-device synchronization. These options are not universal.
5. Move favorites using the Apps screen's menu options if available. Optional deletion is **Settings > Applications > Manage Installed Applications > selected user app > Uninstall**. Prefer reordering; deletion may lose data. Never use this as a system-component removal recipe.

## Permission setup and existing Android limits

Manual steps require only the remote and owner permission. If separately choosing Android tooling, follow Amazon's official ADB connection instructions and [PROMPT.md](../../PROMPT.md): enable the supported Developer options/ADB debugging route and approve the trusted host on screen; close it afterwards. Do not enable unknown-source installs for settings cleanup.

Keep Amazon Home enabled. Fire OS can protect the launcher and telemetry components or re-enable them at boot. A protected-package failure is not an invitation to root, block updates or install an accessibility watcher. Existing Android backup/disable guards still apply, including one package per call and recorded undo. No generic Fire OS package list is safe for every build.

## Community evidence, not a default workflow

Read the [upstream TCL Fire OS example](../../examples/tcl-43s450f-ca/README.md) and [single-session Fire OS 8 note](../devices/amazon-fire-tv-aftma08c15.md). The former keeps protected Amazon Home; the latter reports physical Home failing despite passing injected-key/helper checks. They establish model/build-specific observations, not this fork's compatibility. [SHOWCASE](../../SHOWCASE.md#other-platforms-fire-tv-and-lg-webos) watchers are external projects and need their own security/recovery review. None is installed here.

## Undo and validate

Restore each privacy toggle and app order from your notes. Reinstall a removed user app only if still available; restored package enabled state does not undo third-party scripts' app-ops, animation or background restrictions. Use the exact recorded Android restore flow for Android changes. Test physical Home (also after reboot), Alexa if retained, playback, volume and HDMI/CEC/tuner on integrated TVs. Revoke ADB grants and disable debugging after any ADB session.

## Sources

- Amazon privacy scope: https://www.amazon.com/gp/help/customer/display.html?nodeId=GQFYXZHZB2H629WN
- Viewing sharing: https://www.amazon.com/gp/help/customer/display.html?nodeId=TpJxOEPHMPJbmKq5Bh
- User-app removal: https://www.amazon.com/gp/help/customer/display.html?nodeId=G45H7PUWXUSTAY48
- Official ADB setup: https://developer.amazon.com/docs/fire-tv/connecting-adb-to-device.html
- Amazon distinguishes Fire OS and Vega: https://developer.amazon.com/docs/apps-and-games/documentation.html

Evidence gap: a current primary consumer Fire TV autoplay-toggle procedure was not verified during this research; no firmware-independent autoplay path is promised here.
