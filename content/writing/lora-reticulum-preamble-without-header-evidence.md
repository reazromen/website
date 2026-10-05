---
title: Preamble Detected but No Header Was Better Than “Nothing Happened”
url: /posts/lora-reticulum-preamble-without-header-evidence.html
date: '2023-05-18'
read_time: 9
excerpt: A scan could fail to decode a packet yet still reveal that one PHY was closer
  to the transmitter than all the others.
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
- url: /posts/lora-reticulum-preamble-without-header-evidence.html
  template: cms/templates/posts/posts--lora-reticulum-preamble-without-header-evidence.tpl
  source: cms/templates/posts/posts--lora-reticulum-preamble-without-header-evidence.json
---

# Preamble Detected but No Header Was Better Than “Nothing Happened”

I started this test with hardware on the desk and ended up debugging the boundary between host, modem and RF because A scan could fail to decode a packet yet still reveal that one PHY was closer to the transmitter than all the others.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **At SF7/BW125 the LR1121 scan recorded multiple preamble IRQs while header and RX counts remained zero in one captured run.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **Intermediate IRQ counters became diagnostic evidence instead of discarded noise.**

## How I framed the problem

I approached this as an experiment-design problem. Starting from A scan could fail to decode a packet yet still reveal that one PHY was closer to the transmitter than all the others., I chose an observation that could separate at least two plausible causes: At SF7/BW125 the LR1121 scan recorded multiple preamble IRQs while header and RX counts remained zero in one captured run. The result made sense because Preamble detection proves partial waveform recognition; header failure moves the investigation toward packet parameters, sync, payload framing or marginal RF rather than total RF silence. It also prevented me from treating Collapsing every non-RX result into the same “no signal” state. as proof. The retained result was Intermediate IRQ counters became diagnostic evidence instead of discarded noise.

LoRa compatibility is a tuple, not a frequency number. Frequency, bandwidth, spreading factor, coding rate, preamble, sync word, CRC and packet parameters all participate. A receiver can detect part of a waveform without accepting a valid packet, which is why I prefer IRQ/state counters over one final RX counter.

The rule I carried forward was: **Expose receiver state transitions, not only final packet counts.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | A scan could fail to decode a packet yet still reveal that one PHY was closer to the transmitter than all the others. |
| Strongest evidence | At SF7/BW125 the LR1121 scan recorded multiple preamble IRQs while header and RX counts remained zero in one captured run. |
| Mechanism | Preamble detection proves partial waveform recognition; header failure moves the investigation toward packet parameters, sync, payload framing or marginal RF rather than total RF silence. |
| Rejected shortcut | Collapsing every non-RX result into the same “no signal” state. |
| Retained result | Intermediate IRQ counters became diagnostic evidence instead of discarded noise. |
| Carry-forward rule | Expose receiver state transitions, not only final packet counts. |

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

The experiment-specific mechanism was: Preamble detection proves partial waveform recognition; header failure moves the investigation toward packet parameters, sync, payload framing or marginal RF rather than total RF silence. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## Investigation sequence

I keep physical prerequisites outside the software hypothesis. Correct antennas, stable supply and deliberate spacing are test conditions, not optional accessories. If they are unknown, the right conclusion is “RF evidence invalid or incomplete,” not a guessed range number.

The shortcut I avoided was **Collapsing every non-RX result into the same “no signal” state.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## What would falsify the conclusion

The retained result is **Intermediate IRQ counters became diagnostic evidence instead of discarded noise.** A useful conclusion must say what future observation would force me to revisit it.

If the same controlled topology produced evidence inconsistent with **At SF7/BW125 the LR1121 scan recorded multiple preamble IRQs while header and RX counts remained zero in one captured run.**, I would reopen the diagnosis. If a wired recovery read showed the remote module was already in the expected state, the fault domain would move back toward RF/profile compatibility. If a matched antenna and known-good peer produced clean packets, the earlier silence could not be used as proof that the local modem was defective. If Reticulum failed while direct packet exchange remained clean, the investigation would move up the stack.

This is how I keep RF work from turning into stories about invisible signals. The hypothesis has to predict an observable difference.

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

The reason is simple: **At SF7/BW125 the LR1121 scan recorded multiple preamble IRQs while header and RX counts remained zero in one captured run.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For E22/EWM, I keep local-control PASS separate from remote-reply PASS. The canonical command must produce its expected remote response before I call the OTA configuration path compatible. AUX activity alone cannot satisfy that gate.

For this case the pass condition follows directly from the retained result: **Intermediate IRQ counters became diagnostic evidence instead of discarded noise.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## What I would do next at larger scale

I would stop treating every node as an interactive lab device. Radio identity, firmware identity, interface type and accepted PHY profiles would become inventory. A deployment test would validate the host serial mapping, interface initialization, pairwise packet exchange and Reticulum reachability before the node was allowed to act as transport.

For RF planning I would add a real link-budget worksheet and measured site data instead of extrapolating from desk tests. The question would become required margin for a defined path rather than “how far can LoRa go?” For mixed hardware, I would maintain compatibility profiles so a 433 MHz LR1121 experiment could never be confused with an 867 MHz SX1262 RNode configuration.

For **Preamble Detected but No Header Was Better Than “Nothing Happened”**, the mechanism still scales: Preamble detection proves partial waveform recognition; header failure moves the investigation toward packet parameters, sync, payload framing or marginal RF rather than total RF silence. Scaling adds automation; it does not remove the need to know which layer a PASS actually proves.

## The next experiment I would run

I would also reverse the test direction where possible. A result that survives transmitter/receiver role reversal is stronger than one that depends on an unexplained asymmetry in the lab setup.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Expose receiver state transitions, not only final packet counts.**

The retained result was: Intermediate IRQ counters became diagnostic evidence instead of discarded noise.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
