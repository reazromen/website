---
title: Ten Kilometres Starts with a Link Budget, Not Maximum TX Power
url: /posts/lora-reticulum-ten-km-starts-link-budget.html
date: '2026-09-10'
read_time: 9
excerpt: The desire for multi-kilometre range could easily turn into a single-variable
  question about how many dBm the radio can transmit.
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
- url: /posts/lora-reticulum-ten-km-starts-link-budget.html
  template: cms/templates/posts/posts--lora-reticulum-ten-km-starts-link-budget.tpl
  source: cms/templates/posts/posts--lora-reticulum-ten-km-starts-link-budget.json
---

# Ten Kilometres Starts with a Link Budget, Not Maximum TX Power

This experiment looked like a radio problem until I wrote down the layers. The actual issue was that The desire for multi-kilometre range could easily turn into a single-variable question about how many dBm the radio can transmit.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **The available radios exposed very different TX capabilities and PHY choices, but the experiments also showed the need for matching frequency, bandwidth, SF, antennas and receiver behavior.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **Long-range planning was reframed as a budget and environment problem.**

## How I framed the problem

This case became a state-machine problem rather than a signal-strength problem. The symptom was The desire for multi-kilometre range could easily turn into a single-variable question about how many dBm the radio can transmit. The evidence was The available radios exposed very different TX capabilities and PHY choices, but the experiments also showed the need for matching frequency, bandwidth, SF, antennas and receiver behavior. The underlying state transition mattered because Range emerges from EIRP, antenna gains/losses, path loss, receiver sensitivity, interference, terrain and required packet margin. I rejected Assuming maximum transmit power guarantees a target distance. and kept the narrower result: Long-range planning was reframed as a budget and environment problem.

Range discussions become useful only after the antenna and link budget are real. TX power is one term. Antenna match, cable/connector loss, receiver sensitivity, PHY, interference, terrain, height and margin all matter. A test with the wrong antenna or an unknown remote mode is not evidence for maximum distance.

The rule I carried forward was: **Distance is an outcome of the whole RF path, not a radio datasheet headline.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | The desire for multi-kilometre range could easily turn into a single-variable question about how many dBm the radio can transmit. |
| Strongest evidence | The available radios exposed very different TX capabilities and PHY choices, but the experiments also showed the need for matching frequency, bandwidth, SF, antennas and receiver behavior. |
| Mechanism | Range emerges from EIRP, antenna gains/losses, path loss, receiver sensitivity, interference, terrain and required packet margin. |
| Rejected shortcut | Assuming maximum transmit power guarantees a target distance. |
| Retained result | Long-range planning was reframed as a budget and environment problem. |
| Carry-forward rule | Distance is an outcome of the whole RF path, not a radio datasheet headline. |

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

The experiment-specific mechanism was: Range emerges from EIRP, antenna gains/losses, path loss, receiver sensitivity, interference, terrain and required packet margin. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## What would falsify the conclusion

The retained result is **Long-range planning was reframed as a budget and environment problem.** A useful conclusion must say what future observation would force me to revisit it.

If the same controlled topology produced evidence inconsistent with **The available radios exposed very different TX capabilities and PHY choices, but the experiments also showed the need for matching frequency, bandwidth, SF, antennas and receiver behavior.**, I would reopen the diagnosis. If a wired recovery read showed the remote module was already in the expected state, the fault domain would move back toward RF/profile compatibility. If a matched antenna and known-good peer produced clean packets, the earlier silence could not be used as proof that the local modem was defective. If Reticulum failed while direct packet exchange remained clean, the investigation would move up the stack.

This is how I keep RF work from turning into stories about invisible signals. The hypothesis has to predict an observable difference.

## Investigation sequence

I change one compatibility dimension at a time. A sweep is useful only if every profile records the exact SF, bandwidth, sync word and result. Otherwise the console becomes a blur and a later successful profile cannot be reconstructed.

The shortcut I avoided was **Assuming maximum transmit power guarantees a target distance.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

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

The reason is simple: **The available radios exposed very different TX capabilities and PHY choices, but the experiments also showed the need for matching frequency, bandwidth, SF, antennas and receiver behavior.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For range work, I would not publish a distance without antenna identity, height/environment, TX power, PHY and repeated packet statistics. A single successful packet is a discovery event; a usable link needs margin and repeatability.

For this case the pass condition follows directly from the retained result: **Long-range planning was reframed as a budget and environment problem.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## What I would do next at larger scale

I would stop treating every node as an interactive lab device. Radio identity, firmware identity, interface type and accepted PHY profiles would become inventory. A deployment test would validate the host serial mapping, interface initialization, pairwise packet exchange and Reticulum reachability before the node was allowed to act as transport.

For RF planning I would add a real link-budget worksheet and measured site data instead of extrapolating from desk tests. The question would become required margin for a defined path rather than “how far can LoRa go?” For mixed hardware, I would maintain compatibility profiles so a 433 MHz LR1121 experiment could never be confused with an 867 MHz SX1262 RNode configuration.

For **Ten Kilometres Starts with a Link Budget, Not Maximum TX Power**, the mechanism still scales: Range emerges from EIRP, antenna gains/losses, path loss, receiver sensitivity, interference, terrain and required packet margin. Scaling adds automation; it does not remove the need to know which layer a PASS actually proves.

## The next experiment I would run

A useful negative control is to reproduce the local success while deliberately making the remote side incompatible. That should preserve local evidence but remove the end-to-end result, proving the layers are being measured separately.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Distance is an outcome of the whole RF path, not a radio datasheet headline.**

The retained result was: Long-range planning was reframed as a budget and environment problem.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
