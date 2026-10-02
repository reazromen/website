---
title: Scanning 32 PHY Profiles Was a Diagnostic, Not a Network Design
url: /posts/lora-reticulum-phy-scan-diagnostic-not-design.html
date: '2026-09-15'
read_time: 9
excerpt: Auto-scanning many SF/BW combinations helped discover compatibility clues
  but could not replace an agreed production PHY.
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
- url: /posts/lora-reticulum-phy-scan-diagnostic-not-design.html
  template: cms/templates/posts/posts--lora-reticulum-phy-scan-diagnostic-not-design.tpl
  source: cms/templates/posts/posts--lora-reticulum-phy-scan-diagnostic-not-design.json
---

# Scanning 32 PHY Profiles Was a Diagnostic, Not a Network Design

One of the fastest ways to get lost in LoRa debugging is to treat silence as one failure mode. Here, Auto-scanning many SF/BW combinations helped discover compatibility clues but could not replace an agreed production PHY.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **The LR1121 diagnostic iterated 32 profiles at roughly 2.5 seconds each and recorded preamble/header/CRC/RX counters.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **The scan was used to narrow the search and then return to a deterministic profile.**

## How I framed the problem

The important part was preserving the distinction between local success and end-to-end success. The issue was Auto-scanning many SF/BW combinations helped discover compatibility clues but could not replace an agreed production PHY. I had The LR1121 diagnostic iterated 32 profiles at roughly 2.5 seconds each and recorded preamble/header/CRC/RX counters., but the mechanism—A sweep explores an unknown parameter space; normal communication requires both ends to spend airtime on one agreed profile.—bounded what that evidence meant. The conclusion was The scan was used to narrow the search and then return to a deterministic profile.

LoRa compatibility is a tuple, not a frequency number. Frequency, bandwidth, spreading factor, coding rate, preamble, sync word, CRC and packet parameters all participate. A receiver can detect part of a waveform without accepting a valid packet, which is why I prefer IRQ/state counters over one final RX counter.

The rule I carried forward was: **Use brute-force discovery to learn, then freeze a documented compatible PHY.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | Auto-scanning many SF/BW combinations helped discover compatibility clues but could not replace an agreed production PHY. |
| Strongest evidence | The LR1121 diagnostic iterated 32 profiles at roughly 2.5 seconds each and recorded preamble/header/CRC/RX counters. |
| Mechanism | A sweep explores an unknown parameter space; normal communication requires both ends to spend airtime on one agreed profile. |
| Rejected shortcut | Leaving a production node in broad scan mode because it eventually hears something. |
| Retained result | The scan was used to narrow the search and then return to a deterministic profile. |
| Carry-forward rule | Use brute-force discovery to learn, then freeze a documented compatible PHY. |

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

The experiment-specific mechanism was: A sweep explores an unknown parameter space; normal communication requires both ends to spend airtime on one agreed profile. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## From bench experiment to infrastructure

The durable rule is **Use brute-force discovery to learn, then freeze a documented compatible PHY.**

If I keep this node running, I want the radio profile and host mapping versioned, the serial device stable, the container health tied to the Reticulum interface, and raw diagnostic evidence retained for failures. I do not want the only record of a working SF/BW/sync combination to be scrollback from one terminal.

I also want the physical layer documented with the same discipline. Antenna band, connector, placement and any gain/loss assumptions belong beside the radio configuration. Otherwise a later hardware substitution can change the link while the software repository remains unchanged.

At the Reticulum layer, I separate roles: which node is an endpoint, which is transport-capable, which interface reaches the LAN, and which interface reaches radio peers. That makes later scaling easier to reason about because every additional path has an owner and a failure model.

## Investigation sequence

I preserve negative results. A documented no-reply after a known command is valuable when the local mode/profile and AUX evidence are recorded. It narrows the next test toward the remote side without pretending to prove a failed RF front end.

The shortcut I avoided was **Leaving a production node in broad scan mode because it eventually hears something.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

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

The reason is simple: **The LR1121 diagnostic iterated 32 profiles at roughly 2.5 seconds each and recorded preamble/header/CRC/RX counters.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For recovery, the test is intentionally hostile: assume the wireless profile is unknown and prove the wired path can still read or restore the module. A recovery procedure that needs the broken wireless state to be correct is not a recovery procedure.

For this case the pass condition follows directly from the retained result: **The scan was used to narrow the search and then return to a deterministic profile.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## Local success and end-to-end success are different

A recurring pattern in this lab was that one half of the system could be proven healthy while the complete link remained unknown. The Linux host could see the USB device. The container could run. RNS could parse its config. The local E22 could accept register commands. The LR1121 could arm RX. None of those facts alone proved that a remote radio decoded a packet and delivered it to Reticulum.

For **Scanning 32 PHY Profiles Was a Diagnostic, Not a Network Design**, the distinction matters because A sweep explores an unknown parameter space; normal communication requires both ends to spend airtime on one agreed profile. The evidence **The LR1121 diagnostic iterated 32 profiles at roughly 2.5 seconds each and recorded preamble/header/CRC/RX counters.** therefore supports a bounded statement, not a complete wireless PASS.

I now label test outcomes by layer: HOST, SERIAL, LOCAL\_MODEM, PHY\_DETECT, PACKET\_RX, REMOTE\_REPLY, RNS\_INTERFACE and RETICULUM\_PATH. That vocabulary keeps a green result at one layer from hiding an unknown state at the next.

## The next experiment I would run

The decisive follow-up is the one that replaces an inferred state with a directly observed one. In this case, that means targeting the uncertainty behind: Auto-scanning many SF/BW combinations helped discover compatibility clues but could not replace an agreed production PHY.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Use brute-force discovery to learn, then freeze a documented compatible PHY.**

The retained result was: The scan was used to narrow the search and then return to a deterministic profile.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
