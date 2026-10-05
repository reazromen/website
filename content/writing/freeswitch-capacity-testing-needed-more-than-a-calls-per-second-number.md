---
title: FreeSWITCH Capacity Testing Needed More Than a Calls-Per-Second Number
url: /posts/freeswitch-capacity-testing-needed-more-than-a-calls-per-second-number.html
date: '2025-09-09'
read_time: 1
excerpt: Call setup rate, concurrent calls and media work stress different parts of
  a voice platform.
topic: telecom-voip
tags:
- freeswitch
- capacity
- sipp
- performance
draft: false
featured: false
language: en
eyebrow: 2025 Voice and Infrastructure Notes · advanced
outputs:
- url: /posts/freeswitch-capacity-testing-needed-more-than-a-calls-per-second-number.html
  template: cms/templates/posts/posts--freeswitch-capacity-testing-needed-more-than-a-calls-per-second-number.tpl
  source: cms/templates/posts/posts--freeswitch-capacity-testing-needed-more-than-a-calls-per-second-number.json
---

Calls per second is an attractive benchmark because it produces one number. It can also hide the resource that actually limits the system.

A signalling-only call that connects and clears quickly stresses transaction processing differently from a ten-minute call with RTP, recording or transcoding. Concurrent-call capacity depends on memory, sockets and media work. CPS depends heavily on setup-path CPU and database or application latency.

I started defining scenarios before measuring: registration load, short signalling calls, long pass-through media, codec conversion, and failure bursts. For each scenario I watched CPU, scheduler delay, memory, file descriptors and SIP response distribution.

The useful capacity number is therefore tied to a workload. 'This server handles X CPS' means little unless I know what each call required and what failure threshold defined the end of the test.
