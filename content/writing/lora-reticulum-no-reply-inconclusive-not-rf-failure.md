---
title: No Reply Was an Inconclusive Result, Not Proof of RF Failure
url: /posts/lora-reticulum-no-reply-inconclusive-not-rf-failure.html
date: '2026-09-15'
read_time: 9
excerpt: Silence from the EWM looked like a hardware failure but the observation did
  not isolate which half of the wireless path was wrong.
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
- url: /posts/lora-reticulum-no-reply-inconclusive-not-rf-failure.html
  template: cms/templates/posts/posts--lora-reticulum-no-reply-inconclusive-not-rf-failure.tpl
  source: cms/templates/posts/posts--lora-reticulum-no-reply-inconclusive-not-rf-failure.json
---

# No Reply Was an Inconclusive Result, Not Proof of RF Failure

The radio was only one part of the system. The engineering problem was that Silence from the EWM looked like a hardware failure but the observation did not isolate which half of the wireless path was wrong.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **The automated analysis explicitly reported no reply while listing remote Mode 0, default profile, readiness/power and RF/antenna path as remaining causes.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **The verdict stayed bounded and the next test targeted missing observability.**

## How I framed the problem

The important part was preserving the distinction between local success and end-to-end success. The issue was Silence from the EWM looked like a hardware failure but the observation did not isolate which half of the wireless path was wrong. I had The automated analysis explicitly reported no reply while listing remote Mode 0, default profile, readiness/power and RF/antenna path as remaining causes., but the mechanism—An end-to-end timeout collapses transmitter, channel, receiver and remote protocol state into one symptom.—bounded what that evidence meant. The conclusion was The verdict stayed bounded and the next test targeted missing observability.

The E22/EWM investigation was valuable because it separated local module control from remote over-air state. Register reads, operating-mode GPIOs and AUX transitions can prove the local half while saying nothing definitive about the remote target. The exact documented management command gave us a narrow compatibility probe, but silence still had multiple possible causes.

The rule I carried forward was: **A timeout is a symptom until you can observe both sides of the boundary.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | Silence from the EWM looked like a hardware failure but the observation did not isolate which half of the wireless path was wrong. |
| Strongest evidence | The automated analysis explicitly reported no reply while listing remote Mode 0, default profile, readiness/power and RF/antenna path as remaining causes. |
| Mechanism | An end-to-end timeout collapses transmitter, channel, receiver and remote protocol state into one symptom. |
| Rejected shortcut | Replacing a radio module solely because a documented command timed out. |
| Retained result | The verdict stayed bounded and the next test targeted missing observability. |
| Carry-forward rule | A timeout is a symptom until you can observe both sides of the boundary. |

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

The experiment-specific mechanism was: An end-to-end timeout collapses transmitter, channel, receiver and remote protocol state into one symptom. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## Investigation sequence

I preserve negative results. A documented no-reply after a known command is valuable when the local mode/profile and AUX evidence are recorded. It narrows the next test toward the remote side without pretending to prove a failed RF front end.

The shortcut I avoided was **Replacing a radio module solely because a documented command timed out.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## Local success and end-to-end success are different

A recurring pattern in this lab was that one half of the system could be proven healthy while the complete link remained unknown. The Linux host could see the USB device. The container could run. RNS could parse its config. The local E22 could accept register commands. The LR1121 could arm RX. None of those facts alone proved that a remote radio decoded a packet and delivered it to Reticulum.

For **No Reply Was an Inconclusive Result, Not Proof of RF Failure**, the distinction matters because An end-to-end timeout collapses transmitter, channel, receiver and remote protocol state into one symptom. The evidence **The automated analysis explicitly reported no reply while listing remote Mode 0, default profile, readiness/power and RF/antenna path as remaining causes.** therefore supports a bounded statement, not a complete wireless PASS.

I now label test outcomes by layer: HOST, SERIAL, LOCAL\_MODEM, PHY\_DETECT, PACKET\_RX, REMOTE\_REPLY, RNS\_INTERFACE and RETICULUM\_PATH. That vocabulary keeps a green result at one layer from hiding an unknown state at the next.

## Instrumentation I would keep

```
ESP32 -> UART -> local E22 -> RF ---> remote EWM -> reply
  |        |        |                 |
 GPIO     bytes    AUX              mode/profile/power
```

The instrumentation should make state transitions explicit rather than print only final success. For serial/host work I want device identity, open failures and interface initialization. For LoRa PHY work I want the full profile plus preamble/header/header-error/CRC/RX counters. For E22/EWM I want UART writes, AUX timing and remote reply counts separated. For Reticulum I want interface state and rnstatus-visible behavior.

The reason is simple: **The automated analysis explicitly reported no reply while listing remote Mode 0, default profile, readiness/power and RF/antenna path as remaining causes.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For recovery, the test is intentionally hostile: assume the wireless profile is unknown and prove the wired path can still read or restore the module. A recovery procedure that needs the broken wireless state to be correct is not a recovery procedure.

For this case the pass condition follows directly from the retained result: **The verdict stayed bounded and the next test targeted missing observability.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## From bench experiment to infrastructure

The durable rule is **A timeout is a symptom until you can observe both sides of the boundary.**

If I keep this node running, I want the radio profile and host mapping versioned, the serial device stable, the container health tied to the Reticulum interface, and raw diagnostic evidence retained for failures. I do not want the only record of a working SF/BW/sync combination to be scrollback from one terminal.

I also want the physical layer documented with the same discipline. Antenna band, connector, placement and any gain/loss assumptions belong beside the radio configuration. Otherwise a later hardware substitution can change the link while the software repository remains unchanged.

At the Reticulum layer, I separate roles: which node is an endpoint, which is transport-capable, which interface reaches the LAN, and which interface reaches radio peers. That makes later scaling easier to reason about because every additional path has an owner and a failure model.

## The next experiment I would run

The decisive follow-up is the one that replaces an inferred state with a directly observed one. In this case, that means targeting the uncertainty behind: Silence from the EWM looked like a hardware failure but the observation did not isolate which half of the wireless path was wrong.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**A timeout is a symptom until you can observe both sides of the boundary.**

The retained result was: The verdict stayed bounded and the next test targeted missing observability.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
