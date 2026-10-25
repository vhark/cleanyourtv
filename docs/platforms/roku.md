# Roku OS (`roku`)

**Coverage:** offline plan, explicit read-only device-info inspection and manual cleanup; no shell, system debloat, remote keys or alternative Home installation. No fork hardware validation. Applies to Roku TVs and streaming players where the controls exist; panel inputs/ACR settings do not automatically exist on a separate player.

## Manual cleanup

1. Open **Settings > System > About** and privately note model/software version/build. Record app order and original privacy/Home values. Do not publish the About screen or account/device identifiers.
2. From Home's Apps section, highlight an app, press **Star**, then **Move app** (or Move app to the top on newer layouts). Repeat for favorites. Removing a Quick Access shortcut is different from uninstalling the app.
3. For an unwanted user app, **Star > Remove app > confirm**. Roku warns a Remove option may be unavailable during an active Roku-billed subscription/current billing cycle; manage subscription separately. Do not assume removal cancels billing. Before deleting, check the owner's linked-device/account behavior; this guide has not verified app-removal synchronization across devices.
4. In **Settings > Home Screen**, review the available recommendation-row/shortcut options. Newer Home layouts offer Recommendation rows and Quick Access controls; older firmware has different hide/show choices. Roku says the newer layout cannot be switched back to the old one. This is not ad-free Home.
5. On a **Roku TV**, review **Settings > Privacy > Smart TV experience > Use info from TV inputs**. Clear it to opt out of input-based viewing recognition if desired. If keeping it on but declining notifications, review Enable auto notifications separately. The v13 guide warns opting out does not delete previously collected data and does not remove all guide recommendations.

## Optional read-only inspection

```sh
python3 tools/platforms.py plan --platform roku
python3 tools/platforms.py inspect --platform roku --host <tv-private-ipv4> --confirm-local-device
```

Substitute the explicitly approved device's RFC1918 IPv4 literal without angle brackets. Add `--json` for structured output. The only network operation is **GET http://host:8060/query/device-info**. No discovery, app inventory, keypress, POST or pairing; raw XML (which includes private identifiers) is not printed. Use only a trusted local network; local HTTP is unencrypted. A failed read does not establish that the device is not Roku.

Manual cleanup needs no network-control grant. **Do not enable Developer Mode for the inspector.** Official ECP docs list device-info as a GET without a required device setting. Roku OS 14.1+ requires Control by mobile apps enabled for listed control commands such as keypress, but those are not implemented here. If separately using Roku's official mobile remote, review the TV's mobile-control setting, allow only the needed access and restore it afterwards; don't switch to permissive access to make a metadata failure go away. ECP capabilities and third-party-use policies change; this is not an unrestricted remote API promise.

## Undo and validate

Restore tile order, Quick Access/Home options and original privacy settings. Re-add a removed app from the Roku store if available; check whether credentials and account-wide app changes need recovery. Do not factory-reset to undo a Home edit. Check physical Home/Back, playback and required TV inputs/tuner, volume/CEC, standby and restart. Record settings that are absent rather than simulating remote sequences. Metadata doesn't prove cleanup or a restorable backup.

## Sources

- Official app removal/billing caveats: https://support.roku.com/article/remove-an-app
- Move app: https://support.roku.com/article/move-an-app
- New Home layout limits/options: https://support.roku.com/article/why-does-my-roku-home-screen-look-different
- Roku TV v13 guide, Smart TV experience and version-specific settings: https://image.roku.com/c3VwcG9ydC1B/Roku%20TV%20User%20Guide-13.0/en-US.pdf
- Official ECP endpoint/permissions: https://developer.roku.com/dev/docs/external-control-api

The v13 manual is versioned evidence, not an exact map for every current firmware. No system-package removal or Home-replacement method was established for this release.
