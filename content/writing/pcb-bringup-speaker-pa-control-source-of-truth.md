---
title: GPIO17 Was Not Enough to Explain the Speaker PA Control
url: /posts/pcb-bringup-speaker-pa-control-source-of-truth.html
date: '2026-09-15'
read_time: 9
excerpt: Historical board notes associated amplifier enable with GPIO17, while later
  verified board-path evidence showed the physical speaker PA controlled through TCA9555
  EXIO08 in the working implementation.
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
- url: /posts/pcb-bringup-speaker-pa-control-source-of-truth.html
  template: cms/templates/posts/posts--pcb-bringup-speaker-pa-control-source-of-truth.tpl
  source: cms/templates/posts/posts--pcb-bringup-speaker-pa-control-source-of-truth.json
---

# GPIO17 Was Not Enough to Explain the Speaker PA Control

This was not primarily a firmware problem or a hardware problem. It was an interface problem: Historical board notes associated amplifier enable with GPIO17, while later verified board-path evidence showed the physical speaker PA controlled through TCA9555 EXIO08 in the working implementation.

The board context for this series is LOUP's Minewing V1.6 ESP32-S3 hardware: ESP32-S3 N16R8-class memory configuration, ES8311 playback, ES7210 capture, AXP2101 power management, e-paper display, physical controls and factory/recovery interfaces. I use those identifiers only where they help explain the engineering boundary; the larger lesson is about how firmware, schematic and physical assembly have to agree.

The evidence for this case was specific: **The audio recovery evidence explicitly warned that GPIO\_PWR\_CTRL was not the physical PA control in the verified board path, even though older V1.6 maps listed an amp-related GPIO17.** I treat that as evidence from this board/revision and investigation, not as a universal statement about every ESP32-S3 design.

The result I retained was equally narrow: **The PA control became a source-of-truth reconciliation problem rather than a one-line GPIO patch.**

## How I framed the problem

The first plausible explanation was not the one I wanted to preserve. The observed problem was Historical board notes associated amplifier enable with GPIO17, while later verified board-path evidence showed the physical speaker PA controlled through TCA9555 EXIO08 in the working implementation. The more authoritative observation was The audio recovery evidence explicitly warned that GPIO\_PWR\_CTRL was not the physical PA control in the verified board path, even though older V1.6 maps listed an amp-related GPIO17. Once I accounted for the actual mechanism—A logical function can move through an I/O expander, transistor network or board revision while firmware names remain similar; the assembled control path is what matters.—the shortcut explanation, Toggling a remembered GPIO and concluding the amplifier hardware is defective when nothing changes., stopped being good enough. The engineering result was The PA control became a source-of-truth reconciliation problem rather than a one-line GPIO patch.

Audio hardware sits across several domains at once. Digital I2S can be correct while analog gain is wrong. The ADC can answer over I2C while its physical reference channel is misinterpreted. A speaker can reproduce every sample and still sound thin because the amplifier, driver and enclosure do not support the expected acoustic response. The useful unit of debugging is therefore the complete signal path, not the codec part number.

The practical rule that came out of the case was: **Trace enable signals from firmware API to the actual transistor/amp pin before diagnosing power or gain faults.** I prefer a rule like that over a one-off patch because it changes the next bring-up decision before another board is modified.

## Evidence matrix

| Question | Answer |
| --- | --- |
| Observed problem | Historical board notes associated amplifier enable with GPIO17, while later verified board-path evidence showed the physical speaker PA controlled through TCA9555 EXIO08 in the working implementation. |
| Strongest evidence | The audio recovery evidence explicitly warned that GPIO\_PWR\_CTRL was not the physical PA control in the verified board path, even though older V1.6 maps listed an amp-related GPIO17. |
| Mechanism | A logical function can move through an I/O expander, transistor network or board revision while firmware names remain similar; the assembled control path is what matters. |
| Rejected shortcut | Toggling a remembered GPIO and concluding the amplifier hardware is defective when nothing changes. |
| Retained result | The PA control became a source-of-truth reconciliation problem rather than a one-line GPIO patch. |
| Carry-forward rule | Trace enable signals from firmware API to the actual transistor/amp pin before diagnosing power or gain faults. |

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

For this case, **A logical function can move through an I/O expander, transistor network or board revision while firmware names remain similar; the assembled control path is what matters.** That mechanism defines which measurement belongs before the patch and which measurement should change afterward.

## Investigation method

