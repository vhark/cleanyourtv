# LG webOS (`webos`)

**Coverage:** offline plan plus owner-operated settings. No webOS inspect, remote pairing, package disabling, developer deployment or Home takeover is implemented here; no fork hardware validation. webOS TVs do not accept this repository's Android launcher/APK or ADB package lists.

## Practical manual cleanup

1. Privately record model, full software version and webOS version from TV Information/About and the original Home settings/app order. LG's version names and marketing year can differ; use the TV's own User Guide when menus do not match.
2. Press **Home**; hold **Wheel/OK** on an app to enter **Edit App List**, or choose Edit App List at the row's end. Move favorites forward. Use the delete icon only for an unwanted removable user app after accepting data loss. LG's guide says default apps cannot be deleted. Some content lists also cannot be moved.
3. For the documented webOS 2024 layout, open **All Settings > General > System > Additional Settings > Home Settings**. Set **Home Promotion** off if unwanted. Where offered, turn **Content Recommendation** off too. These are Home controls, not filters for ads inside streaming apps.
4. In the same Home Settings, set **Power On Screen > Recent Input** if the owner wants the last input instead of Home at startup. Older layouts can call this Home Auto Launch; do not assume a missing switch exists.
5. A specific 2020/webOS 5.0 update supports **General > Home Settings > Home Style > Basic Home**. Use it only if present; this is not a promise of Basic Home on later firmware. Review optional consents in the TV's own privacy/user-agreements screen separately, not by accepting or withdrawing all agreements blindly.

## Permissions: normal settings versus developer apps

Manual cleanup requires only owner permission and the remote. Reinstallation through LG's store can require an LG account and regional availability; don't publish account information.

LG's separate **Developer Mode** app requires an LG developer account, an on-TV enable/reboot and the documented Key Server/key setup for development. It is **not root**. Developer sessions expire; LG warns developer-installed apps are uninstalled when Developer Mode is disabled. Do not turn it on for routine settings cleanup, promise indefinite developer-app persistence or silently renew it. The fork does not install the SDK or any helper.

## External SHOWCASE leads, not integrated support

- [webos-vibehack](https://github.com/OmkarK97/webos-vibehack): developer-mode web app; its Home watcher runs on another device. Author-reported results name a particular model/build, not all LG TVs.
- [clean-your-tv-lg-webos](https://github.com/Razdva122/clean-your-tv-lg-webos): now documents separate No-root and Root editions, with an on-TV Home helper for No-root. Recovery gestures changed between releases; read the exact version's recovery instructions instead of copying an old SHOWCASE summary.
- [cleanyourtv-WebOS](https://github.com/lasharor/cleanyourtv-WebOS): requires existing root/Homebrew access and uses root services/boot behavior. It is not equivalent to official Developer Mode and is outside this routine route.

These projects have different trust, pairing, persistence and undo boundaries. None is executed, installed or validated by this fork; no automatic root or launcher takeover is offered.

## Undo and validate

Restore the recorded Home Promotion/recommendation, Power On Screen and Home Style values; move app tiles back manually. Reinstall deleted user apps only if still available; this does not restore all data. Settings snapshots are not firmware backups. If you separately used a developer app, keep its source/configuration and follow LG/project-specific removal instructions; disabling Developer Mode can remove other developer apps too.

With the physical remote test Home/Back, required playback, HDMI/tuner, volume/CEC, standby and restart. Verify each profile's edited app list if applicable. If startup changes but Home still opens LG Home, that is expected and not launcher replacement.

## Sources

- LG version-scoped startup settings: https://www.lg.com/au/support/product-support/troubleshoot/help-library/cs-CT20088015-20153529296644/
- LG 2024 user guide (Home Promotion, app editing/default-app limits): http://kr.eguide.lgappstv.com/manual/w24_mr4/w24_eu12/eng.html
- LG Basic Home, 2020/webOS 5.0 only: https://www.lg.com/us/support/help-library/lg-tv-how-to-change-home-menu-layout--20153529302967
- Official Developer Mode permissions/expiry: https://webostv.developer.lge.com/develop/getting-started/developer-mode-app

Evidence limit: LG's support extraction omits some illustrated controls; the textual 2024 e-guide supports Home Promotion. Exact recommendation/consent names on other releases remain model-specific.
