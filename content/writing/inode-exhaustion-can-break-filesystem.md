---
title: Inode Exhaustion Can Break a Filesystem with Free Gigabytes
url: /posts/inode-exhaustion-can-break-filesystem.html
date: '2026-04-02'
read_time: 1
excerpt: Free-space graphs can remain green while a workload creates huge numbers
  of tiny files and consumes the available inode table.
topic: observability-monitoring
tags:
- inodes
- filesystem
- capacity
- linux
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Storage & I/O · advanced'
outputs:
- url: /posts/inode-exhaustion-can-break-filesystem.html
  template: cms/templates/posts/posts--inode-exhaustion-can-break-filesystem.tpl
  source: cms/templates/posts/posts--inode-exhaustion-can-break-filesystem.json
---

Free-space graphs can remain green while a workload creates huge numbers of tiny files and consumes the available inode table. I ended up treating `node_filesystem_files_free and inode-usage panels` as the useful observation point rather than relying on a generic service-up indicator. Byte capacity and object-count capacity are separate resources; exhausting either can prevent file creation and break applications.

This is a good example of multi-dimensional filesystem capacity monitoring. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Alert on inode percentage independently from disk bytes and investigate log, cache or spool directories when inode growth accelerates. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `b65d5d4` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
