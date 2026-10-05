---
title: FreeSWITCH Session Counts Need Per-Node Breakdown
url: /posts/freeswitch-session-counts-per-node.html
date: '2025-02-03'
read_time: 1
excerpt: A healthy total session count can hide a load-balancing problem if one FreeSWITCH
  node carries nearly all calls while another remains idle.
topic: observability-monitoring
tags:
- freeswitch
- sessions
- load-balancing
- grafana
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: VoIP · advanced'
outputs:
- url: /posts/freeswitch-session-counts-per-node.html
  template: cms/templates/posts/posts--freeswitch-session-counts-per-node.tpl
  source: cms/templates/posts/posts--freeswitch-session-counts-per-node.json
---

A healthy total session count can hide a load-balancing problem if one FreeSWITCH node carries nearly all calls while another remains idle. What made the issue measurable was `FreeSWITCH sessions by node`. Per-node distribution reveals skew, draining problems and backend selection bias that aggregate call totals cannot show.

I classify this as load-distribution monitoring. The useful debugging sequence is to confirm the signal, compare it with the neighboring subsystem, then look at logs or detailed metrics only after the failure domain is smaller.

The production rule that came out of it is: Graph sessions and idle CPU per worker and compare them during steady traffic before changing balancing weights. This is deliberately more specific than adding another broad alert with no response procedure.

Commit `b65d5d4` is the repository evidence behind the note. It provides the concrete configuration or fix that turned the observation into a repeatable monitoring control.
