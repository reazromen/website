---
title: Secrets Are Part of Disaster Recovery Even When They Are Correctly Missing
  from Git
url: /posts/secrets-are-part-of-disaster-recovery-even-when-missing-from-git.html
date: '2026-09-14'
read_time: 1
excerpt: Separating secrets from source control creates a recovery dependency that
  must be documented and tested.
topic: disaster-recovery
tags:
- secrets
- dr
- gitops
- recovery
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Permissions and Secrets · advanced'
outputs:
- url: /posts/secrets-are-part-of-disaster-recovery-even-when-missing-from-git.html
  template: cms/templates/posts/posts--secrets-are-part-of-disaster-recovery-even-when-missing-from-git.tpl
  source: cms/templates/posts/posts--secrets-are-part-of-disaster-recovery-even-when-missing-from-git.json
---

The hserver source-of-truth model correctly keeps secret values out of Git, but that creates an important recovery question: a clean checkout can recreate configuration without recreating credentials, encryption keys or private certificates.

OpenGitOps separates versioned desired state from mutable runtime state, while OWASP recommends centralized secret lifecycle management. Recovery planning has to bridge those two models without collapsing them into one insecure repository. Desired state and confidential state have different storage requirements. Treating Git as the only recovery source would make a security best practice become a disaster-recovery failure.

Service records now distinguish Git-owned configuration, runtime data paths and secret locations. Backup classes and restore procedures cover the state that version control intentionally excludes.

Every production service should be reconstructable from three documented inputs: reviewed configuration, controlled secrets and restored persistent state. If one of those inputs has no owner or restore path, the service is not actually reproducible. The concrete hserver evidence is commit 9d36c75, so this note is tied to an actual production change rather than a hypothetical failure.
