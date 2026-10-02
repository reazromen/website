---
title: You Build It, You Help Operate It
url: /posts/you-build-it-you-help-operate-it.html
date: '2026-09-14'
read_time: 1
excerpt: DevOps ownership gets real when the team that changes a service also cares
  about its runtime behavior.
topic: devops-culture
tags:
- devops
- ownership
- operations
draft: false
featured: false
language: en
eyebrow: 'DevOps Culture: Ownership & Collaboration · advanced'
outputs:
- url: /posts/you-build-it-you-help-operate-it.html
  template: cms/templates/posts/posts--you-build-it-you-help-operate-it.tpl
  source: cms/templates/posts/posts--you-build-it-you-help-operate-it.json
---

A service is not finished when the merge button turns green. The team that designed the change understands its assumptions better than anyone else, so that knowledge should follow the software into production.

On hserver, deployment work now includes health checks, backup evidence, rollback targets and post-change verification instead of handing a container to a separate invisible operations layer. LOUP follows the same logic: firmware decisions are tied to call quality, OTA behavior and field recovery.

This is the practical meaning of shared ownership. Development and operations remain different skills, but reliability is not somebody else’s queue after release.

The cultural change is small in wording and large in consequence: shipping includes staying responsible for what the system does after shipping.

## Engineering evidence

Repository/project evidence for this note: `9d36c75`. The point is the operating model behind the change, not the commit number itself.