I also record negative evidence. If a suspected GPIO toggle does not change the physical enable node, that is valuable. If changing host I2S mode makes the packing look different but breaks the known-good architecture, that experiment can still reveal representation. Failed experiments are useful when I keep their scope narrow enough to know what they disproved.

The shortcut I deliberately avoided here was **Toggling a remembered GPIO and concluding the amplifier hardware is defective when nothing changes.** That shortcut is attractive because it converts a cross-disciplinary problem into something one person can edit immediately. It is also how firmware becomes a compensation layer for an electrical problem that nobody has actually measured.

## What firmware can prove—and what it cannot

Firmware can prove that it configured a peripheral, observed an I2C ACK, selected a pin mux, received DMA data, read a status bit or saw a button transition. Those are useful facts. They are not substitutes for physical measurements when the disputed state exists outside the MCU.

For **GPIO17 Was Not Enough to Explain the Speaker PA Control**, the relevant distinction is that A logical function can move through an I/O expander, transistor network or board revision while firmware names remain similar; the assembled control path is what matters. A log can expose the software side of that relationship, but the electrical/mechanical side still needs the appropriate observation point.

This matters most when a diagnostic success is weaker than the product claim. An I2C scan cannot prove microphone quality. A BUSY transition cannot prove display alignment or long-term FPC reliability. A GPIO write cannot prove the amplifier enable pin actually changed if an expander or transistor sits between them. A factory programming command cannot prove traceability unless the result is tied to the unit identity.

I therefore write two columns in bring-up notes: “software evidence” and “physical evidence.” A fix is stronger when both point at the same mechanism.

## Acceptance test I would keep

A good acceptance test tells me where to look when it fails. “Display failed” is weak. “ALDO3 present, FPC continuity good, SPI commands issued, BUSY never released” is actionable. The same principle applies to audio, power and controls: preserve intermediate evidence instead of reducing everything to a final green/red LED.

For this case the acceptance target is derived from the retained result: **The PA control became a source-of-truth reconciliation problem rather than a one-line GPIO patch.** The test should prove that result directly rather than infer it from a neighboring signal.

## What this changes before PCB release

The lesson is not only about debugging the current EVT. It changes the release package. **Trace enable signals from firmware API to the actual transistor/amp pin before diagnosing power or gain faults.**

For a board revision, I want the schematic revision, BOM identity, power-tree assumptions, pin map, factory/recovery interfaces and firmware hardware contract to move together. If one changes, the others should either change or explicitly state why they do not. This is especially important around programmable parts such as the PMIC and around signals whose semantics are created jointly by analog routing and software mapping.

I also want unresolved questions to remain visible. “Works on EVT” should not silently close an electrical-margin question, a tactile-control mismatch or an acoustic uncertainty. A production decision needs evidence appropriate to the risk. That may be a reset-time voltage analysis, a fixture measurement, a component supplier confirmation, an enclosed-device acoustic test or a repeated assembly trial.

The factory benefits from the same clarity. A deterministic test path reduces rework and makes a failed unit diagnosable instead of merely rejected.

## What I would change on the next board

I would make more of these boundaries explicit before layout. Each programmable power rail would have a table with voltage, owner, default state and test point. Boot-sensitive GPIOs would be reviewed as a separate checklist before peripheral placement is frozen. Codec and ADC channel mapping would be documented from schematic net to DMA representation. Recovery pads would be designed with the fixture, not added after the board already existed.

For human-interface parts, I would require an exact supplier variant and physical sample whenever the requirement contains a tactile or acoustic adjective. “Detented,” “loud,” “clear,” “thin,” “clicky” and “stable” cannot be accepted from a symbol or generic family datasheet alone.

For **GPIO17 Was Not Enough to Explain the Speaker PA Control**, I would carry forward the mechanism directly: A logical function can move through an I/O expander, transistor network or board revision while firmware names remain similar; the assembled control path is what matters. That turns this incident into a design-review question instead of another bring-up surprise.

## The rule I kept

**Trace enable signals from firmware API to the actual transistor/amp pin before diagnosing power or gain faults.**

The retained result from this case was: The PA control became a source-of-truth reconciliation problem rather than a one-line GPIO patch.

That is how I now approach PCB bring-up. I do not ask firmware to compensate for an unmeasured electrical problem, and I do not ask hardware engineers to redesign a circuit because a software label looked wrong. I locate the boundary, choose an observation point that can actually see it, reconcile the authoritative artifacts, and only then change the layer that owns the failure.

The process feels slower than immediately editing code. Across multiple board revisions it is much faster, because every confirmed boundary becomes reusable evidence for the next failure.
