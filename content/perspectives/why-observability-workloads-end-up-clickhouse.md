---
title: Why Observability Workloads Keep Ending Up in ClickHouse
url: /posts/why-observability-workloads-end-up-clickhouse.html
date: '2026-09-26'
read_time: 9
excerpt: Logs and traces are wide, append-heavy events that are usually filtered by
  time and a few fields, then aggregated. That workload shape explains the attraction
  to a columnar analytical database better than any benchmark headline.
topic: ''
tags:
- clickhouse
- opentelemetry
- logs
- traces
draft: false
featured: false
language: en
eyebrow: Observability & Data · systems note
outputs:
- url: /posts/why-observability-workloads-end-up-clickhouse.html
  template: cms/templates/posts/posts--why-observability-workloads-end-up-clickhouse.tpl
  source: cms/templates/posts/posts--why-observability-workloads-end-up-clickhouse.json
---

The current observability stack has an interesting habit: eventually somebody proposes ClickHouse.

The explanation is often reduced to two words—fast and cheap—which is not enough to make an architecture decision.

The more useful question is why logs and traces map well to the execution model of a columnar analytical database in the first place.

## Telemetry is a wide-event workload[#](#telemetry-is-a-wide-event-workload)

A trace span can carry timestamps, service identity, operation name, duration, status, resource attributes, span attributes, IDs, events, and links. A log event can be similarly wide once Kubernetes, cloud, host, request, and application metadata are attached.

But a typical investigation rarely reads every field from every row.

You ask something like:

```
last 30 minutes
service = checkout
status = error
group by exception.type
show count and p95 duration
```

The query touches time, service, status, one attribute, and a measure. The event may have a hundred other fields.

Columnar storage is attractive because it can read and compress the columns relevant to the query rather than treating every event as an indivisible record.

## Append-heavy data matches analytical storage[#](#append-heavy-data-matches-analytical-storage)

Observability data is overwhelmingly append-oriented. Spans and logs arrive, are queried for a retention window, and eventually expire. Corrections to old rows are unusual compared with transactional databases.

That fits systems optimized for large inserts, immutable-ish parts, background merges, partition pruning, and analytical scans.

It is a very different shape from an OLTP workload where individual rows are constantly updated under point transactions.

## High cardinality is easier when dimensions are data, not pre-created series[#](#high-cardinality-is-easier-when-dimensions-are-data-not-pre-created-series)

Metrics systems often model each unique label set as a time series. Logs and traces are naturally event-oriented: high-cardinality values such as trace IDs, request IDs, URLs, users, or arbitrary attributes live inside rows.

That does not make cardinality free. Indexes, maps, text search, and query design still matter. But the storage model is not forced to materialize every combination as a separate long-lived metric series.

This is one reason teams looking for unified log/trace analysis gravitate toward a general analytical engine.

## Schema still decides performance[#](#schema-still-decides-performance)

ClickHouse's own recent ClickStack engineering posts make an important point: putting telemetry into ClickHouse does not automatically produce fast observability.

They redesigned log and trace schemas, changed primary ordering, added text indexes, rewrote queries, and used materialized views because real observability query patterns exposed weaknesses in the original layout.

That is the part vendor diagrams usually skip.

Columnar storage gives you a good set of primitives. You still have to align ordering keys, indexes, codecs, partitions, materialized columns, and query patterns with the workload.

## OpenTelemetry helps because ingestion becomes less proprietary[#](#opentelemetry-helps-because-ingestion-becomes-less-proprietary)

OpenTelemetry has matured at roughly the same time as this storage pattern. A team can instrument once, collect through OTel, and choose an observability backend without binding every application to one vendor SDK.

ClickStack's architecture explicitly leans on this: OpenTelemetry Collector for ingestion, ClickHouse for storage/query, and a purpose-built UI on top.

That separation is valuable even if ClickHouse is not the final backend. Collection becomes a pipeline boundary rather than an application rewrite.

## The counter-case matters[#](#the-counter-case-matters)

ClickHouse is not automatically the right answer for every telemetry signal.

A specialized metrics TSDB can provide data structures, caching, downsampling, and query semantics tuned specifically for time-series metrics. A search engine may provide different text-search ergonomics. A managed observability product can remove the operational burden entirely.

Operating ClickHouse also means owning ingestion durability, schema evolution, replication, merges, resource isolation, retention, upgrades, and the behavior of expensive queries unless a managed service absorbs those responsibilities.

The community discussion around ClickHouse observability is useful precisely because people are asking the counter-question: are three specialized stores sometimes better than one general engine?

That depends on whether cross-signal correlation and shared operational machinery are worth more than signal-specific optimization.

## Keep the raw event model honest[#](#keep-the-raw-event-model-honest)

One failure mode I would avoid is treating ClickHouse as permission to ingest every attribute forever.

Bad telemetry is still bad telemetry. Unbounded strings, duplicate semantic attributes, inconsistent service naming, uncontrolled log bodies, and accidental payload capture create cost and query problems no storage engine can wish away.

A good architecture still needs:

- semantic conventions,
- sampling policy,
- attribute governance,
- retention classes,
- PII/security controls,
- query budgets,
- and durable buffering where losing telemetry is unacceptable.

## Workload shape, not fashion[#](#workload-shape-not-fashion)

ClickHouse keeps appearing in observability because modern telemetry increasingly looks like a stream of wide analytical events.

Those events are append-heavy, compressible, filtered by time, queried across a subset of columns, and aggregated interactively. A column-oriented analytical database is structurally good at that workload.

That is a better explanation than “everybody is moving to ClickHouse.”

Architecture should begin with the shape of the data and the questions operators need to ask. If those match ClickHouse, the current trend makes sense. If they do not, copying the trend just gives you a complicated database to operate.

## Sources and further reading[#](#sources-and-further-reading)

- [ClickHouse: How ClickStack makes ClickHouse faster for observability](https://clickhouse.com/blog/clickstack-faster-observability)
- [ClickHouse: schema and query redesign for ClickStack](https://clickhouse.com/blog/making-clickstack-5x-faster-clickhouse-observability)
- [Community discussion: why observability keeps ending up on ClickHouse](https://www.reddit.com/r/Observability/comments/1vlzbii/why_is_all_observability_going_to_clickhouse_and/)
- [ClickHouse: reliable OpenTelemetry ingestion at scale](https://clickhouse.com/blog/reliable-opentelemetry-ingestion-at-scale)
