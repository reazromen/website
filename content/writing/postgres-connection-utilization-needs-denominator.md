---
title: PostgreSQL Connection Utilization Needs a Denominator
url: /posts/postgres-connection-utilization-needs-denominator.html
date: '2023-02-12'
read_time: 1
excerpt: A count of sixty active PostgreSQL connections is meaningless until it is
  compared with the configured maximum for that server.
topic: observability-monitoring
tags:
- postgresql
- connections
- capacity
- prometheus
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Databases · advanced'
outputs:
- url: /posts/postgres-connection-utilization-needs-denominator.html
  template: cms/templates/posts/posts--postgres-connection-utilization-needs-denominator.tpl
  source: cms/templates/posts/posts--postgres-connection-utilization-needs-denominator.json
---

A count of sixty active PostgreSQL connections is meaningless until it is compared with the configured maximum for that server. I ended up treating `hserver_postgres_connections divided by hserver_postgres_max_connections` as the useful observation point rather than relying on a generic service-up indicator. Connection pressure is a capacity ratio, which is why the alert triggers when usage remains above eighty percent instead of on an arbitrary raw count.

This is a good example of capacity-ratio alerting. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Track utilization by database and investigate pool sizing, leaked sessions and traffic growth before simply raising `max_connections`. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `b65d5d4` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
