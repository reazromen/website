---
title: A Restore Alert Should Distinguish Failed from Stale
url: /posts/restore-alert-failed-vs-stale.html
date: '2026-09-14'
read_time: 1
excerpt: No recent restore verification and a recent restore verification that actively
  failed are both bad, but they communicate different operational urgency.
topic: observability-monitoring
tags:
- restore-verification
- freshness
- alert-semantics
- dr
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Backup & DR · advanced'
outputs:
- url: /posts/restore-alert-failed-vs-stale.html
  template: cms/templates/posts/posts--restore-alert-failed-vs-stale.tpl
  source: cms/templates/posts/posts--restore-alert-failed-vs-stale.json
---

No recent restore verification and a recent restore verification that actively failed are both bad, but they communicate different operational urgency. What made the issue measurable was `restore success state plus verification age`. Failure means current evidence says recovery is broken; staleness means confidence has expired because the test is too old.

I classify this as typed evidence states. The useful debugging sequence is to confirm the signal, compare it with the neighboring subsystem, then look at logs or detailed metrics only after the failure domain is smaller.

The production rule that came out of it is: Represent PASS, FAIL and STALE separately so dashboards and paging policies can guide the right response instead of flattening everything to red. This is deliberately more specific than adding another broad alert with no response procedure.

Commit `3387a0e` is the repository evidence behind the note. It provides the concrete configuration or fix that turned the observation into a repeatable monitoring control.
