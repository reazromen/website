---
title: Socket Counts Are Capacity Clues, Not Health by Themselves
url: /posts/socket-counts-are-capacity-clues-not-health.html
date: '2026-09-14'
read_time: 1
excerpt: A rising established-connection count can represent normal load, a leak,
  slow clients or a downstream dependency holding sockets open.
topic: observability-monitoring
tags:
- tcp-sockets
- capacity
- linux
- networking
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Network & Edge · advanced'
outputs:
- url: /posts/socket-counts-are-capacity-clues-not-health.html
  template: cms/templates/posts/posts--socket-counts-are-capacity-clues-not-health.tpl
  source: cms/templates/posts/posts--socket-counts-are-capacity-clues-not-health.json
---

A rising established-connection count can represent normal load, a leak, slow clients or a downstream dependency holding sockets open. What made the issue measurable was `established TCP sockets and total socket usage`. Connection counts need baseline and service context; the same value can be healthy at peak traffic and abnormal during an idle period.

I classify this as baseline-driven capacity monitoring. The useful debugging sequence is to confirm the signal, compare it with the neighboring subsystem, then look at logs or detailed metrics only after the failure domain is smaller.

The production rule that came out of it is: Trend sockets with request rate, latency and process file-descriptor usage before declaring a connection leak. This is deliberately more specific than adding another broad alert with no response procedure.

Commit `b65d5d4` is the repository evidence behind the note. It provides the concrete configuration or fix that turned the observation into a repeatable monitoring control.
