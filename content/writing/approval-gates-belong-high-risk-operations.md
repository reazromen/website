---
title: Approval Gates Belong on High-Risk Operations, Not Every Button
url: /posts/approval-gates-belong-high-risk-operations.html
date: '2026-09-14'
read_time: 1
excerpt: Blanket approvals create friction; risk-based approvals preserve review where
  it actually reduces danger.
topic: web-control-plane
tags:
- approval
- risk
- change-management
- operations
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Safe Automation · advanced'
outputs:
- url: /posts/approval-gates-belong-high-risk-operations.html
  template: cms/templates/posts/posts--approval-gates-belong-high-risk-operations.tpl
  source: cms/templates/posts/posts--approval-gates-belong-high-risk-operations.json
---

The Operations Portal had to support both harmless read-only checks and future mutating actions. Requiring manual approval for every posture check would make operators avoid the system, while auto-running destructive work would defeat the control plane.

This is risk-based change control. Controls work better when they are proportional to consequence and do not create unnecessary toil around observation-only tasks. The authorization model needed to distinguish operational risk, not just user role. Different jobs have different blast radius and reversibility.

Job definitions carry a risk level and `approval_required` flag. LOW-risk read-only checks can run directly, while higher-risk operations can be routed through explicit approval.

Review risk classification with each job change and include rollback or recovery expectations for mutating jobs before they are enabled. The concrete hserver evidence is commit 9e6f8a5, so this note is tied to an actual production change rather than a hypothetical failure.
