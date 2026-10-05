---
title: OpenSIPS 5xx Spikes Show Signaling Quality
url: /posts/opensips-5xx-spikes-signaling-quality.html
date: '2025-12-23'
read_time: 1
excerpt: Registration counts and dialog counts can look stable while transaction failures
  increase for a subset of calls.
topic: observability-monitoring
tags:
- opensips
- 5xx
- sip
- red-method
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: VoIP · advanced'
outputs:
- url: /posts/opensips-5xx-spikes-signaling-quality.html
  template: cms/templates/posts/posts--opensips-5xx-spikes-signaling-quality.tpl
  source: cms/templates/posts/posts--opensips-5xx-spikes-signaling-quality.json
---

Registration counts and dialog counts can look stable while transaction failures increase for a subset of calls. I ended up treating `increase(hserver_opensips_tm_5xx_transactions_total[5m])` as the useful observation point rather than relying on a generic service-up indicator. 5xx transaction growth captures server-side signaling failure and complements raw request volume with an outcome signal.

This is a good example of RED-style service monitoring. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Track transaction rate, errors and latency where available, then correlate a spike with backend health and recent configuration changes. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `b65d5d4` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
