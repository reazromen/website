---
title: Charging Records Are Easier to Trust When I Trace the Event That Created Them
url: /posts/charging-records-are-easier-to-trust-when-i-trace-the-event-that-created-them.html
date: '2026-09-14'
read_time: 1
excerpt: Usage records become meaningful only when they can be tied back to the session,
  rule and network event that produced them.
topic: mobile-networks
tags:
- charging
- cdr
- usage
- policy
draft: false
featured: false
language: en
eyebrow: 2023 Mobile and 5G Notes · advanced
outputs:
- url: /posts/charging-records-are-easier-to-trust-when-i-trace-the-event-that-created-them.html
  template: cms/templates/posts/posts--charging-records-are-easier-to-trust-when-i-trace-the-event-that-created-them.tpl
  source: cms/templates/posts/posts--charging-records-are-easier-to-trust-when-i-trace-the-event-that-created-them.json
---

Charging data looks deceptively simple after it has been turned into a row in a database. There is a subscriber, a duration or byte count, perhaps a rating result, and a timestamp. The difficult part is proving which network event produced that row and whether the counters represent what I think they do.

I started tracing usage from the session outward. Which bearer or PDU session was active? Which policy or charging rule applied? Which component counted the traffic? Was the report interim, final, or triggered by a rule change? Those questions matter because the same subscriber can have multiple services and multiple reporting intervals.

The lesson carried over from SIP CDRs. A billing record is not the call itself, just as a packet counter is not the session. It is derived state. If the derivation is wrong, the record can look internally consistent while still being inaccurate.

For lab work I therefore kept the raw signalling and usage reports around long enough to reconcile them against the final record. It is slower than trusting the database, but it makes charging bugs much easier to isolate and prevents business logic from hiding network mistakes.
