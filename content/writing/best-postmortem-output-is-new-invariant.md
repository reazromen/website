---
title: The Best Postmortem Output Is a New Invariant
url: /posts/best-postmortem-output-is-new-invariant.html
date: '2026-09-14'
read_time: 1
excerpt: Fixing one incident is useful; changing the system so the same class of failure
  becomes detectable or impossible is more valuable.
topic: production-engineering
tags:
- postmortem
- sre
- invariant
- continuous-improvement
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Production Acceptance · advanced'
outputs:
- url: /posts/best-postmortem-output-is-new-invariant.html
  template: cms/templates/posts/posts--best-postmortem-output-is-new-invariant.tpl
  source: cms/templates/posts/posts--best-postmortem-output-is-new-invariant.json
---

The recent hserver history contains many small fixes: a permission, a stale heartbeat result, a wrong container name, a missing timeout, a bad HTML entity and a CSP omission. The useful pattern is what happened after each fix.

Google SRE postmortem culture focuses on learning and systemic corrective action rather than blame. A strong action item changes a process, test or design constraint that prevents recurrence. A patch only repairs the observed instance. Without a guardrail, the organization keeps paying for the same reasoning again under a slightly different symptom. The fixes were followed by CI checks, source-ownership rules, freshness policies, explicit state-machine invariants, permission validation and reproducible runbooks.

For every incident, ask what invariant was missing, where it can be enforced automatically and what evidence will prove the new control still works six months later. The concrete hserver evidence is commit 9d36c75, so this note is tied to an actual production change rather than a hypothetical failure.
