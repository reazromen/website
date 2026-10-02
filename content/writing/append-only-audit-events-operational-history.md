---
title: Append-Only Audit Events Make Operational History Harder to Rewrite
url: /posts/append-only-audit-events-operational-history.html
date: '2026-09-14'
read_time: 1
excerpt: Control-plane actions are easier to trust when later updates cannot silently
  replace the original event record.
topic: web-control-plane
tags:
- audit
- append-only
- operations
- security
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Safe Automation · advanced'
outputs:
- url: /posts/append-only-audit-events-operational-history.html
  template: cms/templates/posts/posts--append-only-audit-events-operational-history.tpl
  source: cms/templates/posts/posts--append-only-audit-events-operational-history.json
---

The portal records approvals, executions and state changes that may be needed during incident review. If those rows were casually editable, the same interface that performs an action could also rewrite the evidence of that action.

Operational data and operational history have different mutation requirements. Current state changes; historical evidence should normally accumulate. The control plane uses append-only audit events and CI verifies audit immutability behavior alongside database least privilege.

Event logs are strongest when they preserve original facts and corrections appear as new events rather than destructive edits. That supports forensic reconstruction and accountability. Restrict update/delete permissions on audit tables, include actor and object identifiers, and test that ordinary application roles cannot rewrite historical rows. The concrete hserver evidence is commit 9e6f8a5, so this note is tied to an actual production change rather than a hypothetical failure.
