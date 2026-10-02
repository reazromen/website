---
title: AUX Activity Proved Transmission Work, Not Remote Reception
url: /posts/lora-reticulum-aux-activity-not-remote-reception.html
date: '2026-09-15'
read_time: 8
excerpt: The E22 AUX pin changed around transmissions, but the remote EWM still returned
  no bytes.
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
- url: /posts/lora-reticulum-aux-activity-not-remote-reception.html
  template: cms/templates/posts/posts--lora-reticulum-aux-activity-not-remote-reception.tpl
  source: cms/templates/posts/posts--lora-reticulum-aux-activity-not-remote-reception.json
---

# AUX Activity Proved Transmission Work, Not Remote Reception

One of the fastest ways to get lost in LoRa debugging is to treat silence as one failure mode. Here, The E22 AUX pin changed around transmissions, but the remote EWM still returned no bytes.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **Autotest captured AUX low/high timing and TX evidence even while EWM reply counters stayed at zero.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **AUX was retained as local-transmit evidence only.**

## How I framed the problem

This case became a state-machine problem rather than a signal-strength problem. The symptom was The E22 AUX pin changed around transmissions, but the remote EWM still returned no bytes. The evidence was Autotest captured AUX low/high timing and TX evidence even while EWM reply counters stayed at zero. The underlying state transition mattered because AUX reflects local module busy/state transitions; it cannot observe what happened after the signal left the transmitter. I rejected Treating AUX toggling as proof that the remote device received and decoded the frame. and kept the narrower result: AUX was retained as local-transmit evidence only.

The E22/EWM investigation was valuable because it separated local module control from remote over-air state. Register reads, operating-mode GPIOs and AUX transitions can prove the local half while saying nothing definitive about the remote target. The exact documented management command gave us a narrow compatibility probe, but silence still had multiple possible causes.

The rule I carried forward was: **Name diagnostics after what they actually observe, not what you hope they imply.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | The E22 AUX pin changed around transmissions, but the remote EWM still returned no bytes. |
| Strongest evidence | Autotest captured AUX low/high timing and TX evidence even while EWM reply counters stayed at zero. |
| Mechanism | AUX reflects local module busy/state transitions; it cannot observe what happened after the signal left the transmitter. |
| Rejected shortcut | Treating AUX toggling as proof that the remote device received and decoded the frame. |
| Retained result | AUX was retained as local-transmit evidence only. |
| Carry-forward rule | Name diagnostics after what they actually observe, not what you hope they imply. |

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

The experiment-specific mechanism was: AUX reflects local module busy/state transitions; it cannot observe what happened after the signal left the transmitter. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## Investigation sequence

I change one compatibility dimension at a time. A sweep is useful only if every profile records the exact SF, bandwidth, sync word and result. Otherwise the console becomes a blur and a later successful profile cannot be reconstructed.

The shortcut I avoided was **Treating AUX toggling as proof that the remote device received and decoded the frame.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## From bench experiment to infrastructure

The durable rule is **Name diagnostics after what they actually observe, not what you hope they imply.**

If I keep this node running, I want the radio profile and host mapping versioned, the serial device stable, the container health tied to the Reticulum interface, and raw diagnostic evidence retained for failures. I do not want the only record of a working SF/BW/sync combination to be scrollback from one terminal.

I also want the physical layer documented with the same discipline. Antenna band, connector, placement and any gain/loss assumptions belong beside the radio configuration. Otherwise a later hardware substitution can change the link while the software repository remains unchanged.

At the Reticulum layer, I separate roles: which node is an endpoint, which is transport-capable, which interface reaches the LAN, and which interface reaches radio peers. That makes later scaling easier to reason about because every additional path has an owner and a failure model.

## Instrumentation I would keep

```
ESP32 -> UART -> local E22 -> RF ---> remote EWM -> reply
  |        |        |                 |
 GPIO     bytes    AUX              mode/profile/power
```

The instrumentation should make state transitions explicit rather than print only final success. For serial/host work I want device identity, open failures and interface initialization. For LoRa PHY work I want the full profile plus preamble/header/header-error/CRC/RX counters. For E22/EWM I want UART writes, AUX timing and remote reply counts separated. For Reticulum I want interface state and rnstatus-visible behavior.

The reason is simple: **Autotest captured AUX low/high timing and TX evidence even while EWM reply counters stayed at zero.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For range work, I would not publish a distance without antenna identity, height/environment, TX power, PHY and repeated packet statistics. A single successful packet is a discovery event; a usable link needs margin and repeatability.

For this case the pass condition follows directly from the retained result: **AUX was retained as local-transmit evidence only.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## Local success and end-to-end success are different

A recurring pattern in this lab was that one half of the system could be proven healthy while the complete link remained unknown. The Linux host could see the USB device. The container could run. RNS could parse its config. The local E22 could accept register commands. The LR1121 could arm RX. None of those facts alone proved that a remote radio decoded a packet and delivered it to Reticulum.

For **AUX Activity Proved Transmission Work, Not Remote Reception**, the distinction matters because AUX reflects local module busy/state transitions; it cannot observe what happened after the signal left the transmitter. The evidence **Autotest captured AUX low/high timing and TX evidence even while EWM reply counters stayed at zero.** therefore supports a bounded statement, not a complete wireless PASS.

I now label test outcomes by layer: HOST, SERIAL, LOCAL\_MODEM, PHY\_DETECT, PACKET\_RX, REMOTE\_REPLY, RNS\_INTERFACE and RETICULUM\_PATH. That vocabulary keeps a green result at one layer from hiding an unknown state at the next.

## The next experiment I would run

A useful negative control is to reproduce the local success while deliberately making the remote side incompatible. That should preserve local evidence but remove the end-to-end result, proving the layers are being measured separately.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Name diagnostics after what they actually observe, not what you hope they imply.**

The retained result was: AUX was retained as local-transmit evidence only.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
