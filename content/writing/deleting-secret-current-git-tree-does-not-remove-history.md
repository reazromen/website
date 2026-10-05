---
title: Deleting a Secret from the Current Git Tree Does Not Remove It from History
url: /posts/deleting-secret-current-git-tree-does-not-remove-history.html
date: '2025-03-06'
read_time: 1
excerpt: Production readiness has to treat leaked credentials as compromised even
  after the file disappears from the latest commit.
topic: security-secrets
tags:
- git
- secrets
- rotation
- incident-response
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Permissions and Secrets · advanced'
outputs:
- url: /posts/deleting-secret-current-git-tree-does-not-remove-history.html
  template: cms/templates/posts/posts--deleting-secret-current-git-tree-does-not-remove-history.tpl
  source: cms/templates/posts/posts--deleting-secret-current-git-tree-does-not-remove-history.json
---

The production-readiness audit forced a distinction that is easy to skip during cleanup: removing a credential from the current branch does not erase earlier commits, clones, caches or CI artifacts that may still contain it.

OWASP secrets guidance recommends centralizing, auditing and rotating credentials while applying least privilege. Incident response should treat exposure as a credential-lifecycle event, not just a repository hygiene event. The mistake is treating source-control deletion as credential revocation. Once a secret enters version history, the security question is no longer whether the latest tree contains it, but whether any unauthorized copy can still authenticate.

The readiness policy now requires rotation of any credential that appeared in Git history and separates secret material from version-controlled configuration. Git keeps policy and references; runtime secret stores keep secret values.

Pre-commit scanning, CI secret detection and documented rotation procedures reduce recurrence. More importantly, application design should make rotation routine enough that a suspected leak does not become a high-risk emergency change. The concrete hserver evidence is commit 9d36c75, so this note is tied to an actual production change rather than a hypothetical failure.
