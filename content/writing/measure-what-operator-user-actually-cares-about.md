---
title: Measure What the Operator or User Actually Cares About
url: /posts/measure-what-operator-user-actually-cares-about.html
date: '2026-09-15'
read_time: 1
excerpt: CPU and container counts are supporting signals; service reachability, backup
  validity and call-path health are closer to the real objective.
topic: observability
tags:
- sre
- sli
- prometheus
- availability
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Observability · advanced'
outputs:
- url: /posts/measure-what-operator-user-actually-cares-about.html
  template: cms/templates/posts/posts--measure-what-operator-user-actually-cares-about.tpl
  source: cms/templates/posts/posts--measure-what-operator-user-actually-cares-about.json
---

The hserver observability stack grew from host metrics into endpoint health, backup posture, deployment provenance, database state and VoIP-specific dashboards. That expansion made it clear that low CPU does not mean the platform is doing its job.

Prometheus guidance emphasizes measuring what users care about, and SRE formalizes that idea through service-level indicators. Internal saturation is useful mainly because it helps explain or predict outcome degradation. Infrastructure metrics describe internal conditions, while users and operators experience outcomes. A healthy process with a broken trust chain, stale backup or failed SIP path is still a production failure.

The monitoring model now combines resource telemetry with service endpoints, safety evidence, storage state, deployment metadata and domain-specific VoIP signals.

For every critical service, define at least one outcome-oriented signal and then add internal metrics that help diagnose it. Dashboards should lead from impact to cause, not force operators to infer impact from machine counters. The concrete hserver evidence is commit b65d5d4, so this note is tied to an actual production change rather than a hypothetical failure.
