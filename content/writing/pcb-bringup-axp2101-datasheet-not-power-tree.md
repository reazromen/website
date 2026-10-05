---
title: An AXP2101 Datasheet Is Not a LOUP Power Tree
url: /posts/pcb-bringup-axp2101-datasheet-not-power-tree.html
date: '2025-03-27'
read_time: 9
excerpt: Receiving the PMIC datasheet did not answer which regulator powered each
  subsystem, what came up before firmware, or how the product behaved on battery and
  USB insertion.
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
- url: /posts/pcb-bringup-axp2101-datasheet-not-power-tree.html
  template: cms/templates/posts/posts--pcb-bringup-axp2101-datasheet-not-power-tree.tpl
  source: cms/templates/posts/posts--pcb-bringup-axp2101-datasheet-not-power-tree.json
---

# An AXP2101 Datasheet Is Not a LOUP Power Tree

I learned this boundary the hard way: Receiving the PMIC datasheet did not answer which regulator powered each subsystem, what came up before firmware, or how the product behaved on battery and USB insertion.

The board context for this series is LOUP's Minewing V1.6 ESP32-S3 hardware: ESP32-S3 N16R8-class memory configuration, ES8311 playback, ES7210 capture, AXP2101 power management, e-paper display, physical controls and factory/recovery interfaces. I use those identifiers only where they help explain the engineering boundary; the larger lesson is about how firmware, schematic and physical assembly have to agree.

The evidence for this case was specific: **The schematic review requested the exact AXP2101 ordering code, PWRON behavior, regulator/load/default-state/startup sequence and battery/USB/power-off behavior as a LOUP-specific power-tree table.** I treat that as evidence from this board/revision and investigation, not as a universal statement about every ESP32-S3 design.

The result I retained was equally narrow: **The review made the power tree a required design deliverable before final Gerber release.**

## How I framed the problem

I treated the issue as a source-of-truth conflict. The symptom was Receiving the PMIC datasheet did not answer which regulator powered each subsystem, what came up before firmware, or how the product behaved on battery and USB insertion. The strongest evidence was The schematic review requested the exact AXP2101 ordering code, PWRON behavior, regulator/load/default-state/startup sequence and battery/USB/power-off behavior as a LOUP-specific power-tree table. The mechanism was A programmable PMIC exposes capabilities; the product configuration is a separate artifact that spans schematic straps, firmware writes and startup defaults. That made the tempting alternative—Assuming the chip datasheet documents the product power architecture.—something I could test instead of a story I had to believe. The retained result was The review made the power tree a required design deliverable before final Gerber release.

Power bugs are especially dangerous because they can masquerade as almost anything else: boot instability, display failure, codec silence, intermittent resets or unexplained battery behavior. With a programmable PMIC, the schematic alone does not fully define startup. Defaults, firmware register writes, external switches, load transients and reset sequencing all matter. I want each rail to have a named purpose and a measurable state.

The practical rule that came out of the case was: **Power architecture must be documented at the product level, not inferred from a PMIC feature list.** I prefer a rule like that over a one-off patch because it changes the next bring-up decision before another board is modified.

## Evidence matrix

| Question | Answer |
| --- | --- |
| Observed problem | Receiving the PMIC datasheet did not answer which regulator powered each subsystem, what came up before firmware, or how the product behaved on battery and USB insertion. |
| Strongest evidence | The schematic review requested the exact AXP2101 ordering code, PWRON behavior, regulator/load/default-state/startup sequence and battery/USB/power-off behavior as a LOUP-specific power-tree table. |
| Mechanism | A programmable PMIC exposes capabilities; the product configuration is a separate artifact that spans schematic straps, firmware writes and startup defaults. |
| Rejected shortcut | Assuming the chip datasheet documents the product power architecture. |
| Retained result | The review made the power tree a required design deliverable before final Gerber release. |
| Carry-forward rule | Power architecture must be documented at the product level, not inferred from a PMIC feature list. |

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

For this case, **A programmable PMIC exposes capabilities; the product configuration is a separate artifact that spans schematic straps, firmware writes and startup defaults.** That mechanism defines which measurement belongs before the patch and which measurement should change afterward.

## Investigation method

My investigation sequence is intentionally boring: freeze the board revision, record the exact artifact versions, inspect the electrical path, instrument the nearest software boundary, then change one variable. On hardware problems, “boring” is useful because every uncontrolled substitution—a different speaker, FPC, battery state, USB supply or firmware branch—creates another possible explanation.

