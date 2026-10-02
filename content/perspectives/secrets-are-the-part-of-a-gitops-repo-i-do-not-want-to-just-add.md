---
title: Secrets Are the Part of a GitOps Repo I Do Not Want to “Just Add”
url: /posts/secrets-are-the-part-of-a-gitops-repo-i-do-not-want-to-just-add.html
date: '2026-09-18'
read_time: 2
excerpt: How to think about credentials when application manifests are intentionally
  stored in Git.
topic: voiceware-engineering
tags:
- voiceware
- secrets
- security
- gitops
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Operations & Lessons · deep-dive'
outputs:
- url: /posts/secrets-are-the-part-of-a-gitops-repo-i-do-not-want-to-just-add.html
  template: cms/templates/posts/posts--secrets-are-the-part-of-a-gitops-repo-i-do-not-want-to-just-add.tpl
  source: cms/templates/posts/posts--secrets-are-the-part-of-a-gitops-repo-i-do-not-want-to-just-add.json
---

The security issue here is not exotic. It is the interaction between **how to think about credentials when application manifests are intentionally stored in Git** and a deployment model where Git intentionally stores desired state.

## Threat model

In that first pass I covered application configuration, but I had not built a complete secret-management workflow into the manifests.

A GitOps repository is designed to be copied, reviewed, indexed by tooling, and consumed automatically. Those are strengths for configuration and liabilities for raw credentials.

## What I do not want

Putting raw credentials into the same repository that drives deployment creates a high-impact leakage path.

Plaintext credentials also create a rotation problem: removing the current value from the latest commit does not necessarily remove it from history, clones, caches, CI logs, or backups.

## Safer design

I want Git to reference the existence and usage of a secret without becoming the plaintext secret store. The exact mechanism can be an external secret manager, encrypted-secret workflow, or another controlled system, but the trust boundary should be explicit.

```
change -> review -> deploy -> observe -> diagnose -> recover -> document
```

## Operational implications

The secret path has to support rotation, environment separation, audit, recovery, and least privilege. It also has to fail clearly. A pod stuck because a secret cannot be materialized should be distinguishable from an application crash or image-pull problem.

What this came down to was this: Putting raw credentials into the same repository that drives deployment creates a high-impact leakage path. From that I kept one rule: Use a dedicated secret-management approach and keep the desired-state workflow without storing plaintext secrets.

## Security checklist

- Keep secrets out of plaintext Git.
- Document what is implemented versus what remains a hardening next step.
- Change one layer at a time during migration.
- Review infrastructure by blast radius, not line count.
- Define rollback before the risky change.

My security rule is **Use a dedicated secret-management approach and keep the desired-state workflow without storing plaintext secrets.** That lesson has been more reusable for me than any particular YAML pattern.
