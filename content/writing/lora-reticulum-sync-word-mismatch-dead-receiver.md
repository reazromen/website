---
title: Sync Word Mismatch Can Look Like a Dead Receiver
url: /posts/lora-reticulum-sync-word-mismatch-dead-receiver.html
date: '2024-06-30'
read_time: 8
excerpt: A receiver can detect energy or even preamble-like activity while rejecting
  the packet format expected by the application.
topic: lora-reticulum
tags:
- lora
- reticulum
- rnode
draft: false
featured: false
language: en
eyebrow: 'LoRa & Reticulum: PHY Parameters and Radio Evidence · deep-dive'
outputs:
- url: /posts/lora-reticulum-sync-word-mismatch-dead-receiver.html
  template: cms/templates/posts/posts--lora-reticulum-sync-word-mismatch-dead-receiver.tpl
  source: cms/templates/posts/posts--lora-reticulum-sync-word-mismatch-dead-receiver.json
---

# Sync Word Mismatch Can Look Like a Dead Receiver

I started this test with hardware on the desk and ended up debugging the boundary between host, modem and RF because A receiver can detect energy or even preamble-like activity while rejecting the packet format expected by the application.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **The LR1121 diagnostics explicitly printed sync-word settings such as 0x12 or 0x34 alongside SF/BW/CRC state during different tests.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **Sync word became part of the profile record and scan interpretation.**

## How I framed the problem

This case became a state-machine problem rather than a signal-strength problem. The symptom was A receiver can detect energy or even preamble-like activity while rejecting the packet format expected by the application. The evidence was The LR1121 diagnostics explicitly printed sync-word settings such as 0x12 or 0x34 alongside SF/BW/CRC state during different tests. The underlying state transition mattered because LoRa sync word participates in packet compatibility after coarse RF detection; mismatched values can prevent valid packet acceptance. I rejected Assuming matching frequency and spreading factor are sufficient for interoperability. and kept the narrower result: Sync word became part of the profile record and scan interpretation.

LoRa compatibility is a tuple, not a frequency number. Frequency, bandwidth, spreading factor, coding rate, preamble, sync word, CRC and packet parameters all participate. A receiver can detect part of a waveform without accepting a valid packet, which is why I prefer IRQ/state counters over one final RX counter.

The rule I carried forward was: **Packet compatibility extends beyond frequency, SF and bandwidth.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | A receiver can detect energy or even preamble-like activity while rejecting the packet format expected by the application. |
| Strongest evidence | The LR1121 diagnostics explicitly printed sync-word settings such as 0x12 or 0x34 alongside SF/BW/CRC state during different tests. |
| Mechanism | LoRa sync word participates in packet compatibility after coarse RF detection; mismatched values can prevent valid packet acceptance. |
| Rejected shortcut | Assuming matching frequency and spreading factor are sufficient for interoperability. |
| Retained result | Sync word became part of the profile record and scan interpretation. |
| Carry-forward rule | Packet compatibility extends beyond frequency, SF and bandwidth. |

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

- record frequency/BW/SF/CR together
- record sync word and packet parameters
- clear/read IRQ state between profiles
- separate preamble/header/CRC/RX counters
- freeze one profile after discovery

The experiment-specific mechanism was: LoRa sync word participates in packet compatibility after coarse RF detection; mismatched values can prevent valid packet acceptance. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## Investigation sequence

I change one compatibility dimension at a time. A sweep is useful only if every profile records the exact SF, bandwidth, sync word and result. Otherwise the console becomes a blur and a later successful profile cannot be reconstructed.

The shortcut I avoided was **Assuming matching frequency and spreading factor are sufficient for interoperability.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## Local success and end-to-end success are different

A recurring pattern in this lab was that one half of the system could be proven healthy while the complete link remained unknown. The Linux host could see the USB device. The container could run. RNS could parse its config. The local E22 could accept register commands. The LR1121 could arm RX. None of those facts alone proved that a remote radio decoded a packet and delivered it to Reticulum.

For **Sync Word Mismatch Can Look Like a Dead Receiver**, the distinction matters because LoRa sync word participates in packet compatibility after coarse RF detection; mismatched values can prevent valid packet acceptance. The evidence **The LR1121 diagnostics explicitly printed sync-word settings such as 0x12 or 0x34 alongside SF/BW/CRC state during different tests.** therefore supports a bounded statement, not a complete wireless PASS.

I now label test outcomes by layer: HOST, SERIAL, LOCAL\_MODEM, PHY\_DETECT, PACKET\_RX, REMOTE\_REPLY, RNS\_INTERFACE and RETICULUM\_PATH. That vocabulary keeps a green result at one layer from hiding an unknown state at the next.

## Instrumentation I would keep

```
frequency + bandwidth + SF + CR + sync + packet params
                     |
                     v
               compatible waveform
                     |
          preamble -> header -> CRC -> RX
```

The instrumentation should make state transitions explicit rather than print only final success. For serial/host work I want device identity, open failures and interface initialization. For LoRa PHY work I want the full profile plus preamble/header/header-error/CRC/RX counters. For E22/EWM I want UART writes, AUX timing and remote reply counts separated. For Reticulum I want interface state and rnstatus-visible behavior.

The reason is simple: **The LR1121 diagnostics explicitly printed sync-word settings such as 0x12 or 0x34 alongside SF/BW/CRC state during different tests.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For range work, I would not publish a distance without antenna identity, height/environment, TX power, PHY and repeated packet statistics. A single successful packet is a discovery event; a usable link needs margin and repeatability.

For this case the pass condition follows directly from the retained result: **Sync word became part of the profile record and scan interpretation.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## From bench experiment to infrastructure

The durable rule is **Packet compatibility extends beyond frequency, SF and bandwidth.**

If I keep this node running, I want the radio profile and host mapping versioned, the serial device stable, the container health tied to the Reticulum interface, and raw diagnostic evidence retained for failures. I do not want the only record of a working SF/BW/sync combination to be scrollback from one terminal.

I also want the physical layer documented with the same discipline. Antenna band, connector, placement and any gain/loss assumptions belong beside the radio configuration. Otherwise a later hardware substitution can change the link while the software repository remains unchanged.

At the Reticulum layer, I separate roles: which node is an endpoint, which is transport-capable, which interface reaches the LAN, and which interface reaches radio peers. That makes later scaling easier to reason about because every additional path has an owner and a failure model.

## The next experiment I would run

A useful negative control is to reproduce the local success while deliberately making the remote side incompatible. That should preserve local evidence but remove the end-to-end result, proving the layers are being measured separately.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Packet compatibility extends beyond frequency, SF and bandwidth.**

The retained result was: Sync word became part of the profile record and scan interpretation.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
