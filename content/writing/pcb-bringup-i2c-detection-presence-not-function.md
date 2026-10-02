---
title: I2C Detection Proves Presence, Not Functional Correctness
url: /posts/pcb-bringup-i2c-detection-presence-not-function.html
date: '2026-09-15'
read_time: 9
excerpt: Seeing ES8311, ES7210 and AXP2101 on the I2C bus was necessary but insufficient
  evidence that the audio and power architecture worked correctly.
topic: pcb-bringup-hardware
tags:
- esp32-s3
- pcb-bring-up
- hardware
draft: false
featured: false
language: en
eyebrow: 'PCB Bring-Up: Evidence & Source of Truth · deep-dive'
outputs:
- url: /posts/pcb-bringup-i2c-detection-presence-not-function.html
  template: cms/templates/posts/posts--pcb-bringup-i2c-detection-presence-not-function.tpl
  source: cms/templates/posts/posts--pcb-bringup-i2c-detection-presence-not-function.json
---

# I2C Detection Proves Presence, Not Functional Correctness

This was not primarily a firmware problem or a hardware problem. It was an interface problem: Seeing ES8311, ES7210 and AXP2101 on the I2C bus was necessary but insufficient evidence that the audio and power architecture worked correctly.

The board context for this series is LOUP's Minewing V1.6 ESP32-S3 hardware: ESP32-S3 N16R8-class memory configuration, ES8311 playback, ES7210 capture, AXP2101 power management, e-paper display, physical controls and factory/recovery interfaces. I use those identifiers only where they help explain the engineering boundary; the larger lesson is about how firmware, schematic and physical assembly have to agree.

The evidence for this case was specific: **The V1.6 board exposed ES8311 at 0x18, ES7210 at 0x40 and AXP2101 at 0x34, while later runtime work still found ES7210 channel-packing and reference-routing mistakes.** I treat that as evidence from this board/revision and investigation, not as a universal statement about every ESP32-S3 design.

The result I retained was equally narrow: **Bring-up separated bus-presence tests from functional signal-path tests.**

## How I framed the problem

I wrote down the physical signal or state first, then asked which document and which firmware path claimed to own it. The problem was Seeing ES8311, ES7210 and AXP2101 on the I2C bus was necessary but insufficient evidence that the audio and power architecture worked correctly. Runtime/document evidence showed The V1.6 board exposed ES8311 at 0x18, ES7210 at 0x40 and AXP2101 at 0x34, while later runtime work still found ES7210 channel-packing and reference-routing mistakes. Because An ACK proves that a device responds at an address; it does not prove clocking, analog routing, channel semantics, power state or application behavior., I refused to accept Declaring a codec path healthy because the scan found the expected address. as proof. The useful outcome was Bring-up separated bus-presence tests from functional signal-path tests.

The bring-up problem is epistemic before it is electrical: which artifact deserves to be believed? A schematic can be stale, firmware can carry a previous board's GPIO map, a datasheet can describe the right family but the wrong exact part, and a runtime label can assign a friendly channel name to the wrong halfword. I therefore treat the board as the final physical truth and use documents, source and probes as competing representations that must converge.

The practical rule that came out of the case was: **Presence checks are layer-zero evidence, not end-to-end acceptance.** I prefer a rule like that over a one-off patch because it changes the next bring-up decision before another board is modified.

## Evidence matrix

| Question | Answer |
| --- | --- |
| Observed problem | Seeing ES8311, ES7210 and AXP2101 on the I2C bus was necessary but insufficient evidence that the audio and power architecture worked correctly. |
| Strongest evidence | The V1.6 board exposed ES8311 at 0x18, ES7210 at 0x40 and AXP2101 at 0x34, while later runtime work still found ES7210 channel-packing and reference-routing mistakes. |
| Mechanism | An ACK proves that a device responds at an address; it does not prove clocking, analog routing, channel semantics, power state or application behavior. |
| Rejected shortcut | Declaring a codec path healthy because the scan found the expected address. |
| Retained result | Bring-up separated bus-presence tests from functional signal-path tests. |
| Carry-forward rule | Presence checks are layer-zero evidence, not end-to-end acceptance. |

I keep this table because board bring-up narratives become unreliable very quickly. A working prototype encourages retrospective certainty: once the device boots, it is easy to rewrite every earlier guess as if it had been obvious. The matrix preserves the difference between what the board actually demonstrated and what I merely considered plausible.

## The boundary I wanted to prove

```
claim from schematic ----+
claim from firmware -----+--> reconcile --> probe physical board
claim from datasheet ----+                    |
runtime labels ----------+                    v
                                      accepted hardware contract
```

For this layer I wanted at least these checks before changing the design:

- board revision and exact schematic revision
- BOM/datasheet identity
- firmware pin/channel constants
- runtime probe at the physical boundary
- documented owner for any unresolved mismatch

