---
title: DNS SRV Made SIP Service Discovery Feel Less Hard-Coded
url: /posts/dns-srv-made-sip-service-discovery-feel-less-hard-coded.html
date: '2026-09-14'
read_time: 2
excerpt: Using DNS SRV records showed me how SIP clients can discover service hosts
  and ports without baking one server address into every configuration.
topic: networking
tags:
- dns
- sip
- srv
- service-discovery
draft: false
featured: false
language: en
eyebrow: 2021 SIP Infrastructure · intermediate
outputs:
- url: /posts/dns-srv-made-sip-service-discovery-feel-less-hard-coded.html
  template: cms/templates/posts/posts--dns-srv-made-sip-service-discovery-feel-less-hard-coded.tpl
  source: cms/templates/posts/posts--dns-srv-made-sip-service-discovery-feel-less-hard-coded.json
---

Most of my early SIP labs used an IP address or a single hostname in the phone configuration. That is fine for a small test, but it ties the client directly to one destination. DNS SRV records introduced a cleaner way to describe where a service lives and which port and transport should be used.

An SRV record contains a service, protocol, priority, weight, port and target hostname. For SIP, records such as `_sip._udp.example.net` can point clients toward one or more servers. Lower priority values are preferred, and weight can distribute selections among records with the same priority.

I built a small DNS zone with two SIP targets. The first had the preferred priority and the second acted as a fallback. Using `dig SRV` made the result easy to inspect. The important detail was that the SRV target is a hostname, not an IP address, so the resolver still needs A or AAAA records for the target afterward.

This made failover design more explicit. A client that supports the relevant SIP DNS procedures can try another SRV target when the preferred one is unavailable. That is different from relying on one hostname with several A records, because SRV includes service-specific port and priority information.

The lab also reminded me that DNS behavior is only useful if the application actually implements it. Not every SIP client follows every discovery rule in the same way. I therefore tested the specific user agents rather than assuming that publishing an SRV record guaranteed failover.

Caching matters too. DNS changes are not instant from the application's point of view. Resolver caches and TTL values can make an old answer persist after I modify the zone. During troubleshooting I used direct queries against the authoritative or intended resolver and compared that with what the client was actually doing.

This was a small step toward removing static topology from endpoint configuration. Instead of telling every phone exactly which server to use, DNS could publish a service location and let the client discover it. The same pattern appears throughout distributed systems: move changeable service location out of the client where possible, then make the discovery layer observable and testable.
