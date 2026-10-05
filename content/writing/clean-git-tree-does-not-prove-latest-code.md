---
title: A Clean Git Tree Does Not Prove You Deployed the Latest Code
url: /posts/clean-git-tree-does-not-prove-latest-code.html
date: '2024-01-22'
read_time: 1
excerpt: Cleanliness answers whether local tracked files changed; freshness answers
  whether the revision is the one you intended to run.
topic: production-engineering
tags:
- git
- deployment
- clean-tree
- provenance
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Git and Provenance · intermediate'
outputs:
- url: /posts/clean-git-tree-does-not-prove-latest-code.html
  template: cms/templates/posts/posts--clean-git-tree-does-not-prove-latest-code.tpl
  source: cms/templates/posts/posts--clean-git-tree-does-not-prove-latest-code.json
---

The provenance checker reports CLEANLINESS, HEAD, UPSTREAM\_HEAD, BEHIND and AHEAD separately and assigns a warning when the clean checkout diverges from its known upstream ref.

A production checkout can be perfectly clean while sitting several commits behind the reviewed main branch. Conversely, it can be ahead because a local commit was created intentionally or accidentally. Worktree cleanliness and revision alignment are independent dimensions. Treating `git status` as a complete deployment proof collapses them into one misleading signal.

Deployment evidence should be composable rather than binary. Revision identity, uncommitted drift, upstream relation and artifact identity answer different forensic questions.

Store the accepted commit with every deployment record and verify it directly after rollout. Use cleanliness as a guardrail, not as the release identifier. The concrete hserver evidence is commit e7b87ff, so this note is tied to an actual production change rather than a hypothetical failure.
