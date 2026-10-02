---
title: STD 2x32 Beat My “More Obvious” TDM 4x16 Experiment
url: /posts/pcb-bringup-std2x32-vs-tdm4x16.html
date: '2026-09-15'
read_time: 9
excerpt: Seeing four 16-bit-looking positions in memory made true four-slot TDM seem
  like the natural host configuration.
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
- url: /posts/pcb-bringup-std2x32-vs-tdm4x16.html
  template: cms/templates/posts/posts--pcb-bringup-std2x32-vs-tdm4x16.tpl
  source: cms/templates/posts/posts--pcb-bringup-std2x32-vs-tdm4x16.json
---

# STD 2x32 Beat My “More Obvious” TDM 4x16 Experiment

One of the fastest ways to waste bring-up time is to debug the wrong representation of the hardware. In this case, Seeing four 16-bit-looking positions in memory made true four-slot TDM seem like the natural host configuration.

The board context for this series is LOUP's Minewing V1.6 ESP32-S3 hardware: ESP32-S3 N16R8-class memory configuration, ES8311 playback, ES7210 capture, AXP2101 power management, e-paper display, physical controls and factory/recovery interfaces. I use those identifiers only where they help explain the engineering boundary; the larger lesson is about how firmware, schematic and physical assembly have to agree.

The evidence for this case was specific: **The TDM4x16 experiment changed which halfwords looked active but was explicitly rejected; the known-good architecture kept ESP32 host RX/TX in STD stereo 2x32 at 16 kHz while the ES7210 handled its internal TDM behavior.** I treat that as evidence from this board/revision and investigation, not as a universal statement about every ESP32-S3 design.

The result I retained was equally narrow: **The experiment was reverted and used only as diagnostic evidence about packing.**

## How I framed the problem

This case became a boundary test. On one side was the electrical/mechanical design; on the other was firmware or factory logic. The failure was Seeing four 16-bit-looking positions in memory made true four-slot TDM seem like the natural host configuration. I used The TDM4x16 experiment changed which halfwords looked active but was explicitly rejected; the known-good architecture kept ESP32 host RX/TX in STD stereo 2x32 at 16 kHz while the ES7210 handled its internal TDM behavior. to decide which side of the boundary needed the next experiment. The reason that evidence mattered is Peripheral wire format, codec internal channeling and host DMA representation are separate layers; making the host format look conceptually neat can break a proven compatibility arrangement. The conclusion was The experiment was reverted and used only as diagnostic evidence about packing.

Audio hardware sits across several domains at once. Digital I2S can be correct while analog gain is wrong. The ADC can answer over I2C while its physical reference channel is misinterpreted. A speaker can reproduce every sample and still sound thin because the amplifier, driver and enclosure do not support the expected acoustic response. The useful unit of debugging is therefore the complete signal path, not the codec part number.

The practical rule that came out of the case was: **Do not replace a proven transport merely because an alternative maps more cleanly to your mental model.** I prefer a rule like that over a one-off patch because it changes the next bring-up decision before another board is modified.

## Evidence matrix

| Question | Answer |
| --- | --- |
| Observed problem | Seeing four 16-bit-looking positions in memory made true four-slot TDM seem like the natural host configuration. |
| Strongest evidence | The TDM4x16 experiment changed which halfwords looked active but was explicitly rejected; the known-good architecture kept ESP32 host RX/TX in STD stereo 2x32 at 16 kHz while the ES7210 handled its internal TDM behavior. |
| Mechanism | Peripheral wire format, codec internal channeling and host DMA representation are separate layers; making the host format look conceptually neat can break a proven compatibility arrangement. |
| Rejected shortcut | Redesigning the I2S mode to match the number of conceptual ADC channels. |
| Retained result | The experiment was reverted and used only as diagnostic evidence about packing. |
| Carry-forward rule | Do not replace a proven transport merely because an alternative maps more cleanly to your mental model. |

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

For this case, **Peripheral wire format, codec internal channeling and host DMA representation are separate layers; making the host format look conceptually neat can break a proven compatibility arrangement.** That mechanism defines which measurement belongs before the patch and which measurement should change afterward.

## What firmware can prove—and what it cannot

Firmware can prove that it configured a peripheral, observed an I2C ACK, selected a pin mux, received DMA data, read a status bit or saw a button transition. Those are useful facts. They are not substitutes for physical measurements when the disputed state exists outside the MCU.

