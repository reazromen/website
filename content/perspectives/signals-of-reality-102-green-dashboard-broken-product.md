---
title: Green Dashboard, Broken Product
url: /posts/signals-of-reality-102-green-dashboard-broken-product.html
date: '2026-01-13'
read_time: 7
excerpt: Component health can remain green while an end-to-end user journey fails. Monitoring must include the composition of services, not only their individual vital signs.
topic: observability
tags:
- dashboards
- health-checks
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · The System Behind the Dashboard'
editorial_batch: signals-of-reality-200
---

Every service is green.

Login fails.

This kind of incident is not paradoxical.

Each component can satisfy its local health check while the product assembled from those components fails.

The dashboard is telling the truth it was designed to tell.

The design is incomplete.

## Local health is not composition health

A database accepts connections.

An API responds to `/health`.

A message broker is running.

A frontend loads.

An identity provider responds.

Yet login can still fail because the token audience is wrong, a clock drift invalidates signatures, a callback URL changed, or one service interprets identity differently from another.

No component is necessarily "down."

The relationship is broken.

Distributed products fail at boundaries.

## Green checks are often shallow

A health endpoint may test only that the process loop is alive.

That is useful for orchestration.

It prevents a dependency outage from causing every container to restart repeatedly.

But operators often read the same check as proof the application works.

Readiness and liveness are different concepts for a reason.

A process can be alive but unable to serve useful traffic.

A service can be ready for one operation and broken for another.

Health needs a scope.

## End-to-end probes test a stronger claim

A synthetic transaction can log in, perform a search, create a harmless object, read it back, and clean it up.

Now the monitor asks a question closer to user reality.

The cost is complexity.

Synthetic checks require credentials, test data, cleanup, careful rate control, and stable assumptions.

They can fail because of the test harness.

But they expose integration failures that component probes cannot see.

Both layers are needed.

## Dependencies can be individually healthy and jointly incompatible

Version mismatch is a good example.

Service A deploys a new field.

Service B still expects the old schema.

Both processes run.

Both health endpoints return 200.

Requests between them fail.

The incident is not located inside either component.

It exists in the contract between them.

This is why compatibility tests, canaries, schema discipline, and distributed tracing matter.

## User segmentation hides behind averages

A dashboard may be green because 99.9% of requests succeed.

That is excellent unless the failed 0.1% represents every user in one country, every device on one firmware revision, or every call using one carrier.

Aggregate health can coexist with total failure for a meaningful subgroup.

Break down critical metrics by dimensions that map to architecture and user experience.

But do so carefully: too many labels create cost and complexity.

Observability always trades detail against scale.

## Green can be stale

If telemetry ingestion stops, the last green value may remain on screen.

A dashboard should make freshness visible.

When was this sample produced?

When was it ingested?

Is the query returning new points?

A healthy-looking old measurement can be more dangerous than a red current one.

Freshness is part of health.

## The user is an observability signal

Support tickets, failed workflows, and user reports are not inferior to machine telemetry.

They are measurements from the highest layer of the product.

They can be noisy.

They can be incomplete.

So can metrics.

When users and dashboards disagree, the correct response is not to choose one immediately.

Correlate.

Which users?

Which time?

Which workflow?

Which backend traces?

Which deployment?

The contradiction can reveal the blind spot.

A green dashboard and a broken product can coexist because the dashboard is not lying.

It is answering a smaller question than the user is asking.
