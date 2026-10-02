---
title: Running Containers Are Not Healthy Containers
url: /posts/running-containers-are-not-healthy-containers.html
date: '2026-09-14'
read_time: 1
excerpt: The Docker daemon can report a container as running even when the application
  inside it has stopped serving useful traffic.
topic: observability-monitoring
tags:
- docker
- healthcheck
- readiness
- grafana
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Docker & Containers · advanced'
outputs:
- url: /posts/running-containers-are-not-healthy-containers.html
  template: cms/templates/posts/posts--running-containers-are-not-healthy-containers.tpl
  source: cms/templates/posts/posts--running-containers-are-not-healthy-containers.json
---

The Docker daemon can report a container as running even when the application inside it has stopped serving useful traffic. On hserver the first signal I use for this question is `container state plus Docker healthcheck state`. Process liveness and application readiness are different contracts; monitoring only the former creates false green dashboards.

The important part is interpretation rather than collecting another graph. liveness-versus-readiness monitoring. That gives the metric a specific operational job instead of making it another number on a dashboard.

The practical control is straightforward: Use healthchecks where the application has a meaningful probe, graph unhealthy counts, and keep external probes for user-visible reachability. This also gives me a repeatable check after deployments, exporter changes, or capacity tuning.

Repository evidence for this monitoring behavior is commit `b65d5d4`. I keep that reference with the note because a monitoring conclusion is stronger when the configuration and runtime decision that produced it can be inspected later.
