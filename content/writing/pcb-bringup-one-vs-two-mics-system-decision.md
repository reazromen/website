---
title: One Microphone or Two Is a System Decision
url: /posts/pcb-bringup-one-vs-two-mics-system-decision.html
date: '2021-01-13'
read_time: 9
excerpt: The microphone count could not be chosen only by firmware or only by mechanical
  design because it changes acoustics, channels, BOM, placement, assembly and test.
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
- url: /posts/pcb-bringup-one-vs-two-mics-system-decision.html
  template: cms/templates/posts/posts--pcb-bringup-one-vs-two-mics-system-decision.tpl
  source: cms/templates/posts/posts--pcb-bringup-one-vs-two-mics-system-decision.json
---

# One Microphone or Two Is a System Decision

One of the fastest ways to waste bring-up time is to debug the wrong representation of the hardware. In this case, The microphone count could not be chosen only by firmware or only by mechanical design because it changes acoustics, channels, BOM, placement, assembly and test.

The board context for this series is LOUP's Minewing V1.6 ESP32-S3 hardware: ESP32-S3 N16R8-class memory configuration, ES8311 playback, ES7210 capture, AXP2101 power management, e-paper display, physical controls and factory/recovery interfaces. I use those identifiers only where they help explain the engineering boundary; the larger lesson is about how firmware, schematic and physical assembly have to agree.

The evidence for this case was specific: **The Minewing discussion explicitly asked for a one-vs-two microphone recommendation including placement, speaker relationship, enclosure, codec channels, BOM, assembly and factory-test impact; Minewing noted dual microphones increase material and assembly/testing cost.** I treat that as evidence from this board/revision and investigation, not as a universal statement about every ESP32-S3 design.

The result I retained was equally narrow: **The requirement was reframed around clear outgoing voice and echo reduction with joint hardware/mechanical/acoustic/firmware impact.**

## How I framed the problem

I treated the issue as a source-of-truth conflict. The symptom was The microphone count could not be chosen only by firmware or only by mechanical design because it changes acoustics, channels, BOM, placement, assembly and test. The strongest evidence was The Minewing discussion explicitly asked for a one-vs-two microphone recommendation including placement, speaker relationship, enclosure, codec channels, BOM, assembly and factory-test impact; Minewing noted dual microphones increase material and assembly/testing cost. The mechanism was Microphone topology changes both the physical acoustic observation points and the software/DSP inputs, so the decision spans hardware and firmware ownership. That made the tempting alternative—Calling the requirement “ANC” and letting one discipline optimize it in isolation.—something I could test instead of a story I had to believe. The retained result was The requirement was reframed around clear outgoing voice and echo reduction with joint hardware/mechanical/acoustic/firmware impact.

The transition from EVT to production changes the engineering question. A hand-built unit can tolerate ambiguous assembly, undocumented tweaks and manual rework. Production cannot. The design has to become repeatable, testable, traceable and recoverable. That means the manufacturer and firmware team need explicit ownership while sharing a precise hardware/firmware contract and a common acceptance language.

The practical rule that came out of the case was: **Transducer count is a system architecture choice, not a BOM line item.** I prefer a rule like that over a one-off patch because it changes the next bring-up decision before another board is modified.

## Evidence matrix

| Question | Answer |
| --- | --- |
| Observed problem | The microphone count could not be chosen only by firmware or only by mechanical design because it changes acoustics, channels, BOM, placement, assembly and test. |
| Strongest evidence | The Minewing discussion explicitly asked for a one-vs-two microphone recommendation including placement, speaker relationship, enclosure, codec channels, BOM, assembly and factory-test impact; Minewing noted dual microphones increase material and assembly/testing cost. |
| Mechanism | Microphone topology changes both the physical acoustic observation points and the software/DSP inputs, so the decision spans hardware and firmware ownership. |
| Rejected shortcut | Calling the requirement “ANC” and letting one discipline optimize it in isolation. |
| Retained result | The requirement was reframed around clear outgoing voice and echo reduction with joint hardware/mechanical/acoustic/firmware impact. |
| Carry-forward rule | Transducer count is a system architecture choice, not a BOM line item. |

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

For this case, **Microphone topology changes both the physical acoustic observation points and the software/DSP inputs, so the decision spans hardware and firmware ownership.** That mechanism defines which measurement belongs before the patch and which measurement should change afterward.

## Investigation method

