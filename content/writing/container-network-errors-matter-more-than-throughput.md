---
title: Container Network Errors Matter More Than Throughput Alone
url: /posts/container-network-errors-matter-more-than-throughput.html
date: '2020-05-25'
read_time: 1
excerpt: RX and TX graphs looked busy enough, but throughput by itself could not tell
  whether traffic was healthy.
topic: observability-monitoring
tags:
- docker-networking
- drops
- errors
- prometheus
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Docker & Containers · advanced'
outputs:
- url: /posts/container-network-errors-matter-more-than-throughput.html
  template: cms/templates/posts/posts--container-network-errors-matter-more-than-throughput.tpl
  source: cms/templates/posts/posts--container-network-errors-matter-more-than-throughput.json
---

RX and TX graphs looked busy enough, but throughput by itself could not tell whether traffic was healthy. On hserver the first signal I use for this question is `container network RX/TX plus errors and drops`. Errors and drops distinguish normal high traffic from packet loss, interface pressure, queue problems or broken virtual networking.

The important part is interpretation rather than collecting another graph. quality-of-service signal correlation. That gives the metric a specific operational job instead of making it another number on a dashboard.

The practical control is straightforward: Keep traffic rate and error/drop rate on the same dashboard and alert on sustained failures rather than bandwidth volume alone. This also gives me a repeatable check after deployments, exporter changes, or capacity tuning.

Repository evidence for this monitoring behavior is commit `b65d5d4`. I keep that reference with the note because a monitoring conclusion is stronger when the configuration and runtime decision that produced it can be inspected later.
