---
title: A Tinny Speaker Is Not Automatically an ES8311 Problem
url: /posts/pcb-bringup-tinny-speaker-not-es8311-problem.html
date: '2026-09-15'
read_time: 9
excerpt: Field feedback described the EVT speaker as very tinny even though the digital
  voice path and codec communication were functioning.
topic: pcb-bringup-hardware
tags:
- esp32-s3
- pcb-bring-up
- hardware
draft: false
featured: false
language: en
eyebrow: 'PCB Bring-Up: Audio Hardware Boundaries · deep-dive'
outputs:
- url: /posts/pcb-bringup-tinny-speaker-not-es8311-problem.html
  template: cms/templates/posts/posts--pcb-bringup-tinny-speaker-not-es8311-problem.tpl
  source: cms/templates/posts/posts--pcb-bringup-tinny-speaker-not-es8311-problem.json
---

# A Tinny Speaker Is Not Automatically an ES8311 Problem

I learned this boundary the hard way: Field feedback described the EVT speaker as very tinny even though the digital voice path and codec communication were functioning.

The board context for this series is LOUP's Minewing V1.6 ESP32-S3 hardware: ESP32-S3 N16R8-class memory configuration, ES8311 playback, ES7210 capture, AXP2101 power management, e-paper display, physical controls and factory/recovery interfaces. I use those identifiers only where they help explain the engineering boundary; the larger lesson is about how firmware, schematic and physical assembly have to agree.

The evidence for this case was specific: **The hardware brief required speaker, microphone, grille, cavity, PCB placement, enclosure and firmware audio path to be designed as one system; later audio investigation stated there was no evidence yet proving ES8311, speaker, amplifier or enclosure defective in isolation.** I treat that as evidence from this board/revision and investigation, not as a universal statement about every ESP32-S3 design.

The result I retained was equally narrow: **The issue was framed as an electro-acoustic root-cause problem requiring reference hardware/measurements rather than a default codec blame.**

## How I framed the problem

This was a good reminder that bring-up is mostly hypothesis control. I started from Field feedback described the EVT speaker as very tinny even though the digital voice path and codec communication were functioning. and demanded an observation that could distinguish competing causes. That observation was The hardware brief required speaker, microphone, grille, cavity, PCB placement, enclosure and firmware audio path to be designed as one system; later audio investigation stated there was no evidence yet proving ES8311, speaker, amplifier or enclosure defective in isolation. It fit the mechanism because Perceived frequency response depends on DAC configuration, amplifier headroom, driver response, cavity volume, vents, sealing and mechanical mounting. and ruled out treating Adding EQ or changing sample-rate code before comparing a known electrical signal through the physical speaker path. as an accepted diagnosis. The retained result was The issue was framed as an electro-acoustic root-cause problem requiring reference hardware/measurements rather than a default codec blame.

Audio hardware sits across several domains at once. Digital I2S can be correct while analog gain is wrong. The ADC can answer over I2C while its physical reference channel is misinterpreted. A speaker can reproduce every sample and still sound thin because the amplifier, driver and enclosure do not support the expected acoustic response. The useful unit of debugging is therefore the complete signal path, not the codec part number.

The practical rule that came out of the case was: **Timbre problems cross the digital/analog/mechanical boundary; measure each boundary before compensating in DSP.** I prefer a rule like that over a one-off patch because it changes the next bring-up decision before another board is modified.

## Evidence matrix

| Question | Answer |
| --- | --- |
| Observed problem | Field feedback described the EVT speaker as very tinny even though the digital voice path and codec communication were functioning. |
| Strongest evidence | The hardware brief required speaker, microphone, grille, cavity, PCB placement, enclosure and firmware audio path to be designed as one system; later audio investigation stated there was no evidence yet proving ES8311, speaker, amplifier or enclosure defective in isolation. |
| Mechanism | Perceived frequency response depends on DAC configuration, amplifier headroom, driver response, cavity volume, vents, sealing and mechanical mounting. |
| Rejected shortcut | Adding EQ or changing sample-rate code before comparing a known electrical signal through the physical speaker path. |
| Retained result | The issue was framed as an electro-acoustic root-cause problem requiring reference hardware/measurements rather than a default codec blame. |
| Carry-forward rule | Timbre problems cross the digital/analog/mechanical boundary; measure each boundary before compensating in DSP. |

I keep this table because board bring-up narratives become unreliable very quickly. A working prototype encourages retrospective certainty: once the device boots, it is easy to rewrite every earlier guess as if it had been obvious. The matrix preserves the difference between what the board actually demonstrated and what I merely considered plausible.

## The boundary I wanted to prove

```
PCM -> ES8311 -> amplifier -> speaker -> enclosure/room
                              ^             |
                              |             v
                    electrical ref       microphones
                              \----------> ES7210 -> DMA/DSP
```

For this layer I wanted at least these checks before changing the design:

- codec presence and clocks
- physical channel/reference routing
- analog enable/power path
- known electrical stimulus or capture
- acoustic result after digital path is proven

