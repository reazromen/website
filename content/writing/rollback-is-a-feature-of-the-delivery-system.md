---
title: Rollback Is a Feature of the Delivery System
url: /posts/rollback-is-a-feature-of-the-delivery-system.html
date: '2024-12-16'
read_time: 1
excerpt: A rollback plan has to exist before deployment and be exercised by the same
  system that performs forward changes.
topic: devops-culture
tags:
- rollback
- delivery
- resilience
draft: false
featured: false
language: en
eyebrow: 'DevOps Culture: Delivery & Reliability · advanced'
outputs:
- url: /posts/rollback-is-a-feature-of-the-delivery-system.html
  template: cms/templates/posts/posts--rollback-is-a-feature-of-the-delivery-system.tpl
  source: cms/templates/posts/posts--rollback-is-a-feature-of-the-delivery-system.json
---

Rollback is often written as the final bullet in a runbook even though it should shape the deployment from the beginning.

hserver changes preserve previous configuration, database backups and source revisions before mutation. LOUP OTA explicitly models accepted and trial firmware slots so a failed image can return to a known-good release without an emergency reflashing session.

This is reversible delivery. The team designs data compatibility, artifacts and state transitions around the possibility that the new version will not be accepted.

A culture that plans rollback early is admitting uncertainty in a productive way: every release is a hypothesis until production evidence confirms it.

## Engineering evidence

Repository/project evidence for this note: `35d63b8`. The point is the operating model behind the change, not the commit number itself.
