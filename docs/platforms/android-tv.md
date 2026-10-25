# Android TV (`android-tv`)

**Coverage:** offline platform plan plus the repository's existing Android/ADB workflow, not a new cross-platform mutation command. No fork hardware validation. First verify Android TV and exact model, Android version and firmware in Settings > Device Preferences > About (wording varies). A brand or an Android-looking home screen is insufficient.

## Manual cleanup first

1. Privately record original Home rows, preview toggles and favorites. Agree which apps and casting/voice functions must stay.
2. Where available, open **Settings > Device preferences > Home screen > Customize channels** and turn off unwanted channel rows. On Home, move to a row's left-side controls to reorder it.
3. In Home screen settings, turn off **Enable video previews** and/or **Enable audio previews** if unwanted. Reorder favorite apps rather than deleting anything essential.
4. Review individual user apps in Settings > Apps. Do not clear data as routine cleanup: sign-ins and preferences can be lost. Google explicitly says some trending/sponsored suggestions cannot be turned off with these Home settings.

## Existing tools: separate permission boundary

Read [PROMPT.md](../../PROMPT.md) and [AGENTS.md](../../AGENTS.md) completely before an ADB session; the platform planner does not execute them. Enable Developer options and the device's supported USB/network or wireless debugging route only with owner consent; accept only your trusted computer's authorization on the TV. Do not open a factory menu to obtain debugging.

Use the existing backup, protected-package, small-batch disable and restore procedure. Match an [example](../../examples/README.md) by actual board/model/build; never apply a brand-wide list blindly. Disable, never uninstall system packages. Keep Settings, input/tuner, keyboard, remote/Bluetooth, Play components and updates. A refused disable is a stop condition, not permission to root.

The launcher requires API 26 or later. No automatic takeover: keep stock Home until the existing installation/Home checks pass; CVTE boards have additional restrictions. Accessibility helpers are additional sensitive permissions, not a default requirement of manual cleanup.

## Undo and validate

Restore recorded row/preview values and tile positions through the same menus. For package changes use the existing `tools/restore.sh` / PowerShell counterpart with the session record; it does not restore erased app data. Test physical Home, held volume, HDMI/tuner, chosen streaming apps, voice/casting and a reboot. Close debugging, revoke authorizations, reboot and follow the existing ADB-closure check. No speed gain is assumed.

## Sources

- Google, Home customization and sponsored-content limits: https://support.google.com/androidtv/answer/6121336?hl=en
- Android, developer options/debugging permissions (TV UI may differ): https://developer.android.com/studio/debug/dev-options
- Repository safety and tools: [PROMPT.md](../../PROMPT.md), [AGENTS.md](../../AGENTS.md), [examples](../../examples/README.md). Upstream observations are not this fork's hardware results.
