---
title: Drachtio Connectivity Is a Control-Plane Health Signal
url: /posts/drachtio-connectivity-control-plane-signal.html
date: '2024-08-18'
read_time: 1
excerpt: The SIP proxy can be running as a process while its control connection to
  drachtio is down, leaving signaling logic unable to operate correctly.
topic: observability-monitoring
tags:
- drachtio
- sip
- voip
- prometheus
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: VoIP · advanced'
outputs:
- url: /posts/drachtio-connectivity-control-plane-signal.html
  template: cms/templates/posts/posts--drachtio-connectivity-control-plane-signal.tpl
  source: cms/templates/posts/posts--drachtio-connectivity-control-plane-signal.json
---

The SIP proxy can be running as a process while its control connection to drachtio is down, leaving signaling logic unable to operate correctly. On hserver the first signal I use for this question is `voip_drachtio_connected`. Monitoring the application-to-drachtio relationship is more specific than checking either container independently and directly reflects a critical signaling dependency.

The important part is interpretation rather than collecting another graph. dependency health monitoring. That gives the metric a specific operational job instead of making it another number on a dashboard.

The practical control is straightforward: Page on sustained disconnect, then inspect both drachtio and proxy logs before restarting components that may only be symptoms. This also gives me a repeatable check after deployments, exporter changes, or capacity tuning.

Repository evidence for this monitoring behavior is commit `b65d5d4`. I keep that reference with the note because a monitoring conclusion is stronger when the configuration and runtime decision that produced it can be inspected later.
