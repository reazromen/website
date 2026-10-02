---
title: Reconciling Concurrent Git Changes Without Force Push
url: /posts/reconcile-concurrent-git-changes-without-force-push.html
date: '2026-09-14'
read_time: 1
excerpt: Production work continued in multiple streams, so safe synchronization had
  to preserve both histories rather than overwrite whichever side moved first.
topic: production-engineering
tags:
- git
- merge
- production
- change-management
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Git and Provenance · advanced'
outputs:
- url: /posts/reconcile-concurrent-git-changes-without-force-push.html
  template: cms/templates/posts/posts--reconcile-concurrent-git-changes-without-force-push.tpl
  source: cms/templates/posts/posts--reconcile-concurrent-git-changes-without-force-push.json
---

We fetched the remote state on the authorized workstation, merged the independent work, pushed normally to GitHub, then transferred the merged revision back to hserver and fast-forwarded the production source tree.

While blog, observability, OpenBao and authentication work were landing, GitHub main and the hserver checkout could advance independently. A naive push from either side risked rejecting changes or encouraging a force push. There were legitimate concurrent histories rather than one obviously disposable branch. The task was reconciliation, not replacement.

This is conservative change integration: preserve reviewed history, resolve conflicts explicitly and avoid force when the divergence represents real work. Production Git should optimize for traceability over convenience.

Fetch before deployment, keep production changes committed in small units, and use temporary reconciliation branches or bundles when the server lacks direct repository credentials. The concrete hserver evidence is commit cf2a467, so this note is tied to an actual production change rather than a hypothetical failure.
