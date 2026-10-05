---
title: USB-C Charging Is Not a Factory Debug Strategy
url: /posts/pcb-bringup-usb-c-not-factory-debug-strategy.html
date: '2026-07-30'
read_time: 9
excerpt: A product can have a USB-C connector and still lack a reliable programming/recovery
  path for failed units.
topic: pcb-bringup-hardware
tags:
- esp32-s3
- pcb-bring-up
- hardware
draft: false
featured: false
language: en
eyebrow: 'PCB Bring-Up: Display, Controls & Factory Interfaces · deep-dive'
outputs:
- url: /posts/pcb-bringup-usb-c-not-factory-debug-strategy.html
  template: cms/templates/posts/posts--pcb-bringup-usb-c-not-factory-debug-strategy.tpl
  source: cms/templates/posts/posts--pcb-bringup-usb-c-not-factory-debug-strategy.json
---

# USB-C Charging Is Not a Factory Debug Strategy

The board did not care what the variable name said. The practical problem was that A product can have a USB-C connector and still lack a reliable programming/recovery path for failed units.

The board context for this series is LOUP's Minewing V1.6 ESP32-S3 hardware: ESP32-S3 N16R8-class memory configuration, ES8311 playback, ES7210 capture, AXP2101 power management, e-paper display, physical controls and factory/recovery interfaces. I use those identifiers only where they help explain the engineering boundary; the larger lesson is about how firmware, schematic and physical assembly have to agree.

The evidence for this case was specific: **The hardware requirements separately required USB-C charging, controlled programming/debug access, factory test interface and recovery/reflash without destructive teardown.** I treat that as evidence from this board/revision and investigation, not as a universal statement about every ESP32-S3 design.

The result I retained was equally narrow: **Factory programming and recovery access were specified independently from charging.**

## How I framed the problem

The first plausible explanation was not the one I wanted to preserve. The observed problem was A product can have a USB-C connector and still lack a reliable programming/recovery path for failed units. The more authoritative observation was The hardware requirements separately required USB-C charging, controlled programming/debug access, factory test interface and recovery/reflash without destructive teardown. Once I accounted for the actual mechanism—Charging, USB data, ROM download, UART/JTAG and fixture access are distinct interfaces with different availability during boot failure.—the shortcut explanation, Assuming the consumer USB-C connector is sufficient for manufacturing and field recovery., stopped being good enough. The engineering result was Factory programming and recovery access were specified independently from charging.

Human-interface hardware creates another kind of boundary problem. A display is not “working” merely because SPI toggles, and a rotary encoder is not accepted merely because firmware counts pulses. The physical part, power rail, connector, mechanism, firmware driver and factory fixture all participate. Recovery interfaces matter most when normal interfaces are unavailable, which is exactly why they are easy to undervalue during a successful prototype demo.

The practical rule that came out of the case was: **Design recovery for the device state where the application is already broken.** I prefer a rule like that over a one-off patch because it changes the next bring-up decision before another board is modified.

## Evidence matrix

| Question | Answer |
| --- | --- |
| Observed problem | A product can have a USB-C connector and still lack a reliable programming/recovery path for failed units. |
| Strongest evidence | The hardware requirements separately required USB-C charging, controlled programming/debug access, factory test interface and recovery/reflash without destructive teardown. |
| Mechanism | Charging, USB data, ROM download, UART/JTAG and fixture access are distinct interfaces with different availability during boot failure. |
| Rejected shortcut | Assuming the consumer USB-C connector is sufficient for manufacturing and field recovery. |
| Retained result | Factory programming and recovery access were specified independently from charging. |
| Carry-forward rule | Design recovery for the device state where the application is already broken. |

I keep this table because board bring-up narratives become unreliable very quickly. A working prototype encourages retrospective certainty: once the device boots, it is easy to rewrite every earlier guess as if it had been obvious. The matrix preserves the difference between what the board actually demonstrated and what I merely considered plausible.

## The boundary I wanted to prove

```
part identity -> power prerequisite -> electrical interface
       -> mechanical assembly -> firmware driver -> factory gate

recovery path must still work when "firmware driver" does not.
```

For this layer I wanted at least these checks before changing the design:

- exact component part number
- required rail/power prerequisite
- electrical I/O behavior
- mechanical/connector behavior
- factory/recovery test access

The important part is ordering. I do not start with the last item just because firmware is the easiest thing for me to edit. If the rail is absent, a driver rewrite is irrelevant. If the exact part differs from the assumed part, a timing tweak may only hide the mismatch. If the physical channel is wrong, the DSP can be perfectly stable while processing the wrong signal.

