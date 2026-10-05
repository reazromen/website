---
title: Parent-Approved Contacts Are an Architecture Rule, Not a UI Filter
url: /posts/parent-approved-contacts-are-an-architecture-rule-not-a-ui-filter.html
date: '2025-11-27'
read_time: 1
excerpt: Contact approval has to be enforced by backend identity and call routing,
  not only hidden buttons.
topic: loup-engineering
tags:
- contacts
- backend
- authorization
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Product Architecture · advanced'
outputs:
- url: /posts/parent-approved-contacts-are-an-architecture-rule-not-a-ui-filter.html
  template: cms/templates/posts/posts--parent-approved-contacts-are-an-architecture-rule-not-a-ui-filter.tpl
  source: cms/templates/posts/posts--parent-approved-contacts-are-an-architecture-rule-not-a-ui-filter.json
---

I reached Parent-Approved Contacts Are an Architecture Rule, Not a UI Filter through a repeatable lab problem rather than a design slogan. A contact list is not a security boundary if the device can still dial or receive arbitrary identities underneath it.

LOUP treats approved contacts as backend-controlled state. The device renders the allowed list, while backend and PBX-facing logic are expected to enforce who can be provisioned, called, blocked or revoked. That keeps authorization outside the display code and makes a lost or modified UI unable to create new communication rights by itself.

The useful debugging step was separating signal path, state and timing instead of modifying all three and then guessing which change mattered. Evidence marker: `parent-approved-contacts`.

Authorization belongs where identities and routing decisions are authoritative. The screen should reflect policy, not invent it. That distinction also makes regressions cheaper to isolate when hardware, firmware and infrastructure are changing in parallel.

## Project evidence

LOUP engineering marker: `parent-approved-contacts`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
