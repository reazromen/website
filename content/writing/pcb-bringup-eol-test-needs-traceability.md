---
title: A 100 Percent End-of-Line Test Needs Traceability, Not Just a Green LED
url: /posts/pcb-bringup-eol-test-needs-traceability.html
date: '2024-08-28'
read_time: 9
excerpt: A factory test that says PASS without linking the result to a specific unit,
  programmed identity and relevant component history is weak forensic evidence.
topic: pcb-bringup-hardware
tags:
- esp32-s3
- pcb-bring-up
- hardware
draft: false
featured: false
language: en
eyebrow: 'PCB Bring-Up: EVT-to-Production Validation · deep-dive'
outputs:
- url: /posts/pcb-bringup-eol-test-needs-traceability.html
  template: cms/templates/posts/posts--pcb-bringup-eol-test-needs-traceability.tpl
  source: cms/templates/posts/posts--pcb-bringup-eol-test-needs-traceability.json
---

# A 100 Percent End-of-Line Test Needs Traceability, Not Just a Green LED

One of the fastest ways to waste bring-up time is to debug the wrong representation of the hardware. In this case, A factory test that says PASS without linking the result to a specific unit, programmed identity and relevant component history is weak forensic evidence.

The board context for this series is LOUP's Minewing V1.6 ESP32-S3 hardware: ESP32-S3 N16R8-class memory configuration, ES8311 playback, ES7210 capture, AXP2101 power management, e-paper display, physical controls and factory/recovery interfaces. I use those identifiers only where they help explain the engineering boundary; the larger lesson is about how firmware, schematic and physical assembly have to agree.

The evidence for this case was specific: **The HRS required 100% unit-level tests for power, boot, display, controls, speaker, microphone, Wi-Fi, USB-C charging, battery measurement, device identity and programming, with serial/device/test result and key component lots traceable.** I treat that as evidence from this board/revision and investigation, not as a universal statement about every ESP32-S3 design.

The result I retained was equally narrow: **Factory test requirements connected programming, identity and pass/fail recording before PVT.**

## How I framed the problem

The first plausible explanation was not the one I wanted to preserve. The observed problem was A factory test that says PASS without linking the result to a specific unit, programmed identity and relevant component history is weak forensic evidence. The more authoritative observation was The HRS required 100% unit-level tests for power, boot, display, controls, speaker, microphone, Wi-Fi, USB-C charging, battery measurement, device identity and programming, with serial/device/test result and key component lots traceable. Once I accounted for the actual mechanism—Production quality is a data system: the fixture observes functions, programming creates identity, and records bind the outcome to the shipped unit.—the shortcut explanation, Treating a manual functional check as equivalent to a traceable EOL process., stopped being good enough. The engineering result was Factory test requirements connected programming, identity and pass/fail recording before PVT.

The transition from EVT to production changes the engineering question. A hand-built unit can tolerate ambiguous assembly, undocumented tweaks and manual rework. Production cannot. The design has to become repeatable, testable, traceable and recoverable. That means the manufacturer and firmware team need explicit ownership while sharing a precise hardware/firmware contract and a common acceptance language.

The practical rule that came out of the case was: **A production test is only as useful as the evidence it leaves behind.** I prefer a rule like that over a one-off patch because it changes the next bring-up decision before another board is modified.

## Evidence matrix

| Question | Answer |
| --- | --- |
| Observed problem | A factory test that says PASS without linking the result to a specific unit, programmed identity and relevant component history is weak forensic evidence. |
| Strongest evidence | The HRS required 100% unit-level tests for power, boot, display, controls, speaker, microphone, Wi-Fi, USB-C charging, battery measurement, device identity and programming, with serial/device/test result and key component lots traceable. |
| Mechanism | Production quality is a data system: the fixture observes functions, programming creates identity, and records bind the outcome to the shipped unit. |
| Rejected shortcut | Treating a manual functional check as equivalent to a traceable EOL process. |
| Retained result | Factory test requirements connected programming, identity and pass/fail recording before PVT. |
| Carry-forward rule | A production test is only as useful as the evidence it leaves behind. |

I keep this table because board bring-up narratives become unreliable very quickly. A working prototype encourages retrospective certainty: once the device boots, it is easy to rewrite every earlier guess as if it had been obvious. The matrix preserves the difference between what the board actually demonstrated and what I merely considered plausible.

## The boundary I wanted to prove

```
prototype works
   -> EVT architecture evidence
   -> DVT design verification
   -> PVT repeatability / fixture / traceability
   -> controlled production release
```

For this layer I wanted at least these checks before changing the design:

- explicit milestone acceptance
- repeatable assembly feature
- unit identity and test record
- rework/retest path
- golden sample and ownership sign-off