For this case, **Charging, USB data, ROM download, UART/JTAG and fixture access are distinct interfaces with different availability during boot failure.** That mechanism defines which measurement belongs before the patch and which measurement should change afterward.

## Investigation method

I also record negative evidence. If a suspected GPIO toggle does not change the physical enable node, that is valuable. If changing host I2S mode makes the packing look different but breaks the known-good architecture, that experiment can still reveal representation. Failed experiments are useful when I keep their scope narrow enough to know what they disproved.

The shortcut I deliberately avoided here was **Assuming the consumer USB-C connector is sufficient for manufacturing and field recovery.** That shortcut is attractive because it converts a cross-disciplinary problem into something one person can edit immediately. It is also how firmware becomes a compensation layer for an electrical problem that nobody has actually measured.

## What firmware can prove—and what it cannot

Firmware can prove that it configured a peripheral, observed an I2C ACK, selected a pin mux, received DMA data, read a status bit or saw a button transition. Those are useful facts. They are not substitutes for physical measurements when the disputed state exists outside the MCU.

For **USB-C Charging Is Not a Factory Debug Strategy**, the relevant distinction is that Charging, USB data, ROM download, UART/JTAG and fixture access are distinct interfaces with different availability during boot failure. A log can expose the software side of that relationship, but the electrical/mechanical side still needs the appropriate observation point.

This matters most when a diagnostic success is weaker than the product claim. An I2C scan cannot prove microphone quality. A BUSY transition cannot prove display alignment or long-term FPC reliability. A GPIO write cannot prove the amplifier enable pin actually changed if an expander or transistor sits between them. A factory programming command cannot prove traceability unless the result is tied to the unit identity.

I therefore write two columns in bring-up notes: “software evidence” and “physical evidence.” A fix is stronger when both point at the same mechanism.

## Acceptance test I would keep

A good acceptance test tells me where to look when it fails. “Display failed” is weak. “ALDO3 present, FPC continuity good, SPI commands issued, BUSY never released” is actionable. The same principle applies to audio, power and controls: preserve intermediate evidence instead of reducing everything to a final green/red LED.

For this case the acceptance target is derived from the retained result: **Factory programming and recovery access were specified independently from charging.** The test should prove that result directly rather than infer it from a neighboring signal.

## What this changes before PCB release

The lesson is not only about debugging the current EVT. It changes the release package. **Design recovery for the device state where the application is already broken.**

For a board revision, I want the schematic revision, BOM identity, power-tree assumptions, pin map, factory/recovery interfaces and firmware hardware contract to move together. If one changes, the others should either change or explicitly state why they do not. This is especially important around programmable parts such as the PMIC and around signals whose semantics are created jointly by analog routing and software mapping.

I also want unresolved questions to remain visible. “Works on EVT” should not silently close an electrical-margin question, a tactile-control mismatch or an acoustic uncertainty. A production decision needs evidence appropriate to the risk. That may be a reset-time voltage analysis, a fixture measurement, a component supplier confirmation, an enclosed-device acoustic test or a repeated assembly trial.

The factory benefits from the same clarity. A deterministic test path reduces rework and makes a failed unit diagnosable instead of merely rejected.

## What I would change on the next board

I would make more of these boundaries explicit before layout. Each programmable power rail would have a table with voltage, owner, default state and test point. Boot-sensitive GPIOs would be reviewed as a separate checklist before peripheral placement is frozen. Codec and ADC channel mapping would be documented from schematic net to DMA representation. Recovery pads would be designed with the fixture, not added after the board already existed.

For human-interface parts, I would require an exact supplier variant and physical sample whenever the requirement contains a tactile or acoustic adjective. “Detented,” “loud,” “clear,” “thin,” “clicky” and “stable” cannot be accepted from a symbol or generic family datasheet alone.

For **USB-C Charging Is Not a Factory Debug Strategy**, I would carry forward the mechanism directly: Charging, USB data, ROM download, UART/JTAG and fixture access are distinct interfaces with different availability during boot failure. That turns this incident into a design-review question instead of another bring-up surprise.

## The rule I kept

**Design recovery for the device state where the application is already broken.**

The retained result from this case was: Factory programming and recovery access were specified independently from charging.

That is how I now approach PCB bring-up. I do not ask firmware to compensate for an unmeasured electrical problem, and I do not ask hardware engineers to redesign a circuit because a software label looked wrong. I locate the boundary, choose an observation point that can actually see it, reconcile the authoritative artifacts, and only then change the layer that owns the failure.

The process feels slower than immediately editing code. Across multiple board revisions it is much faster, because every confirmed boundary becomes reusable evidence for the next failure.
