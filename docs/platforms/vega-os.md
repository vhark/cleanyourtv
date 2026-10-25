# Vega OS (`vega-os`)

**Coverage:** offline plan and manual guidance only. No fork device inspection, mutation, sideload or launcher integration; no hardware validation. Amazon documents Vega as a Linux-based Fire TV platform with its own SDK. **Do not run Android APK installers, ADB package lists or Fire OS debloat recipes against it.** Fire TV branding alone is ambiguous.

## User-guided route

1. Open the device's Settings/About screen and privately record its exact model, OS and full software version. Cross-check the model in Amazon's current device documentation; if OS remains ambiguous, use [unknown](unknown.md).
2. Record current app order and available privacy values. In Fire TV **Settings > Preferences > Privacy Settings**, review only the controls actually present and described in Amazon's privacy FAQ. Decline optional device/app usage or advertising processing as desired; these are not a promise of zero collection or no ads.
3. If **Manage Sharing From Apps** appears, review participating-app sharing before changing it. Amazon limits this control to devices with Continue Watching; it must not be assumed for every Vega build.
4. Prefer supported app reordering. If your interface offers Amazon's **Applications > Manage Installed Applications** removal flow for a user app, verify its store availability and accept data loss before deleting. If that menu is absent, stop and use the exact model's help; do not substitute shell commands.

## Permissions and limits

No developer mode, pairing, network access or account disclosure is required for this manual review. Store actions may require the owner's Amazon account on-device. The Vega SDK is an app-development route, not an Android compatibility layer or system-debloat permission. No automatic root, Amazon Home replacement, accessibility takeover or updater blocking is provided.

**Evidence limit:** primary Amazon sources establish the distinct OS/SDK and general Fire TV privacy/user-app controls, but an exact consumer menu map for every Vega model/build was not verified. The conditional steps above are not a claim that all Fire OS menus carry over. Record unavailable controls instead of forcing a workaround.

## Undo and validation

Restore only the values/order you recorded. Deleted app data may not return with reinstallation; don't use factory reset as undo. Check physical Home/Back, selected playback, voice if retained, HDMI/CEC control of the connected display and restart behavior. Recheck settings after firmware updates without disabling updates.

## Sources

- Amazon OS split: https://developer.amazon.com/docs/apps-and-games/documentation.html
- Amazon's Linux-based Vega development overview: https://developer.amazon.com/apps-and-games/blogs/2026/07/guide-to-building-for-fire-tv-on-vega-os
- Vega documentation: https://developer.amazon.com/docs/vega/vega
- Fire TV privacy FAQ: https://www.amazon.com/gp/help/customer/display.html?nodeId=GQFYXZHZB2H629WN
- Conditional user-app removal: https://www.amazon.com/gp/help/customer/display.html?nodeId=G45H7PUWXUSTAY48
