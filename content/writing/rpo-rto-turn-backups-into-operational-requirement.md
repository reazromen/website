---
title: RPO and RTO Turn 'We Have Backups' into an Operational Requirement
url: /posts/rpo-rto-turn-backups-into-operational-requirement.html
date: '2024-01-19'
read_time: 1
excerpt: Recovery planning becomes actionable when data-loss tolerance and recovery-time
  tolerance are explicit.
topic: disaster-recovery
tags:
- rpo
- rto
- backup
- sre
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Backup and DR · intermediate'
outputs:
- url: /posts/rpo-rto-turn-backups-into-operational-requirement.html
  template: cms/templates/posts/posts--rpo-rto-turn-backups-into-operational-requirement.tpl
  source: cms/templates/posts/posts--rpo-rto-turn-backups-into-operational-requirement.json
---

RPO expresses tolerable data loss and RTO expresses tolerable recovery time. These objectives let engineering choose backup cadence, off-host frequency and automation based on service impact. Different hserver services have very different state: OTA artifacts, PostgreSQL control planes, dashboards, session state and source code. A single statement that 'the server is backed up' hides how much data each service could lose and how quickly it must return. Backup frequency and restore effort had no common decision language without recovery objectives.

The production maturity plan ties backup classes, retention and restore drills to service criticality and calls for recorded recovery duration rather than assuming all state is equally urgent. Assign RPO/RTO targets per stateful service and verify them during drills. A backup design is successful only when its measured recovery behavior meets the objective it was intended to support. The concrete hserver evidence is commit 9d36c75, so this note is tied to an actual production change rather than a hypothetical failure.
