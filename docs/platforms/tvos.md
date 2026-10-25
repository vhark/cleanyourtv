# Apple tvOS (`tvos`)

**Coverage:** offline plan and manual Apple TV box settings only; no tvOS inspector, remote API, app sideload, system debloat or Home replacement. No fork hardware validation. **An Apple TV app on a television is not tvOS.** This guide is for an Apple TV HD/4K connected by HDMI; the display's Samsung/LG/etc. settings are a separate layer. Apple's cited current instructions primarily target Apple TV 4K; older HD/tvOS menus can differ.

## Simplify the box

1. In **Settings > General > About**, privately record model and tvOS version. Record Home layout, permissions and relevant TV app settings. Check whether One Home Screen syncing is enabled before changing a layout shared with other Apple TV boxes.
2. On Home, highlight an app, hold the clickpad/touch surface and select **Edit Home Screen**. Move favorites to the top row; use **Move to > New Folder** to group others. This avoids data loss.
3. For storage pressure, hold an unwanted app and choose **Delete App > Offload** where offered. Apple says offload retains data; **Delete** also deletes data. Re-download still depends on App Store availability. App removal is not subscription cancellation.
4. Open **Settings > General > Privacy & Security > Tracking** (older tvOS calls the parent Privacy). Review individual requests or turn **Allow Apps to Ask to Track** off. Review optional **Analytics and Improvements** sharing separately. These choices do not remove ads or all third-party collection.
5. For the Apple TV app's top-row previews, review **Settings > Apps > TV > Top Shelf** and choose **Continue Watching** rather than What to Watch if desired. This is a presentation choice and still uses viewing history. Do not use Clear Play History as cosmetic cleanup: it can affect the profile across devices.

## Permissions and limits

These steps use owner-authorized remote settings; no Developer Mode, Xcode signing, accessibility grant, local network inspector or jailbreak is required. Account sign-in remains on the owner's device. Installing the Android launcher/APK is not a tvOS route. A third-party app cannot be assumed to replace the system Home screen.

## Undo and validate

Restore layout/folders and recorded tracking, analytics and TV app values. If One Home Screen is on, check other synced boxes too. Re-download an offloaded app to recover retained data when still available; deleted data and cleared history may not return. Don't reset the box to reverse a folder or permission change.

Test physical Home/Back, required playback, Siri if retained, HDMI/CEC power/volume and restart. Then separately test the display's input/startup behavior: changing tvOS does not change a panel's ACR/privacy settings or guarantee an HDMI-first panel startup.

## Sources

- Box/display distinction and One Home Screen: https://support.apple.com/en-us/102451
- Rearranging apps/folders: https://support.apple.com/guide/tv/rearrange-apps-on-the-home-screen-atvbad14dc6a/tvos
- Offload versus delete: https://support.apple.com/guide/tv/install-or-delete-apps-atvbaa1a9524/tvos
- Tracking/privacy/analytics: https://support.apple.com/en-gb/guide/tv/atvb66239fa1/tvos
- TV app Top Shelf and history scope: https://support.apple.com/guide/tv/adjust-tv-app-settings-atvbae11a68b/tvos
