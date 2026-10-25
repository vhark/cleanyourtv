# Start here: clean up the TV you actually have

This fork expands the original Android-first project into an operating-system-aware
assistant workflow. **It does not turn a brand name into a promise of root or
package removal.** A TCL, Hisense, Toshiba or Panasonic badge can sit on several
different operating systems. An HDMI streaming box is a separate device from the TV.

## What is implemented

- An offline, standard-library Python capability planner: `tools/platforms.py`.
- User-guided platform-specific cleanup and control routes in [the platform guides](docs/platforms/README.md).
- Explicit opt-in, read-only metadata inspection for Samsung Tizen and Roku.
- The upstream Android tools, launcher, safeguards and model examples remain unchanged.

New platform inspection is tested with synthetic protocol fixtures, **not certified
on real TVs**. Plans and guides are not automatic cleanup actions. No new root,
pairing, app installation, keypress, power or package-removal command is included.
For Android, existing commands retain their existing effects and require their own
review and approval; the planner never executes them.

## 1. Identify the operating system before connecting

Ask the owner for the model, OS and firmware from About/Support. Reuse answers
already given; ask one question at a time. Do not ask them to publish a serial,
MAC address, account name, pairing code or an unredacted About screenshot.

```sh
python3 tools/platforms.py list
python3 tools/platforms.py plan --platform tizen --json
python3 tools/platforms.py plan --platform roku
python3 tools/platforms.py plan --brand TCL --json
```

The last command must stay **unknown** until the OS is identified. Optional
`--model` and `--firmware` arguments preserve the supplied strings; they are owner
claims, not device-verified identity or proof of exploit compatibility. Treat any
plan containing those values as private if the owner entered personal labels.

## 2. Agree on the useful outcome

Choose the smallest useful change: a tidier Home screen, fewer unwanted apps,
less autoplay, better privacy, a preferred startup input, local remote control,
or diagnosis of sluggish performance. Ask which apps, inputs, casting,
accessibility aids, voice features and parental controls must remain.

Explain the platform limits before asking for debug privileges. Ordinary local
remote control is not root. Developer-mode sideloading is not permission to
remove system packages. A launcher app is not necessarily a replacement for the
system Home button. Root can still be constrained by firmware security controls.

## 3. Inspect only a specifically approved endpoint

Most guides start with the physical remote and need no network connection. For a
known Samsung or Roku, the owner can separately authorize an identity check:

```sh
# Example address only — replace it with the owner's confirmed local TV address.
python3 tools/platforms.py inspect --platform tizen --host 192.168.50.20 --confirm-local-device --json
python3 tools/platforms.py inspect --platform roku --host 192.168.50.20 --confirm-local-device --json
```

These are alternative examples, **not a sequence to try against one device**.
The flag records the operator's explicit opt-in; it does not prove network or
device ownership. Validate the returned model against the physical TV. This first
version accepts only explicit RFC1918 IPv4 literals: no public addresses,
hostnames, URLs, arbitrary ports, IPv6 or automatic discovery. It uses fixed
read-only endpoints, no redirects or environment proxies, and bounded responses.
A blocked or unavailable endpoint is inconclusive—not permission to scan, change
settings, weaken authentication or try another protocol.

The response intentionally omits raw identifiers and server payloads. Metadata
is reported evidence, not proof that cleanup, root, power-off or every advertised
feature works. Missing firmware is unknown, not a fabricated version.

## 4. Prepare and approve the change

Follow the exact platform guide. Record current settings privately and explain
what each proposed change removes, what may stop working and how to undo it.
Ask for approval of the explicit target and change list. Make one small change,
read it back and verify with the owner and physical remote. Keep a working Home,
Settings, input and network/recovery path throughout.

Do not interpret "clean everything" as consent to a factory reset, uninstalling
paid apps, cancelling subscriptions, disabling firmware updates, changing DNS
for the whole household, rooting or flashing firmware. Removing an app may
remove its local data and does not necessarily cancel its subscription. Account-
synced changes can affect other TVs. Those need separate explanations/approvals.

Never run a root tool merely because its command is named "probe": some such
commands actually execute an exploit. Firmware research is separate from routine
cleanup. No root exploit is included in this fork's platform planner.

## 5. Verify the result, then close maintenance access

Check Home/Back, volume, inputs, retained apps, playback/audio, casting and
accessibility functions. A network success response is not evidence of physical
TV behavior. Ask before rebooting. Store changes, readback, rollback instructions
and limitations in the owner's private record, not this public repository.

Close temporary debugging/pairing access when finished. After a partial failure,
first ensure that closing it will not strand the only recovery path; any extended
local recovery session needs an explicit scope and time limit. Prefer ordinary
native integrations over indefinitely open maintenance shells.

## Contribute evidence, not blanket support claims

For a new model, provide a **redacted** exact model/firmware/OS record, source,
confirmed capability, method and result, rollback, and what remains untested.
Do not place closed-platform reports in Android `debloat.txt` examples or label a
model tested merely because a mock test passed. See the
[coverage roadmap and acceptance gates](docs/coverage-roadmap.md).

Tests for this extension run offline:

```sh
python3 -m unittest discover -s tests -p 'test_platforms.py' -v
```

The complete upstream suite has additional environment requirements documented
in [CONTRIBUTING.md](CONTRIBUTING.md). No network-enabled `inspect` command is run
as a test against household hardware.
