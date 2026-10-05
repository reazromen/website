---
title: GDEY029T71H vs GDEY029T94 Was Not a Cosmetic Part-Number Detail
url: /posts/pcb-bringup-gdey029t71h-vs-t94-not-cosmetic.html
date: '2026-10-01'
read_time: 9
excerpt: The display firmware could be perfectly written for the wrong panel if the
  exact part number was not reconciled with the schematic.
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
- url: /posts/pcb-bringup-gdey029t71h-vs-t94-not-cosmetic.html
  template: cms/templates/posts/posts--pcb-bringup-gdey029t71h-vs-t94-not-cosmetic.tpl
  source: cms/templates/posts/posts--pcb-bringup-gdey029t71h-vs-t94-not-cosmetic.json
---

# GDEY029T71H vs GDEY029T94 Was Not a Cosmetic Part-Number Detail

I learned this boundary the hard way: The display firmware could be perfectly written for the wrong panel if the exact part number was not reconciled with the schematic.

The board context for this series is LOUP's Minewing V1.6 ESP32-S3 hardware: ESP32-S3 N16R8-class memory configuration, ES8311 playback, ES7210 capture, AXP2101 power management, e-paper display, physical controls and factory/recovery interfaces. I use those identifiers only where they help explain the engineering boundary; the larger lesson is about how firmware, schematic and physical assembly have to agree.

The evidence for this case was specific: **Factory documentation explicitly confirmed GDEY029T71H, SSD1685 and 168x384 visible pixels, rejected GDEY029T94, and required the corresponding source shift and refresh sequence.** I treat that as evidence from this board/revision and investigation, not as a universal statement about every ESP32-S3 design.

The result I retained was equally narrow: **The exact panel/controller pair became a hardware contract and factory gate.**

## How I framed the problem

I treated the issue as a source-of-truth conflict. The symptom was The display firmware could be perfectly written for the wrong panel if the exact part number was not reconciled with the schematic. The strongest evidence was Factory documentation explicitly confirmed GDEY029T71H, SSD1685 and 168x384 visible pixels, rejected GDEY029T94, and required the corresponding source shift and refresh sequence. The mechanism was Display controller, panel geometry and source mapping determine command sequence and framebuffer interpretation; similar product names do not imply compatible initialization. That made the tempting alternative—Treating two 2.9-inch e-paper modules as interchangeable because their physical size is similar.—something I could test instead of a story I had to believe. The retained result was The exact panel/controller pair became a hardware contract and factory gate.

Human-interface hardware creates another kind of boundary problem. A display is not “working” merely because SPI toggles, and a rotary encoder is not accepted merely because firmware counts pulses. The physical part, power rail, connector, mechanism, firmware driver and factory fixture all participate. Recovery interfaces matter most when normal interfaces are unavailable, which is exactly why they are easy to undervalue during a successful prototype demo.

The practical rule that came out of the case was: **Display drivers should bind to verified BOM identity, not a family nickname.** I prefer a rule like that over a one-off patch because it changes the next bring-up decision before another board is modified.

## Evidence matrix

| Question | Answer |
| --- | --- |
| Observed problem | The display firmware could be perfectly written for the wrong panel if the exact part number was not reconciled with the schematic. |
| Strongest evidence | Factory documentation explicitly confirmed GDEY029T71H, SSD1685 and 168x384 visible pixels, rejected GDEY029T94, and required the corresponding source shift and refresh sequence. |
| Mechanism | Display controller, panel geometry and source mapping determine command sequence and framebuffer interpretation; similar product names do not imply compatible initialization. |
| Rejected shortcut | Treating two 2.9-inch e-paper modules as interchangeable because their physical size is similar. |
| Retained result | The exact panel/controller pair became a hardware contract and factory gate. |
| Carry-forward rule | Display drivers should bind to verified BOM identity, not a family nickname. |

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

For this case, **Display controller, panel geometry and source mapping determine command sequence and framebuffer interpretation; similar product names do not imply compatible initialization.** That mechanism defines which measurement belongs before the patch and which measurement should change afterward.

## What firmware can prove—and what it cannot

Firmware can prove that it configured a peripheral, observed an I2C ACK, selected a pin mux, received DMA data, read a status bit or saw a button transition. Those are useful facts. They are not substitutes for physical measurements when the disputed state exists outside the MCU.