The important part is ordering. I do not start with the last item just because firmware is the easiest thing for me to edit. If the rail is absent, a driver rewrite is irrelevant. If the exact part differs from the assumed part, a timing tweak may only hide the mismatch. If the physical channel is wrong, the DSP can be perfectly stable while processing the wrong signal.

For this case, **Perceived frequency response depends on DAC configuration, amplifier headroom, driver response, cavity volume, vents, sealing and mechanical mounting.** That mechanism defines which measurement belongs before the patch and which measurement should change afterward.

## What firmware can prove—and what it cannot

Firmware can prove that it configured a peripheral, observed an I2C ACK, selected a pin mux, received DMA data, read a status bit or saw a button transition. Those are useful facts. They are not substitutes for physical measurements when the disputed state exists outside the MCU.

For **A Tinny Speaker Is Not Automatically an ES8311 Problem**, the relevant distinction is that Perceived frequency response depends on DAC configuration, amplifier headroom, driver response, cavity volume, vents, sealing and mechanical mounting. A log can expose the software side of that relationship, but the electrical/mechanical side still needs the appropriate observation point.

This matters most when a diagnostic success is weaker than the product claim. An I2C scan cannot prove microphone quality. A BUSY transition cannot prove display alignment or long-term FPC reliability. A GPIO write cannot prove the amplifier enable pin actually changed if an expander or transistor sits between them. A factory programming command cannot prove traceability unless the result is tied to the unit identity.

I therefore write two columns in bring-up notes: “software evidence” and “physical evidence.” A fix is stronger when both point at the same mechanism.

## Investigation method

My acceptance condition is written before the patch. That makes it harder to move the goalposts after a build boots. The expected physical observation, firmware observation and user-visible behavior should line up. If only one layer improves, the change is a lead rather than an accepted fix.

The shortcut I deliberately avoided here was **Adding EQ or changing sample-rate code before comparing a known electrical signal through the physical speaker path.** That shortcut is attractive because it converts a cross-disciplinary problem into something one person can edit immediately. It is also how firmware becomes a compensation layer for an electrical problem that nobody has actually measured.

## Acceptance test I would keep

I also keep recovery in the acceptance path. A test firmware that can only be installed on a perfectly working unit is insufficient for manufacturing. The debug/reflash interface must be testable under the failure modes that make it necessary: bad app image, broken provisioning, failed normal boot or an incomplete factory programming step.

For this case the acceptance target is derived from the retained result: **The issue was framed as an electro-acoustic root-cause problem requiring reference hardware/measurements rather than a default codec blame.** The test should prove that result directly rather than infer it from a neighboring signal.

## What this changes before PCB release

The lesson is not only about debugging the current EVT. It changes the release package. **Timbre problems cross the digital/analog/mechanical boundary; measure each boundary before compensating in DSP.**

For a board revision, I want the schematic revision, BOM identity, power-tree assumptions, pin map, factory/recovery interfaces and firmware hardware contract to move together. If one changes, the others should either change or explicitly state why they do not. This is especially important around programmable parts such as the PMIC and around signals whose semantics are created jointly by analog routing and software mapping.

I also want unresolved questions to remain visible. “Works on EVT” should not silently close an electrical-margin question, a tactile-control mismatch or an acoustic uncertainty. A production decision needs evidence appropriate to the risk. That may be a reset-time voltage analysis, a fixture measurement, a component supplier confirmation, an enclosed-device acoustic test or a repeated assembly trial.

The factory benefits from the same clarity. A deterministic test path reduces rework and makes a failed unit diagnosable instead of merely rejected.

## What I would change on the next board

I would make more of these boundaries explicit before layout. Each programmable power rail would have a table with voltage, owner, default state and test point. Boot-sensitive GPIOs would be reviewed as a separate checklist before peripheral placement is frozen. Codec and ADC channel mapping would be documented from schematic net to DMA representation. Recovery pads would be designed with the fixture, not added after the board already existed.

For human-interface parts, I would require an exact supplier variant and physical sample whenever the requirement contains a tactile or acoustic adjective. “Detented,” “loud,” “clear,” “thin,” “clicky” and “stable” cannot be accepted from a symbol or generic family datasheet alone.

For **A Tinny Speaker Is Not Automatically an ES8311 Problem**, I would carry forward the mechanism directly: Perceived frequency response depends on DAC configuration, amplifier headroom, driver response, cavity volume, vents, sealing and mechanical mounting. That turns this incident into a design-review question instead of another bring-up surprise.

## The rule I kept

**Timbre problems cross the digital/analog/mechanical boundary; measure each boundary before compensating in DSP.**

The retained result from this case was: The issue was framed as an electro-acoustic root-cause problem requiring reference hardware/measurements rather than a default codec blame.

That is how I now approach PCB bring-up. I do not ask firmware to compensate for an unmeasured electrical problem, and I do not ask hardware engineers to redesign a circuit because a software label looked wrong. I locate the boundary, choose an observation point that can actually see it, reconcile the authoritative artifacts, and only then change the layer that owns the failure.

The process feels slower than immediately editing code. Across multiple board revisions it is much faster, because every confirmed boundary becomes reusable evidence for the next failure.
