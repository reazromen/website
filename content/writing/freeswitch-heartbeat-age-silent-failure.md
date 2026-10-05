---
title: Worker Heartbeat Age Catches Silent FreeSWITCH Failure
url: /posts/freeswitch-heartbeat-age-silent-failure.html
date: '2020-03-25'
read_time: 1
excerpt: A FreeSWITCH process may remain alive while its worker integration stops
  reporting useful state to the signaling layer.
topic: observability-monitoring
tags:
- freeswitch
- heartbeat
- freshness
- voip
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: VoIP · advanced'
outputs:
- url: /posts/freeswitch-heartbeat-age-silent-failure.html
  template: cms/templates/posts/posts--freeswitch-heartbeat-age-silent-failure.tpl
  source: cms/templates/posts/posts--freeswitch-heartbeat-age-silent-failure.json
---

A FreeSWITCH process may remain alive while its worker integration stops reporting useful state to the signaling layer. The monitoring mistake would be to read one metric in isolation. `voip_freeswitch_heartbeat_age_seconds` is useful because it narrows the question, and heartbeat age is a freshness signal that detects stale application state even when process liveness and tcp reachability still look normal.

In software operations this falls under freshness-based distributed health monitoring. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Alert after the heartbeat contract is exceeded and use node-specific labels so one stale worker does not obscure the rest of the pool. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `b65d5d4`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
