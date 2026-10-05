---
title: ALDO2 and ALDO3 Became Named Product Rails
url: /posts/pcb-bringup-aldo2-aldo3-named-product-rails.html
date: '2020-11-15'
read_time: 9
excerpt: Display and audio bring-up failed more predictably once regulator names were
  tied to actual product loads instead of generic PMIC outputs.
topic: pcb-bringup-hardware
tags:
- esp32-s3
- pcb-bring-up
- hardware
draft: false
featured: false
language: en
eyebrow: 'PCB Bring-Up: Power, Boot & Electrical Margins · deep-dive'
outputs:
- url: /posts/pcb-bringup-aldo2-aldo3-named-product-rails.html
  template: cms/templates/posts/posts--pcb-bringup-aldo2-aldo3-named-product-rails.tpl
  source: cms/templates/posts/posts--pcb-bringup-aldo2-aldo3-named-product-rails.json
---

# ALDO2 and ALDO3 Became Named Product Rails

One of the fastest ways to waste bring-up time is to debug the wrong representation of the hardware. In this case, Display and audio bring-up failed more predictably once regulator names were tied to actual product loads instead of generic PMIC outputs.

The board context for this series is LOUP's Minewing V1.6 ESP32-S3 hardware: ESP32-S3 N16R8-class memory configuration, ES8311 playback, ES7210 capture, AXP2101 power management, e-paper display, physical controls and factory/recovery interfaces. I use those identifiers only where they help explain the engineering boundary; the larger lesson is about how firmware, schematic and physical assembly have to agree.

The evidence for this case was specific: **Factory evidence identified ALDO2 as the 3.3 V audio-control rail and ALDO3 as the e-paper EPD\_VCC\_AXP rail; display testing required ALDO3 to be at 3.3 V before the panel test.** I treat that as evidence from this board/revision and investigation, not as a universal statement about every ESP32-S3 design.

The result I retained was equally narrow: **Power-rail semantics became visible in runtime/factory logs and acceptance instructions.**

## How I framed the problem

This case became a boundary test. On one side was the electrical/mechanical design; on the other was firmware or factory logic. The failure was Display and audio bring-up failed more predictably once regulator names were tied to actual product loads instead of generic PMIC outputs. I used Factory evidence identified ALDO2 as the 3.3 V audio-control rail and ALDO3 as the e-paper EPD\_VCC\_AXP rail; display testing required ALDO3 to be at 3.3 V before the panel test. to decide which side of the boundary needed the next experiment. The reason that evidence mattered is Naming a power rail by function links PMIC configuration, schematic net, firmware initialization and fixture expectations. The conclusion was Power-rail semantics became visible in runtime/factory logs and acceptance instructions.

Power bugs are especially dangerous because they can masquerade as almost anything else: boot instability, display failure, codec silence, intermittent resets or unexplained battery behavior. With a programmable PMIC, the schematic alone does not fully define startup. Defaults, firmware register writes, external switches, load transients and reset sequencing all matter. I want each rail to have a named purpose and a measurable state.

The practical rule that came out of the case was: **A rail should have an owner, voltage, load, startup state and verification method.** I prefer a rule like that over a one-off patch because it changes the next bring-up decision before another board is modified.

## Evidence matrix

| Question | Answer |
| --- | --- |
| Observed problem | Display and audio bring-up failed more predictably once regulator names were tied to actual product loads instead of generic PMIC outputs. |
| Strongest evidence | Factory evidence identified ALDO2 as the 3.3 V audio-control rail and ALDO3 as the e-paper EPD\_VCC\_AXP rail; display testing required ALDO3 to be at 3.3 V before the panel test. |
| Mechanism | Naming a power rail by function links PMIC configuration, schematic net, firmware initialization and fixture expectations. |
| Rejected shortcut | Debugging a dead peripheral without first proving its assigned rail is present and enabled. |
| Retained result | Power-rail semantics became visible in runtime/factory logs and acceptance instructions. |
| Carry-forward rule | A rail should have an owner, voltage, load, startup state and verification method. |

I keep this table because board bring-up narratives become unreliable very quickly. A working prototype encourages retrospective certainty: once the device boots, it is easy to rewrite every earlier guess as if it had been obvious. The matrix preserves the difference between what the board actually demonstrated and what I merely considered plausible.

## The boundary I wanted to prove

```
VBUS / BAT
   |
 AXP2101
   |-- rail A -> ESP32 / always-needed domain
   |-- ALDO2 -> audio/control domain
   |-- ALDO3 -> e-paper domain
   `-- unused rails -> explicitly OFF, not merely NC
