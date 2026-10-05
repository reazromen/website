---
title: STABLE Should Mean a Device Actually Ran the Release
url: /posts/stable-should-mean-device-actually-ran-release.html
date: '2025-02-26'
read_time: 1
excerpt: A release should not become stable merely because an administrator clicked
  a promotion button.
topic: ota-fleet
tags:
- ota
- canary
- promotion
- acceptance
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: OTA State Machines · advanced'
outputs:
- url: /posts/stable-should-mean-device-actually-ran-release.html
  template: cms/templates/posts/posts--stable-should-mean-device-actually-ran-release.tpl
  source: cms/templates/posts/posts--stable-should-mean-device-actually-ran-release.json
---

The STABLE transition requires at least one ACTIVE assignment and rejects promotion when failed or rolled-back assignments are present. The production OTA design needed a concrete rule for promotion to STABLE. Without one, lifecycle labels could become administrative intent rather than evidence that the firmware survived a real device rollout. Promotion authority had to be tied to runtime acceptance. A control-plane record alone cannot prove that the artifact booted, validated and stayed active on target hardware.

This is evidence-based promotion and canary release discipline. A production state should represent observed system behavior, not just a requested status.

Make promotion gates executable invariants and keep the evidence query close to the transition. Manual checklists are useful, but the database should refuse impossible or unsafe promotion states. The concrete hserver evidence is commit 4a4554c, so this note is tied to an actual production change rather than a hypothetical failure.
