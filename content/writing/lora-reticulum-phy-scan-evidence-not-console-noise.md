---
title: A PHY Scan Should Produce Evidence, Not Just Console Noise
url: /posts/lora-reticulum-phy-scan-evidence-not-console-noise.html
date: '2024-11-14'
read_time: 9
excerpt: Long automatic scans produced hundreds of lines that were hard to compare
  across runs.
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
- url: /posts/lora-reticulum-phy-scan-evidence-not-console-noise.html
  template: cms/templates/posts/posts--lora-reticulum-phy-scan-evidence-not-console-noise.tpl
  source: cms/templates/posts/posts--lora-reticulum-phy-scan-evidence-not-console-noise.json
---

# A PHY Scan Should Produce Evidence, Not Just Console Noise

One of the fastest ways to get lost in LoRa debugging is to treat silence as one failure mode. Here, Long automatic scans produced hundreds of lines that were hard to compare across runs.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **The LR1121 diagnostic summarized each profile with preamble, header, header-error, CRC and RX counts, making SF7/BW125 behavior distinguishable from neighboring profiles.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **Per-profile result records became the useful output of the scan.**

## How I framed the problem

I approached this as an experiment-design problem. Starting from Long automatic scans produced hundreds of lines that were hard to compare across runs., I chose an observation that could separate at least two plausible causes: The LR1121 diagnostic summarized each profile with preamble, header, header-error, CRC and RX counts, making SF7/BW125 behavior distinguishable from neighboring profiles. The result made sense because Structured counters turn a sweep into comparable evidence and allow partial reception states to survive beyond the terminal session. It also prevented me from treating Watching a live console and relying on memory for which profile looked promising. as proof. The retained result was Per-profile result records became the useful output of the scan.

A radio experiment becomes infrastructure when it needs reproducibility, recovery and health semantics. That means versioned PHY configuration, stable device mapping, interface-aware health, structured scan results and a wired recovery path below the wireless state machine. Scaling to more nodes should add one new failure domain at a time.

The rule I carried forward was: **Automation is valuable when it compresses experiments into comparable evidence.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | Long automatic scans produced hundreds of lines that were hard to compare across runs. |
| Strongest evidence | The LR1121 diagnostic summarized each profile with preamble, header, header-error, CRC and RX counts, making SF7/BW125 behavior distinguishable from neighboring profiles. |
| Mechanism | Structured counters turn a sweep into comparable evidence and allow partial reception states to survive beyond the terminal session. |
| Rejected shortcut | Watching a live console and relying on memory for which profile looked promising. |
| Retained result | Per-profile result records became the useful output of the scan. |
| Carry-forward rule | Automation is valuable when it compresses experiments into comparable evidence. |

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

The experiment-specific mechanism was: Structured counters turn a sweep into comparable evidence and allow partial reception states to survive beyond the terminal session. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## Investigation sequence

I keep physical prerequisites outside the software hypothesis. Correct antennas, stable supply and deliberate spacing are test conditions, not optional accessories. If they are unknown, the right conclusion is “RF evidence invalid or incomplete,” not a guessed range number.

The shortcut I avoided was **Watching a live console and relying on memory for which profile looked promising.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## Local success and end-to-end success are different

A recurring pattern in this lab was that one half of the system could be proven healthy while the complete link remained unknown. The Linux host could see the USB device. The container could run. RNS could parse its config. The local E22 could accept register commands. The LR1121 could arm RX. None of those facts alone proved that a remote radio decoded a packet and delivered it to Reticulum.

For **A PHY Scan Should Produce Evidence, Not Just Console Noise**, the distinction matters because Structured counters turn a sweep into comparable evidence and allow partial reception states to survive beyond the terminal session. The evidence **The LR1121 diagnostic summarized each profile with preamble, header, header-error, CRC and RX counts, making SF7/BW125 behavior distinguishable from neighboring profiles.** therefore supports a bounded statement, not a complete wireless PASS.

I now label test outcomes by layer: HOST, SERIAL, LOCAL\_MODEM, PHY\_DETECT, PACKET\_RX, REMOTE\_REPLY, RNS\_INTERFACE and RETICULUM\_PATH. That vocabulary keeps a green result at one layer from hiding an unknown state at the next.

## Instrumentation I would keep

```
lab evidence -> reproducible config -> recovery -> health
       -> pair validation -> transport validation -> mesh scale
```

The instrumentation should make state transitions explicit rather than print only final success. For serial/host work I want device identity, open failures and interface initialization. For LoRa PHY work I want the full profile plus preamble/header/header-error/CRC/RX counters. For E22/EWM I want UART writes, AUX timing and remote reply counts separated. For Reticulum I want interface state and rnstatus-visible behavior.

The reason is simple: **The LR1121 diagnostic summarized each profile with preamble, header, header-error, CRC and RX counts, making SF7/BW125 behavior distinguishable from neighboring profiles.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For E22/EWM, I keep local-control PASS separate from remote-reply PASS. The canonical command must produce its expected remote response before I call the OTA configuration path compatible. AUX activity alone cannot satisfy that gate.

For this case the pass condition follows directly from the retained result: **Per-profile result records became the useful output of the scan.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## From bench experiment to infrastructure

The durable rule is **Automation is valuable when it compresses experiments into comparable evidence.**

If I keep this node running, I want the radio profile and host mapping versioned, the serial device stable, the container health tied to the Reticulum interface, and raw diagnostic evidence retained for failures. I do not want the only record of a working SF/BW/sync combination to be scrollback from one terminal.

I also want the physical layer documented with the same discipline. Antenna band, connector, placement and any gain/loss assumptions belong beside the radio configuration. Otherwise a later hardware substitution can change the link while the software repository remains unchanged.

At the Reticulum layer, I separate roles: which node is an endpoint, which is transport-capable, which interface reaches the LAN, and which interface reaches radio peers. That makes later scaling easier to reason about because every additional path has an owner and a failure model.

## The next experiment I would run

I would also reverse the test direction where possible. A result that survives transmitter/receiver role reversal is stronger than one that depends on an unexplained asymmetry in the lab setup.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Automation is valuable when it compresses experiments into comparable evidence.**

The retained result was: Per-profile result records became the useful output of the scan.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
