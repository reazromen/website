---
title: CGrates Time Rules Taught Me to Test Billing Schedules Like Code
url: /posts/cgrates-time-rules-taught-me-to-test-billing-schedules-like-code.html
date: '2026-09-14'
read_time: 1
excerpt: Recurring charging rules look harmless until timezone, month-end and relative-time
  semantics collide.
topic: telecom-voip
tags:
- cgrates
- billing
- charging
- time
draft: false
featured: false
language: en
eyebrow: 2025 Voice and Infrastructure Notes · advanced
outputs:
- url: /posts/cgrates-time-rules-taught-me-to-test-billing-schedules-like-code.html
  template: cms/templates/posts/posts--cgrates-time-rules-taught-me-to-test-billing-schedules-like-code.tpl
  source: cms/templates/posts/posts--cgrates-time-rules-taught-me-to-test-billing-schedules-like-code.json
---

Charging systems contain an uncomfortable amount of time logic. Expiry, recurring actions, monthly resets and delayed changes can all depend on date parsing and timezone behavior.

I stopped treating those values as configuration strings and started testing them like code. For each schedule I wanted a fixed input time and a predictable next execution time. Month-end rules deserve special attention because February, leap years and local timezone offsets can expose assumptions that daily rules never hit.

This is especially important in rating systems because a schedule bug is not just a failed job. It can apply the wrong price window or leave balances in the wrong state. A small table-driven test around time expressions was more valuable than repeatedly checking the live scheduler after a change.
