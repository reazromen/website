---
title: Small Teams Still Need Production Discipline
url: /posts/small-teams-still-need-production-discipline.html
date: '2024-03-25'
read_time: 1
excerpt: Team size changes process weight, not the need for rollback, observability
  and ownership.
topic: devops-culture
tags:
- small-team
- production
- culture
draft: false
featured: false
language: en
eyebrow: 'DevOps Culture: Ownership & Collaboration · advanced'
outputs:
- url: /posts/small-teams-still-need-production-discipline.html
  template: cms/templates/posts/posts--small-teams-still-need-production-discipline.tpl
  source: cms/templates/posts/posts--small-teams-still-need-production-discipline.json
---

It is tempting to treat production discipline as something for large organizations with dedicated SRE and platform departments. Small teams actually have less spare attention when something breaks.

The hserver environment runs on modest hardware, but changes still use backups, Git revisions, health checks and recovery evidence. LOUP firmware work preserves known-good releases because a tiny team cannot afford to rediscover a working audio path after every regression.

DevOps culture scales down by reducing ceremony while preserving invariants. A two-person team may not need a change advisory board, but it still needs to know how to undo a risky change.

Process should be proportional, not absent. The smallest team benefits most from automation that protects scarce engineering time and reduces avoidable rediscovery during incidents.

## Engineering evidence

Repository/project evidence for this note: `49fc6ca`. The point is the operating model behind the change, not the commit number itself.
