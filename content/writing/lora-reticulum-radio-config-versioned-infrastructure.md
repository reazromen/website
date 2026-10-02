---
title: Radio Configuration Belongs in Versioned Infrastructure
url: /posts/lora-reticulum-radio-config-versioned-infrastructure.html
date: '2026-09-15'
read_time: 8
excerpt: Frequency, bandwidth, SF, coding rate and device mapping were being changed
  during experiments and could easily become undocumented shell history.
topic: lora-reticulum
tags:
- lora
- reticulum
- rnode
draft: false
featured: false
language: en
eyebrow: 'LoRa & Reticulum: Recovery, Operations and Scaling · deep-dive'
outputs:
- url: /posts/lora-reticulum-radio-config-versioned-infrastructure.html
  template: cms/templates/posts/posts--lora-reticulum-radio-config-versioned-infrastructure.tpl
  source: cms/templates/posts/posts--lora-reticulum-radio-config-versioned-infrastructure.json
---

# Radio Configuration Belongs in Versioned Infrastructure

One of the fastest ways to get lost in LoRa debugging is to treat silence as one failure mode. Here, Frequency, bandwidth, SF, coding rate and device mapping were being changed during experiments and could easily become undocumented shell history.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **The hserver setup stored Docker compose, .env device selection and Reticulum config together under /opt/reticulum-rnode.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **The node configuration became declarative enough to recreate.**

## How I framed the problem

This case became a state-machine problem rather than a signal-strength problem. The symptom was Frequency, bandwidth, SF, coding rate and device mapping were being changed during experiments and could easily become undocumented shell history. The evidence was The hserver setup stored Docker compose, .env device selection and Reticulum config together under /opt/reticulum-rnode. The underlying state transition mattered because A radio node is both hardware and software configuration; reproducibility requires the host mapping and PHY tuple to be reviewable together. I rejected Remembering the last working radio settings from terminal output. and kept the narrower result: The node configuration became declarative enough to recreate.

A radio experiment becomes infrastructure when it needs reproducibility, recovery and health semantics. That means versioned PHY configuration, stable device mapping, interface-aware health, structured scan results and a wired recovery path below the wireless state machine. Scaling to more nodes should add one new failure domain at a time.

The rule I carried forward was: **Treat radio parameters like network infrastructure configuration, not temporary lab knobs.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | Frequency, bandwidth, SF, coding rate and device mapping were being changed during experiments and could easily become undocumented shell history. |
| Strongest evidence | The hserver setup stored Docker compose, .env device selection and Reticulum config together under /opt/reticulum-rnode. |
| Mechanism | A radio node is both hardware and software configuration; reproducibility requires the host mapping and PHY tuple to be reviewable together. |
| Rejected shortcut | Remembering the last working radio settings from terminal output. |
| Retained result | The node configuration became declarative enough to recreate. |
| Carry-forward rule | Treat radio parameters like network infrastructure configuration, not temporary lab knobs. |

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

- version host mapping and radio profile
- keep interface-aware health checks
- retain raw and summarized experiment logs
- provide a wired recovery path
- scale from pairwise links to transport topology

The experiment-specific mechanism was: A radio node is both hardware and software configuration; reproducibility requires the host mapping and PHY tuple to be reviewable together. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## Investigation sequence

I change one compatibility dimension at a time. A sweep is useful only if every profile records the exact SF, bandwidth, sync word and result. Otherwise the console becomes a blur and a later successful profile cannot be reconstructed.

The shortcut I avoided was **Remembering the last working radio settings from terminal output.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## What I would do next at larger scale

I would stop treating every node as an interactive lab device. Radio identity, firmware identity, interface type and accepted PHY profiles would become inventory. A deployment test would validate the host serial mapping, interface initialization, pairwise packet exchange and Reticulum reachability before the node was allowed to act as transport.

For RF planning I would add a real link-budget worksheet and measured site data instead of extrapolating from desk tests. The question would become required margin for a defined path rather than “how far can LoRa go?” For mixed hardware, I would maintain compatibility profiles so a 433 MHz LR1121 experiment could never be confused with an 867 MHz SX1262 RNode configuration.

For **Radio Configuration Belongs in Versioned Infrastructure**, the mechanism still scales: A radio node is both hardware and software configuration; reproducibility requires the host mapping and PHY tuple to be reviewable together. Scaling adds automation; it does not remove the need to know which layer a PASS actually proves.

## Instrumentation I would keep

```
lab evidence -> reproducible config -> recovery -> health
       -> pair validation -> transport validation -> mesh scale
```

The instrumentation should make state transitions explicit rather than print only final success. For serial/host work I want device identity, open failures and interface initialization. For LoRa PHY work I want the full profile plus preamble/header/header-error/CRC/RX counters. For E22/EWM I want UART writes, AUX timing and remote reply counts separated. For Reticulum I want interface state and rnstatus-visible behavior.

The reason is simple: **The hserver setup stored Docker compose, .env device selection and Reticulum config together under /opt/reticulum-rnode.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For range work, I would not publish a distance without antenna identity, height/environment, TX power, PHY and repeated packet statistics. A single successful packet is a discovery event; a usable link needs margin and repeatability.

For this case the pass condition follows directly from the retained result: **The node configuration became declarative enough to recreate.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## What would falsify the conclusion

The retained result is **The node configuration became declarative enough to recreate.** A useful conclusion must say what future observation would force me to revisit it.

If the same controlled topology produced evidence inconsistent with **The hserver setup stored Docker compose, .env device selection and Reticulum config together under /opt/reticulum-rnode.**, I would reopen the diagnosis. If a wired recovery read showed the remote module was already in the expected state, the fault domain would move back toward RF/profile compatibility. If a matched antenna and known-good peer produced clean packets, the earlier silence could not be used as proof that the local modem was defective. If Reticulum failed while direct packet exchange remained clean, the investigation would move up the stack.

This is how I keep RF work from turning into stories about invisible signals. The hypothesis has to predict an observable difference.

## The next experiment I would run

A useful negative control is to reproduce the local success while deliberately making the remote side incompatible. That should preserve local evidence but remove the end-to-end result, proving the layers are being measured separately.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Treat radio parameters like network infrastructure configuration, not temporary lab knobs.**

The retained result was: The node configuration became declarative enough to recreate.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