The important part is ordering. I do not start with the last item just because firmware is the easiest thing for me to edit. If the rail is absent, a driver rewrite is irrelevant. If the exact part differs from the assumed part, a timing tweak may only hide the mismatch. If the physical channel is wrong, the DSP can be perfectly stable while processing the wrong signal.

For this case, **Production quality is a data system: the fixture observes functions, programming creates identity, and records bind the outcome to the shipped unit.** That mechanism defines which measurement belongs before the patch and which measurement should change afterward.

## What firmware can prove—and what it cannot

Firmware can prove that it configured a peripheral, observed an I2C ACK, selected a pin mux, received DMA data, read a status bit or saw a button transition. Those are useful facts. They are not substitutes for physical measurements when the disputed state exists outside the MCU.

For **A 100 Percent End-of-Line Test Needs Traceability, Not Just a Green LED**, the relevant distinction is that Production quality is a data system: the fixture observes functions, programming creates identity, and records bind the outcome to the shipped unit. A log can expose the software side of that relationship, but the electrical/mechanical side still needs the appropriate observation point.

This matters most when a diagnostic success is weaker than the product claim. An I2C scan cannot prove microphone quality. A BUSY transition cannot prove display alignment or long-term FPC reliability. A GPIO write cannot prove the amplifier enable pin actually changed if an expander or transistor sits between them. A factory programming command cannot prove traceability unless the result is tied to the unit identity.

I therefore write two columns in bring-up notes: “software evidence” and “physical evidence.” A fix is stronger when both point at the same mechanism.

## Investigation method

I also record negative evidence. If a suspected GPIO toggle does not change the physical enable node, that is valuable. If changing host I2S mode makes the packing look different but breaks the known-good architecture, that experiment can still reveal representation. Failed experiments are useful when I keep their scope narrow enough to know what they disproved.

The shortcut I deliberately avoided here was **Treating a manual functional check as equivalent to a traceable EOL process.** That shortcut is attractive because it converts a cross-disciplinary problem into something one person can edit immediately. It is also how firmware becomes a compensation layer for an electrical problem that nobody has actually measured.

## Acceptance test I would keep

A good acceptance test tells me where to look when it fails. “Display failed” is weak. “ALDO3 present, FPC continuity good, SPI commands issued, BUSY never released” is actionable. The same principle applies to audio, power and controls: preserve intermediate evidence instead of reducing everything to a final green/red LED.

For this case the acceptance target is derived from the retained result: **Factory test requirements connected programming, identity and pass/fail recording before PVT.** The test should prove that result directly rather than infer it from a neighboring signal.

## What this changes before PCB release

The lesson is not only about debugging the current EVT. It changes the release package. **A production test is only as useful as the evidence it leaves behind.**

For a board revision, I want the schematic revision, BOM identity, power-tree assumptions, pin map, factory/recovery interfaces and firmware hardware contract to move together. If one changes, the others should either change or explicitly state why they do not. This is especially important around programmable parts such as the PMIC and around signals whose semantics are created jointly by analog routing and software mapping.

I also want unresolved questions to remain visible. “Works on EVT” should not silently close an electrical-margin question, a tactile-control mismatch or an acoustic uncertainty. A production decision needs evidence appropriate to the risk. That may be a reset-time voltage analysis, a fixture measurement, a component supplier confirmation, an enclosed-device acoustic test or a repeated assembly trial.

The factory benefits from the same clarity. A deterministic test path reduces rework and makes a failed unit diagnosable instead of merely rejected.

## What I would change on the next board

I would make more of these boundaries explicit before layout. Each programmable power rail would have a table with voltage, owner, default state and test point. Boot-sensitive GPIOs would be reviewed as a separate checklist before peripheral placement is frozen. Codec and ADC channel mapping would be documented from schematic net to DMA representation. Recovery pads would be designed with the fixture, not added after the board already existed.

For human-interface parts, I would require an exact supplier variant and physical sample whenever the requirement contains a tactile or acoustic adjective. “Detented,” “loud,” “clear,” “thin,” “clicky” and “stable” cannot be accepted from a symbol or generic family datasheet alone.

For **A 100 Percent End-of-Line Test Needs Traceability, Not Just a Green LED**, I would carry forward the mechanism directly: Production quality is a data system: the fixture observes functions, programming creates identity, and records bind the outcome to the shipped unit. That turns this incident into a design-review question instead of another bring-up surprise.

## The rule I kept

**A production test is only as useful as the evidence it leaves behind.**

The retained result from this case was: Factory test requirements connected programming, identity and pass/fail recording before PVT.

That is how I now approach PCB bring-up. I do not ask firmware to compensate for an unmeasured electrical problem, and I do not ask hardware engineers to redesign a circuit because a software label looked wrong. I locate the boundary, choose an observation point that can actually see it, reconcile the authoritative artifacts, and only then change the layer that owns the failure.

The process feels slower than immediately editing code. Across multiple board revisions it is much faster, because every confirmed boundary becomes reusable evidence for the next failure.
