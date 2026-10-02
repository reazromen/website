---
title: Deployment Is Not Acceptance
url: /posts/deployment-is-not-acceptance.html
date: '2026-09-14'
read_time: 1
excerpt: Applying a change and proving it works are separate milestones that need
  separate evidence.
topic: devops-culture
tags:
- deployment
- acceptance
- production
draft: false
featured: false
language: en
eyebrow: 'DevOps Culture: Delivery & Reliability · advanced'
outputs:
- url: /posts/deployment-is-not-acceptance.html
  template: cms/templates/posts/posts--deployment-is-not-acceptance.tpl
  source: cms/templates/posts/posts--deployment-is-not-acceptance.json
---

Many systems use “deployed” as a synonym for “done.” That collapses two different events: the system accepted a change, and the change actually satisfies production requirements.

hserver acceptance checks live health, backups, restore posture, security boundaries and rollback evidence after deployment. LOUP OTA has an even clearer distinction: firmware can boot in a trial state and still fail acceptance before becoming permanent.

This separation creates a healthier delivery culture because success is defined by observed behavior rather than by completion of the automation step.

A production change should earn acceptance with evidence; it should not inherit acceptance merely because the deploy command returned zero.

## Engineering evidence

Repository/project evidence for this note: `9d36c75`. The point is the operating model behind the change, not the commit number itself.
