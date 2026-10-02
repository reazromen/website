---
title: Gx Charging Rules Only Made Sense After I Followed the TFT
url: /posts/gx-charging-rules-only-made-sense-after-i-followed-the-tft.html
date: '2026-09-14'
read_time: 1
excerpt: A charging rule becomes concrete when its packet filters are followed all
  the way into bearer treatment.
topic: mobile-networks
tags:
- gx
- tft
- diameter
- qos
draft: false
featured: false
language: en
eyebrow: 2024 Telecom and Embedded Notes · advanced
outputs:
- url: /posts/gx-charging-rules-only-made-sense-after-i-followed-the-tft.html
  template: cms/templates/posts/posts--gx-charging-rules-only-made-sense-after-i-followed-the-tft.tpl
  source: cms/templates/posts/posts--gx-charging-rules-only-made-sense-after-i-followed-the-tft.json
---

Gx policy messages were easy to read as configuration objects and hard to connect to packets. The useful change was to follow one rule all the way through: PCC rule, flow description, packet filter, bearer decision, then actual traffic.

A Traffic Flow Template is not a billing label. It describes which packets match a bearer or policy treatment. Direction, address ranges, protocol and port information determine which traffic the rule applies to. If the filter is wrong, the network can create a perfectly valid dedicated bearer that carries none of the traffic I expected.

I started validating rules from both sides. On the policy side I inspected what PCRF delivered. On the EPC side I checked the resulting bearer and TFT. Then I generated traffic that should match one rule and traffic that should not. That simple A/B test caught assumptions about local versus remote ports faster than reading the rule text repeatedly.

The bigger lesson was familiar from routing ACLs: policy is only useful when I can predict the packet match. Telecom names make the objects sound special, but eventually a packet either matches the classifier or it does not.
