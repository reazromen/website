---
title: Critical systemd Units Need Their Own Health Signal
url: /posts/critical-systemd-units-need-health-signal.html
date: '2026-06-08'
read_time: 1
excerpt: Container monitoring does not cover host services such as Docker, networking,
  tunnels, backup timers or other systemd-managed dependencies.
topic: observability-monitoring
tags:
- systemd
- health
- dependencies
- prometheus
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Host & Resource Signals · advanced'
outputs:
- url: /posts/critical-systemd-units-need-health-signal.html
  template: cms/templates/posts/posts--critical-systemd-units-need-health-signal.tpl
  source: cms/templates/posts/posts--critical-systemd-units-need-health-signal.json
---

Container monitoring does not cover host services such as Docker, networking, tunnels, backup timers or other systemd-managed dependencies. What made the issue measurable was `hserver_systemd_unit_active and hserver_systemd_unit_failed`. A healthy container stack can still be unusable when a required host unit is inactive, failed or repeatedly restarting.

I classify this as dependency-aware service monitoring. The useful debugging sequence is to confirm the signal, compare it with the neighboring subsystem, then look at logs or detailed metrics only after the failure domain is smaller.

The production rule that came out of it is: Maintain a reviewed allow-list of critical host units and alert on state changes instead of scraping every systemd unit indiscriminately. This is deliberately more specific than adding another broad alert with no response procedure.

Commit `b65d5d4` is the repository evidence behind the note. It provides the concrete configuration or fix that turned the observation into a repeatable monitoring control.
