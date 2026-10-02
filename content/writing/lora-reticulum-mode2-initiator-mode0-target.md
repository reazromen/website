---
title: Mode 2 Initiator and Mode 0 Target Was a Topology Contract
url: /posts/lora-reticulum-mode2-initiator-mode0-target.html
date: '2026-09-15'
read_time: 9
excerpt: Different EBYTE operating modes made it possible for both devices to be powered
  and configured yet unable to execute the intended over-air management transaction.
topic: lora-reticulum
tags:
- lora
- reticulum
- rnode
draft: false
featured: false
language: en
eyebrow: 'LoRa & Reticulum: E22/EWM Failure Isolation · deep-dive'
outputs:
- url: /posts/lora-reticulum-mode2-initiator-mode0-target.html
  template: cms/templates/posts/posts--lora-reticulum-mode2-initiator-mode0-target.tpl
  source: cms/templates/posts/posts--lora-reticulum-mode2-initiator-mode0-target.json
---

# Mode 2 Initiator and Mode 0 Target Was a Topology Contract

This experiment looked like a radio problem until I wrote down the layers. The actual issue was that Different EBYTE operating modes made it possible for both devices to be powered and configured yet unable to execute the intended over-air management transaction.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **V2.6 explicitly validated the local E22 as the Mode-2 OTA initiator and required the remote EWM target in Mode 0 for the canonical topology.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **Mode became a first-class compatibility parameter alongside RF profile.**

## How I framed the problem

I approached this as an experiment-design problem. Starting from Different EBYTE operating modes made it possible for both devices to be powered and configured yet unable to execute the intended over-air management transaction., I chose an observation that could separate at least two plausible causes: V2.6 explicitly validated the local E22 as the Mode-2 OTA initiator and required the remote EWM target in Mode 0 for the canonical topology. The result made sense because Operating mode changes how bytes are interpreted and whether wireless configuration commands are accepted or forwarded. It also prevented me from treating Assuming matching channel and air rate override an incorrect mode state. as proof. The retained result was Mode became a first-class compatibility parameter alongside RF profile.

The E22/EWM investigation was valuable because it separated local module control from remote over-air state. Register reads, operating-mode GPIOs and AUX transitions can prove the local half while saying nothing definitive about the remote target. The exact documented management command gave us a narrow compatibility probe, but silence still had multiple possible causes.

The rule I carried forward was: **Wireless protocols have control-plane state as well as PHY state.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | Different EBYTE operating modes made it possible for both devices to be powered and configured yet unable to execute the intended over-air management transaction. |
| Strongest evidence | V2.6 explicitly validated the local E22 as the Mode-2 OTA initiator and required the remote EWM target in Mode 0 for the canonical topology. |
| Mechanism | Operating mode changes how bytes are interpreted and whether wireless configuration commands are accepted or forwarded. |
| Rejected shortcut | Assuming matching channel and air rate override an incorrect mode state. |
| Retained result | Mode became a first-class compatibility parameter alongside RF profile. |
| Carry-forward rule | Wireless protocols have control-plane state as well as PHY state. |

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

- read/configure the local E22 first
- prove local mode GPIO state
- observe AUX only as local-module evidence
- send the exact documented remote command
- count remote replies independently from TX activity

The experiment-specific mechanism was: Operating mode changes how bytes are interpreted and whether wireless configuration commands are accepted or forwarded. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## What I would do next at larger scale

I would stop treating every node as an interactive lab device. Radio identity, firmware identity, interface type and accepted PHY profiles would become inventory. A deployment test would validate the host serial mapping, interface initialization, pairwise packet exchange and Reticulum reachability before the node was allowed to act as transport.

For RF planning I would add a real link-budget worksheet and measured site data instead of extrapolating from desk tests. The question would become required margin for a defined path rather than “how far can LoRa go?” For mixed hardware, I would maintain compatibility profiles so a 433 MHz LR1121 experiment could never be confused with an 867 MHz SX1262 RNode configuration.

For **Mode 2 Initiator and Mode 0 Target Was a Topology Contract**, the mechanism still scales: Operating mode changes how bytes are interpreted and whether wireless configuration commands are accepted or forwarded. Scaling adds automation; it does not remove the need to know which layer a PASS actually proves.

## Investigation sequence

I keep physical prerequisites outside the software hypothesis. Correct antennas, stable supply and deliberate spacing are test conditions, not optional accessories. If they are unknown, the right conclusion is “RF evidence invalid or incomplete,” not a guessed range number.

The shortcut I avoided was **Assuming matching channel and air rate override an incorrect mode state.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## Instrumentation I would keep

```
ESP32 -> UART -> local E22 -> RF ---> remote EWM -> reply
  |        |        |                 |
 GPIO     bytes    AUX              mode/profile/power
```

The instrumentation should make state transitions explicit rather than print only final success. For serial/host work I want device identity, open failures and interface initialization. For LoRa PHY work I want the full profile plus preamble/header/header-error/CRC/RX counters. For E22/EWM I want UART writes, AUX timing and remote reply counts separated. For Reticulum I want interface state and rnstatus-visible behavior.

The reason is simple: **V2.6 explicitly validated the local E22 as the Mode-2 OTA initiator and required the remote EWM target in Mode 0 for the canonical topology.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For E22/EWM, I keep local-control PASS separate from remote-reply PASS. The canonical command must produce its expected remote response before I call the OTA configuration path compatible. AUX activity alone cannot satisfy that gate.

For this case the pass condition follows directly from the retained result: **Mode became a first-class compatibility parameter alongside RF profile.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## What would falsify the conclusion

The retained result is **Mode became a first-class compatibility parameter alongside RF profile.** A useful conclusion must say what future observation would force me to revisit it.

If the same controlled topology produced evidence inconsistent with **V2.6 explicitly validated the local E22 as the Mode-2 OTA initiator and required the remote EWM target in Mode 0 for the canonical topology.**, I would reopen the diagnosis. If a wired recovery read showed the remote module was already in the expected state, the fault domain would move back toward RF/profile compatibility. If a matched antenna and known-good peer produced clean packets, the earlier silence could not be used as proof that the local modem was defective. If Reticulum failed while direct packet exchange remained clean, the investigation would move up the stack.

This is how I keep RF work from turning into stories about invisible signals. The hypothesis has to predict an observable difference.

## The next experiment I would run

I would also reverse the test direction where possible. A result that survives transmitter/receiver role reversal is stronger than one that depends on an unexplained asymmetry in the lab setup.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Wireless protocols have control-plane state as well as PHY state.**

The retained result was: Mode became a first-class compatibility parameter alongside RF profile.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
