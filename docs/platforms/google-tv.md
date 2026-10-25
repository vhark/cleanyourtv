# Google TV (`google-tv`)

**Coverage:** offline plan and existing Android tools separately; no new automated cleanup or hardware validation. Google TV is an Android-based experience, not every Google-branded TV service. Record model, Android OS version and exact firmware under Settings > System > About before using Android tools.

## Manual cleanup

1. Privately note the active profile, original Apps-only value and app order; agree whether search/Assistant is needed.
2. Open **All settings > Accounts & Profiles > your profile > Apps only mode > Turn on** if the owner accepts its limits. It hides personalized Home recommendations, **not sponsored content and teasers**. Google says Search/Assistant and some watchlist actions are unavailable in this mode. Individual apps can still personalize content; Web & App Activity is separate.
3. Reorder Your apps using the on-screen app options, placing required apps first. Do not delete app data just to simplify Home.
4. For an app problem, inspect Settings > Apps and its permissions before removing anything. Keep the store, input, remote, casting and update services.

Basic TV mode, on supported televisions during setup, is different from Apps-only mode and loses account-dependent features. Do not factory-reset a working TV merely to obtain it.

## Debugging and launcher limits

Manual settings require no ADB, developer account or accessibility grant. An optional ADB session requires owner-approved Developer options/debugging and trusted-host authorization, then the full [Android guide](android-tv.md) and [PROMPT.md](../../PROMPT.md), including backups and closure.

No new launcher takeover is implemented. The existing guard must confirm a new Home before stock Home can be disabled. **Do not disable setupwraith when it owns the saved Wi-Fi network**; loss of Wi-Fi/ADB and casting failures are known upstream risks. Never bypass a guard based on a similar model's example. A newer firmware may protect packages an older report could disable.

## Undo and validate

Turn Apps only mode off at the same profile menu; restore app order/permissions to recorded values. For actual Android disable changes, use the existing recorded restore procedure, not factory reset. With the physical remote test Home, search/voice if retained, HDMI/tuner, required playback and casting, then restart. Revoke debugging authorization after any ADB work. Verify the actual Home screen: Apps-only does not mean ad-free.

## Sources

- Google, Apps-only procedure, advertising and Basic TV limits: https://support.google.com/googletv/answer/10267283?hl=en
- Android developer options: https://developer.android.com/studio/debug/dev-options
- Existing safety rules: [AGENTS.md](../../AGENTS.md), [PROMPT.md](../../PROMPT.md); [upstream casting recovery lead](https://github.com/thayford/castfix) is not an automatic step or a fork-tested fix.
