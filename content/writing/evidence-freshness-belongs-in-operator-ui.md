---
title: Evidence Freshness Belongs in the Operator UI
url: /posts/evidence-freshness-belongs-in-operator-ui.html
date: '2021-08-26'
read_time: 1
excerpt: A production acceptance result should carry age and policy, not just a green
  badge.
topic: web-control-plane
tags:
- sre
- evidence
- ops-portal
- freshness
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Observability · advanced'
outputs:
- url: /posts/evidence-freshness-belongs-in-operator-ui.html
  template: cms/templates/posts/posts--evidence-freshness-belongs-in-operator-ui.tpl
  source: cms/templates/posts/posts--evidence-freshness-belongs-in-operator-ui.json
---

The portal gained per-check freshness policies, calculated age, states such as CURRENT, STALE and IN\_PROGRESS, and separate criticality rules for failed evidence.

The Command Center stored results for production posture, backups, DR, security and endpoint health, but the operator still had to infer whether an old success was recent enough for the current change window. The evidence model recorded status without fully encoding its useful lifetime. Different checks also have different freshness requirements: endpoint health can age quickly while backup evidence may remain valid for many hours.

This is policy-based observability. SRE systems should present both the result and the confidence context around that result, including when it was collected and how long it remains actionable.

Safety gates should consume freshness-aware evidence directly instead of relying on humans to remember timing rules. An old PASS must automatically decay into STALE when its evidence budget expires. The concrete hserver evidence is commit 3387a0e, so this note is tied to an actual production change rather than a hypothetical failure.
