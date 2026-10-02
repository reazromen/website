---
title: Git, Runtime State and Secrets Need Different Jobs
url: /posts/git-runtime-state-secrets-different-jobs.html
date: '2026-09-14'
read_time: 1
excerpt: Operational confusion falls when desired configuration, mutable data and
  confidential values stop competing to be one source of truth.
topic: production-engineering
tags:
- gitops
- state
- secrets
- architecture
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Git and Provenance · advanced'
outputs:
- url: /posts/git-runtime-state-secrets-different-jobs.html
  template: cms/templates/posts/posts--git-runtime-state-secrets-different-jobs.tpl
  source: cms/templates/posts/posts--git-runtime-state-secrets-different-jobs.json
---

As hserver accumulated databases, dashboards, OTA artifacts, credentials and Compose definitions, a single 'server folder' mental model stopped working. Some state must change continuously, some must be reviewed, and some must never enter source control.

The categories have different lifecycle semantics. Git is excellent for versioned desired state; databases and volumes hold mutable runtime state; secret stores control confidential material. The production model documents these boundaries and gives backup responsibilities to the data and secrets that Git intentionally does not contain.

OpenGitOps centers versioned desired state and reconciliation. Twelve-Factor separates deploy-specific configuration from code, while secrets guidance adds restricted lifecycle management for credentials. For every file or datum, decide which class it belongs to and who owns recovery. Ambiguous state is where manual drift and accidental secret commits usually begin. The concrete hserver evidence is commit 9d36c75, so this note is tied to an actual production change rather than a hypothetical failure.
