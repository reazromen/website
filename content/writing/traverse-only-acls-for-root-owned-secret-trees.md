---
title: Traverse-Only ACLs Are Useful When Secrets Live Under Root-Owned Trees
url: /posts/traverse-only-acls-for-root-owned-secret-trees.html
date: '2022-05-10'
read_time: 1
excerpt: A service can be allowed through one protected directory without being allowed
  to inspect the directory itself.
topic: security-secrets
tags:
- acl
- secrets
- linux
- ops-runner
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Permissions and Secrets · advanced'
outputs:
- url: /posts/traverse-only-acls-for-root-owned-secret-trees.html
  template: cms/templates/posts/posts--traverse-only-acls-for-root-owned-secret-trees.tpl
  source: cms/templates/posts/posts--traverse-only-acls-for-root-owned-secret-trees.json
---

A POSIX ACL granted only execute permission on the protected parent to the runner identity. The child directory and token retained their existing restrictive ownership and read rules.

The runner enrollment path exposed a subtle conflict: the root-owned secrets tree should stay opaque, but the dedicated runner still needed to reach one credential below it. Moving the secret into a weaker location would have solved the symptom by weakening the boundary. Traditional owner/group/mode bits were too coarse for this path because the trust requirement was one principal, one path capability and no directory listing. The mismatch was in the authorization model, not the application.

Fine-grained ACLs are appropriate when the base Unix permission model cannot express the intended relationship cleanly. The important engineering step is to document why the exception exists and test it automatically.

We added an explicit validation path for the ACL so future hardening cannot accidentally remove the traverse permission and future convenience changes cannot broaden it into read or write access. The concrete hserver evidence is commit 7c10cbe, so this note is tied to an actual production change rather than a hypothetical failure.