The shortcut I deliberately avoided here was **Assuming the chip datasheet documents the product power architecture.** That shortcut is attractive because it converts a cross-disciplinary problem into something one person can edit immediately. It is also how firmware becomes a compensation layer for an electrical problem that nobody has actually measured.

## What firmware can prove—and what it cannot

Firmware can prove that it configured a peripheral, observed an I2C ACK, selected a pin mux, received DMA data, read a status bit or saw a button transition. Those are useful facts. They are not substitutes for physical measurements when the disputed state exists outside the MCU.

For **An AXP2101 Datasheet Is Not a LOUP Power Tree**, the relevant distinction is that A programmable PMIC exposes capabilities; the product configuration is a separate artifact that spans schematic straps, firmware writes and startup defaults. A log can expose the software side of that relationship, but the electrical/mechanical side still needs the appropriate observation point.

This matters most when a diagnostic success is weaker than the product claim. An I2C scan cannot prove microphone quality. A BUSY transition cannot prove display alignment or long-term FPC reliability. A GPIO write cannot prove the amplifier enable pin actually changed if an expander or transistor sits between them. A factory programming command cannot prove traceability unless the result is tied to the unit identity.

I therefore write two columns in bring-up notes: “software evidence” and “physical evidence.” A fix is stronger when both point at the same mechanism.

## Acceptance test I would keep

The acceptance test should recreate the exact boundary that failed. I want a precondition, a stimulus, a measurable physical/software response and a pass/fail threshold. If the issue is power, test battery and USB transitions. If it is display, prove the rail, connector and render path. If it is audio routing, inject or capture a known signal. If it is a control, verify both electrical pulses and physical feel.

For this case the acceptance target is derived from the retained result: **The review made the power tree a required design deliverable before final Gerber release.** The test should prove that result directly rather than infer it from a neighboring signal.

## What this changes before PCB release

The lesson is not only about debugging the current EVT. It changes the release package. **Power architecture must be documented at the product level, not inferred from a PMIC feature list.**

For a board revision, I want the schematic revision, BOM identity, power-tree assumptions, pin map, factory/recovery interfaces and firmware hardware contract to move together. If one changes, the others should either change or explicitly state why they do not. This is especially important around programmable parts such as the PMIC and around signals whose semantics are created jointly by analog routing and software mapping.

I also want unresolved questions to remain visible. “Works on EVT” should not silently close an electrical-margin question, a tactile-control mismatch or an acoustic uncertainty. A production decision needs evidence appropriate to the risk. That may be a reset-time voltage analysis, a fixture measurement, a component supplier confirmation, an enclosed-device acoustic test or a repeated assembly trial.

The factory benefits from the same clarity. A deterministic test path reduces rework and makes a failed unit diagnosable instead of merely rejected.

## What I would change on the next board

I would make more of these boundaries explicit before layout. Each programmable power rail would have a table with voltage, owner, default state and test point. Boot-sensitive GPIOs would be reviewed as a separate checklist before peripheral placement is frozen. Codec and ADC channel mapping would be documented from schematic net to DMA representation. Recovery pads would be designed with the fixture, not added after the board already existed.

For human-interface parts, I would require an exact supplier variant and physical sample whenever the requirement contains a tactile or acoustic adjective. “Detented,” “loud,” “clear,” “thin,” “clicky” and “stable” cannot be accepted from a symbol or generic family datasheet alone.

For **An AXP2101 Datasheet Is Not a LOUP Power Tree**, I would carry forward the mechanism directly: A programmable PMIC exposes capabilities; the product configuration is a separate artifact that spans schematic straps, firmware writes and startup defaults. That turns this incident into a design-review question instead of another bring-up surprise.

## The rule I kept

**Power architecture must be documented at the product level, not inferred from a PMIC feature list.**

The retained result from this case was: The review made the power tree a required design deliverable before final Gerber release.

That is how I now approach PCB bring-up. I do not ask firmware to compensate for an unmeasured electrical problem, and I do not ask hardware engineers to redesign a circuit because a software label looked wrong. I locate the boundary, choose an observation point that can actually see it, reconcile the authoritative artifacts, and only then change the layer that owns the failure.

The process feels slower than immediately editing code. Across multiple board revisions it is much faster, because every confirmed boundary becomes reusable evidence for the next failure.
