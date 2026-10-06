---
title: Data Without Provenance Is Half a Fact
url: /posts/signals-of-reality-064-data-without-provenance.html
date: '2026-08-27'
read_time: 7
excerpt: Data becomes evidence only when its origin and transformation chain are knowable. Provenance connects a value to the process that produced it and lets others test the claim.
topic: information-computation
tags:
- provenance
- data-quality
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · How Do We Know?'
editorial_batch: signals-of-reality-200
---

A spreadsheet appears in a shared folder.

The columns are neatly named.

The values look plausible.

There is no source note.

No one knows who generated it.

No one knows whether it came from production, a test system, an export from last month, or a manually edited copy.

The data may be correct.

But as evidence, it is damaged.

Provenance is the record of where data came from and what happened to it on the way to the current form.

Without provenance, a fact loses half of what makes it useful: the ability to verify it.

## Origin answers the first question

Every dataset should make basic questions easy.

Which instrument, service, experiment, or institution produced it?

At what time?

Under which configuration?

For what purpose?

Was the source authoritative for the quantity being reported?

These questions can expose category mistakes immediately.

A staging database can contain realistic records while being the wrong source for a production incident.

A simulation output can look like an observation.

A sensor mounted indoors can be perfectly calibrated and still be the wrong source for outdoor temperature.

Provenance identifies the relationship between source and claim.

## Transformation answers the second question

Raw origin is not enough.

Most data is transformed.

It is filtered, joined, converted, normalized, interpolated, deduplicated, compressed, classified, or aggregated.

Each transformation can be legitimate.

Each transformation can also change what the data means.

A provenance chain therefore records not only *where did this come from?* but also *what did we do to it?*

Version-controlled code, immutable source files, checksums, workflow logs, and data lineage systems are practical ways to preserve that chain.

## Provenance makes disagreement productive

Suppose two teams report different values for the same metric.

Without provenance, the disagreement becomes social.

Which team do we trust?

With provenance, it becomes technical.

Team A used events from one database and excluded retries.

Team B used a warehouse table and included retries.

The difference can be reproduced.

Perhaps one definition is better for the decision. Perhaps both are valid for different questions.

The conflict moves from authority to method.

That is a major epistemic advantage.

## Source quality is not the same as source fame

A prestigious institution can publish a number outside its strongest domain.

An obscure sensor can provide excellent local data.

Provenance lets us evaluate the actual chain instead of substituting reputation for method.

Who measured it?

How?

With what instrument?

Under what calibration?

What processing?

What uncertainty?

What later revisions?

These questions scale from laboratory science to public statistics to observability dashboards.

## Derived data needs stronger provenance, not weaker

The farther a number moves from direct observation, the more lineage matters.

A machine-learning score may depend on dozens of features collected from different sources.

A climate reanalysis combines observations with a numerical model.

A business KPI may combine logs, billing data, user state, and manually maintained mappings.

Derived products can be extremely useful.

But without their recipe, users cannot know what changed when the number changes.

A source link alone is no longer enough.

The transformation graph becomes part of the definition.

## Reproducibility is provenance tested

A strong provenance record allows another person—or your future self—to reconstruct the result.

Not always byte-for-byte. External sources may be revised, hardware may disappear, and nondeterministic processes exist.

But the path should be clear enough that discrepancies can be located.

Which input version?

Which code revision?

Which parameters?

Which environment?

Which calibration?

If those answers are available, a result can be challenged constructively.

If they are missing, the result becomes an orphan.

## Half a fact is not necessarily false

Calling provenance-less data half a fact does not mean the values are fabricated.

They may be completely correct.

The problem is that correctness cannot be efficiently established.

A claim without lineage forces every later user to begin from trust.

A claim with lineage invites verification.

That difference matters most when the result is surprising, politically consequential, scientifically important, or operationally expensive.

Data becomes durable evidence when its history travels with it.

The value is one part.

The path that produced the value is the other.