My investigation sequence is intentionally boring: freeze the board revision, record the exact artifact versions, inspect the electrical path, instrument the nearest software boundary, then change one variable. On hardware problems, “boring” is useful because every uncontrolled substitution—a different speaker, FPC, battery state, USB supply or firmware branch—creates another possible explanation.

The shortcut I deliberately avoided here was **Calling the requirement “ANC” and letting one discipline optimize it in isolation.** That shortcut is attractive because it converts a cross-disciplinary problem into something one person can edit immediately. It is also how firmware becomes a compensation layer for an electrical problem that nobody has actually measured.

## What firmware can prove—and what it cannot

Firmware can prove that it configured a peripheral, observed an I2C ACK, selected a pin mux, received DMA data, read a status bit or saw a button transition. Those are useful facts. They are not substitutes for physical measurements when the disputed state exists outside the MCU.

For **One Microphone or Two Is a System Decision**, the relevant distinction is that Microphone topology changes both the physical acoustic observation points and the software/DSP inputs, so the decision spans hardware and firmware ownership. A log can expose the software side of that relationship, but the electrical/mechanical side still needs the appropriate observation point.

This matters most when a diagnostic success is weaker than the product claim. An I2C scan cannot prove microphone quality. A BUSY transition cannot prove display alignment or long-term FPC reliability. A GPIO write cannot prove the amplifier enable pin actually changed if an expander or transistor sits between them. A factory programming command cannot prove traceability unless the result is tied to the unit identity.

I therefore write two columns in bring-up notes: “software evidence” and “physical evidence.” A fix is stronger when both point at the same mechanism.

## Acceptance test I would keep

The acceptance test should recreate the exact boundary that failed. I want a precondition, a stimulus, a measurable physical/software response and a pass/fail threshold. If the issue is power, test battery and USB transitions. If it is display, prove the rail, connector and render path. If it is audio routing, inject or capture a known signal. If it is a control, verify both electrical pulses and physical feel.

For this case the acceptance target is derived from the retained result: **The requirement was reframed around clear outgoing voice and echo reduction with joint hardware/mechanical/acoustic/firmware impact.** The test should prove that result directly rather than infer it from a neighboring signal.

## What this changes before PCB release

The lesson is not only about debugging the current EVT. It changes the release package. **Transducer count is a system architecture choice, not a BOM line item.**

For a board revision, I want the schematic revision, BOM identity, power-tree assumptions, pin map, factory/recovery interfaces and firmware hardware contract to move together. If one changes, the others should either change or explicitly state why they do not. This is especially important around programmable parts such as the PMIC and around signals whose semantics are created jointly by analog routing and software mapping.

I also want unresolved questions to remain visible. “Works on EVT” should not silently close an electrical-margin question, a tactile-control mismatch or an acoustic uncertainty. A production decision needs evidence appropriate to the risk. That may be a reset-time voltage analysis, a fixture measurement, a component supplier confirmation, an enclosed-device acoustic test or a repeated assembly trial.

The factory benefits from the same clarity. A deterministic test path reduces rework and makes a failed unit diagnosable instead of merely rejected.

## What I would change on the next board

I would make more of these boundaries explicit before layout. Each programmable power rail would have a table with voltage, owner, default state and test point. Boot-sensitive GPIOs would be reviewed as a separate checklist before peripheral placement is frozen. Codec and ADC channel mapping would be documented from schematic net to DMA representation. Recovery pads would be designed with the fixture, not added after the board already existed.

For human-interface parts, I would require an exact supplier variant and physical sample whenever the requirement contains a tactile or acoustic adjective. “Detented,” “loud,” “clear,” “thin,” “clicky” and “stable” cannot be accepted from a symbol or generic family datasheet alone.

For **One Microphone or Two Is a System Decision**, I would carry forward the mechanism directly: Microphone topology changes both the physical acoustic observation points and the software/DSP inputs, so the decision spans hardware and firmware ownership. That turns this incident into a design-review question instead of another bring-up surprise.

## The rule I kept

**Transducer count is a system architecture choice, not a BOM line item.**

The retained result from this case was: The requirement was reframed around clear outgoing voice and echo reduction with joint hardware/mechanical/acoustic/firmware impact.

That is how I now approach PCB bring-up. I do not ask firmware to compensate for an unmeasured electrical problem, and I do not ask hardware engineers to redesign a circuit because a software label looked wrong. I locate the boundary, choose an observation point that can actually see it, reconcile the authoritative artifacts, and only then change the layer that owns the failure.

The process feels slower than immediately editing code. Across multiple board revisions it is much faster, because every confirmed boundary becomes reusable evidence for the next failure.
