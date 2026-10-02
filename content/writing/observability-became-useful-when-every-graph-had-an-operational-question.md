---
title: Observability Became Useful When Every Graph Had an Operational Question
url: /posts/observability-became-useful-when-every-graph-had-an-operational-question.html
date: '2026-09-14'
read_time: 1
excerpt: Dashboards improved once I stopped collecting attractive metrics and started
  collecting evidence for specific failure modes.
topic: linux-homelab
tags:
- prometheus
- grafana
- observability
- linux
draft: false
featured: false
language: en
eyebrow: 2025 Voice and Infrastructure Notes · intermediate
outputs:
- url: /posts/observability-became-useful-when-every-graph-had-an-operational-question.html
  template: cms/templates/posts/posts--observability-became-useful-when-every-graph-had-an-operational-question.tpl
  source: cms/templates/posts/posts--observability-became-useful-when-every-graph-had-an-operational-question.json
---

A dashboard can become a wall of numbers that looks professional and answers nothing. I began deleting panels unless I could state the operational question they answered.

CPU usage matters when I can connect saturation to call processing or packet delay. Memory matters when growth predicts a restart. SIP response codes matter when their distribution changes. RTP statistics matter when they explain audio complaints.

The same rule helped with alerts. 'Container down' is useful for a service that must always run. It is noise for a short-lived migration job. Alerts need an expected state and an action, otherwise they train me to ignore them.

The result was fewer metrics on the main view and more confidence in each one. Deep dashboards still existed, but the front page became a decision surface instead of decoration.
