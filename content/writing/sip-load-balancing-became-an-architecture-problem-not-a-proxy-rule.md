---
title: SIP Load Balancing Became an Architecture Problem, Not a Proxy Rule
url: /posts/sip-load-balancing-became-an-architecture-problem-not-a-proxy-rule.html
date: '2026-08-13'
read_time: 1
excerpt: Once dialog state, media anchoring and backend health mattered, forwarding
  INVITEs round-robin was the easy part.
topic: telecom-voip
tags:
- sip
- drachtio
- freeswitch
- load-balancing
draft: false
featured: false
language: en
eyebrow: 2026 Production Voice Systems · advanced
outputs:
- url: /posts/sip-load-balancing-became-an-architecture-problem-not-a-proxy-rule.html
  template: cms/templates/posts/posts--sip-load-balancing-became-an-architecture-problem-not-a-proxy-rule.tpl
  source: cms/templates/posts/posts--sip-load-balancing-became-an-architecture-problem-not-a-proxy-rule.json
---

The first version of a SIP load balancer can be one rule: pick a backend and send the INVITE there. That proves distribution and almost nothing else.

A production path has to answer what happens to sequential requests, which component owns dialog routing, how failed backends are removed, and whether media stays tied to the same call leg. Health checking new-call capacity is different from moving an established call.

I found it useful to separate the signalling edge from the media/application servers. The edge can own Record-Route and backend selection while FreeSWITCH handles call processing. Media anchoring is another deliberate decision rather than an accidental consequence of whichever server answered first.

The result is more components but fewer hidden assumptions. The architecture becomes testable because each layer has a defined failure mode.
