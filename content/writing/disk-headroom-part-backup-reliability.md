---
title: Disk Headroom Is Part of Backup Reliability
url: /posts/disk-headroom-part-backup-reliability.html
date: '2022-01-23'
read_time: 1
excerpt: A backup process can be perfectly configured and still fail when the destination
  filesystem no longer has enough capacity for the next archive.
topic: observability-monitoring
tags:
- disk-capacity
- backup
- retention
- reliability
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Backup & DR · advanced'
outputs:
- url: /posts/disk-headroom-part-backup-reliability.html
  template: cms/templates/posts/posts--disk-headroom-part-backup-reliability.tpl
  source: cms/templates/posts/posts--disk-headroom-part-backup-reliability.json
---

A backup process can be perfectly configured and still fail when the destination filesystem no longer has enough capacity for the next archive. I ended up treating `root disk usage combined with backup size trend` as the useful observation point rather than relying on a generic service-up indicator. Backup reliability depends on future free space, not only the health of the backup command at the previous run.

This is a good example of capacity-aware reliability monitoring. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Compare expected next backup size with filesystem headroom and retention policy so cleanup happens before the job reaches ENOSPC. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `b65d5d4` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
