---
title: Automation Needs a Permission Model
url: /posts/automation-needs-a-permission-model.html
date: '2026-09-14'
read_time: 1
excerpt: Automation should be fast inside a narrow authority boundary rather than
  powerful enough to mutate anything.
topic: devops-culture
tags:
- automation
- least-privilege
- operations
draft: false
featured: false
language: en
eyebrow: 'DevOps Culture: Delivery & Reliability · advanced'
outputs:
- url: /posts/automation-needs-a-permission-model.html
  template: cms/templates/posts/posts--automation-needs-a-permission-model.tpl
  source: cms/templates/posts/posts--automation-needs-a-permission-model.json
---

The easiest automation to build is a script with broad credentials and arbitrary shell access. It is also the hardest automation to trust.

The hserver Operations model uses reviewed jobs, bounded commands, explicit risk levels and narrow runner permissions instead of exposing a generic remote terminal through the portal. OpenBao machine identities follow the same idea with path-scoped policies.

DevOps culture values automation, but mature automation includes authorization, audit and failure containment. Removing manual work should not remove control.

The useful question is not whether a task can be automated; it is what minimum authority the automation requires to perform that task safely.

## Engineering evidence

Repository/project evidence for this note: `9e6f8a5`. The point is the operating model behind the change, not the commit number itself.
