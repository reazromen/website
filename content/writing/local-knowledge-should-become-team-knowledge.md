---
title: Local Knowledge Should Become Team Knowledge
url: /posts/local-knowledge-should-become-team-knowledge.html
date: '2026-09-14'
read_time: 1
excerpt: A production fix is incomplete until the reasoning can survive outside the
  engineer who discovered it.
topic: devops-culture
tags:
- knowledge
- runbook
- automation
draft: false
featured: false
language: en
eyebrow: 'DevOps Culture: Ownership & Collaboration · advanced'
outputs:
- url: /posts/local-knowledge-should-become-team-knowledge.html
  template: cms/templates/posts/posts--local-knowledge-should-become-team-knowledge.tpl
  source: cms/templates/posts/posts--local-knowledge-should-become-team-knowledge.json
---

Every system accumulates details that initially exist only in someone’s head: why a port is unusual, which release is known-good, or which restart order avoids corruption.

The response should not be to eliminate expertise but to externalize it. Recent hserver work turns local knowledge into source-ownership files, runbooks and acceptance scripts; LOUP turns it into preserved binaries, measurements and release markers.

This is a DevOps knowledge-management habit: capture the decision, evidence and recovery path at the moment they are fresh, before context decays into guesswork.

The team becomes more resilient when production can be understood from artifacts rather than oral tradition, especially during recovery when the original engineer may be unavailable.

## Engineering evidence

Repository/project evidence for this note: `cf2a467`. The point is the operating model behind the change, not the commit number itself.
