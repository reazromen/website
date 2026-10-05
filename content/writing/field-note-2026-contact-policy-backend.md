---
title: Contact Authorization Belongs to Backend Policy, Not Dialing Logic
url: /posts/field-note-2026-contact-policy-backend.html
date: '2026-07-13'
read_time: 2
excerpt: SIP addresses endpoints; the product still needs an explicit policy for who
  is allowed to contact whom.
topic: telecom-voip
tags:
- authorization
- sip
- backend
- contacts
draft: false
featured: false
language: en
eyebrow: VoIP Field Notes · advanced
outputs:
- url: /posts/field-note-2026-contact-policy-backend.html
  template: cms/templates/posts/posts--field-note-2026-contact-policy-backend.tpl
  source: cms/templates/posts/posts--field-note-2026-contact-policy-backend.json
---

# Contact Authorization Belongs to Backend Policy, Not Dialing Logic

SIP addresses endpoints; the product still needs an explicit policy for who is allowed to contact whom.

I keep this as a field note because the failure mode is easy to misclassify: any syntactically valid dial target is accidentally treated as an allowed contact. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Authorization should be decided before dialing begins.**

## Implementation pattern

Distribute only approved contacts to the device and keep approval, revocation and association in the backend.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- revoked contacts fail closed
- UI cannot construct unrestricted targets
- policy changes do not require firmware rebuild

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Authorization should be decided before dialing begins. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
