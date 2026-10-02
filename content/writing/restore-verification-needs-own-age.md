---
title: Restore Verification Needs Its Own Age
url: /posts/restore-verification-needs-own-age.html
date: '2026-09-14'
read_time: 1
excerpt: A restore drill that passed months ago does not prove that today's schema,
  credentials and backup format can still be recovered.
topic: observability-monitoring
tags:
- restore-test
- evidence-freshness
- dr
- sre
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Backup & DR · advanced'
outputs:
- url: /posts/restore-verification-needs-own-age.html
  template: cms/templates/posts/posts--restore-verification-needs-own-age.tpl
  source: cms/templates/posts/posts--restore-verification-needs-own-age.json
---

A restore drill that passed months ago does not prove that today's schema, credentials and backup format can still be recovered. The monitoring mistake would be to read one metric in isolation. `hserver_restore_verify_success and last-success timestamp` is useful because it narrows the question, and recovery evidence decays as production changes, so the monitoring system needs to know both the last result and how old that result is.

In software operations this falls under evidence-freshness monitoring. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Set a restore-verification cadence, alert when evidence becomes stale, and rerun after major state-format or deployment changes. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `b65d5d4`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
