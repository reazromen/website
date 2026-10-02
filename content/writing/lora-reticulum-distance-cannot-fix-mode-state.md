---
title: Changing Distance Did Not Turn an Unknown Mode into a Known Mode
url: /posts/lora-reticulum-distance-cannot-fix-mode-state.html
date: '2026-09-15'
read_time: 9
excerpt: Repeated no-response behavior at different physical setups did not prove
  a pure propagation problem because the remote device mode/profile was still uncertain.
topic: lora-reticulum
tags:
- lora
- reticulum
- rnode
draft: false
featured: false
language: en
eyebrow: 'LoRa & Reticulum: Antennas, Range and Link Budget · deep-dive'
outputs:
- url: /posts/lora-reticulum-distance-cannot-fix-mode-state.html
  template: cms/templates/posts/posts--lora-reticulum-distance-cannot-fix-mode-state.tpl
  source: cms/templates/posts/posts--lora-reticulum-distance-cannot-fix-mode-state.json
---

# Changing Distance Did Not Turn an Unknown Mode into a Known Mode

This experiment looked like a radio problem until I wrote down the layers. The actual issue was that Repeated no-response behavior at different physical setups did not prove a pure propagation problem because the remote device mode/profile was still uncertain.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **The E22/EWM analysis consistently kept EWM mode, stored profile, readiness/power and RF/antenna path as unresolved causes when no reply arrived.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **The next decisive test moved toward direct wired access instead of more distance experiments.**

## How I framed the problem

The important part was preserving the distinction between local success and end-to-end success. The issue was Repeated no-response behavior at different physical setups did not prove a pure propagation problem because the remote device mode/profile was still uncertain. I had The E22/EWM analysis consistently kept EWM mode, stored profile, readiness/power and RF/antenna path as unresolved causes when no reply arrived., but the mechanism—Distance changes path loss but cannot repair a remote configuration mismatch or disabled transport state.—bounded what that evidence meant. The conclusion was The next decisive test moved toward direct wired access instead of more distance experiments.

Range discussions become useful only after the antenna and link budget are real. TX power is one term. Antenna match, cable/connector loss, receiver sensitivity, PHY, interference, terrain, height and margin all matter. A test with the wrong antenna or an unknown remote mode is not evidence for maximum distance.

The rule I carried forward was: **When configuration state is unknown, change observability before changing geography.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | Repeated no-response behavior at different physical setups did not prove a pure propagation problem because the remote device mode/profile was still uncertain. |
| Strongest evidence | The E22/EWM analysis consistently kept EWM mode, stored profile, readiness/power and RF/antenna path as unresolved causes when no reply arrived. |
| Mechanism | Distance changes path loss but cannot repair a remote configuration mismatch or disabled transport state. |
| Rejected shortcut | Treating “same result at another distance” as proof of a failed radio front end. |
| Retained result | The next decisive test moved toward direct wired access instead of more distance experiments. |
| Carry-forward rule | When configuration state is unknown, change observability before changing geography. |

I keep this table because radio work is unusually vulnerable to folklore. A missing packet can become “bad antenna,” “wrong SF,” “dead module” or “too close” depending on which theory is most convenient. Writing the evidence beside the theory forces the conclusion to remain narrower than the timeout.

## The boundary I wanted to prove

```
Linux host / Docker
   |
   +--> Reticulum rnsd
   |      |-- RNodeInterface -> /dev/rnode -> USB/UART -> radio MCU
   |      `-- TCPServerInterface -> LAN peers
   |
radio firmware
   -> frequency + BW + SF + CR + sync word + power
   -> RF front end
   -> matched antenna
   -> propagation path
   -> remote radio profile/mode
   -> remote host / Reticulum
```

For this layer I wanted these checks before changing another parameter:

- use a band-appropriate antenna at both ends
- record TX power without making it the only variable
- document distance/height/environment
- know the receiver sensitivity/PHY assumptions
- keep margin for real deployment variation

The experiment-specific mechanism was: Distance changes path loss but cannot repair a remote configuration mismatch or disabled transport state. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## Investigation sequence

I preserve negative results. A documented no-reply after a known command is valuable when the local mode/profile and AUX evidence are recorded. It narrows the next test toward the remote side without pretending to prove a failed RF front end.

The shortcut I avoided was **Treating “same result at another distance” as proof of a failed radio front end.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## What I would do next at larger scale

I would stop treating every node as an interactive lab device. Radio identity, firmware identity, interface type and accepted PHY profiles would become inventory. A deployment test would validate the host serial mapping, interface initialization, pairwise packet exchange and Reticulum reachability before the node was allowed to act as transport.

For RF planning I would add a real link-budget worksheet and measured site data instead of extrapolating from desk tests. The question would become required margin for a defined path rather than “how far can LoRa go?” For mixed hardware, I would maintain compatibility profiles so a 433 MHz LR1121 experiment could never be confused with an 867 MHz SX1262 RNode configuration.

For **Changing Distance Did Not Turn an Unknown Mode into a Known Mode**, the mechanism still scales: Distance changes path loss but cannot repair a remote configuration mismatch or disabled transport state. Scaling adds automation; it does not remove the need to know which layer a PASS actually proves.

## Instrumentation I would keep

```
TX power + TX antenna - losses - path loss + RX antenna
                         |
                         v
               received level vs sensitivity
                         |
                      margin
```

The instrumentation should make state transitions explicit rather than print only final success. For serial/host work I want device identity, open failures and interface initialization. For LoRa PHY work I want the full profile plus preamble/header/header-error/CRC/RX counters. For E22/EWM I want UART writes, AUX timing and remote reply counts separated. For Reticulum I want interface state and rnstatus-visible behavior.

The reason is simple: **The E22/EWM analysis consistently kept EWM mode, stored profile, readiness/power and RF/antenna path as unresolved causes when no reply arrived.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For recovery, the test is intentionally hostile: assume the wireless profile is unknown and prove the wired path can still read or restore the module. A recovery procedure that needs the broken wireless state to be correct is not a recovery procedure.

For this case the pass condition follows directly from the retained result: **The next decisive test moved toward direct wired access instead of more distance experiments.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## What would falsify the conclusion

The retained result is **The next decisive test moved toward direct wired access instead of more distance experiments.** A useful conclusion must say what future observation would force me to revisit it.

If the same controlled topology produced evidence inconsistent with **The E22/EWM analysis consistently kept EWM mode, stored profile, readiness/power and RF/antenna path as unresolved causes when no reply arrived.**, I would reopen the diagnosis. If a wired recovery read showed the remote module was already in the expected state, the fault domain would move back toward RF/profile compatibility. If a matched antenna and known-good peer produced clean packets, the earlier silence could not be used as proof that the local modem was defective. If Reticulum failed while direct packet exchange remained clean, the investigation would move up the stack.

This is how I keep RF work from turning into stories about invisible signals. The hypothesis has to predict an observable difference.

## The next experiment I would run

The decisive follow-up is the one that replaces an inferred state with a directly observed one. In this case, that means targeting the uncertainty behind: Repeated no-response behavior at different physical setups did not prove a pure propagation problem because the remote device mode/profile was still uncertain.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**When configuration state is unknown, change observability before changing geography.**

The retained result was: The next decisive test moved toward direct wired access instead of more distance experiments.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
