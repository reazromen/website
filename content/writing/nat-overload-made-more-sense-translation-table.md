---
title: NAT Overload Made More Sense When I Looked at the Translation Table
url: /posts/nat-overload-made-more-sense-translation-table.html
date: '2025-03-31'
read_time: 3
excerpt: PAT stopped feeling like a magic Internet-sharing feature once I watched
  inside local addresses, public translations and transport ports change in the NAT
  table.
topic: networking
tags:
- ccna
- nat
- pat
- ipv4
draft: false
featured: false
language: en
eyebrow: 2019 Routing, Linux & First VoIP · intermediate
outputs:
- url: /posts/nat-overload-made-more-sense-translation-table.html
  template: cms/templates/posts/posts--nat-overload-made-more-sense-translation-table.tpl
  source: cms/templates/posts/posts--nat-overload-made-more-sense-translation-table.json
---

NAT overload was easy to use before it was easy to explain. Home routers had already made the behavior familiar: many private hosts could reach the Internet through one public IPv4 address. In a routing lab, seeing the translation state directly made the mechanism much less mysterious. The router is not simply replacing one address globally. It is keeping enough state to map returning traffic back to the correct internal flow.

I built a small inside network using 192.168.10.0/24 and treated one router interface as the outside path. The NAT configuration matched the inside addresses with an access list and overloaded them onto the outside interface address. With two internal hosts opening connections at the same time, the translation table showed multiple entries using the same public address but different transport-layer identifiers.

That is the important part of PAT. If 192.168.10.10 opens a TCP connection and 192.168.10.20 opens another, both can appear externally as the same public IP. The router distinguishes the conversations using source ports and protocol state. When replies return, the translation entry tells the router which inside local address should receive each packet. The public address alone would not be enough to identify the internal endpoint.

Cisco terminology initially added more confusion than the protocol itself. Inside local is the address of the inside host as it appears on the inside network. Inside global is the translated address representing that host externally. The labels are easier to remember if I look at the actual packet on each side of the NAT boundary instead of treating them as vocabulary. A capture before and after translation shows which fields changed.

`show ip nat translations` became the most useful verification command in the lab. `show ip nat statistics` helped confirm which interfaces were considered inside and outside and whether translations were being created. If a host had correct routing but no translations appeared when traffic was generated, I knew to inspect the match criteria or interface roles before blaming the upstream network.

I also learned not to use NAT as an explanation for every connectivity problem. NAT does not replace routing. The inside host still needs a route toward the NAT device, and the NAT device still needs a route toward the external destination. Return traffic needs to arrive back at the device that owns the translation state. If asymmetric routing sends the reply somewhere else, the existence of a NAT rule does not help.

The translation table also hinted at problems I would meet later with SIP and other protocols that carry addressing information inside application payloads. Rewriting the IP header is straightforward. Protocols that describe media addresses, ports or peer identity inside their messages can interact with NAT in much more complicated ways. At this stage I did not need to solve those cases yet, but NAT overload was the first clue that sharing one public address creates state and assumptions above simple forwarding.