The important part is ordering. I do not start with the last item just because firmware is the easiest thing for me to edit. If the rail is absent, a driver rewrite is irrelevant. If the exact part differs from the assumed part, a timing tweak may only hide the mismatch. If the physical channel is wrong, the DSP can be perfectly stable while processing the wrong signal.

For this case, **An ACK proves that a device responds at an address; it does not prove clocking, analog routing, channel semantics, power state or application behavior.** That mechanism defines which measurement belongs before the patch and which measurement should change afterward.

## What firmware can prove—and what it cannot

Firmware can prove that it configured a peripheral, observed an I2C ACK, selected a pin mux, received DMA data, read a status bit or saw a button transition. Those are useful facts. They are not substitutes for physical measurements when the disputed state exists outside the MCU.

For **I2C Detection Proves Presence, Not Functional Correctness**, the relevant distinction is that An ACK proves that a device responds at an address; it does not prove clocking, analog routing, channel semantics, power state or application behavior. A log can expose the software side of that relationship, but the electrical/mechanical side still needs the appropriate observation point.

This matters most when a diagnostic success is weaker than the product claim. An I2C scan cannot prove microphone quality. A BUSY transition cannot prove display alignment or long-term FPC reliability. A GPIO write cannot prove the amplifier enable pin actually changed if an expander or transistor sits between them. A factory programming command cannot prove traceability unless the result is tied to the unit identity.

I therefore write two columns in bring-up notes: “software evidence” and “physical evidence.” A fix is stronger when both point at the same mechanism.

## Investigation method

I try to separate presence, configuration and function. Presence means the part answers or the net exists. Configuration means register state, pin mux and power state are what I intended. Function means a real signal traverses the subsystem. A component can pass the first two and fail the third. That hierarchy prevented several I2C and display checks from being promoted to false product acceptance.

The shortcut I deliberately avoided here was **Declaring a codec path healthy because the scan found the expected address.** That shortcut is attractive because it converts a cross-disciplinary problem into something one person can edit immediately. It is also how firmware becomes a compensation layer for an electrical problem that nobody has actually measured.

## Acceptance test I would keep

I prefer a fixture-friendly acceptance test over a one-off engineering ritual. Anything that needs a probe point should have an accessible point or a factory diagnostic. Anything that relies on component identity should appear in the BOM/revision record. Anything that can regress in firmware should have a boot or factory log marker that is cheap enough to retain.

For this case the acceptance target is derived from the retained result: **Bring-up separated bus-presence tests from functional signal-path tests.** The test should prove that result directly rather than infer it from a neighboring signal.

## What this changes before PCB release

The lesson is not only about debugging the current EVT. It changes the release package. **Presence checks are layer-zero evidence, not end-to-end acceptance.**

For a board revision, I want the schematic revision, BOM identity, power-tree assumptions, pin map, factory/recovery interfaces and firmware hardware contract to move together. If one changes, the others should either change or explicitly state why they do not. This is especially important around programmable parts such as the PMIC and around signals whose semantics are created jointly by analog routing and software mapping.

I also want unresolved questions to remain visible. “Works on EVT” should not silently close an electrical-margin question, a tactile-control mismatch or an acoustic uncertainty. A production decision needs evidence appropriate to the risk. That may be a reset-time voltage analysis, a fixture measurement, a component supplier confirmation, an enclosed-device acoustic test or a repeated assembly trial.

The factory benefits from the same clarity. A deterministic test path reduces rework and makes a failed unit diagnosable instead of merely rejected.

## What I would change on the next board

I would make more of these boundaries explicit before layout. Each programmable power rail would have a table with voltage, owner, default state and test point. Boot-sensitive GPIOs would be reviewed as a separate checklist before peripheral placement is frozen. Codec and ADC channel mapping would be documented from schematic net to DMA representation. Recovery pads would be designed with the fixture, not added after the board already existed.

For human-interface parts, I would require an exact supplier variant and physical sample whenever the requirement contains a tactile or acoustic adjective. “Detented,” “loud,” “clear,” “thin,” “clicky” and “stable” cannot be accepted from a symbol or generic family datasheet alone.

For **I2C Detection Proves Presence, Not Functional Correctness**, I would carry forward the mechanism directly: An ACK proves that a device responds at an address; it does not prove clocking, analog routing, channel semantics, power state or application behavior. That turns this incident into a design-review question instead of another bring-up surprise.

## The rule I kept

**Presence checks are layer-zero evidence, not end-to-end acceptance.**

The retained result from this case was: Bring-up separated bus-presence tests from functional signal-path tests.

That is how I now approach PCB bring-up. I do not ask firmware to compensate for an unmeasured electrical problem, and I do not ask hardware engineers to redesign a circuit because a software label looked wrong. I locate the boundary, choose an observation point that can actually see it, reconcile the authoritative artifacts, and only then change the layer that owns the failure.

The process feels slower than immediately editing code. Across multiple board revisions it is much faster, because every confirmed boundary becomes reusable evidence for the next failure.
