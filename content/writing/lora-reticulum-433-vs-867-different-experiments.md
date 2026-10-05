---
title: 433 MHz and 867.2 MHz Belonged to Different Experiments
url: /posts/lora-reticulum-433-vs-867-different-experiments.html
date: '2025-05-06'
read_time: 9
excerpt: The lab used both 433-class LR1121/E22 work and an 867.2 MHz RNode profile,
  which could easily be mixed in memory.
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
- url: /posts/lora-reticulum-433-vs-867-different-experiments.html
  template: cms/templates/posts/posts--lora-reticulum-433-vs-867-different-experiments.tpl
  source: cms/templates/posts/posts--lora-reticulum-433-vs-867-different-experiments.json
---

# 433 MHz and 867.2 MHz Belonged to Different Experiments

The useful lesson was not 'LoRa has long range.' It was that The lab used both 433-class LR1121/E22 work and an 867.2 MHz RNode profile, which could easily be mixed in memory.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **LR1121 diagnostics were run around 433.125/434 MHz, while Khulna RNode A was configured at 867.2 MHz on an SX1262-class 860–930 MHz device.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **The experiments were documented as separate radio profiles rather than one generic LoRa setup.**

## How I framed the problem

I wrote down what the local node could prove and what it could not prove. The problem was The lab used both 433-class LR1121/E22 work and an 867.2 MHz RNode profile, which could easily be mixed in memory. The observation LR1121 diagnostics were run around 433.125/434 MHz, while Khulna RNode A was configured at 867.2 MHz on an SX1262-class 860–930 MHz device. covered one side of the path. Because Frequency is a physical compatibility boundary tied to radio front end, antenna and regional/test configuration., it did not justify Copying a working SF/BW profile across radios while forgetting the operating band.. The useful result was The experiments were documented as separate radio profiles rather than one generic LoRa setup.

LoRa compatibility is a tuple, not a frequency number. Frequency, bandwidth, spreading factor, coding rate, preamble, sync word, CRC and packet parameters all participate. A receiver can detect part of a waveform without accepting a valid packet, which is why I prefer IRQ/state counters over one final RX counter.

The rule I carried forward was: **Always write the frequency next to the PHY parameters and hardware identity.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | The lab used both 433-class LR1121/E22 work and an 867.2 MHz RNode profile, which could easily be mixed in memory. |
| Strongest evidence | LR1121 diagnostics were run around 433.125/434 MHz, while Khulna RNode A was configured at 867.2 MHz on an SX1262-class 860–930 MHz device. |
| Mechanism | Frequency is a physical compatibility boundary tied to radio front end, antenna and regional/test configuration. |
| Rejected shortcut | Copying a working SF/BW profile across radios while forgetting the operating band. |
| Retained result | The experiments were documented as separate radio profiles rather than one generic LoRa setup. |
| Carry-forward rule | Always write the frequency next to the PHY parameters and hardware identity. |

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

The experiment-specific mechanism was: Frequency is a physical compatibility boundary tied to radio front end, antenna and regional/test configuration. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## What I would do next at larger scale

I would stop treating every node as an interactive lab device. Radio identity, firmware identity, interface type and accepted PHY profiles would become inventory. A deployment test would validate the host serial mapping, interface initialization, pairwise packet exchange and Reticulum reachability before the node was allowed to act as transport.

For RF planning I would add a real link-budget worksheet and measured site data instead of extrapolating from desk tests. The question would become required margin for a defined path rather than “how far can LoRa go?” For mixed hardware, I would maintain compatibility profiles so a 433 MHz LR1121 experiment could never be confused with an 867 MHz SX1262 RNode configuration.

For **433 MHz and 867.2 MHz Belonged to Different Experiments**, the mechanism still scales: Frequency is a physical compatibility boundary tied to radio front end, antenna and regional/test configuration. Scaling adds automation; it does not remove the need to know which layer a PASS actually proves.

## Investigation sequence

I separate configuration from reception. A local register read proves the local module. A local AUX transition proves local work. A preamble IRQ proves partial RF recognition. A valid header/CRC/RX proves more. A Reticulum announcement proves more again. Each layer earns a different claim.

The shortcut I avoided was **Copying a working SF/BW profile across radios while forgetting the operating band.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

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

The reason is simple: **LR1121 diagnostics were run around 433.125/434 MHz, while Khulna RNode A was configured at 867.2 MHz on an SX1262-class 860–930 MHz device.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For a host/interface article, acceptance means the service survives restart and re-enumeration without silently binding to the wrong device. For a PHY article, it means two endpoints agree on the complete packet profile and produce valid RX evidence rather than only RF activity.

For this case the pass condition follows directly from the retained result: **The experiments were documented as separate radio profiles rather than one generic LoRa setup.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## What would falsify the conclusion

The retained result is **The experiments were documented as separate radio profiles rather than one generic LoRa setup.** A useful conclusion must say what future observation would force me to revisit it.

If the same controlled topology produced evidence inconsistent with **LR1121 diagnostics were run around 433.125/434 MHz, while Khulna RNode A was configured at 867.2 MHz on an SX1262-class 860–930 MHz device.**, I would reopen the diagnosis. If a wired recovery read showed the remote module was already in the expected state, the fault domain would move back toward RF/profile compatibility. If a matched antenna and known-good peer produced clean packets, the earlier silence could not be used as proof that the local modem was defective. If Reticulum failed while direct packet exchange remained clean, the investigation would move up the stack.

This is how I keep RF work from turning into stories about invisible signals. The hypothesis has to predict an observable difference.

## The next experiment I would run

The next test should try to break the conclusion on purpose. Keep the known-good side fixed, alter only the state described by the mechanism, and ask whether the evidence moves with it: Frequency is a physical compatibility boundary tied to radio front end, antenna and regional/test configuration.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Always write the frequency next to the PHY parameters and hardware identity.**

The retained result was: The experiments were documented as separate radio profiles rather than one generic LoRa setup.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
