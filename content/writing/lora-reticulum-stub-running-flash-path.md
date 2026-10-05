---
title: “Stub Is Already Running” Was Evidence About the Flash Path
url: /posts/lora-reticulum-stub-running-flash-path.html
date: '2022-07-24'
read_time: 9
excerpt: Flashing through the bridge looked ambiguous because the USB side and target
  side were different MCUs.
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
- url: /posts/lora-reticulum-stub-running-flash-path.html
  template: cms/templates/posts/posts--lora-reticulum-stub-running-flash-path.tpl
  source: cms/templates/posts/posts--lora-reticulum-stub-running-flash-path.json
---

# “Stub Is Already Running” Was Evidence About the Flash Path

One of the fastest ways to get lost in LoRa debugging is to treat silence as one failure mode. Here, Flashing through the bridge looked ambiguous because the USB side and target side were different MCUs.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **esptool communication with the ESP32-S3 target succeeded through the bridge path and reported an already-running stub during repeated operations.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **Target-chip identity became part of every flash/monitor step.**

## How I framed the problem

I wrote down what the local node could prove and what it could not prove. The problem was Flashing through the bridge looked ambiguous because the USB side and target side were different MCUs. The observation esptool communication with the ESP32-S3 target succeeded through the bridge path and reported an already-running stub during repeated operations. covered one side of the path. Because The ROM/stub protocol response comes from the selected target chip; it is stronger evidence than the USB bridge product name alone., it did not justify Assuming a successful USB connection means the firmware was written to the intended MCU.. The useful result was Target-chip identity became part of every flash/monitor step.

The first layer of a radio network is often not RF at all. USB enumeration, bridge firmware, target-chip identity, Linux device ownership and serial stability can fail before a LoRa symbol is transmitted. I therefore bring the hardware up from the host inward: identify every MCU, prove the programming endpoint, stabilize the serial path, remove competing host services and only then interpret radio logs.

The rule I carried forward was: **In multi-MCU boards, prove the endpoint of the programming protocol, not just the cable path.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | Flashing through the bridge looked ambiguous because the USB side and target side were different MCUs. |
| Strongest evidence | esptool communication with the ESP32-S3 target succeeded through the bridge path and reported an already-running stub during repeated operations. |
| Mechanism | The ROM/stub protocol response comes from the selected target chip; it is stronger evidence than the USB bridge product name alone. |
| Rejected shortcut | Assuming a successful USB connection means the firmware was written to the intended MCU. |
| Retained result | Target-chip identity became part of every flash/monitor step. |
| Carry-forward rule | In multi-MCU boards, prove the endpoint of the programming protocol, not just the cable path. |

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

The experiment-specific mechanism was: The ROM/stub protocol response comes from the selected target chip; it is stronger evidence than the USB bridge product name alone. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## Investigation sequence

I separate configuration from reception. A local register read proves the local module. A local AUX transition proves local work. A preamble IRQ proves partial RF recognition. A valid header/CRC/RX proves more. A Reticulum announcement proves more again. Each layer earns a different claim.

The shortcut I avoided was **Assuming a successful USB connection means the firmware was written to the intended MCU.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## What would falsify the conclusion

The retained result is **Target-chip identity became part of every flash/monitor step.** A useful conclusion must say what future observation would force me to revisit it.

If the same controlled topology produced evidence inconsistent with **esptool communication with the ESP32-S3 target succeeded through the bridge path and reported an already-running stub during repeated operations.**, I would reopen the diagnosis. If a wired recovery read showed the remote module was already in the expected state, the fault domain would move back toward RF/profile compatibility. If a matched antenna and known-good peer produced clean packets, the earlier silence could not be used as proof that the local modem was defective. If Reticulum failed while direct packet exchange remained clean, the investigation would move up the stack.

This is how I keep RF work from turning into stories about invisible signals. The hypothesis has to predict an observable difference.

## Instrumentation I would keep

```
USB cable -> bridge MCU -> target programming protocol -> radio MCU -> modem
       ^           ^                ^                    ^
    enumerate    forward         identify            run app
```

The instrumentation should make state transitions explicit rather than print only final success. For serial/host work I want device identity, open failures and interface initialization. For LoRa PHY work I want the full profile plus preamble/header/header-error/CRC/RX counters. For E22/EWM I want UART writes, AUX timing and remote reply counts separated. For Reticulum I want interface state and rnstatus-visible behavior.

The reason is simple: **esptool communication with the ESP32-S3 target succeeded through the bridge path and reported an already-running stub during repeated operations.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For a host/interface article, acceptance means the service survives restart and re-enumeration without silently binding to the wrong device. For a PHY article, it means two endpoints agree on the complete packet profile and produce valid RX evidence rather than only RF activity.

For this case the pass condition follows directly from the retained result: **Target-chip identity became part of every flash/monitor step.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## What I would do next at larger scale

I would stop treating every node as an interactive lab device. Radio identity, firmware identity, interface type and accepted PHY profiles would become inventory. A deployment test would validate the host serial mapping, interface initialization, pairwise packet exchange and Reticulum reachability before the node was allowed to act as transport.

For RF planning I would add a real link-budget worksheet and measured site data instead of extrapolating from desk tests. The question would become required margin for a defined path rather than “how far can LoRa go?” For mixed hardware, I would maintain compatibility profiles so a 433 MHz LR1121 experiment could never be confused with an 867 MHz SX1262 RNode configuration.

For **“Stub Is Already Running” Was Evidence About the Flash Path**, the mechanism still scales: The ROM/stub protocol response comes from the selected target chip; it is stronger evidence than the USB bridge product name alone. Scaling adds automation; it does not remove the need to know which layer a PASS actually proves.

## The next experiment I would run

The next test should try to break the conclusion on purpose. Keep the known-good side fixed, alter only the state described by the mechanism, and ask whether the evidence moves with it: The ROM/stub protocol response comes from the selected target chip; it is stronger evidence than the USB bridge product name alone.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**In multi-MCU boards, prove the endpoint of the programming protocol, not just the cable path.**

The retained result was: Target-chip identity became part of every flash/monitor step.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
