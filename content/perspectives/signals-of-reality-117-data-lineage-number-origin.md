---
title: "Data Lineage: Where Did This Number Come From?"
url: /posts/signals-of-reality-117-data-lineage-number-origin.html
date: '2026-01-15'
read_time: 7
excerpt: Data lineage reconstructs the path from source observations through transformations to a reported number, making disagreement and debugging tractable.
topic: information-computation
tags:
- data-quality
- provenance
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · The System Behind the Dashboard'
editorial_batch: signals-of-reality-200
---

The dashboard says 83.7.

Someone asks:

Where did that number come from?

Nobody knows.

The SQL was changed months ago.

One table is populated by a job maintained by another team.

A spreadsheet contributes one mapping.

A cache holds intermediate results.

Now the number is not merely uncertain.

It is epistemically orphaned.

Data lineage is the discipline of keeping the ancestry.

## A metric is a path, not a point

Suppose a dashboard displays daily active devices.

The number may depend on:

device events,

ingestion,

deduplication,

identity mapping,

timezone conversion,

eligibility rules,

database joins,

aggregation,

and dashboard queries.

Each step can change the count.

The final integer contains none of that history visibly.

Lineage makes the hidden path inspectable.

## Lineage localizes disagreement

Two dashboards disagree.

Without lineage, teams compare screenshots.

With lineage:

Dashboard A reads warehouse table X built at 02:00.

Dashboard B queries event store Y in near real time.

A excludes test devices.

B does not.

The numbers are no longer mysterious.

They answer different questions through different pipelines.

Lineage converts conflict into method.

## Transformations are claims

A join says two identifiers represent the same entity.

A filter says certain records are irrelevant.

An aggregation says certain differences can be collapsed.

An imputation says a missing value can be estimated by a rule.

These are not merely technical operations.

They are assumptions.

Lineage records where assumptions entered.

That matters when a conclusion is disputed.

## Versions belong in the lineage

Data logic changes.

A parser fixes a bug.

A metric definition changes.

A calibration coefficient updates.

A model is retrained.

If the output changes, operators need to know whether reality changed or the transformation changed.

Versioned lineage makes that distinction possible.

A number should be connected to code and configuration versions whenever practical.

## Lineage is observability for data

Application observability asks:

where did this request go?

Data lineage asks:

where did this value come from?

The structures are surprisingly similar.

Nodes.

Edges.

Transformations.

Timing.

Failures.

A trace follows computation through services.

Lineage follows information through datasets.

Both are methods for reconstructing causality inside complex systems.

## External sources need lineage too

A public dataset can enter an internal model.

Which release?

Downloaded when?

Was it modified?

Were columns renamed?

Were missing values dropped?

A URL alone is not complete provenance if the external source changes over time.

Checksums, snapshots, versions, and retrieval dates preserve reproducibility.

## The lineage graph can become large

Perfect lineage has cost.

Column-level lineage across every transformation can be difficult.

Dynamic SQL, notebooks, manual files, and external systems complicate capture.

The goal should follow risk.

Critical metrics deserve stronger lineage than exploratory scratch work.

Regulated or high-impact decisions deserve stronger evidence than decorative charts.

Lineage is an architecture choice.

## A number with ancestry can be challenged

That is its strength.

If someone doubts 83.7, they can move backward.

Which records?

Which query?

Which source?

Which calibration?

Which version?

At each step the claim becomes testable.

Data lineage does not guarantee the final number is correct.

It does something more practical:

it preserves the route by which correctness can be investigated.

When a number matters, "where did it come from?" should never be an archaeological question.
