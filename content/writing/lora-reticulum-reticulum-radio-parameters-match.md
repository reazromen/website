---
title: Reticulum Radio Parameters Must Match Exactly
url: /posts/lora-reticulum-reticulum-radio-parameters-match.html
date: '2026-09-15'
read_time: 8
excerpt: Two healthy RNodes can be mutually deaf when frequency, bandwidth, spreading
  factor or coding rate differ.
topic: lora-reticulum
tags:
- lora
- reticulum
- rnode
draft: false
featured: false
language: en
eyebrow: 'LoRa & Reticulum: RNode and Reticulum Architecture · deep-dive'
outputs:
- url: /posts/lora-reticulum-reticulum-radio-parameters-match.html
  template: cms/templates/posts/posts--lora-reticulum-reticulum-radio-parameters-match.tpl
  source: cms/templates/posts/posts--lora-reticulum-reticulum-radio-parameters-match.json
---

# Reticulum Radio Parameters Must Match Exactly

The radio was only one part of the system. The engineering problem was that Two healthy RNodes can be mutually deaf when frequency, bandwidth, spreading factor or coding rate differ.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **The Khulna RNode A lab profile explicitly used 867200000 Hz, 125000 Hz bandwidth, txpower 2, SF8 and coding rate 5 with a note that both RNodes must match exactly.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **PHY equality became a precondition before network-layer debugging.**

## How I framed the problem

This case became a state-machine problem rather than a signal-strength problem. The symptom was Two healthy RNodes can be mutually deaf when frequency, bandwidth, spreading factor or coding rate differ. The evidence was The Khulna RNode A lab profile explicitly used 867200000 Hz, 125000 Hz bandwidth, txpower 2, SF8 and coding rate 5 with a note that both RNodes must match exactly. The underlying state transition mattered because LoRa demodulation depends on compatible PHY settings; higher-layer Reticulum cannot repair a mismatched waveform. I rejected Changing Reticulum identities or routes when the radios are not on the same PHY. and kept the narrower result: PHY equality became a precondition before network-layer debugging.

Reticulum adds an overlay and routing model on top of physical interfaces, but it does not erase the interfaces. RNode serial access, LAN TCP, transport mode and instance sharing have different roles. A healthy overlay depends on the underlay being explicit enough that I can tell whether failure happened in USB, radio, Reticulum configuration or another interface.

The rule I carried forward was: **Validate the waveform before debugging the overlay network.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | Two healthy RNodes can be mutually deaf when frequency, bandwidth, spreading factor or coding rate differ. |
| Strongest evidence | The Khulna RNode A lab profile explicitly used 867200000 Hz, 125000 Hz bandwidth, txpower 2, SF8 and coding rate 5 with a note that both RNodes must match exactly. |
| Mechanism | LoRa demodulation depends on compatible PHY settings; higher-layer Reticulum cannot repair a mismatched waveform. |
| Rejected shortcut | Changing Reticulum identities or routes when the radios are not on the same PHY. |
| Retained result | PHY equality became a precondition before network-layer debugging. |
| Carry-forward rule | Validate the waveform before debugging the overlay network. |

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

- prove /dev/rnode exists inside the container
- validate rnstatus/interface health
- record the exact RNode PHY tuple
- separate transport role from endpoint role
- test TCP and radio interfaces independently

The experiment-specific mechanism was: LoRa demodulation depends on compatible PHY settings; higher-layer Reticulum cannot repair a mismatched waveform. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## Investigation sequence

I change one compatibility dimension at a time. A sweep is useful only if every profile records the exact SF, bandwidth, sync word and result. Otherwise the console becomes a blur and a later successful profile cannot be reconstructed.

The shortcut I avoided was **Changing Reticulum identities or routes when the radios are not on the same PHY.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## What I would do next at larger scale

I would stop treating every node as an interactive lab device. Radio identity, firmware identity, interface type and accepted PHY profiles would become inventory. A deployment test would validate the host serial mapping, interface initialization, pairwise packet exchange and Reticulum reachability before the node was allowed to act as transport.

For RF planning I would add a real link-budget worksheet and measured site data instead of extrapolating from desk tests. The question would become required margin for a defined path rather than “how far can LoRa go?” For mixed hardware, I would maintain compatibility profiles so a 433 MHz LR1121 experiment could never be confused with an 867 MHz SX1262 RNode configuration.

For **Reticulum Radio Parameters Must Match Exactly**, the mechanism still scales: LoRa demodulation depends on compatible PHY settings; higher-layer Reticulum cannot repair a mismatched waveform. Scaling adds automation; it does not remove the need to know which layer a PASS actually proves.

## Instrumentation I would keep

```
              Reticulum instance
              /                     RNodeInterface        TCPServerInterface
          |                     |
        LoRa RF                LAN/IP
```

The instrumentation should make state transitions explicit rather than print only final success. For serial/host work I want device identity, open failures and interface initialization. For LoRa PHY work I want the full profile plus preamble/header/header-error/CRC/RX counters. For E22/EWM I want UART writes, AUX timing and remote reply counts separated. For Reticulum I want interface state and rnstatus-visible behavior.

The reason is simple: **The Khulna RNode A lab profile explicitly used 867200000 Hz, 125000 Hz bandwidth, txpower 2, SF8 and coding rate 5 with a note that both RNodes must match exactly.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For range work, I would not publish a distance without antenna identity, height/environment, TX power, PHY and repeated packet statistics. A single successful packet is a discovery event; a usable link needs margin and repeatability.

For this case the pass condition follows directly from the retained result: **PHY equality became a precondition before network-layer debugging.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## What would falsify the conclusion

The retained result is **PHY equality became a precondition before network-layer debugging.** A useful conclusion must say what future observation would force me to revisit it.

If the same controlled topology produced evidence inconsistent with **The Khulna RNode A lab profile explicitly used 867200000 Hz, 125000 Hz bandwidth, txpower 2, SF8 and coding rate 5 with a note that both RNodes must match exactly.**, I would reopen the diagnosis. If a wired recovery read showed the remote module was already in the expected state, the fault domain would move back toward RF/profile compatibility. If a matched antenna and known-good peer produced clean packets, the earlier silence could not be used as proof that the local modem was defective. If Reticulum failed while direct packet exchange remained clean, the investigation would move up the stack.

This is how I keep RF work from turning into stories about invisible signals. The hypothesis has to predict an observable difference.

## The next experiment I would run

A useful negative control is to reproduce the local success while deliberately making the remote side incompatible. That should preserve local evidence but remove the end-to-end result, proving the layers are being measured separately.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Validate the waveform before debugging the overlay network.**

The retained result was: PHY equality became a precondition before network-layer debugging.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
