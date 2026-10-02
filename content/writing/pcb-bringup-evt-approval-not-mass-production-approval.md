---
title: EVT Approval Is Not Mass-Production Approval
url: /posts/pcb-bringup-evt-approval-not-mass-production-approval.html
date: '2026-09-15'
read_time: 9
excerpt: Moving quickly toward EVT created pressure to interpret every interim approval
  as a final product freeze.
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
- url: /posts/pcb-bringup-evt-approval-not-mass-production-approval.html
  template: cms/templates/posts/posts--pcb-bringup-evt-approval-not-mass-production-approval.tpl
  source: cms/templates/posts/posts--pcb-bringup-evt-approval-not-mass-production-approval.json
---

# EVT Approval Is Not Mass-Production Approval

I learned this boundary the hard way: Moving quickly toward EVT created pressure to interpret every interim approval as a final product freeze.

The board context for this series is LOUP's Minewing V1.6 ESP32-S3 hardware: ESP32-S3 N16R8-class memory configuration, ES8311 playback, ES7210 capture, AXP2101 power management, e-paper display, physical controls and factory/recovery interfaces. I use those identifiers only where they help explain the engineering boundary; the larger lesson is about how firmware, schematic and physical assembly have to agree.

The evidence for this case was specific: **The July review explicitly allowed structural optimization, PCB floor-planning, sourcing and EVT preparation while withholding final Gerber/fabrication approval until power, encoder, schematic and other corrections were closed.** I treat that as evidence from this board/revision and investigation, not as a universal statement about every ESP32-S3 design.

The result I retained was equally narrow: **The project used staged approval language to keep progress moving without erasing open engineering risks.**

## How I framed the problem

I wrote down the physical signal or state first, then asked which document and which firmware path claimed to own it. The problem was Moving quickly toward EVT created pressure to interpret every interim approval as a final product freeze. Runtime/document evidence showed The July review explicitly allowed structural optimization, PCB floor-planning, sourcing and EVT preparation while withholding final Gerber/fabrication approval until power, encoder, schematic and other corrections were closed. Because EVT validates architecture and exposes defects; DVT and PVT answer later questions about design verification and production repeatability., I refused to accept Treating “continue EVT” as evidence that the hardware is production-approved. as proof. The useful outcome was The project used staged approval language to keep progress moving without erasing open engineering risks.

The transition from EVT to production changes the engineering question. A hand-built unit can tolerate ambiguous assembly, undocumented tweaks and manual rework. Production cannot. The design has to become repeatable, testable, traceable and recoverable. That means the manufacturer and firmware team need explicit ownership while sharing a precise hardware/firmware contract and a common acceptance language.

The practical rule that came out of the case was: **Milestone names only help when their acceptance scope is explicit.** I prefer a rule like that over a one-off patch because it changes the next bring-up decision before another board is modified.

## Evidence matrix

| Question | Answer |
| --- | --- |
| Observed problem | Moving quickly toward EVT created pressure to interpret every interim approval as a final product freeze. |
| Strongest evidence | The July review explicitly allowed structural optimization, PCB floor-planning, sourcing and EVT preparation while withholding final Gerber/fabrication approval until power, encoder, schematic and other corrections were closed. |
| Mechanism | EVT validates architecture and exposes defects; DVT and PVT answer later questions about design verification and production repeatability. |
| Rejected shortcut | Treating “continue EVT” as evidence that the hardware is production-approved. |
| Retained result | The project used staged approval language to keep progress moving without erasing open engineering risks. |
| Carry-forward rule | Milestone names only help when their acceptance scope is explicit. |

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

For this case, **EVT validates architecture and exposes defects; DVT and PVT answer later questions about design verification and production repeatability.** That mechanism defines which measurement belongs before the patch and which measurement should change afterward.

## What firmware can prove—and what it cannot

Firmware can prove that it configured a peripheral, observed an I2C ACK, selected a pin mux, received DMA data, read a status bit or saw a button transition. Those are useful facts. They are not substitutes for physical measurements when the disputed state exists outside the MCU.