For **GDEY029T71H vs GDEY029T94 Was Not a Cosmetic Part-Number Detail**, the relevant distinction is that Display controller, panel geometry and source mapping determine command sequence and framebuffer interpretation; similar product names do not imply compatible initialization. A log can expose the software side of that relationship, but the electrical/mechanical side still needs the appropriate observation point.

This matters most when a diagnostic success is weaker than the product claim. An I2C scan cannot prove microphone quality. A BUSY transition cannot prove display alignment or long-term FPC reliability. A GPIO write cannot prove the amplifier enable pin actually changed if an expander or transistor sits between them. A factory programming command cannot prove traceability unless the result is tied to the unit identity.

I therefore write two columns in bring-up notes: “software evidence” and “physical evidence.” A fix is stronger when both point at the same mechanism.

## Investigation method

My investigation sequence is intentionally boring: freeze the board revision, record the exact artifact versions, inspect the electrical path, instrument the nearest software boundary, then change one variable. On hardware problems, “boring” is useful because every uncontrolled substitution—a different speaker, FPC, battery state, USB supply or firmware branch—creates another possible explanation.

The shortcut I deliberately avoided here was **Treating two 2.9-inch e-paper modules as interchangeable because their physical size is similar.** That shortcut is attractive because it converts a cross-disciplinary problem into something one person can edit immediately. It is also how firmware becomes a compensation layer for an electrical problem that nobody has actually measured.

## Acceptance test I would keep

The acceptance test should recreate the exact boundary that failed. I want a precondition, a stimulus, a measurable physical/software response and a pass/fail threshold. If the issue is power, test battery and USB transitions. If it is display, prove the rail, connector and render path. If it is audio routing, inject or capture a known signal. If it is a control, verify both electrical pulses and physical feel.

For this case the acceptance target is derived from the retained result: **The exact panel/controller pair became a hardware contract and factory gate.** The test should prove that result directly rather than infer it from a neighboring signal.

## What this changes before PCB release

The lesson is not only about debugging the current EVT. It changes the release package. **Display drivers should bind to verified BOM identity, not a family nickname.**

For a board revision, I want the schematic revision, BOM identity, power-tree assumptions, pin map, factory/recovery interfaces and firmware hardware contract to move together. If one changes, the others should either change or explicitly state why they do not. This is especially important around programmable parts such as the PMIC and around signals whose semantics are created jointly by analog routing and software mapping.

I also want unresolved questions to remain visible. “Works on EVT” should not silently close an electrical-margin question, a tactile-control mismatch or an acoustic uncertainty. A production decision needs evidence appropriate to the risk. That may be a reset-time voltage analysis, a fixture measurement, a component supplier confirmation, an enclosed-device acoustic test or a repeated assembly trial.

The factory benefits from the same clarity. A deterministic test path reduces rework and makes a failed unit diagnosable instead of merely rejected.

## What I would change on the next board

I would make more of these boundaries explicit before layout. Each programmable power rail would have a table with voltage, owner, default state and test point. Boot-sensitive GPIOs would be reviewed as a separate checklist before peripheral placement is frozen. Codec and ADC channel mapping would be documented from schematic net to DMA representation. Recovery pads would be designed with the fixture, not added after the board already existed.

For human-interface parts, I would require an exact supplier variant and physical sample whenever the requirement contains a tactile or acoustic adjective. “Detented,” “loud,” “clear,” “thin,” “clicky” and “stable” cannot be accepted from a symbol or generic family datasheet alone.

For **GDEY029T71H vs GDEY029T94 Was Not a Cosmetic Part-Number Detail**, I would carry forward the mechanism directly: Display controller, panel geometry and source mapping determine command sequence and framebuffer interpretation; similar product names do not imply compatible initialization. That turns this incident into a design-review question instead of another bring-up surprise.

## The rule I kept

**Display drivers should bind to verified BOM identity, not a family nickname.**

The retained result from this case was: The exact panel/controller pair became a hardware contract and factory gate.

That is how I now approach PCB bring-up. I do not ask firmware to compensate for an unmeasured electrical problem, and I do not ask hardware engineers to redesign a circuit because a software label looked wrong. I locate the boundary, choose an observation point that can actually see it, reconcile the authoritative artifacts, and only then change the layer that owns the failure.

The process feels slower than immediately editing code. Across multiple board revisions it is much faster, because every confirmed boundary becomes reusable evidence for the next failure.
