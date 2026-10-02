---
title: HTTPS Latency Needs More Than One Number
url: /posts/https-latency-needs-more-than-one-number.html
date: '2026-09-14'
read_time: 1
excerpt: A single total probe duration hides whether slowness came from name resolution,
  TCP connection, TLS negotiation or server response.
topic: observability-monitoring
tags:
- https
- latency
- tls
- synthetic-monitoring
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Network & Edge · advanced'
outputs:
- url: /posts/https-latency-needs-more-than-one-number.html
  template: cms/templates/posts/posts--https-latency-needs-more-than-one-number.tpl
  source: cms/templates/posts/posts--https-latency-needs-more-than-one-number.json
---

A single total probe duration hides whether slowness came from name resolution, TCP connection, TLS negotiation or server response. What made the issue measurable was `Blackbox Exporter phase timings and probe duration`. Phase timing turns an end-to-end symptom into a network diagnosis without requiring packet capture for every incident.

I classify this as synthetic transaction decomposition. The useful debugging sequence is to confirm the signal, compare it with the neighboring subsystem, then look at logs or detailed metrics only after the failure domain is smaller.

The production rule that came out of it is: Keep phase panels available for slow endpoints and alert on sustained end-to-end degradation rather than one noisy request. This is deliberately more specific than adding another broad alert with no response procedure.

Commit `b65d5d4` is the repository evidence behind the note. It provides the concrete configuration or fix that turned the observation into a repeatable monitoring control.
