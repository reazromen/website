---
title: OTA Updates Became a Reliability Problem Before They Became a Delivery Problem
url: /posts/ota-updates-became-a-reliability-problem-before-they-became-a-delivery-problem.html
date: '2026-09-14'
read_time: 1
excerpt: Downloading new firmware is easy; proving the device can recover from a bad
  update is the real OTA design work.
topic: embedded-firmware
tags:
- ota
- esp32
- rollback
- firmware
draft: false
featured: false
language: en
eyebrow: 2024 Telecom and Embedded Notes · advanced
outputs:
- url: /posts/ota-updates-became-a-reliability-problem-before-they-became-a-delivery-problem.html
  template: cms/templates/posts/posts--ota-updates-became-a-reliability-problem-before-they-became-a-delivery-problem.tpl
  source: cms/templates/posts/posts--ota-updates-became-a-reliability-problem-before-they-became-a-delivery-problem.json
---

The first OTA design question I asked was how to download an image. That was not the important question. The important question was what happens when power fails, the image is corrupt, the new firmware crashes before networking starts, or the server accidentally offers the wrong build.

A/B application slots gave me a cleaner model. The running image stays available while a new image is written to the inactive slot. Boot state changes only after validation, and the new firmware has to prove it can reach a known-good state before being accepted permanently.

That introduced version and policy questions. A device needs to know which releases are allowed, whether downgrade is permitted, and how to identify a failed boot. Hashes or signatures protect the artifact itself; rollback logic protects availability.

I started treating OTA as a state machine with evidence: downloaded, verified, staged, booted, health-checked, accepted or rolled back. Once those states are explicit, the dashboard and backend become much easier to design later.
