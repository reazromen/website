---
title: Self-Hosted ntfy Removed an External Delivery Dependency
url: /posts/self-hosted-ntfy-removes-external-dependency.html
date: '2026-09-14'
read_time: 1
excerpt: The alert sink originally targeted a public ntfy service, which made production
  notification depend on infrastructure outside the hserver control boundary.
topic: observability-monitoring
tags:
- ntfy
- alertmanager
- self-hosted
- notifications
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Alerting & Notification · advanced'
outputs:
- url: /posts/self-hosted-ntfy-removes-external-dependency.html
  template: cms/templates/posts/posts--self-hosted-ntfy-removes-external-dependency.tpl
  source: cms/templates/posts/posts--self-hosted-ntfy-removes-external-dependency.json
---

The alert sink originally targeted a public ntfy service, which made production notification depend on infrastructure outside the hserver control boundary. What made the issue measurable was `self-hosted hserver-ntfy health and delivery counters`. Running ntfy locally gives the monitoring path an owned endpoint while public ingress can still expose the subscriber interface under the reviewed security model.

I classify this as dependency ownership for alert delivery. The useful debugging sequence is to confirm the signal, compare it with the neighboring subsystem, then look at logs or detailed metrics only after the failure domain is smaller.

The production rule that came out of it is: Monitor ntfy health, keep its image pinned and resource-bounded, and test external notification delivery after every observability change. This is deliberately more specific than adding another broad alert with no response procedure.

Commit `49ec1dd` is the repository evidence behind the note. It provides the concrete configuration or fix that turned the observation into a repeatable monitoring control.
