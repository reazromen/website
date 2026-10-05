---
title: A Local Remote-Tracking Ref Can Be Stale While Git Says You Match Upstream
url: /posts/remote-tracking-ref-can-be-stale.html
date: '2024-08-14'
read_time: 1
excerpt: Comparing HEAD with origin/main proves consistency with the last fetched
  view, not with the current remote repository.
topic: production-engineering
tags:
- git
- fetch
- provenance
- drift
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Git and Provenance · advanced'
outputs:
- url: /posts/remote-tracking-ref-can-be-stale.html
  template: cms/templates/posts/posts--remote-tracking-ref-can-be-stale.tpl
  source: cms/templates/posts/posts--remote-tracking-ref-can-be-stale.json
---

Good observability documents the scope of its claim. A check should say exactly what was measured rather than letting a green result imply stronger freshness guarantees than the data supports. The production checker could report that the deployed checkout matched its upstream ref even when no recent network fetch had occurred. The local `origin/main` reference might itself be old.

A remote-tracking branch is cached metadata, not a live query. The comparison was technically correct but easy to overinterpret as proof that the server matched GitHub at that moment.

Provenance output now states that a clean match is against the local remote-tracking ref and may be stale until an explicit fetch. The evidence includes both HEAD and upstream-head values. Record fetch age or perform a controlled fetch in workflows that require remote-current evidence. Keep read-only local checks useful when network access is intentionally unavailable. The concrete hserver evidence is commit 2ca3009, so this note is tied to an actual production change rather than a hypothetical failure.
