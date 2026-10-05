---
title: Latency-Sensitive Work and Batch Work Should Not Share Every Knob
url: /posts/latency-sensitive-work-and-batch-work-should-not-share-every-knob.html
date: '2026-03-24'
read_time: 2
excerpt: Why the presence of audio services and background workers argues for differentiated
  scaling and monitoring.
topic: voiceware-engineering
tags:
- voiceware
- latency
- scaling
- architecture
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Voice Services · deep-dive'
outputs:
- url: /posts/latency-sensitive-work-and-batch-work-should-not-share-every-knob.html
  template: cms/templates/posts/posts--latency-sensitive-work-and-batch-work-should-not-share-every-knob.tpl
  source: cms/templates/posts/posts--latency-sensitive-work-and-batch-work-should-not-share-every-knob.json
---

This is the decision I am examining: **why the presence of audio services and background workers argues for differentiated scaling and monitoring**.

## Context

I kept audio-fork separate from the Celery workers because they had different runtime jobs and latency concerns.

The decision mattered because A single CPU threshold or replica policy across every workload ignores very different performance objectives.

## Options I consider

**Option A — keep the simplest current behavior.** This minimizes moving parts and is often the right choice while proving a migration path.

**Option B — introduce a stronger abstraction immediately.** This can improve long-term consistency, but it also adds another system to debug before the underlying workload contract is stable.

**Option C — keep the simple implementation, but make the boundary explicit and define the trigger for revisiting it.** This is often my preferred migration posture.

## Decision criteria

```
voice/telephony event -> integration or audio service -> application/background processing -> resulting action
```

## Why the Voiceware implementation is useful signal

The repository tells me what was actually chosen at that point in the project. It does not force me to argue that the choice is universal. Infrastructure decisions are contextual: an early test cluster, a production environment, and a multi-team platform may reasonably choose different levels of abstraction.

## Trade-offs I would write into the ADR

The primary downside is the failure mode already identified: A single CPU threshold or replica policy across every workload ignores very different performance objectives. The primary reason to keep the decision is the lesson: Operational policy should follow workload behavior: interactive latency, queue throughput, or scheduled execution.

I would also record what would make me revisit the decision: traffic growth, stronger availability targets, additional environments, security constraints, release complexity, or operational pain that the current model can no longer absorb cheaply.

## Revisit triggers

- Protect interactive work from batch backlog.
- Do not use pod liveness as the only media-health signal.
- Keep voice-specific services independently restartable where useful.
- Verify internal endpoint contracts provider-to-consumer.
- Separate observed repository facts from protocol assumptions.

A good infrastructure decision is not one that never changes. It is one whose assumptions are visible enough that the team knows when it should change. The tool is secondary. The contract between layers is what makes the system operable.
