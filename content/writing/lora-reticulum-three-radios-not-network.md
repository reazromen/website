---
title: Three Powered Radios Are Not Yet a Network
url: /posts/lora-reticulum-three-radios-not-network.html
date: '2024-08-13'
read_time: 9
excerpt: Having multiple radio boards powered and visible created a false sense that
  a multi-node Reticulum network already existed.
topic: lora-reticulum
tags:
- lora
- reticulum
- rnode
draft: false
featured: false
language: en
eyebrow: 'LoRa & Reticulum: Hardware and Host Bring-Up · deep-dive'
outputs:
- url: /posts/lora-reticulum-three-radios-not-network.html
  template: cms/templates/posts/posts--lora-reticulum-three-radios-not-network.tpl
  source: cms/templates/posts/posts--lora-reticulum-three-radios-not-network.json
---

# Three Powered Radios Are Not Yet a Network

I started this test with hardware on the desk and ended up debugging the boundary between host, modem and RF because Having multiple radio boards powered and visible created a false sense that a multi-node Reticulum network already existed.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **The lab had multiple Waveshare/RNode-class devices, but each link still required matching PHY, valid antennas, correct host interfaces and successful Reticulum discovery.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **The test plan moved from node count to proven pairwise links and transport behavior.**

## How I framed the problem

The important part was preserving the distinction between local success and end-to-end success. The issue was Having multiple radio boards powered and visible created a false sense that a multi-node Reticulum network already existed. I had The lab had multiple Waveshare/RNode-class devices, but each link still required matching PHY, valid antennas, correct host interfaces and successful Reticulum discovery., but the mechanism—Network membership is an end-to-end state built from physical compatibility, link configuration and higher-layer protocol exchange.—bounded what that evidence meant. The conclusion was The test plan moved from node count to proven pairwise links and transport behavior.

The first layer of a radio network is often not RF at all. USB enumeration, bridge firmware, target-chip identity, Linux device ownership and serial stability can fail before a LoRa symbol is transmitted. I therefore bring the hardware up from the host inward: identify every MCU, prove the programming endpoint, stabilize the serial path, remove competing host services and only then interpret radio logs.

The rule I carried forward was: **Count validated links and identities, not powered PCBs.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | Having multiple radio boards powered and visible created a false sense that a multi-node Reticulum network already existed. |
| Strongest evidence | The lab had multiple Waveshare/RNode-class devices, but each link still required matching PHY, valid antennas, correct host interfaces and successful Reticulum discovery. |
| Mechanism | Network membership is an end-to-end state built from physical compatibility, link configuration and higher-layer protocol exchange. |
| Rejected shortcut | Counting powered boards as functioning nodes. |
| Retained result | The test plan moved from node count to proven pairwise links and transport behavior. |
| Carry-forward rule | Count validated links and identities, not powered PCBs. |

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

- identify every MCU/bridge in the path
- prove the target chip before flashing
- resolve the host serial identity
- confirm exclusive serial ownership
- capture boot identity from the radio application

The experiment-specific mechanism was: Network membership is an end-to-end state built from physical compatibility, link configuration and higher-layer protocol exchange. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## Investigation sequence

I preserve negative results. A documented no-reply after a known command is valuable when the local mode/profile and AUX evidence are recorded. It narrows the next test toward the remote side without pretending to prove a failed RF front end.

The shortcut I avoided was **Counting powered boards as functioning nodes.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## Local success and end-to-end success are different

A recurring pattern in this lab was that one half of the system could be proven healthy while the complete link remained unknown. The Linux host could see the USB device. The container could run. RNS could parse its config. The local E22 could accept register commands. The LR1121 could arm RX. None of those facts alone proved that a remote radio decoded a packet and delivered it to Reticulum.

For **Three Powered Radios Are Not Yet a Network**, the distinction matters because Network membership is an end-to-end state built from physical compatibility, link configuration and higher-layer protocol exchange. The evidence **The lab had multiple Waveshare/RNode-class devices, but each link still required matching PHY, valid antennas, correct host interfaces and successful Reticulum discovery.** therefore supports a bounded statement, not a complete wireless PASS.

I now label test outcomes by layer: HOST, SERIAL, LOCAL\_MODEM, PHY\_DETECT, PACKET\_RX, REMOTE\_REPLY, RNS\_INTERFACE and RETICULUM\_PATH. That vocabulary keeps a green result at one layer from hiding an unknown state at the next.

## Instrumentation I would keep

```
USB cable -> bridge MCU -> target programming protocol -> radio MCU -> modem
       ^           ^                ^                    ^
    enumerate    forward         identify            run app
```

The instrumentation should make state transitions explicit rather than print only final success. For serial/host work I want device identity, open failures and interface initialization. For LoRa PHY work I want the full profile plus preamble/header/header-error/CRC/RX counters. For E22/EWM I want UART writes, AUX timing and remote reply counts separated. For Reticulum I want interface state and rnstatus-visible behavior.

The reason is simple: **The lab had multiple Waveshare/RNode-class devices, but each link still required matching PHY, valid antennas, correct host interfaces and successful Reticulum discovery.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For recovery, the test is intentionally hostile: assume the wireless profile is unknown and prove the wired path can still read or restore the module. A recovery procedure that needs the broken wireless state to be correct is not a recovery procedure.

For this case the pass condition follows directly from the retained result: **The test plan moved from node count to proven pairwise links and transport behavior.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## From bench experiment to infrastructure

The durable rule is **Count validated links and identities, not powered PCBs.**

If I keep this node running, I want the radio profile and host mapping versioned, the serial device stable, the container health tied to the Reticulum interface, and raw diagnostic evidence retained for failures. I do not want the only record of a working SF/BW/sync combination to be scrollback from one terminal.

I also want the physical layer documented with the same discipline. Antenna band, connector, placement and any gain/loss assumptions belong beside the radio configuration. Otherwise a later hardware substitution can change the link while the software repository remains unchanged.

At the Reticulum layer, I separate roles: which node is an endpoint, which is transport-capable, which interface reaches the LAN, and which interface reaches radio peers. That makes later scaling easier to reason about because every additional path has an owner and a failure model.

## The next experiment I would run

The decisive follow-up is the one that replaces an inferred state with a directly observed one. In this case, that means targeting the uncertainty behind: Having multiple radio boards powered and visible created a false sense that a multi-node Reticulum network already existed.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Count validated links and identities, not powered PCBs.**

The retained result was: The test plan moved from node count to proven pairwise links and transport behavior.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
