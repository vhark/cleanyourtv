# Coverage roadmap and evidence rules

Goal: offer the most useful **verified** path for any TV owner, without implying
that every OS supports the same cleanup or launcher replacement. This is an
independent community fork; upstream Android contributions retain their authorship.

## First increment

| Surface | Delivery | Limit |
|---|---|---|
| Operating-system routing | Offline CLI plan/list and per-platform guides | Owner-supplied identity, not automatic identification |
| Samsung Tizen | Settings/control guide; opt-in read-only metadata inspection | No new pairing, keypresses, app removal, root or launcher replacement |
| Roku | Settings/control guide; opt-in read-only metadata inspection | No Android packages or replacement system Home |
| LG webOS | Native settings/control and developer-mode distinctions | Guided only; no new executable webOS adapter |
| Android TV / Google TV | Route to existing upstream tools and model evidence | No universal package list or new hardware certification |
| Fire OS / Vega OS | Separate routes and limitations | Android-derived Fire OS is not the newer Vega platform |
| VIDAA / VIZIO SmartCast / Panasonic My Home Screen / Apple tvOS | Documented guided options and honest restrictions | No generic debloater or automatic mutation backend |
| Unknown or other systems | Identification-first fallback | Never guessed from brand |

Executable inspection for other platforms, automatic setting changes and device
control are **not implemented** in this increment. Guide availability is not API
support. Brands and OS families are not model/firmware test counts.

## What should follow

1. **Hardware acceptance:** volunteer-owned devices, one explicitly approved
   target at a time. Verify reported identity, malformed/error handling, privacy,
   and absence of unintended state changes for Samsung/Roku inspection.
2. **Paired local control:** separately reviewed Samsung/webOS/Roku adapters with
   explicit visible pairing, secret storage, timeouts, one-action confirmation,
   observable results and revocation. Reuse maintained protocol libraries where
   justified; do not create a plugin framework before there is a real need.
3. **Guided cleanup transactions:** record original settings, approve a small
   plan, apply an exact action, verify, and provide its inverse. No blind remote-
   key macros, blanket app-removal lists or pretending a timeout succeeded.
4. **Broader platform evidence:** add model/firmware observations across brands
   and regions. Audit official manuals before giving menu paths. Models that
   share a badge or firmware number may still use different OS/hardware families.
5. **Experimental customization:** developer app installs and root feasibility
   research stay opt-in, separately labeled and exact-version-specific. No claim
   that root makes Android APKs work on Tizen/webOS, or fixes performance.

## Evidence levels

- **Documented:** official/vendor or cited upstream behavior; not tested here.
- **Fixture-tested:** code behavior verified against synthetic inputs; not a
  live device compatibility result.
- **Device-verified:** observed on one exact model/build with stated tests and
  limitations. Does not generalize to an entire brand or later firmware.
- **Experimental/unverified:** plausible route or community claim; no automatic
  action. Root success must distinguish temporary access, reboot reacquisition,
  persistent changes and a genuinely tested restoration path.
- **Unavailable/unknown:** explicitly state the gap and next evidence needed.

A future capability report needs platform, model, full firmware family/version,
source, permissions, exact observed behavior, negative results, restoration
limits and redacted evidence. Serial numbers, IP/MAC addresses, accounts, pairing
codes, tokens and household photographs do not belong in public reports.

## Guardrails and release acceptance

- Preserve upstream Android safety guards, recovery behavior and model lists.
- No platform is selected from brand alone; ambiguous inputs go to identification.
- New inspection must be opt-in, fixed-endpoint, GET-only, bounded, nonredirecting,
  proxy-free and privacy-filtered; never scan a network or perform "helpful" fallback.
- Keep manual settings, executable support and experimental research distinct.
- Run focused tests and existing suite, compare any failure with untouched
  upstream, resolve regressions and publish real test evidence. No test deletion
  to obtain a green result.
- Review public diffs for private data. Publish only the fork-owned work; do not
  open an unsolicited upstream PR or overwrite the upstream project's stance.

See [the entry workflow](../MULTIPLATFORM.md) and [platform guides](platforms/README.md).
