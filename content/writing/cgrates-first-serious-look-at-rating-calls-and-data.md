---
title: CGrates Was My First Serious Look at Rating Calls and Data Sessions
url: /posts/cgrates-first-serious-look-at-rating-calls-and-data.html
date: '2026-09-14'
read_time: 2
excerpt: Rating made telecom architecture feel less like packet forwarding and more
  like a business system where usage events, balances and policy all have to agree.
topic: telecom-voip
tags:
- cgrates
- rating
- charging
- voip
- diameter
draft: false
featured: false
language: en
eyebrow: 2022 Mobile Core and IMS · intermediate
outputs:
- url: /posts/cgrates-first-serious-look-at-rating-calls-and-data.html
  template: cms/templates/posts/posts--cgrates-first-serious-look-at-rating-calls-and-data.tpl
  source: cms/templates/posts/posts--cgrates-first-serious-look-at-rating-calls-and-data.json
---

Most of my earlier labs ended when the call connected or the packet reached the Internet. Charging forced me to look at a different question: how does the platform turn usage into something that can be counted, rated and eventually billed? CGrates was a useful entry point because it could sit beside familiar VoIP systems while also exposing concepts that appear in mobile charging.

The first useful distinction was between creating a communication session and rating it. Asterisk, FreeSWITCH or Kamailio can establish and route calls, but the business decision about price, balance or allowance is separate. That means a working call path is not enough to prove the charging path is correct.

I started with simple call detail information: who called whom, when the call started, when it answered and how long it remained connected. Even there, the definition of billable duration mattered. Charging from INVITE time would be wrong for a call that rang for thirty seconds before answer. The event boundary has to match the service policy.

Prepaid behavior adds another layer because the platform may need to authorize usage before or during the session rather than calculating a bill afterward. Mobile networks use online charging procedures for exactly this reason. The protocol details can vary, but the architectural pattern is familiar: reserve or authorize resources, report usage, update the balance and decide whether the session may continue.

What surprised me was how quickly rating became a data-model problem. Prefixes, destinations, customer groups, time periods and service types can all affect price. A route that is technically valid may not be commercially valid. That is why charging and routing platforms often need integration without becoming the same component.

The lab also reinforced the value of keeping raw usage evidence. If a customer disputes a charge, a final balance is not enough. Call records, session identifiers and rating decisions need enough context to reconstruct what happened. That requirement feels much closer to accounting than packet forwarding.

CGrates made the telecom stack look wider. Signalling, media, subscriber state and packet forwarding are only part of a production service. Rating and charging turn those technical events into controlled consumption, which is where network engineering begins to meet the business system around it.
