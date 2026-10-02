---
title: A LAN TCP Server and a LoRa Interface Solve Different Reachability Problems
url: /posts/lora-reticulum-lan-tcp-server-vs-lora-interface.html
date: '2026-09-15'
read_time: 8
excerpt: The same Reticulum instance needed to bridge local IP-connected peers and
  radio-connected peers without pretending TCP and LoRa were the same medium.
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
- url: /posts/lora-reticulum-lan-tcp-server-vs-lora-interface.html
  template: cms/templates/posts/posts--lora-reticulum-lan-tcp-server-vs-lora-interface.tpl
  source: cms/templates/posts/posts--lora-reticulum-lan-tcp-server-vs-lora-interface.json
---

# A LAN TCP Server and a LoRa Interface Solve Different Reachability Problems

This experiment looked like a radio problem until I wrote down the layers. The actual issue was that The same Reticulum instance needed to bridge local IP-connected peers and radio-connected peers without pretending TCP and LoRa were the same medium.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **The lab design paired an RNodeInterface with a LAN TCPServerInterface listening on port 4242.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **IP and LoRa became independent interfaces inside one Reticulum topology.**

## How I framed the problem

The important part was preserving the distinction between local success and end-to-end success. The issue was The same Reticulum instance needed to bridge local IP-connected peers and radio-connected peers without pretending TCP and LoRa were the same medium. I had The lab design paired an RNodeInterface with a LAN TCPServerInterface listening on port 4242., but the mechanism—Reticulum can carry identities and packets across different interfaces while each interface keeps its own latency, capacity and failure mode.—bounded what that evidence meant. The conclusion was IP and LoRa became independent interfaces inside one Reticulum topology.

Reticulum adds an overlay and routing model on top of physical interfaces, but it does not erase the interfaces. RNode serial access, LAN TCP, transport mode and instance sharing have different roles. A healthy overlay depends on the underlay being explicit enough that I can tell whether failure happened in USB, radio, Reticulum configuration or another interface.

The rule I carried forward was: **Overlay reachability should not erase underlay-specific diagnostics.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | The same Reticulum instance needed to bridge local IP-connected peers and radio-connected peers without pretending TCP and LoRa were the same medium. |
| Strongest evidence | The lab design paired an RNodeInterface with a LAN TCPServerInterface listening on port 4242. |
| Mechanism | Reticulum can carry identities and packets across different interfaces while each interface keeps its own latency, capacity and failure mode. |
| Rejected shortcut | Treating the TCP path as proof that the radio path works, or vice versa. |
| Retained result | IP and LoRa became independent interfaces inside one Reticulum topology. |
| Carry-forward rule | Overlay reachability should not erase underlay-specific diagnostics. |

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

The experiment-specific mechanism was: Reticulum can carry identities and packets across different interfaces while each interface keeps its own latency, capacity and failure mode. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## Investigation sequence

I preserve negative results. A documented no-reply after a known command is valuable when the local mode/profile and AUX evidence are recorded. It narrows the next test toward the remote side without pretending to prove a failed RF front end.

The shortcut I avoided was **Treating the TCP path as proof that the radio path works, or vice versa.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## What would falsify the conclusion

The retained result is **IP and LoRa became independent interfaces inside one Reticulum topology.** A useful conclusion must say what future observation would force me to revisit it.

If the same controlled topology produced evidence inconsistent with **The lab design paired an RNodeInterface with a LAN TCPServerInterface listening on port 4242.**, I would reopen the diagnosis. If a wired recovery read showed the remote module was already in the expected state, the fault domain would move back toward RF/profile compatibility. If a matched antenna and known-good peer produced clean packets, the earlier silence could not be used as proof that the local modem was defective. If Reticulum failed while direct packet exchange remained clean, the investigation would move up the stack.

This is how I keep RF work from turning into stories about invisible signals. The hypothesis has to predict an observable difference.

## Instrumentation I would keep

```
              Reticulum instance
              /                     RNodeInterface        TCPServerInterface
          |                     |
        LoRa RF                LAN/IP
```

The instrumentation should make state transitions explicit rather than print only final success. For serial/host work I want device identity, open failures and interface initialization. For LoRa PHY work I want the full profile plus preamble/header/header-error/CRC/RX counters. For E22/EWM I want UART writes, AUX timing and remote reply counts separated. For Reticulum I want interface state and rnstatus-visible behavior.

The reason is simple: **The lab design paired an RNodeInterface with a LAN TCPServerInterface listening on port 4242.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For recovery, the test is intentionally hostile: assume the wireless profile is unknown and prove the wired path can still read or restore the module. A recovery procedure that needs the broken wireless state to be correct is not a recovery procedure.

For this case the pass condition follows directly from the retained result: **IP and LoRa became independent interfaces inside one Reticulum topology.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## What I would do next at larger scale

I would stop treating every node as an interactive lab device. Radio identity, firmware identity, interface type and accepted PHY profiles would become inventory. A deployment test would validate the host serial mapping, interface initialization, pairwise packet exchange and Reticulum reachability before the node was allowed to act as transport.

For RF planning I would add a real link-budget worksheet and measured site data instead of extrapolating from desk tests. The question would become required margin for a defined path rather than “how far can LoRa go?” For mixed hardware, I would maintain compatibility profiles so a 433 MHz LR1121 experiment could never be confused with an 867 MHz SX1262 RNode configuration.

For **A LAN TCP Server and a LoRa Interface Solve Different Reachability Problems**, the mechanism still scales: Reticulum can carry identities and packets across different interfaces while each interface keeps its own latency, capacity and failure mode. Scaling adds automation; it does not remove the need to know which layer a PASS actually proves.

## The next experiment I would run

The decisive follow-up is the one that replaces an inferred state with a directly observed one. In this case, that means targeting the uncertainty behind: The same Reticulum instance needed to bridge local IP-connected peers and radio-connected peers without pretending TCP and LoRa were the same medium.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Overlay reachability should not erase underlay-specific diagnostics.**

The retained result was: IP and LoRa became independent interfaces inside one Reticulum topology.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
