---
title: Volume Reference Counts Help Detect Orphaned Docker State
url: /posts/volume-reference-counts-detect-orphans.html
date: '2026-09-14'
read_time: 1
excerpt: Old Docker volumes can consume storage after services are removed, and their
  names alone do not always reveal whether anything still depends on them.
topic: observability-monitoring
tags:
- docker-volumes
- inventory
- cleanup
- storage
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Backup & DR · advanced'
outputs:
- url: /posts/volume-reference-counts-detect-orphans.html
  template: cms/templates/posts/posts--volume-reference-counts-detect-orphans.tpl
  source: cms/templates/posts/posts--volume-reference-counts-detect-orphans.json
---

Old Docker volumes can consume storage after services are removed, and their names alone do not always reveal whether anything still depends on them. The monitoring mistake would be to read one metric in isolation. `Docker volume size plus reference-count inventory` is useful because it narrows the question, and reference counts distinguish active persistent state from likely orphaned volumes and make cleanup review safer.

In software operations this falls under inventory-assisted storage monitoring. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Show size and attachment count together, then verify ownership and backup status before deleting any unreferenced volume. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `218300b`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
