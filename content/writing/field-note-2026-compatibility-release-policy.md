---
title: Compatibility Metadata Is Release Policy, Not Tribal Knowledge
url: /posts/field-note-2026-compatibility-release-policy.html
date: '2026-02-07'
read_time: 2
excerpt: Hardware and software eligibility rules should be machine-readable where
  rollout decisions are made.
topic: production-ota-fleet
tags:
- compatibility
- ota
- hardware-revision
- release-engineering
draft: false
featured: false
language: en
eyebrow: OTA Field Notes · advanced
outputs:
- url: /posts/field-note-2026-compatibility-release-policy.html
  template: cms/templates/posts/posts--field-note-2026-compatibility-release-policy.tpl
  source: cms/templates/posts/posts--field-note-2026-compatibility-release-policy.json
---

# Compatibility Metadata Is Release Policy, Not Tribal Knowledge

Hardware and software eligibility rules should be machine-readable where rollout decisions are made.

I keep this as a field note because the failure mode is easy to misclassify: operators remember which build fits which hardware but the control plane cannot enforce it. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Encode compatibility where the assignment decision is made.**

## Implementation pattern

Evaluate device metadata against release compatibility and log explicit inclusion or rejection reasons.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- hardware revision is inventory data
- eligibility has a reason
- device keeps a second local safety check

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Encode compatibility where the assignment decision is made. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
