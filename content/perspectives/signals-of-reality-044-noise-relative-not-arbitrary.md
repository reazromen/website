---
title: Noise Is Relative, Not Arbitrary
url: /posts/signals-of-reality-044-noise-relative-not-arbitrary.html
date: '2026-08-08'
read_time: 6
excerpt: Calling noise task-dependent does not make the distinction subjective whim. A target, receiver, and statistical model create testable criteria for relevance.
topic: signals-and-signaling
tags:
- noise-suppression
- measurement
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Signal / Noise'
editorial_batch: signals-of-reality-200
---

If noise depends on what we care about, does that mean anything can be called noise whenever it is inconvenient?

No.

Relativity to a task is not the same as arbitrariness.

Temperature is relative to a scale, position is relative to a coordinate system, and velocity is relative to a reference frame. Those dependencies do not make the measurements meaningless. They tell us what must be specified before the statement becomes precise.

Signal and noise work the same way.

## Start with the target

Imagine a receiver designed to recover a 1 kHz test tone from a microphone. The target is explicit. Energy at 50 Hz from mains coupling, broadband microphone self-noise, and an unrelated conversation can all interfere with estimating the tone's amplitude.

For this task they are noise or interference.

Now change the task. If the investigator wants to diagnose electrical coupling, the 50 Hz component becomes the signal. If the goal is speech recognition, the test tone may become interference.

The classification follows from a declared objective.

That objective can be criticized. Perhaps the experiment was designed badly. Perhaps the supposedly irrelevant component actually affects the phenomenon of interest. But those disagreements can be argued with evidence because the target is visible.

## A model creates expectations

Noise is often defined statistically relative to a model.

Suppose repeated measurements of a stable voltage vary slightly. If the instrument and environment are well characterized, we may model those deviations as random measurement noise. The model predicts a distribution, correlations, and perhaps a frequency spectrum.

If the residuals begin showing a periodic pattern, the model is challenged.

This is crucial. Calling something noise is not permission to stop looking. A good noise model makes predictions that can fail.

White noise should not suddenly develop long-range correlation without explanation. A stationary process should not drift systematically with temperature. Independent errors should not line up whenever another machine starts.

When the assumptions fail, the category needs revision.

## Filtering is a claim

Every filter says something about relevance.

A low-pass filter says variations above a chosen frequency are not needed for the current task. A median filter treats isolated spikes differently from neighboring values. Averaging assumes the information of interest survives aggregation.

Those operations can be mathematically well defined and still inappropriate.

Suppose a sensor is monitoring a machine for brief shock events. Averaging one-minute windows may produce a wonderfully smooth trend while erasing the very events that matter.

The filter did exactly what it was designed to do. The analytical goal was wrong for the use case.

This is why filter settings belong in the method, not hidden in the plotting code.

## Noise can be quantified

The signal/noise distinction becomes especially useful when we can compare them quantitatively.

Signal-to-noise ratio is one common tool. Depending on the domain it may compare powers, amplitudes, variances, or other quantities under specific conventions. The formula is not universal across every problem, so the definition has to be stated.

What matters is that "too noisy" can become an operational claim: detection probability falls below a requirement, estimation uncertainty becomes too large, bit errors exceed a threshold, or residual variance masks an effect.

Once the threshold is explicit, teams can improve the sensor, change the protocol, collect more data, redesign the experiment, or accept that the measurement cannot support the desired conclusion.

## Relativity can improve rigor

The phrase "noise is relative" sometimes sounds like a retreat from objectivity. In practice it can force greater precision.

Instead of saying:

> This component is just noise.

we can say:

> For estimating the slow temperature trend, we are treating fluctuations above this frequency as nuisance variation, because independent tests show they arise from sensor electronics and do not track the reference thermometer.

The second statement exposes assumptions and evidence. Another investigator can reproduce or challenge it.

That is more objective, not less.

## Nature does not label the channels

The physical world contains overlapping processes. A detector receives some combination of them. We decide which relation we are trying to estimate.

The decision introduces purpose, but physics still constrains the result.

A filter cannot recover a component that was never measured. A model cannot make two indistinguishable inputs distinguishable without additional information. A receiver cannot exceed its physical limitations merely by redefining the target.

So the signal/noise boundary has two parents: a task chosen by an observer and structure supplied by the world.

Forget the first, and we pretend relevance is natural and universal.

Forget the second, and we slide into the idea that any interpretation is as good as any other.

Noise is relative because questions differ.

It is not arbitrary because answers still have to survive measurement.
