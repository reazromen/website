---
title: Extension 3004 and 3005 Became Reference Endpoints
url: /posts/extension-3004-and-3005-became-reference-endpoints.html
date: '2026-09-14'
read_time: 1
excerpt: Named test identities make repeatable call scenarios easier to describe and
  automate.
topic: loup-engineering
tags:
- asterisk
- extensions
- testbed
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: PBX & Network · advanced'
outputs:
- url: /posts/extension-3004-and-3005-became-reference-endpoints.html
  template: cms/templates/posts/posts--extension-3004-and-3005-became-reference-endpoints.tpl
  source: cms/templates/posts/posts--extension-3004-and-3005-became-reference-endpoints.json
---

I reached Extension 3004 and 3005 Became Reference Endpoints through a repeatable lab problem rather than a design slogan. The LOUP lab used device extension 3005 and Linphone extension 3004 as stable reference points.

A fixed pair meant inbound, outbound, registration and media tests could be repeated without changing identities between experiments. When a firmware build changed, the surrounding PBX configuration could stay constant, giving the new build a meaningful comparison against the previous result.

The useful debugging step was separating signal path, state and timing instead of modifying all three and then guessing which change mattered. Evidence marker: `extensions-3004-3005`.

A good testbed removes unnecessary variables. Stable endpoint identities turn call tests into reproducible experiments. That distinction also makes regressions cheaper to isolate when hardware, firmware and infrastructure are changing in parallel.

## Project evidence

LOUP engineering marker: `extensions-3004-3005`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
