---
title: Registered Endpoints Are Capacity and Behavior Signals
url: /posts/registered-endpoints-capacity-behavior.html
date: '2026-09-14'
read_time: 1
excerpt: A sudden drop in registered SIP endpoints can indicate network reachability,
  credential, expiry or registrar problems even when call processing components are
  up.
topic: observability-monitoring
tags:
- sip-registration
- drachtio
- opensips
- voip
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: VoIP · advanced'
outputs:
- url: /posts/registered-endpoints-capacity-behavior.html
  template: cms/templates/posts/posts--registered-endpoints-capacity-behavior.tpl
  source: cms/templates/posts/posts--registered-endpoints-capacity-behavior.json
---

A sudden drop in registered SIP endpoints can indicate network reachability, credential, expiry or registrar problems even when call processing components are up. On the finished hserver stack, `drachtio registered endpoints and OpenSIPS registered users` is the signal that makes the difference visible. Registration population gives a client-side view of service health that server process metrics cannot replace.

The engineering pattern here is user-population monitoring. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Trend registrations against expected daily behavior and investigate abrupt changes with auth logs, DNS, TLS and network probes. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `b65d5d4`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
