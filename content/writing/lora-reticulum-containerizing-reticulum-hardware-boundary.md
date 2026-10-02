---
title: Containerizing Reticulum Did Not Remove the Hardware Boundary
url: /posts/lora-reticulum-containerizing-reticulum-hardware-boundary.html
date: '2026-09-15'
read_time: 9
excerpt: Docker made RNS reproducible, but the radio still existed as a physical character
  device outside the container.
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
- url: /posts/lora-reticulum-containerizing-reticulum-hardware-boundary.html
  template: cms/templates/posts/posts--lora-reticulum-containerizing-reticulum-hardware-boundary.tpl
  source: cms/templates/posts/posts--lora-reticulum-containerizing-reticulum-hardware-boundary.json
---

# Containerizing Reticulum Did Not Remove the Hardware Boundary

The useful lesson was not 'LoRa has long range.' It was that Docker made RNS reproducible, but the radio still existed as a physical character device outside the container.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **The compose file mapped ${RNODE\_DEVICE:-/dev/ttyACM0} to /dev/rnode, mounted the Reticulum config, ran rnsd and checked health with rnstatus.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **The container gained an explicit device mapping and protocol-level health check.**

## How I framed the problem

I treated this as a boundary-identification problem. The observed failure was Docker made RNS reproducible, but the radio still existed as a physical character device outside the container. The strongest evidence was The compose file mapped ${RNODE\_DEVICE:-/dev/ttyACM0} to /dev/rnode, mounted the Reticulum config, ran rnsd and checked health with rnstatus. The mechanism was Container isolation stops at device passthrough; a healthy container can still lose the underlying USB/RNode path. That made the tempting shortcut—Treating docker compose ps as proof that the radio interface is usable.—insufficient. The retained result was The container gained an explicit device mapping and protocol-level health check.

Reticulum adds an overlay and routing model on top of physical interfaces, but it does not erase the interfaces. RNode serial access, LAN TCP, transport mode and instance sharing have different roles. A healthy overlay depends on the underlay being explicit enough that I can tell whether failure happened in USB, radio, Reticulum configuration or another interface.

The rule I carried forward was: **Container health should test the service role, not only the process lifetime.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | Docker made RNS reproducible, but the radio still existed as a physical character device outside the container. |
| Strongest evidence | The compose file mapped ${RNODE\_DEVICE:-/dev/ttyACM0} to /dev/rnode, mounted the Reticulum config, ran rnsd and checked health with rnstatus. |
| Mechanism | Container isolation stops at device passthrough; a healthy container can still lose the underlying USB/RNode path. |
| Rejected shortcut | Treating docker compose ps as proof that the radio interface is usable. |
| Retained result | The container gained an explicit device mapping and protocol-level health check. |
| Carry-forward rule | Container health should test the service role, not only the process lifetime. |

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

The experiment-specific mechanism was: Container isolation stops at device passthrough; a healthy container can still lose the underlying USB/RNode path. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## What would falsify the conclusion

The retained result is **The container gained an explicit device mapping and protocol-level health check.** A useful conclusion must say what future observation would force me to revisit it.

If the same controlled topology produced evidence inconsistent with **The compose file mapped ${RNODE\_DEVICE:-/dev/ttyACM0} to /dev/rnode, mounted the Reticulum config, ran rnsd and checked health with rnstatus.**, I would reopen the diagnosis. If a wired recovery read showed the remote module was already in the expected state, the fault domain would move back toward RF/profile compatibility. If a matched antenna and known-good peer produced clean packets, the earlier silence could not be used as proof that the local modem was defective. If Reticulum failed while direct packet exchange remained clean, the investigation would move up the stack.

This is how I keep RF work from turning into stories about invisible signals. The hypothesis has to predict an observable difference.

## Investigation sequence

My sequence is host first, radio second. I freeze the USB/device path, prove the intended target MCU, capture the radio profile, and only then change RF variables. That prevents a disappearing tty, a bridge/target mix-up or ModemManager from being misdiagnosed as propagation.

The shortcut I avoided was **Treating docker compose ps as proof that the radio interface is usable.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## Instrumentation I would keep

```
              Reticulum instance
              /                     RNodeInterface        TCPServerInterface
          |                     |
        LoRa RF                LAN/IP
```

The instrumentation should make state transitions explicit rather than print only final success. For serial/host work I want device identity, open failures and interface initialization. For LoRa PHY work I want the full profile plus preamble/header/header-error/CRC/RX counters. For E22/EWM I want UART writes, AUX timing and remote reply counts separated. For Reticulum I want interface state and rnstatus-visible behavior.

The reason is simple: **The compose file mapped ${RNODE\_DEVICE:-/dev/ttyACM0} to /dev/rnode, mounted the Reticulum config, ran rnsd and checked health with rnstatus.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

A pass needs a reproducible pair, not a lucky packet. I want the exact hardware identities, antennas, PHY tuple, mode state and host mapping written down, then repeated send/receive evidence. Only after that do I let Reticulum-layer behavior become the acceptance target.

For this case the pass condition follows directly from the retained result: **The container gained an explicit device mapping and protocol-level health check.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## What I would do next at larger scale

I would stop treating every node as an interactive lab device. Radio identity, firmware identity, interface type and accepted PHY profiles would become inventory. A deployment test would validate the host serial mapping, interface initialization, pairwise packet exchange and Reticulum reachability before the node was allowed to act as transport.

For RF planning I would add a real link-budget worksheet and measured site data instead of extrapolating from desk tests. The question would become required margin for a defined path rather than “how far can LoRa go?” For mixed hardware, I would maintain compatibility profiles so a 433 MHz LR1121 experiment could never be confused with an 867 MHz SX1262 RNode configuration.

For **Containerizing Reticulum Did Not Remove the Hardware Boundary**, the mechanism still scales: Container isolation stops at device passthrough; a healthy container can still lose the underlying USB/RNode path. Scaling adds automation; it does not remove the need to know which layer a PASS actually proves.

## The next experiment I would run

If treating docker compose ps as proof that the radio interface is usable. were actually the cause, I would expect a repeatable change in the observation that currently supports the retained result. Without that change, the theory is convenient but weak.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Container health should test the service role, not only the process lifetime.**

The retained result was: The container gained an explicit device mapping and protocol-level health check.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
