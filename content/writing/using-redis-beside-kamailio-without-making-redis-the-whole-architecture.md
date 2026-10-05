---
title: Using Redis Beside Kamailio Without Making Redis the Whole Architecture
url: /posts/using-redis-beside-kamailio-without-making-redis-the-whole-architecture.html
date: '2023-05-24'
read_time: 2
excerpt: Redis was useful for fast shared state in a SIP lab, but the important decision
  was which state belonged there and how the proxy behaved when it disappeared.
topic: telecom-voip
tags:
- kamailio
- redis
- sip
- architecture
draft: false
featured: false
language: en
eyebrow: 2021 SIP Infrastructure · intermediate
outputs:
- url: /posts/using-redis-beside-kamailio-without-making-redis-the-whole-architecture.html
  template: cms/templates/posts/posts--using-redis-beside-kamailio-without-making-redis-the-whole-architecture.tpl
  source: cms/templates/posts/posts--using-redis-beside-kamailio-without-making-redis-the-whole-architecture.json
---

I added Redis to a Kamailio lab because I wanted a small piece of state to be available outside one proxy process. The first temptation was to move more and more logic into it because reads and writes were simple. The better lesson was deciding what data actually benefited from a fast external store.

A useful example was temporary routing state: a short-lived mapping, counter or flag that several workers or proxy nodes might need to read. Kamailio can talk to Redis through modules designed either for generic Redis commands or for specific database-style integrations. I preferred to keep the experiment narrow and use Redis as an explicit dependency rather than pretending it was just another local variable.

The failure test mattered more than the happy path. I stopped Redis while calls were running and watched what the routing script did. If every request blocked or failed because a nonessential lookup disappeared, I had created a fragile dependency. For data that was advisory rather than authoritative, a timeout and sensible fallback was better than turning a cache failure into a signaling outage.

Persistence semantics also mattered. Redis is often described simply as an in-memory store, but durability depends on configuration and workload. I did not want routing correctness to depend on data that I had never decided how to persist or reconstruct. Temporary state and authoritative subscriber or billing data have very different requirements.

The lab pushed me toward clearer ownership of state. Kamailio already has transaction state, dialog-related mechanisms, registration/location options and shared-memory structures. A relational database solves another class of problems. Redis is useful when its data model and latency characteristics match the requirement, not because every distributed system needs Redis.

I added simple timing logs around the lookups and watched Redis with its own tools while placing calls. That made the external dependency visible. A fast lookup on an idle laptop is not the same as predictable behavior under connection loss, restart or load.

By the end of the year my VoIP lab looked less like one PBX and more like a collection of specialized components: proxy, PBX, media relay, DNS, capture tools and now a shared data service. The useful skill was no longer installing each component. It was defining the boundary between them and making failure at one boundary observable.
