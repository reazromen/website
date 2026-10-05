---
title: A Stable /dev/serial/by-id Path Is Part of Radio Reliability
url: /posts/lora-reticulum-stable-serial-by-id-radio-reliability.html
date: '2023-06-06'
read_time: 9
excerpt: A working RNode can disappear after reboot if the host binds to a transient
  tty name that changes when USB devices reorder.
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
- url: /posts/lora-reticulum-stable-serial-by-id-radio-reliability.html
  template: cms/templates/posts/posts--lora-reticulum-stable-serial-by-id-radio-reliability.tpl
  source: cms/templates/posts/posts--lora-reticulum-stable-serial-by-id-radio-reliability.json
---

# A Stable /dev/serial/by-id Path Is Part of Radio Reliability

This experiment looked like a radio problem until I wrote down the layers. The actual issue was that A working RNode can disappear after reboot if the host binds to a transient tty name that changes when USB devices reorder.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **The hserver setup resolved an Espressif USB JTAG/serial device to /dev/ttyACM0 and explicitly preferred a stable /dev/serial/by-id path where available.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **The host-device mapping became an explicit configuration input instead of an incidental tty path.**

## How I framed the problem

This case became a state-machine problem rather than a signal-strength problem. The symptom was A working RNode can disappear after reboot if the host binds to a transient tty name that changes when USB devices reorder. The evidence was The hserver setup resolved an Espressif USB JTAG/serial device to /dev/ttyACM0 and explicitly preferred a stable /dev/serial/by-id path where available. The underlying state transition mattered because Reticulum depends on the host serial device before it can depend on RF; USB enumeration is part of the end-to-end path. I rejected Debugging radio parameters when the container is attached to the wrong or missing character device. and kept the narrower result: The host-device mapping became an explicit configuration input instead of an incidental tty path.

The first layer of a radio network is often not RF at all. USB enumeration, bridge firmware, target-chip identity, Linux device ownership and serial stability can fail before a LoRa symbol is transmitted. I therefore bring the hardware up from the host inward: identify every MCU, prove the programming endpoint, stabilize the serial path, remove competing host services and only then interpret radio logs.

The rule I carried forward was: **Treat USB identity as infrastructure state, not a desktop convenience.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | A working RNode can disappear after reboot if the host binds to a transient tty name that changes when USB devices reorder. |
| Strongest evidence | The hserver setup resolved an Espressif USB JTAG/serial device to /dev/ttyACM0 and explicitly preferred a stable /dev/serial/by-id path where available. |
| Mechanism | Reticulum depends on the host serial device before it can depend on RF; USB enumeration is part of the end-to-end path. |
| Rejected shortcut | Debugging radio parameters when the container is attached to the wrong or missing character device. |
| Retained result | The host-device mapping became an explicit configuration input instead of an incidental tty path. |
| Carry-forward rule | Treat USB identity as infrastructure state, not a desktop convenience. |

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

The experiment-specific mechanism was: Reticulum depends on the host serial device before it can depend on RF; USB enumeration is part of the end-to-end path. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## From bench experiment to infrastructure

The durable rule is **Treat USB identity as infrastructure state, not a desktop convenience.**

If I keep this node running, I want the radio profile and host mapping versioned, the serial device stable, the container health tied to the Reticulum interface, and raw diagnostic evidence retained for failures. I do not want the only record of a working SF/BW/sync combination to be scrollback from one terminal.

I also want the physical layer documented with the same discipline. Antenna band, connector, placement and any gain/loss assumptions belong beside the radio configuration. Otherwise a later hardware substitution can change the link while the software repository remains unchanged.

At the Reticulum layer, I separate roles: which node is an endpoint, which is transport-capable, which interface reaches the LAN, and which interface reaches radio peers. That makes later scaling easier to reason about because every additional path has an owner and a failure model.

## Investigation sequence

I change one compatibility dimension at a time. A sweep is useful only if every profile records the exact SF, bandwidth, sync word and result. Otherwise the console becomes a blur and a later successful profile cannot be reconstructed.

The shortcut I avoided was **Debugging radio parameters when the container is attached to the wrong or missing character device.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## Instrumentation I would keep

```
USB cable -> bridge MCU -> target programming protocol -> radio MCU -> modem
       ^           ^                ^                    ^
    enumerate    forward         identify            run app
```

The instrumentation should make state transitions explicit rather than print only final success. For serial/host work I want device identity, open failures and interface initialization. For LoRa PHY work I want the full profile plus preamble/header/header-error/CRC/RX counters. For E22/EWM I want UART writes, AUX timing and remote reply counts separated. For Reticulum I want interface state and rnstatus-visible behavior.

The reason is simple: **The hserver setup resolved an Espressif USB JTAG/serial device to /dev/ttyACM0 and explicitly preferred a stable /dev/serial/by-id path where available.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For range work, I would not publish a distance without antenna identity, height/environment, TX power, PHY and repeated packet statistics. A single successful packet is a discovery event; a usable link needs margin and repeatability.

For this case the pass condition follows directly from the retained result: **The host-device mapping became an explicit configuration input instead of an incidental tty path.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## Local success and end-to-end success are different

A recurring pattern in this lab was that one half of the system could be proven healthy while the complete link remained unknown. The Linux host could see the USB device. The container could run. RNS could parse its config. The local E22 could accept register commands. The LR1121 could arm RX. None of those facts alone proved that a remote radio decoded a packet and delivered it to Reticulum.

For **A Stable /dev/serial/by-id Path Is Part of Radio Reliability**, the distinction matters because Reticulum depends on the host serial device before it can depend on RF; USB enumeration is part of the end-to-end path. The evidence **The hserver setup resolved an Espressif USB JTAG/serial device to /dev/ttyACM0 and explicitly preferred a stable /dev/serial/by-id path where available.** therefore supports a bounded statement, not a complete wireless PASS.

I now label test outcomes by layer: HOST, SERIAL, LOCAL\_MODEM, PHY\_DETECT, PACKET\_RX, REMOTE\_REPLY, RNS\_INTERFACE and RETICULUM\_PATH. That vocabulary keeps a green result at one layer from hiding an unknown state at the next.

## The next experiment I would run

A useful negative control is to reproduce the local success while deliberately making the remote side incompatible. That should preserve local evidence but remove the end-to-end result, proving the layers are being measured separately.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Treat USB identity as infrastructure state, not a desktop convenience.**

The retained result was: The host-device mapping became an explicit configuration input instead of an incidental tty path.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
