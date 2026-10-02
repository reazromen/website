---
title: Production Infrastructure Became Easier Once Git, Runtime State and Secrets
  Had Different Jobs
url: /posts/production-infrastructure-became-easier-once-git-runtime-state-and-secrets-had-different-jobs.html
date: '2026-09-14'
read_time: 1
excerpt: Most operational confusion came from mixing desired configuration, live state
  and credentials into the same place.
topic: linux-homelab
tags:
- gitops
- secrets
- docker
- operations
draft: false
featured: false
language: en
eyebrow: 2026 Production Voice Systems · advanced
outputs:
- url: /posts/production-infrastructure-became-easier-once-git-runtime-state-and-secrets-had-different-jobs.html
  template: cms/templates/posts/posts--production-infrastructure-became-easier-once-git-runtime-state-and-secrets-had-different-jobs.tpl
  source: cms/templates/posts/posts--production-infrastructure-became-easier-once-git-runtime-state-and-secrets-had-different-jobs.json
---

The server became much easier to operate once I stopped asking one directory to be the source of truth for everything.

Git is good at reviewed desired state: compose files, scripts, runbooks, migrations and documentation. Runtime volumes are good at mutable service state. Secrets need their own control plane and permissions. Backups have to cover the state that Git intentionally does not.

This separation changed deployment work. Before changing a service I can read the repository, inspect live state, take the required backup, apply the reproducible change, verify health, and then record what happened. A future operator does not need to reconstruct the server from shell history.

It also makes disaster recovery testable. Configuration can be checked out, secrets can be restored through a controlled path, and databases or service volumes can be recovered independently. The server is still small hardware, but the operational model no longer depends on remembering what I did last week.
