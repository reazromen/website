---
title: Why Perfect Models Are Useless
url: /posts/signals-of-reality-014-perfect-models-useless.html
date: '2026-06-29'
read_time: 6
excerpt: A model gains usefulness by throwing information away. The difficult part is deciding what it can safely forget.
topic: philosophy-science
tags:
- models
- measurement
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Reality Is Not What You See'
editorial_batch: signals-of-reality-200
---

A model of a city that contains every grain of dust, every moving molecule, every private conversation, every electric field and the precise position of every person would be astonishing.

It would also be unusable.

To answer "How do I get to the railway station?" we do not need a second city.

We need a map.

This is the productive violence of modeling: **a model must discard information**.

The point is easy to miss because scientific and engineering culture often rewards higher resolution. More samples, more parameters, more pixels, more telemetry. Sometimes those improvements reveal structure that coarse measurements missed. But resolution and usefulness are not the same thing. A representation becomes useful when its detail is matched to a question.

Jorge Luis Borges made this absurdly vivid in his tiny story *On Exactitude in Science*. Cartographers create a map of an empire at the scale of the empire itself. The joke works because a one-to-one map defeats the purpose of mapping. It has preserved so much of the territory that it no longer offers the compression that makes a map navigable.

Borges was writing literature, not a theorem of model selection. Still, the image captures something engineers encounter constantly.

### Compression is not a defect

A network diagram may represent a router as one rectangle. The actual router contains processors, queues, firmware, clocks, memory, power rails and millions of electrical events. For routing architecture, the rectangle may be exactly the right abstraction.

Then a packet-loss incident occurs inside a queue, and the rectangle becomes too coarse.

We zoom in.

The lesson is not that the first diagram was wrong. It was built for another question.

Models work by preserving some relations while suppressing others. A subway diagram may distort geographical distance while preserving station order and interchange structure. A thermodynamic model may describe pressure and temperature without tracking the trajectory of every molecule. A population model may use averages that are meaningless for predicting one person's exact outcome but informative about group-level behavior.

Scientific explanation depends on this ability to move between scales.

If every explanation of temperature required listing the quantum state of every particle, thermodynamics would cease to be an explanation humans could use.

### The perfect digital twin problem

The phrase digital twin can tempt us toward a modern version of Borges's empire.

Imagine trying to create a perfect digital twin of a factory. Start with machine positions and operating states. Add vibration. Add temperatures. Add tool wear. Add material properties. Add workers' movements. Add humidity gradients. Add every network packet. Add microscopic cracks in every bearing. Add the state of every transistor in every controller.

At some point the twin becomes at least as difficult to observe and compute as the factory itself.

Real digital twins therefore make choices. They model the variables relevant to defined decisions: maintenance, throughput, energy use, safety or some combination. Their power comes from **selective fidelity**.

A model can be detailed in one dimension and crude in another. A high-fidelity aerodynamic simulation may treat a pilot as a boundary condition. A hospital scheduling model can represent operating rooms precisely and human fatigue poorly. "High fidelity" only means something after we ask: fidelity to which properties?

### Error is sometimes engineered on purpose

Numerical models often simplify equations or discretize continuous systems. Those approximations introduce errors that can be estimated and controlled.

This sounds inferior to an exact calculation until cost enters.

A weather forecast that arrives next week can be mathematically impressive and operationally useless. A real-time control system may choose a simpler model because a slower but more exact calculation cannot meet the timing constraint. In embedded engineering, an approximation that fits memory and power budgets can be more valuable than an algorithm that is theoretically superior and impossible to run on the device.

The model is part of a system with constraints.

The goal is rarely "contain maximum truth." It is closer to: **preserve enough structure to make the required inference at an acceptable cost and error**.

### When simplification becomes deception

This argument could be misused.

If all models simplify, someone might excuse a misleading model by saying, "Of course it leaves things out."

But not all omissions are equally harmless.

A road map that omits the color of every building is usually fine for navigation. A flood-evacuation map that omits a washed-out bridge is not. The difference comes from the decision the map is supposed to support.

Good modeling therefore requires two statements: what is included, and what claim is the model intended to support.

Validation tests the relationship between them.

A climate model, for example, is not assessed by asking whether it contains an atom-for-atom copy of Earth. Researchers compare model behavior with observations, physical constraints and known patterns at relevant scales. Different models may be useful for different spatial and temporal questions.

The word simplified is not a verdict. The important question is whether the simplification destroys the structure that matters.

### The smallest model that survives the question

There is a practical elegance in using the least complicated representation that answers the problem.

Not the crudest.

Not the most elaborate.

The least complicated one that survives the evidence and the decision.

This principle explains why a hand-drawn call-flow diagram can solve an outage that a terabyte of logs did not. The drawing may expose the one dependency the raw data obscured. It also explains why that same drawing becomes inadequate when debugging packet timing. Then we need traces, captures and clocks.

We move between maps.

A perfect model would leave us nowhere to move. It would not clarify the world; it would duplicate it.

Understanding begins when we decide what we can afford to forget—and remain willing to put the forgotten detail back when the question changes.

### Sources and reading

- Stanford Encyclopedia of Philosophy, [Models in Science](https://plato.stanford.edu/entries/models-science/).
- USGS, [Map Projections](https://pubs.usgs.gov/gip/70047422/report.pdf).
- Jorge Luis Borges, *On Exactitude in Science* (1946), used here only as a literary illustration.
