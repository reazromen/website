---
title: Store the Raw Data
url: /posts/signals-of-reality-059-store-raw-data.html
date: '2026-07-14'
read_time: 6
excerpt: The least-processed data preserves options that later processing can remove. Keeping it does not eliminate interpretation, but it makes assumptions revisitable.
topic: information-computation
tags:
- raw-capture
- provenance
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Signal / Noise'
editorial_batch: signals-of-reality-200
---

The clean dataset is smaller.

The units are fixed. Missing values are filled. Spikes are removed. Timestamps are aligned. The file is easy to plot.

Why keep the ugly original?

Because processing makes decisions.

Some decisions will later turn out to be wrong.

Storing the least-processed practical version of a measurement preserves the ability to revisit those decisions when the question changes.

## Raw is always relative

No digital dataset is literally untouched reality.

A sensor already has a response function. Analog electronics condition the signal. An ADC samples and quantizes it. Firmware may apply offset correction. A driver may rearrange bytes before a file exists.

So raw should not mean interpretation-free.

It should mean a clearly defined stage before later transformations that we may want to reconsider.

For one camera, raw might mean sensor values before color rendering. For a network capture, it might mean packets before application summarization. For an environmental station, it might mean calibrated but unaggregated measurements.

The important part is documenting the boundary.

## Cleaning can destroy the anomaly

Suppose a pipeline removes values more than five standard deviations from a rolling mean.

Most removed points may be sensor glitches.

Then one day a real physical transient exceeds the same threshold.

If only the cleaned dataset survives, the event is gone before anyone knows there was something to investigate.

This does not mean outlier filters are bad.

It means irreversible cleaning should be treated as a data-loss operation.

When storage permits, keep the source and generate cleaned views from it.

## Aggregation destroys timing

A one-minute average can be perfect for a dashboard.

It cannot later reconstruct a one-second burst.

A daily count can show volume while erasing order.

A histogram can show distribution while erasing temporal relationships.

Every aggregation answers some questions by sacrificing others.

Once the underlying samples are deleted, no later algorithm can recover distinctions that the aggregation did not preserve.

Compression can be reversible.

Summarization usually is not.

## Reprocessing becomes valuable when models improve

Science and engineering regularly return to old observations with new methods.

A better calibration model may correct a known bias.

A new algorithm may detect patterns that older software missed.

A revised physical theory may suggest a feature nobody originally thought to measure in the derived product.

Archived source data makes these second lives possible.

The instrument cannot travel back in time to repeat an observation of a transient event. The stored record becomes the only remaining interface to that moment.

## Provenance is as important as storage

Keeping files without knowing what they are is not enough.

A useful archive records instrument configuration, timestamps, units, firmware, calibration, processing version, and checksums. It distinguishes immutable source products from derived outputs.

Otherwise teams eventually face directories named final, final2, corrected, new-corrected, and final-really.

Data lineage is not bureaucracy.

It is the ability to say which transformations connect a published result to an observation.

## Raw data has costs

"Store everything forever" is not a serious universal policy.

High-rate sensors can generate enormous volumes. Sensitive data can create privacy and security obligations. Retention costs money and operational attention. Some raw streams may be legally or ethically inappropriate to keep.

The decision should therefore be explicit.

Which information would be impossible to reconstruct later?

What resolution is needed for plausible future questions?

What retention period balances scientific value, cost, and risk?

Can irreversible aggregation happen after a short protected retention window?

These are architecture questions, not slogans.

## Preserve options, not mythology

Raw data is not automatically true.

It can contain instrument faults, mislabeled channels, corrupted packets, and uncalibrated values. A cleaned dataset may be much closer to the quantity we actually want.

The reason to preserve the earlier stage is not that it is purer.

It is that it contains options.

Later investigators can apply a different calibration, examine an outlier, test a new filter, or verify that a reported feature was not created during processing.

"Store the raw data" is therefore shorthand for a more precise rule:

do not destroy distinctions before you are sure no future question will need them.

We rarely get that certainty.

So when the cost is reasonable, preserve the path back.
