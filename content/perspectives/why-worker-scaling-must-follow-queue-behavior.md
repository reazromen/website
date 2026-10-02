---
title: Why Worker Scaling Must Follow Queue Behavior
url: /posts/why-worker-scaling-must-follow-queue-behavior.html
date: '2026-09-18'
read_time: 2
excerpt: Thinking about replicas from queue latency and task cost rather than CPU
  alone.
topic: voiceware-engineering
tags:
- voiceware
- celery
- scaling
- operations
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Background Work · deep-dive'
outputs:
- url: /posts/why-worker-scaling-must-follow-queue-behavior.html
  template: cms/templates/posts/posts--why-worker-scaling-must-follow-queue-behavior.tpl
  source: cms/templates/posts/posts--why-worker-scaling-must-follow-queue-behavior.json
---

The day-two operations question is **thinking about replicas from queue latency and task cost rather than CPU alone**.

## Day-two reality

I kept replicaCount as a per-chart setting, including for the worker deployments.

Getting the first successful deployment is only the beginning. Operations starts when the system has to survive repeated releases, dependency failures, load changes, partial outages, and engineers who were not present during the original build.

## Signals

For this workload class I care about queue depth, oldest-job age, task execution time, worker availability, retry/error rate. I want the signal to map to the actual failure mode, not just to whatever metric is easiest to collect.

```
producer -> queue/broker -> worker class -> task execution -> side effect
```

## Failure scenarios

The primary risk is: CPU utilization can look normal while queue wait time grows because task arrival rate exceeds worker throughput.

I also plan for partial failure. A controller can reconcile while the product is broken. A process can run while a dependency is slow. A queue can accept jobs while completion latency grows. An internal Service can resolve while no useful endpoint answers.

## Operational response

I make the smallest change that addresses the layer with a concrete signal. If an emergency manual change is required, I treat it as temporary state and reconcile the intended fix back into Git afterward.

## Safer defaults

The problem came down to this: CPU utilization can look normal while queue wait time grows because task arrival rate exceeds worker throughput. What I carried forward was this: Scale background workers from workload signals such as queue depth, processing time, and latency objectives—not just generic host metrics.

## Runbook notes

- Scale from workload pressure, not CPU alone.
- Keep scheduler semantics separate from worker semantics.
- Test process commands exactly as rendered in the pod spec.
- Measure queue wait separately from execution time.
- Confirm workers consume the intended queue.

The operational principle is **Scale background workers from workload signals such as queue depth, processing time, and latency objectives—not just generic host metrics.** For me, that is the practical difference between deploying containers and engineering a platform.