For **STD 2x32 Beat My “More Obvious” TDM 4x16 Experiment**, the relevant distinction is that Peripheral wire format, codec internal channeling and host DMA representation are separate layers; making the host format look conceptually neat can break a proven compatibility arrangement. A log can expose the software side of that relationship, but the electrical/mechanical side still needs the appropriate observation point.

This matters most when a diagnostic success is weaker than the product claim. An I2C scan cannot prove microphone quality. A BUSY transition cannot prove display alignment or long-term FPC reliability. A GPIO write cannot prove the amplifier enable pin actually changed if an expander or transistor sits between them. A factory programming command cannot prove traceability unless the result is tied to the unit identity.

I therefore write two columns in bring-up notes: “software evidence” and “physical evidence.” A fix is stronger when both point at the same mechanism.

## Investigation method

Before touching source, I ask what an oscilloscope, multimeter, logic trace, raw sample probe or fixture observation could tell me that a log cannot. Firmware logs are excellent for software state and often weak for power, connector and analog questions. Conversely, a scope can show a clock but cannot prove the application assigned the resulting DMA words to the correct semantic channel.

The shortcut I deliberately avoided here was **Redesigning the I2S mode to match the number of conceptual ADC channels.** That shortcut is attractive because it converts a cross-disciplinary problem into something one person can edit immediately. It is also how firmware becomes a compensation layer for an electrical problem that nobody has actually measured.

## Acceptance test I would keep

The pass condition must also survive repetition. One successful boot or one clear call is evidence of possibility, not production margin. For hardware-facing changes I repeat the test across power cycles and, where relevant, across multiple units or assembly states. The goal is to detect variation before the factory turns it into yield loss.

For this case the acceptance target is derived from the retained result: **The experiment was reverted and used only as diagnostic evidence about packing.** The test should prove that result directly rather than infer it from a neighboring signal.

## What this changes before PCB release

The lesson is not only about debugging the current EVT. It changes the release package. **Do not replace a proven transport merely because an alternative maps more cleanly to your mental model.**

For a board revision, I want the schematic revision, BOM identity, power-tree assumptions, pin map, factory/recovery interfaces and firmware hardware contract to move together. If one changes, the others should either change or explicitly state why they do not. This is especially important around programmable parts such as the PMIC and around signals whose semantics are created jointly by analog routing and software mapping.

I also want unresolved questions to remain visible. “Works on EVT” should not silently close an electrical-margin question, a tactile-control mismatch or an acoustic uncertainty. A production decision needs evidence appropriate to the risk. That may be a reset-time voltage analysis, a fixture measurement, a component supplier confirmation, an enclosed-device acoustic test or a repeated assembly trial.

The factory benefits from the same clarity. A deterministic test path reduces rework and makes a failed unit diagnosable instead of merely rejected.

## What I would change on the next board

I would make more of these boundaries explicit before layout. Each programmable power rail would have a table with voltage, owner, default state and test point. Boot-sensitive GPIOs would be reviewed as a separate checklist before peripheral placement is frozen. Codec and ADC channel mapping would be documented from schematic net to DMA representation. Recovery pads would be designed with the fixture, not added after the board already existed.

For human-interface parts, I would require an exact supplier variant and physical sample whenever the requirement contains a tactile or acoustic adjective. “Detented,” “loud,” “clear,” “thin,” “clicky” and “stable” cannot be accepted from a symbol or generic family datasheet alone.

For **STD 2x32 Beat My “More Obvious” TDM 4x16 Experiment**, I would carry forward the mechanism directly: Peripheral wire format, codec internal channeling and host DMA representation are separate layers; making the host format look conceptually neat can break a proven compatibility arrangement. That turns this incident into a design-review question instead of another bring-up surprise.

## The rule I kept

**Do not replace a proven transport merely because an alternative maps more cleanly to your mental model.**

The retained result from this case was: The experiment was reverted and used only as diagnostic evidence about packing.

That is how I now approach PCB bring-up. I do not ask firmware to compensate for an unmeasured electrical problem, and I do not ask hardware engineers to redesign a circuit because a software label looked wrong. I locate the boundary, choose an observation point that can actually see it, reconcile the authoritative artifacts, and only then change the layer that owns the failure.

The process feels slower than immediately editing code. Across multiple board revisions it is much faster, because every confirmed boundary becomes reusable evidence for the next failure.
