---
title: No Healthy SIP Worker Is a User-Facing Failure Counter
url: /posts/no-healthy-sip-worker-user-facing-counter.html
date: '2026-09-14'
read_time: 1
excerpt: The most important load-balancer failure is not that a backend probe failed;
  it is that an incoming SIP request could not be assigned to any healthy worker.
topic: observability-monitoring
tags:
- sip
- load-balancing
- impact
- voip
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: VoIP · advanced'
outputs:
- url: /posts/no-healthy-sip-worker-user-facing-counter.html
  template: cms/templates/posts/posts--no-healthy-sip-worker-user-facing-counter.tpl
  source: cms/templates/posts/posts--no-healthy-sip-worker-user-facing-counter.json
---

The most important load-balancer failure is not that a backend probe failed; it is that an incoming SIP request could not be assigned to any healthy worker. What made the issue measurable was `voip_sip_proxy_no_healthy_worker_total`. Counting rejected requests translates internal pool health into actual service impact and gives a stronger paging signal than backend state alone.

I classify this as impact-based alerting. The useful debugging sequence is to confirm the signal, compare it with the neighboring subsystem, then look at logs or detailed metrics only after the failure domain is smaller.

The production rule that came out of it is: Alert on any recent increase, then correlate with worker health and heartbeat age to identify whether capacity or routing caused the rejection. This is deliberately more specific than adding another broad alert with no response procedure.

Commit `b65d5d4` is the repository evidence behind the note. It provides the concrete configuration or fix that turned the observation into a repeatable monitoring control.