```

For this layer I wanted at least these checks before changing the design:

- rail name and voltage
- connected load
- default/reset state
- firmware enable/disable state
- measurement on battery and USB transitions

The important part is ordering. I do not start with the last item just because firmware is the easiest thing for me to edit. If the rail is absent, a driver rewrite is irrelevant. If the exact part differs from the assumed part, a timing tweak may only hide the mismatch. If the physical channel is wrong, the DSP can be perfectly stable while processing the wrong signal.

For this case, **Naming a power rail by function links PMIC configuration, schematic net, firmware initialization and fixture expectations.** That mechanism defines which measurement belongs before the patch and which measurement should change afterward.

## Investigation method

Before touching source, I ask what an oscilloscope, multimeter, logic trace, raw sample probe or fixture observation could tell me that a log cannot. Firmware logs are excellent for software state and often weak for power, connector and analog questions. Conversely, a scope can show a clock but cannot prove the application assigned the resulting DMA words to the correct semantic channel.

The shortcut I deliberately avoided here was **Debugging a dead peripheral without first proving its assigned rail is present and enabled.** That shortcut is attractive because it converts a cross-disciplinary problem into something one person can edit immediately. It is also how firmware becomes a compensation layer for an electrical problem that nobody has actually measured.

## What firmware can prove—and what it cannot

Firmware can prove that it configured a peripheral, observed an I2C ACK, selected a pin mux, received DMA data, read a status bit or saw a button transition. Those are useful facts. They are not substitutes for physical measurements when the disputed state exists outside the MCU.

For **ALDO2 and ALDO3 Became Named Product Rails**, the relevant distinction is that Naming a power rail by function links PMIC configuration, schematic net, firmware initialization and fixture expectations. A log can expose the software side of that relationship, but the electrical/mechanical side still needs the appropriate observation point.

This matters most when a diagnostic success is weaker than the product claim. An I2C scan cannot prove microphone quality. A BUSY transition cannot prove display alignment or long-term FPC reliability. A GPIO write cannot prove the amplifier enable pin actually changed if an expander or transistor sits between them. A factory programming command cannot prove traceability unless the result is tied to the unit identity.

I therefore write two columns in bring-up notes: “software evidence” and “physical evidence.” A fix is stronger when both point at the same mechanism.

## Acceptance test I would keep

The pass condition must also survive repetition. One successful boot or one clear call is evidence of possibility, not production margin. For hardware-facing changes I repeat the test across power cycles and, where relevant, across multiple units or assembly states. The goal is to detect variation before the factory turns it into yield loss.

For this case the acceptance target is derived from the retained result: **Power-rail semantics became visible in runtime/factory logs and acceptance instructions.** The test should prove that result directly rather than infer it from a neighboring signal.

## What this changes before PCB release

The lesson is not only about debugging the current EVT. It changes the release package. **A rail should have an owner, voltage, load, startup state and verification method.**

For a board revision, I want the schematic revision, BOM identity, power-tree assumptions, pin map, factory/recovery interfaces and firmware hardware contract to move together. If one changes, the others should either change or explicitly state why they do not. This is especially important around programmable parts such as the PMIC and around signals whose semantics are created jointly by analog routing and software mapping.

I also want unresolved questions to remain visible. “Works on EVT” should not silently close an electrical-margin question, a tactile-control mismatch or an acoustic uncertainty. A production decision needs evidence appropriate to the risk. That may be a reset-time voltage analysis, a fixture measurement, a component supplier confirmation, an enclosed-device acoustic test or a repeated assembly trial.

The factory benefits from the same clarity. A deterministic test path reduces rework and makes a failed unit diagnosable instead of merely rejected.

## What I would change on the next board

I would make more of these boundaries explicit before layout. Each programmable power rail would have a table with voltage, owner, default state and test point. Boot-sensitive GPIOs would be reviewed as a separate checklist before peripheral placement is frozen. Codec and ADC channel mapping would be documented from schematic net to DMA representation. Recovery pads would be designed with the fixture, not added after the board already existed.

For human-interface parts, I would require an exact supplier variant and physical sample whenever the requirement contains a tactile or acoustic adjective. “Detented,” “loud,” “clear,” “thin,” “clicky” and “stable” cannot be accepted from a symbol or generic family datasheet alone.

For **ALDO2 and ALDO3 Became Named Product Rails**, I would carry forward the mechanism directly: Naming a power rail by function links PMIC configuration, schematic net, firmware initialization and fixture expectations. That turns this incident into a design-review question instead of another bring-up surprise.

## The rule I kept

**A rail should have an owner, voltage, load, startup state and verification method.**

The retained result from this case was: Power-rail semantics became visible in runtime/factory logs and acceptance instructions.

That is how I now approach PCB bring-up. I do not ask firmware to compensate for an unmeasured electrical problem, and I do not ask hardware engineers to redesign a circuit because a software label looked wrong. I locate the boundary, choose an observation point that can actually see it, reconcile the authoritative artifacts, and only then change the layer that owns the failure.

The process feels slower than immediately editing code. Across multiple board revisions it is much faster, because every confirmed boundary becomes reusable evidence for the next failure.
