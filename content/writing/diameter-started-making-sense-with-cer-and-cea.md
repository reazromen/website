---
title: Diameter Started Making Sense When I Followed CER and CEA First
url: /posts/diameter-started-making-sense-with-cer-and-cea.html
date: '2024-02-28'
read_time: 2
excerpt: Before looking at subscriber procedures, I needed to understand how Diameter
  peers identify themselves, advertise applications and establish a usable relationship.
topic: mobile-networks
tags:
- diameter
- cer
- cea
- avp
- rfc6733
draft: false
featured: false
language: en
eyebrow: 2022 Mobile Core and IMS · intermediate
outputs:
- url: /posts/diameter-started-making-sense-with-cer-and-cea.html
  template: cms/templates/posts/posts--diameter-started-making-sense-with-cer-and-cea.tpl
  source: cms/templates/posts/posts--diameter-started-making-sense-with-cer-and-cea.json
---

Diameter initially looked like a binary version of SIP with too many fields. That was the wrong comparison. The first useful step was to ignore subscriber procedures and watch two Diameter peers establish their relationship. The Capabilities-Exchange-Request and Capabilities-Exchange-Answer gave me a clean place to start because they describe who the peers are and what applications they support before application-specific traffic begins.

A CER carries identity and capability information such as Origin-Host, Origin-Realm, supported Application-Ids and product information. The CEA returns the other side's capabilities and a result code. If the peers do not share a usable application, the connection can exist at the transport layer while still being useless for the procedure I expected. That distinction explained several confusing lab failures where TCP was established but the Diameter application never became operational.

The second concept was the AVP. Diameter messages are built from Attribute-Value Pairs, and the meaning of many AVPs depends on the application using them. Instead of reading a packet top to bottom as one flat structure, I started separating base-protocol fields from application data. Session-Id, Origin-Host and Destination-Realm help with protocol operation and routing; application-specific AVPs carry subscriber or policy information.

Hop-by-Hop and End-to-End identifiers also helped me understand how requests and answers are correlated through intermediaries. A Diameter route can pass through relays or proxies without every node being the final application endpoint. That makes peer state and routing policy important in a way that is easy to miss in a two-node lab.

Wireshark was useful once I filtered on `diameter` and followed a single peer connection. I would identify CER/CEA first, then look at the Application-Ids advertised by both sides, then move to the request that was actually failing. That order prevented me from debugging a subscriber AVP when the peer relationship itself was incomplete.

The main lesson was that Diameter troubleshooting starts one level lower than the business procedure. Before asking why authentication, policy or charging failed, I need to know whether the peers are connected, whether they agree on capabilities, and whether the request is being routed to a node that actually supports the application.
