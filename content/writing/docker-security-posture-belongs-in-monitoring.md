---
title: Docker Security Posture Belongs in Monitoring
url: /posts/docker-security-posture-belongs-in-monitoring.html
date: '2025-08-28'
read_time: 1
excerpt: Privileged containers, Docker socket mounts, root users and published ports
  are configuration facts that can silently drift after deployment.
topic: observability-monitoring
tags:
- docker
- security-posture
- configuration-drift
- inventory
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Docker & Containers · advanced'
outputs:
- url: /posts/docker-security-posture-belongs-in-monitoring.html
  template: cms/templates/posts/posts--docker-security-posture-belongs-in-monitoring.tpl
  source: cms/templates/posts/posts--docker-security-posture-belongs-in-monitoring.json
---

Privileged containers, Docker socket mounts, root users and published ports are configuration facts that can silently drift after deployment. What made the issue measurable was `inventory-exporter security-sensitive container metadata`. Security posture is operational state, not only a code-review property; the running daemon may differ from the intended Compose model.

I classify this as continuous configuration monitoring. The useful debugging sequence is to confirm the signal, compare it with the neighboring subsystem, then look at logs or detailed metrics only after the failure domain is smaller.

The production rule that came out of it is: Track privileged mode, socket mounts, root users, capabilities, devices and published ports as reviewable metrics and dashboard tables. This is deliberately more specific than adding another broad alert with no response procedure.

Commit `b65d5d4` is the repository evidence behind the note. It provides the concrete configuration or fix that turned the observation into a repeatable monitoring control.
