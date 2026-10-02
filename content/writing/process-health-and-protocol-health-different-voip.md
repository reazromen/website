---
title: Process Health and Protocol Health Are Different in VoIP
url: /posts/process-health-and-protocol-health-different-voip.html
date: '2026-09-14'
read_time: 1
excerpt: A running SIP or RTP process is necessary but not sufficient evidence that
  calls can establish and carry media.
topic: telecom-voip
tags:
- sip
- rtp
- healthcheck
- sre
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Production Acceptance · advanced'
outputs:
- url: /posts/process-health-and-protocol-health-different-voip.html
  template: cms/templates/posts/posts--process-health-and-protocol-health-different-voip.tpl
  source: cms/templates/posts/posts--process-health-and-protocol-health-different-voip.json
---

VoIP containers can report running while a port mapping, route, registration, media relay or backend dependency is broken. The process-level sentinel protects against obvious outages but cannot prove end-to-end call behavior. Liveness, readiness and service-level outcome are different layers of evidence. Each answers a narrower question than the one above it.

The production baseline combines container state with endpoint checks, OpenSIPS/RTPengine metrics and documented call-path verification rather than treating Docker status as the final health signal.

Build synthetic SIP transactions and controlled RTP checks into observability while retaining component metrics for diagnosis after an end-to-end signal fails. SRE monitoring works from user-visible outcomes backward. For telephony, call setup success, media continuity and latency are stronger SLIs than process uptime alone. The concrete hserver evidence is commit b65d5d4, so this note is tied to an actual production change rather than a hypothetical failure.