For **EVT Approval Is Not Mass-Production Approval**, the relevant distinction is that EVT validates architecture and exposes defects; DVT and PVT answer later questions about design verification and production repeatability. A log can expose the software side of that relationship, but the electrical/mechanical side still needs the appropriate observation point.

This matters most when a diagnostic success is weaker than the product claim. An I2C scan cannot prove microphone quality. A BUSY transition cannot prove display alignment or long-term FPC reliability. A GPIO write cannot prove the amplifier enable pin actually changed if an expander or transistor sits between them. A factory programming command cannot prove traceability unless the result is tied to the unit identity.

I therefore write two columns in bring-up notes: “software evidence” and “physical evidence.” A fix is stronger when both point at the same mechanism.

## Investigation method

I try to separate presence, configuration and function. Presence means the part answers or the net exists. Configuration means register state, pin mux and power state are what I intended. Function means a real signal traverses the subsystem. A component can pass the first two and fail the third. That hierarchy prevented several I2C and display checks from being promoted to false product acceptance.

The shortcut I deliberately avoided here was **Treating “continue EVT” as evidence that the hardware is production-approved.** That shortcut is attractive because it converts a cross-disciplinary problem into something one person can edit immediately. It is also how firmware becomes a compensation layer for an electrical problem that nobody has actually measured.

## Acceptance test I would keep

I prefer a fixture-friendly acceptance test over a one-off engineering ritual. Anything that needs a probe point should have an accessible point or a factory diagnostic. Anything that relies on component identity should appear in the BOM/revision record. Anything that can regress in firmware should have a boot or factory log marker that is cheap enough to retain.

For this case the acceptance target is derived from the retained result: **The project used staged approval language to keep progress moving without erasing open engineering risks.** The test should prove that result directly rather than infer it from a neighboring signal.

## What this changes before PCB release

The lesson is not only about debugging the current EVT. It changes the release package. **Milestone names only help when their acceptance scope is explicit.**

For a board revision, I want the schematic revision, BOM identity, power-tree assumptions, pin map, factory/recovery interfaces and firmware hardware contract to move together. If one changes, the others should either change or explicitly state why they do not. This is especially important around programmable parts such as the PMIC and around signals whose semantics are created jointly by analog routing and software mapping.

I also want unresolved questions to remain visible. “Works on EVT” should not silently close an electrical-margin question, a tactile-control mismatch or an acoustic uncertainty. A production decision needs evidence appropriate to the risk. That may be a reset-time voltage analysis, a fixture measurement, a component supplier confirmation, an enclosed-device acoustic test or a repeated assembly trial.

The factory benefits from the same clarity. A deterministic test path reduces rework and makes a failed unit diagnosable instead of merely rejected.

## What I would change on the next board

I would make more of these boundaries explicit before layout. Each programmable power rail would have a table with voltage, owner, default state and test point. Boot-sensitive GPIOs would be reviewed as a separate checklist before peripheral placement is frozen. Codec and ADC channel mapping would be documented from schematic net to DMA representation. Recovery pads would be designed with the fixture, not added after the board already existed.

For human-interface parts, I would require an exact supplier variant and physical sample whenever the requirement contains a tactile or acoustic adjective. “Detented,” “loud,” “clear,” “thin,” “clicky” and “stable” cannot be accepted from a symbol or generic family datasheet alone.

For **EVT Approval Is Not Mass-Production Approval**, I would carry forward the mechanism directly: EVT validates architecture and exposes defects; DVT and PVT answer later questions about design verification and production repeatability. That turns this incident into a design-review question instead of another bring-up surprise.

## The rule I kept

**Milestone names only help when their acceptance scope is explicit.**

The retained result from this case was: The project used staged approval language to keep progress moving without erasing open engineering risks.

That is how I now approach PCB bring-up. I do not ask firmware to compensate for an unmeasured electrical problem, and I do not ask hardware engineers to redesign a circuit because a software label looked wrong. I locate the boundary, choose an observation point that can actually see it, reconcile the authoritative artifacts, and only then change the layer that owns the failure.

The process feels slower than immediately editing code. Across multiple board revisions it is much faster, because every confirmed boundary becomes reusable evidence for the next failure.
