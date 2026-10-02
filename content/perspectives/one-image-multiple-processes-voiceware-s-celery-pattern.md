---
title: 'One Image, Multiple Processes: Voiceware’s Celery Pattern'
url: /posts/one-image-multiple-processes-voiceware-s-celery-pattern.html
date: '2026-09-18'
read_time: 2
excerpt: Reusing the Django application image for several worker roles while changing
  how the container starts.
topic: voiceware-engineering
tags:
- voiceware
- celery
- containers
- django
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Background Work · deep-dive'
outputs:
- url: /posts/one-image-multiple-processes-voiceware-s-celery-pattern.html
  template: cms/templates/posts/posts--one-image-multiple-processes-voiceware-s-celery-pattern.tpl
  source: cms/templates/posts/posts--one-image-multiple-processes-voiceware-s-celery-pattern.json
---

The architecture question is **reusing the Django application image for several worker roles while changing how the container starts**.

## Start with the boundary, not the tool

I reused the voiceware-django-app image for Celery Beat and the high and standard workers, changing the process role through the deployment command.

## Runtime view

```
producer -> queue/broker -> worker class -> task execution -> side effect
```

## Responsibilities

For this topic, the relevant responsibility is reusing the Django application image for several worker roles while changing how the container starts. The boundary is good when each side can be described without hand-waving: what it receives, what it produces, what it depends on, and what happens if it disappears.

## Interfaces and failure isolation

The failure I explicitly design against is: Building a unique image for every process role can create unnecessary duplication when the codebase is shared. That is why I care about the interface, not only whether both pods are currently green.

## Scaling implications

The signals I would attach to this boundary are queue depth, oldest-job age, task execution time, worker availability, retry/error rate.

## Architecture review questions

- Test process commands exactly as rendered in the pod spec.
- Measure queue wait separately from execution time.
- Confirm workers consume the intended queue.
- Scale from workload pressure, not CPU alone.
- Keep scheduler semantics separate from worker semantics.

The design rule I keep is **A shared image with explicit commands can be clean, provided process roles are unambiguous and independently deployable.** Once the boundary is explicit, both automation and debugging get simpler.
