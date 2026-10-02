---
title: Inbound DID Testing Proves a Different Route Than Extension-to-Extension Calls
url: /posts/inbound-did-testing-proves-a-different-route-than-extension-to-extension-calls.html
date: '2026-09-14'
read_time: 1
excerpt: External ingress adds routing and policy that a local PBX call does not exercise.
topic: loup-engineering
tags:
- did
- asterisk
- inbound-call
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: PBX & Network · advanced'
outputs:
- url: /posts/inbound-did-testing-proves-a-different-route-than-extension-to-extension-calls.html
  template: cms/templates/posts/posts--inbound-did-testing-proves-a-different-route-than-extension-to-extension-calls.tpl
  source: cms/templates/posts/posts--inbound-did-testing-proves-a-different-route-than-extension-to-extension-calls.json
---

The useful question in Inbound DID Testing Proves a Different Route Than Extension-to-Extension Calls was where the behaviour actually originated. The testbed routed an inbound DID to LOUP extension 3005 after basic local registration was working.

That path verifies provider ingress, PBX routing, device ringing, answer state and media in a scenario closer to a real user call. It also helps distinguish device issues from trunk or dialplan issues because local extension calls remain available as a control.

I treated the known-good configuration as a control sample, changed only the layer under investigation, and recorded the regression or improvement before the next experiment. Evidence marker: `did-to-3005`.

Add network scope one boundary at a time. Local success should remain a reference when external routing is introduced. Keeping the rule explicit means the same decision can be checked again on the next board revision or firmware branch.

## Project evidence

LOUP engineering marker: `did-to-3005`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
