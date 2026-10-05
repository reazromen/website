---
title: Reliability Work Is Product Work
url: /posts/reliability-work-is-product-work.html
date: '2025-11-17'
read_time: 1
excerpt: Users experience latency, outages, broken recovery and bad upgrades as product
  behavior, not as internal infrastructure details.
topic: devops-culture
tags:
- reliability
- product
- devops
draft: false
featured: false
language: en
eyebrow: 'DevOps Culture: Delivery & Reliability · advanced'
outputs:
- url: /posts/reliability-work-is-product-work.html
  template: cms/templates/posts/posts--reliability-work-is-product-work.tpl
  source: cms/templates/posts/posts--reliability-work-is-product-work.json
---

Reliability engineering is sometimes treated as maintenance that competes with product development. Users do not experience that organizational distinction when failures interrupt the product they depend on.

An OTA control-plane bug that assigns the wrong state is a product bug. A stale authentication session, failed alert path or unstable audio stream changes what the customer can do even if the feature code itself is correct.

DevOps culture treats reliability work as part of the product roadmap because operability and recovery shape the user experience just as directly as interface features.

The question is not whether reliability work creates features. It creates the conditions under which every feature can be trusted.

## Engineering evidence

Repository/project evidence for this note: `a736702`. The point is the operating model behind the change, not the commit number itself.
