---
title: A 2.4 GHz Antenna Is Not a Generic Antenna for 433 or 868 MHz
url: /posts/lora-reticulum-24ghz-antenna-not-generic-lora-antenna.html
date: '2026-09-15'
read_time: 9
excerpt: Having only a 2.4 GHz antenna available created pressure to use it for sub-GHz
  experiments just to continue testing.
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
- url: /posts/lora-reticulum-24ghz-antenna-not-generic-lora-antenna.html
  template: cms/templates/posts/posts--lora-reticulum-24ghz-antenna-not-generic-lora-antenna.tpl
  source: cms/templates/posts/posts--lora-reticulum-24ghz-antenna-not-generic-lora-antenna.json
---

# A 2.4 GHz Antenna Is Not a Generic Antenna for 433 or 868 MHz

The useful lesson was not 'LoRa has long range.' It was that Having only a 2.4 GHz antenna available created pressure to use it for sub-GHz experiments just to continue testing.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **The radio work covered 433 MHz and 867.2 MHz profiles, while the available spare antenna was for a very different 2.4 GHz band.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **The sub-GHz link was kept conceptually separate from Wi-Fi antenna hardware.**

## How I framed the problem

I wrote down what the local node could prove and what it could not prove. The problem was Having only a 2.4 GHz antenna available created pressure to use it for sub-GHz experiments just to continue testing. The observation The radio work covered 433 MHz and 867.2 MHz profiles, while the available spare antenna was for a very different 2.4 GHz band. covered one side of the path. Because Antenna resonance, matching network and electrical length are frequency-dependent; a connector fitting mechanically says nothing about RF match., it did not justify Attaching any small whip with the right connector and treating the result as representative.. The useful result was The sub-GHz link was kept conceptually separate from Wi-Fi antenna hardware.

Range discussions become useful only after the antenna and link budget are real. TX power is one term. Antenna match, cable/connector loss, receiver sensitivity, PHY, interference, terrain, height and margin all matter. A test with the wrong antenna or an unknown remote mode is not evidence for maximum distance.

The rule I carried forward was: **Mechanical compatibility is not RF compatibility.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | Having only a 2.4 GHz antenna available created pressure to use it for sub-GHz experiments just to continue testing. |
| Strongest evidence | The radio work covered 433 MHz and 867.2 MHz profiles, while the available spare antenna was for a very different 2.4 GHz band. |
| Mechanism | Antenna resonance, matching network and electrical length are frequency-dependent; a connector fitting mechanically says nothing about RF match. |
| Rejected shortcut | Attaching any small whip with the right connector and treating the result as representative. |
| Retained result | The sub-GHz link was kept conceptually separate from Wi-Fi antenna hardware. |
| Carry-forward rule | Mechanical compatibility is not RF compatibility. |

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

The experiment-specific mechanism was: Antenna resonance, matching network and electrical length are frequency-dependent; a connector fitting mechanically says nothing about RF match. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## Investigation sequence

I separate configuration from reception. A local register read proves the local module. A local AUX transition proves local work. A preamble IRQ proves partial RF recognition. A valid header/CRC/RX proves more. A Reticulum announcement proves more again. Each layer earns a different claim.

The shortcut I avoided was **Attaching any small whip with the right connector and treating the result as representative.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## Local success and end-to-end success are different

A recurring pattern in this lab was that one half of the system could be proven healthy while the complete link remained unknown. The Linux host could see the USB device. The container could run. RNS could parse its config. The local E22 could accept register commands. The LR1121 could arm RX. None of those facts alone proved that a remote radio decoded a packet and delivered it to Reticulum.

For **A 2.4 GHz Antenna Is Not a Generic Antenna for 433 or 868 MHz**, the distinction matters because Antenna resonance, matching network and electrical length are frequency-dependent; a connector fitting mechanically says nothing about RF match. The evidence **The radio work covered 433 MHz and 867.2 MHz profiles, while the available spare antenna was for a very different 2.4 GHz band.** therefore supports a bounded statement, not a complete wireless PASS.

I now label test outcomes by layer: HOST, SERIAL, LOCAL\_MODEM, PHY\_DETECT, PACKET\_RX, REMOTE\_REPLY, RNS\_INTERFACE and RETICULUM\_PATH. That vocabulary keeps a green result at one layer from hiding an unknown state at the next.

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

The reason is simple: **The radio work covered 433 MHz and 867.2 MHz profiles, while the available spare antenna was for a very different 2.4 GHz band.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For a host/interface article, acceptance means the service survives restart and re-enumeration without silently binding to the wrong device. For a PHY article, it means two endpoints agree on the complete packet profile and produce valid RX evidence rather than only RF activity.

For this case the pass condition follows directly from the retained result: **The sub-GHz link was kept conceptually separate from Wi-Fi antenna hardware.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## From bench experiment to infrastructure

The durable rule is **Mechanical compatibility is not RF compatibility.**

If I keep this node running, I want the radio profile and host mapping versioned, the serial device stable, the container health tied to the Reticulum interface, and raw diagnostic evidence retained for failures. I do not want the only record of a working SF/BW/sync combination to be scrollback from one terminal.

I also want the physical layer documented with the same discipline. Antenna band, connector, placement and any gain/loss assumptions belong beside the radio configuration. Otherwise a later hardware substitution can change the link while the software repository remains unchanged.

At the Reticulum layer, I separate roles: which node is an endpoint, which is transport-capable, which interface reaches the LAN, and which interface reaches radio peers. That makes later scaling easier to reason about because every additional path has an owner and a failure model.

## The next experiment I would run

The next test should try to break the conclusion on purpose. Keep the known-good side fixed, alter only the state described by the mechanism, and ask whether the evidence moves with it: Antenna resonance, matching network and electrical length are frequency-dependent; a connector fitting mechanically says nothing about RF match.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Mechanical compatibility is not RF compatibility.**

The retained result was: The sub-GHz link was kept conceptually separate from Wi-Fi antenna hardware.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
