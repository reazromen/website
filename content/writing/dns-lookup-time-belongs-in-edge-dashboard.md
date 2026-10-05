---
title: DNS Lookup Time Belongs in an Edge Dashboard
url: /posts/dns-lookup-time-belongs-in-edge-dashboard.html
date: '2022-06-02'
read_time: 1
excerpt: A slow public request is not always slow application code; DNS resolution
  can consume a meaningful part of the user-visible path.
topic: observability-monitoring
tags:
- dns
- latency
- blackbox-exporter
- networking
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Network & Edge · advanced'
outputs:
- url: /posts/dns-lookup-time-belongs-in-edge-dashboard.html
  template: cms/templates/posts/posts--dns-lookup-time-belongs-in-edge-dashboard.tpl
  source: cms/templates/posts/posts--dns-lookup-time-belongs-in-edge-dashboard.json
---

A slow public request is not always slow application code; DNS resolution can consume a meaningful part of the user-visible path. The monitoring mistake would be to read one metric in isolation. `blackbox probe DNS phase timing` is useful because it narrows the question, and breaking synthetic latency into dns, connect, tls and processing phases helps locate where the delay begins before opening application logs.

In software operations this falls under phase-based latency decomposition. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Graph DNS lookup time with total public latency and compare multiple endpoints so resolver problems do not masquerade as service regressions. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `b65d5d4`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
