---
title: SF, Bandwidth and Coding Rate Are a Three-Way Trade
url: /posts/lora-reticulum-sf-bandwidth-coding-rate-trade.html
date: '2026-09-15'
read_time: 9
excerpt: Changing one LoRa parameter to chase range can quietly change airtime, sensitivity
  and compatibility elsewhere.
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
- url: /posts/lora-reticulum-sf-bandwidth-coding-rate-trade.html
  template: cms/templates/posts/posts--lora-reticulum-sf-bandwidth-coding-rate-trade.tpl
  source: cms/templates/posts/posts--lora-reticulum-sf-bandwidth-coding-rate-trade.json
---

# SF, Bandwidth and Coding Rate Are a Three-Way Trade

One of the fastest ways to get lost in LoRa debugging is to treat silence as one failure mode. Here, Changing one LoRa parameter to chase range can quietly change airtime, sensitivity and compatibility elsewhere.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **The experiments used profiles such as SF7/BW125/CR4/5 and SF8/BW125/CR4/5, and later scanned multiple SF/BW combinations while keeping coding rate explicit.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **PHY parameters were recorded as a tuple and scanned systematically.**

## How I framed the problem

I treated this as a boundary-identification problem. The observed failure was Changing one LoRa parameter to chase range can quietly change airtime, sensitivity and compatibility elsewhere. The strongest evidence was The experiments used profiles such as SF7/BW125/CR4/5 and SF8/BW125/CR4/5, and later scanned multiple SF/BW combinations while keeping coding rate explicit. The mechanism was Spreading factor changes symbol duration, bandwidth changes noise bandwidth and symbol rate, and coding rate adds redundancy; the combination defines the waveform cost and robustness. That made the tempting shortcut—Treating “higher SF” as a free range upgrade.—insufficient. The retained result was PHY parameters were recorded as a tuple and scanned systematically.

LoRa compatibility is a tuple, not a frequency number. Frequency, bandwidth, spreading factor, coding rate, preamble, sync word, CRC and packet parameters all participate. A receiver can detect part of a waveform without accepting a valid packet, which is why I prefer IRQ/state counters over one final RX counter.

The rule I carried forward was: **Tune LoRa as a complete PHY, not as independent sliders.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | Changing one LoRa parameter to chase range can quietly change airtime, sensitivity and compatibility elsewhere. |
| Strongest evidence | The experiments used profiles such as SF7/BW125/CR4/5 and SF8/BW125/CR4/5, and later scanned multiple SF/BW combinations while keeping coding rate explicit. |
| Mechanism | Spreading factor changes symbol duration, bandwidth changes noise bandwidth and symbol rate, and coding rate adds redundancy; the combination defines the waveform cost and robustness. |
| Rejected shortcut | Treating “higher SF” as a free range upgrade. |
| Retained result | PHY parameters were recorded as a tuple and scanned systematically. |
| Carry-forward rule | Tune LoRa as a complete PHY, not as independent sliders. |

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

The experiment-specific mechanism was: Spreading factor changes symbol duration, bandwidth changes noise bandwidth and symbol rate, and coding rate adds redundancy; the combination defines the waveform cost and robustness. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## Investigation sequence

My sequence is host first, radio second. I freeze the USB/device path, prove the intended target MCU, capture the radio profile, and only then change RF variables. That prevents a disappearing tty, a bridge/target mix-up or ModemManager from being misdiagnosed as propagation.

The shortcut I avoided was **Treating “higher SF” as a free range upgrade.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## From bench experiment to infrastructure

The durable rule is **Tune LoRa as a complete PHY, not as independent sliders.**

If I keep this node running, I want the radio profile and host mapping versioned, the serial device stable, the container health tied to the Reticulum interface, and raw diagnostic evidence retained for failures. I do not want the only record of a working SF/BW/sync combination to be scrollback from one terminal.

I also want the physical layer documented with the same discipline. Antenna band, connector, placement and any gain/loss assumptions belong beside the radio configuration. Otherwise a later hardware substitution can change the link while the software repository remains unchanged.

At the Reticulum layer, I separate roles: which node is an endpoint, which is transport-capable, which interface reaches the LAN, and which interface reaches radio peers. That makes later scaling easier to reason about because every additional path has an owner and a failure model.

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

The reason is simple: **The experiments used profiles such as SF7/BW125/CR4/5 and SF8/BW125/CR4/5, and later scanned multiple SF/BW combinations while keeping coding rate explicit.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

A pass needs a reproducible pair, not a lucky packet. I want the exact hardware identities, antennas, PHY tuple, mode state and host mapping written down, then repeated send/receive evidence. Only after that do I let Reticulum-layer behavior become the acceptance target.

For this case the pass condition follows directly from the retained result: **PHY parameters were recorded as a tuple and scanned systematically.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## Local success and end-to-end success are different

A recurring pattern in this lab was that one half of the system could be proven healthy while the complete link remained unknown. The Linux host could see the USB device. The container could run. RNS could parse its config. The local E22 could accept register commands. The LR1121 could arm RX. None of those facts alone proved that a remote radio decoded a packet and delivered it to Reticulum.

For **SF, Bandwidth and Coding Rate Are a Three-Way Trade**, the distinction matters because Spreading factor changes symbol duration, bandwidth changes noise bandwidth and symbol rate, and coding rate adds redundancy; the combination defines the waveform cost and robustness. The evidence **The experiments used profiles such as SF7/BW125/CR4/5 and SF8/BW125/CR4/5, and later scanned multiple SF/BW combinations while keeping coding rate explicit.** therefore supports a bounded statement, not a complete wireless PASS.

I now label test outcomes by layer: HOST, SERIAL, LOCAL\_MODEM, PHY\_DETECT, PACKET\_RX, REMOTE\_REPLY, RNS\_INTERFACE and RETICULUM\_PATH. That vocabulary keeps a green result at one layer from hiding an unknown state at the next.

## The next experiment I would run

If treating “higher sf” as a free range upgrade. were actually the cause, I would expect a repeatable change in the observation that currently supports the retained result. Without that change, the theory is convenient but weak.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Tune LoRa as a complete PHY, not as independent sliders.**

The retained result was: PHY parameters were recorded as a tuple and scanned systematically.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
