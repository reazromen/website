---
title: A Docker Healthcheck Must Test the Dependency You Actually Need
url: /posts/field-note-2026-healthcheck-real-dependency.html
date: '2026-08-14'
read_time: 2
excerpt: A process can be alive while the service contract its neighbors depend on
  is broken.
topic: linux-homelab
tags:
- docker
- healthcheck
- http
- database
draft: false
featured: false
language: en
eyebrow: Home Infrastructure Field Notes · intermediate
outputs:
- url: /posts/field-note-2026-healthcheck-real-dependency.html
  template: cms/templates/posts/posts--field-note-2026-healthcheck-real-dependency.tpl
  source: cms/templates/posts/posts--field-note-2026-healthcheck-real-dependency.json
---

# A Docker Healthcheck Must Test the Dependency You Actually Need

A process can be alive while the service contract its neighbors depend on is broken.

I keep this as a field note because the failure mode is easy to misclassify: health is defined as process existence instead of useful readiness. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Health should measure the contract consumers rely on.**

## Implementation pattern

Use a fast side-effect-free readiness probe against the actual interface or dependency required by downstream services.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- the check fails on real dependency loss
- the check remains cheap
- restart policy does not hide persistent failure

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Health should measure the contract consumers rely on. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
