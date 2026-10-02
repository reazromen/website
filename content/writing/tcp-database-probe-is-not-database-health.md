---
title: A TCP Database Probe Is Not a Database Health Check
url: /posts/tcp-database-probe-is-not-database-health.html
date: '2026-09-14'
read_time: 1
excerpt: A listening PostgreSQL or Redis port proves that something accepted a TCP
  connection, not that queries, authentication or storage are working correctly.
topic: observability-monitoring
tags:
- postgresql
- blackbox-exporter
- database-monitoring
- health
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Databases · advanced'
outputs:
- url: /posts/tcp-database-probe-is-not-database-health.html
  template: cms/templates/posts/posts--tcp-database-probe-is-not-database-health.tpl
  source: cms/templates/posts/posts--tcp-database-probe-is-not-database-health.json
---

A listening PostgreSQL or Redis port proves that something accepted a TCP connection, not that queries, authentication or storage are working correctly. On hserver the first signal I use for this question is `blackbox TCP probe plus hserver_database_exporter_up`. The hserver dashboards deliberately separate reachability from deep database metrics so a green socket cannot hide a broken query path.

The important part is interpretation rather than collecting another graph. layered dependency monitoring. That gives the metric a specific operational job instead of making it another number on a dashboard.

The practical control is straightforward: Use TCP probes for fast reachability and deep collectors for engine health, then alert differently when the container runs but deep telemetry disappears. This also gives me a repeatable check after deployments, exporter changes, or capacity tuning.

Repository evidence for this monitoring behavior is commit `b65d5d4`. I keep that reference with the note because a monitoring conclusion is stronger when the configuration and runtime decision that produced it can be inspected later.
