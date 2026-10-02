---
title: 'High, Standard, and Low Queues: Designing for Contention'
url: /posts/high-standard-and-low-queues-designing-for-contention.html
date: '2026-09-18'
read_time: 2
excerpt: How priority classes can turn one background-processing system into controlled
  lanes.
topic: voiceware-engineering
tags:
- voiceware
- celery
- queues
- performance
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Background Work · deep-dive'
outputs:
- url: /posts/high-standard-and-low-queues-designing-for-contention.html
  template: cms/templates/posts/posts--high-standard-and-low-queues-designing-for-contention.tpl
  source: cms/templates/posts/posts--high-standard-and-low-queues-designing-for-contention.json
---

The architecture question is **how priority classes can turn one background-processing system into controlled lanes**.

## Start with the boundary, not the tool

I separated high, standard, and low Celery consumers so queue priority had a real runtime boundary.

## Runtime view

```
producer -> queue/broker -> worker class -> task execution -> side effect
```

## Responsibilities

For this topic, the relevant responsibility is how priority classes can turn one background-processing system into controlled lanes. The boundary is good when each side can be described without hand-waving: what it receives, what it produces, what it depends on, and what happens if it disappears.

## Interfaces and failure isolation

The failure I explicitly design against is: Without isolation, a burst of cheap low-priority work can starve jobs that users are actively waiting for. That is why I care about the interface, not only whether both pods are currently green.

## Scaling implications

The signals I would attach to this boundary are queue depth, oldest-job age, task execution time, worker availability, retry/error rate.

## Architecture review questions

- Test process commands exactly as rendered in the pod spec.
- Measure queue wait separately from execution time.
- Confirm workers consume the intended queue.
- Scale from workload pressure, not CPU alone.
- Keep scheduler semantics separate from worker semantics.

The design rule I keep is **Priority is useful only when execution capacity and routing enforce it; naming queues alone does nothing.** The goal is not more Kubernetes. The goal is less ambiguity.
