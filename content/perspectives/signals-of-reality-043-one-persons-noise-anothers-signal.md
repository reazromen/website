---
title: One Person’s Noise Is Another Person’s Signal
url: /posts/signals-of-reality-043-one-persons-noise-anothers-signal.html
date: '2026-04-07'
read_time: 6
excerpt: The boundary between signal and noise depends on the receiver and task. Changing the question can turn interference, residuals, or metadata into the object of study.
topic: signals-and-signaling
tags:
- signals-and-signaling
- noise-suppression
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Signal / Noise'
editorial_batch: signals-of-reality-200
---

A radio engineer points an antenna toward a transmitter and calls everything else interference. An astronomer using another instrument may be interested in exactly the radiation the engineer wants removed.

Nothing about the electromagnetic field changed between those descriptions.

The question changed.

This is one of the simplest ways to understand the signal/noise distinction. A signal is not automatically the strongest component, the cleanest component, or the component produced intentionally. It is the variation relevant to a receiver or inquiry.

Noise is what competes with that relevance.

## A receiver creates a foreground

Tune a receiver to a narrow band and an enormous range of electromagnetic activity becomes background. Select one sensor channel from a machine and dozens of others disappear from the current plot. Query one user's requests from a distributed trace and the rest of the traffic becomes context.

Selection creates a foreground.

That is unavoidable. No finite analysis can treat every variable as equally important at once.

The mistake begins when we forget that foregrounding happened and start treating the discarded background as if it had no structure.

An adjacent radio transmission remains a structured message to its intended receiver. A neighboring service's logs remain meaningful to another investigation. The background is often somebody else's foreground.

## Interference can carry information about the environment

Suppose an accelerometer is installed on a pump to monitor bearing vibration. A periodic component from a nearby motor leaks into the measurement.

For the pump-maintenance task, the motor component is interference. Filtering it may improve sensitivity to bearing features.

But if the same data is later used to investigate facility-wide vibration coupling, the motor component becomes valuable evidence. Deleting it permanently during acquisition would have destroyed information useful to the second question.

This is one reason raw data and processing provenance matter. A filter can be correct for one analysis while making a future analysis impossible.

The operation is not wrong. Its scope must be remembered.

## Biological systems also reclassify variation

A sound in a crowded room may be background until someone says your name. The acoustic energy did not become a different physical substance. Attention and learned relevance changed how the pattern was processed.

Similar context dependence appears throughout biology. A molecule can function as a signal in one pathway and have a different role elsewhere. A neural response can be informative about one variable while carrying little information about another.

This does not mean biological meaning is arbitrary. Receptors, pathways, physiology, and behavior impose strong constraints. The point is that relevance belongs to relationships, not isolated particles.

## Security reverses the perspective

Network defenders provide a vivid example.

Ordinary application traffic is the desired activity for users. To a security analyst, timing, failed requests, unusual source patterns, and protocol deviations may become signals about system behavior. Fields that the application developer considered uninteresting metadata can become central evidence.

The reverse also occurs. A security tool may generate so many alerts that the alerts themselves become noise for an operator. The system technically detects many conditions but fails operationally because the relevant events are buried.

Signal quality is therefore not just detection. It includes the receiver's ability to distinguish what matters.

## Astronomy makes the reversal dramatic

Radio astronomy often operates in bands where human technology also emits. For a telescope measuring cosmic sources, terrestrial radio-frequency interference can dominate observations. Engineers invest heavily in shielding, site selection, scheduling, and filtering.

From the perspective of the communication system producing that interference, however, the emission is the intended signal.

Both descriptions are correct.

The conflict is physical and institutional, not semantic confusion. Two receivers are competing over the same electromagnetic environment with different goals.

This is why spectrum management exists: the fact that signal and noise are relative does not remove practical conflicts. It makes coordination necessary.

## The lesson is methodological

When an analyst says, "We filtered out the noise," the next question should be: according to what criterion?

Was the removed component outside a known frequency band? Was it inconsistent with the instrument model? Was it a documented artifact? Was it simply inconvenient for the expected hypothesis?

The first three can be justified with evidence. The last one should make us cautious.

A well-designed analysis makes the classification inspectable. It records the target, the filter, the assumptions, and ideally preserves the source data.

That practice allows another investigator to ask a different question later.

One person's noise can be another person's signal because relevance is relational.

But that relativity is not an excuse for careless analysis. It is a reason to document exactly how the foreground was chosen.
