---
title: Delete Late, Classify Carefully
url: /posts/signals-of-reality-066-delete-late-classify-carefully.html
date: '2026-04-09'
read_time: 6
excerpt: Early deletion destroys options. A safer data pipeline preserves source observations, adds quality classifications, and excludes records only in derived analyses with documented reasons.
topic: information-computation
tags:
- data-quality
- raw-capture
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · How Do We Know?'
editorial_batch: signals-of-reality-200
---

A sensor reports a value that looks impossible.

One pipeline deletes it immediately.

Another keeps the record, marks it with a quality flag, and lets later analyses decide whether to use it.

The second architecture is usually more powerful because it separates observation from judgment.

## Deletion is irreversible compression

Once a record disappears from the only stored dataset, later investigators cannot ask new questions about it.

Was it a sensor glitch?

Did similar glitches precede failures?

Did another instrument show the same change?

Did the value become impossible only because a unit conversion was wrong?

A deleted record cannot answer.

This is why cleaning should be treated as information loss, not merely tidiness.

Some loss is necessary. Storage is finite, and some records are unusable or inappropriate to retain. But the decision should be explicit.

## Classification preserves ambiguity

Instead of one boolean field called valid, quality can be represented more carefully.

A record might be unreviewed, outside an expected range, missing calibration metadata, duplicated, affected by known maintenance, or confirmed invalid.

These categories preserve why a record is questionable.

An analyst studying normal operations may exclude flagged values. An engineer studying sensor failure may select exactly those values.

The same archive supports both questions.

## Do not confuse bad-for-this-analysis with bad data

A measurement can be valid and still irrelevant.

Suppose a weather station records temperature every minute. An analysis of daytime solar heating may exclude nighttime observations.

The nighttime data is not bad.

It simply falls outside the study design.

If the pipeline deletes it as invalid, one analysis choice has become a permanent property of the archive.

The safer pattern is simple:

preserve broadly, classify explicitly, filter locally.

## Quality rules need versioning

A range check may change.

A calibration model may improve.

A firmware version previously considered suspicious may later be shown to behave correctly.

If quality flags are computed by versioned rules, old data can be reclassified.

If records were deleted when the old rule ran, correction is impossible.

This is a strong argument for treating quality assessment as derived data.

The source remains stable.

The interpretation evolves.

## Keep reasons machine-readable

A note saying "weird data removed" is almost useless at scale.

Quality reasons should be structured enough to query.

Which sensor produced most out-of-range values?

Did questionable records cluster after a release?

How many values were excluded for missing calibration rather than physical impossibility?

Structured classification turns data quality itself into a measurable system.

The cleaning pipeline becomes observable.

## Deletion still has a role

There are legitimate reasons to remove data.

Retention policies bound storage.

Duplicate ingest may have no value once verified.

Corrupted files may be unrecoverable.

Some datasets may need stricter handling because of privacy or contractual rules.

The principle is not never delete.

It is delay irreversible deletion until the reason is strong enough to justify losing future options.

That threshold should be higher than "the point makes the chart ugly."

## A pipeline is also an epistemic system

Data engineering choices determine what later analysts are allowed to know.

If raw distinctions are destroyed early, every later model inherits that blindness.

If classifications remain inspectable, later users can challenge them.

This is why provenance, quality flags, immutable sources, and derived views belong together.

They create a separation between what was observed and what we currently believe about the observation.

Delete late.

Classify carefully.

The rule is not about hoarding data.

It is about preserving the ability to discover that yesterday's cleaning assumption was wrong.
