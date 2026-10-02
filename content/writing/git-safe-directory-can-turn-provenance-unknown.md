---
title: Git safe.directory Can Turn Provenance into UNKNOWN
url: /posts/git-safe-directory-can-turn-provenance-unknown.html
date: '2026-09-14'
read_time: 1
excerpt: A production checkout owned by another identity can be readable on disk while
  Git refuses to trust it.
topic: production-engineering
tags:
- git
- safe-directory
- provenance
- permissions
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Git and Provenance · advanced'
outputs:
- url: /posts/git-safe-directory-can-turn-provenance-unknown.html
  template: cms/templates/posts/posts--git-safe-directory-can-turn-provenance-unknown.tpl
  source: cms/templates/posts/posts--git-safe-directory-can-turn-provenance-unknown.json
---

The deployment-provenance job needed to inspect a production checkout from a restricted operator context. Git's ownership safety rules could reject the repository even though the files were intentionally readable.

Filesystem access and Git repository trust are separate controls. The script assumed that being able to open `.git` meant commands such as `status` and `rev-parse` would behave normally. The checker invokes Git with an explicit `safe.directory` for the reviewed repository path and handles each metadata query independently so one permission issue does not erase all revision evidence.

Observability code should respect security controls instead of disabling them globally. Narrow exceptions are better than changing system-wide Git trust just to make one probe pass. Run provenance checks under the same least-privilege identity used in production and include ownership variations in regression tests. The concrete hserver evidence is commit e7b87ff, so this note is tied to an actual production change rather than a hypothetical failure.
