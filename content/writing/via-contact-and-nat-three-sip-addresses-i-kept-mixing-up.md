---
title: 'Via, Contact and NAT: Three SIP Addresses I Kept Mixing Up'
url: /posts/via-contact-and-nat-three-sip-addresses-i-kept-mixing-up.html
date: '2026-05-26'
read_time: 3
excerpt: NAT problems became easier once I stopped treating every SIP URI and IP header
  as the same kind of return address.
topic: telecom-voip
tags:
- sip
- nat
- via
- contact
draft: false
featured: false
language: en
eyebrow: 2021 SIP Infrastructure · intermediate
outputs:
- url: /posts/via-contact-and-nat-three-sip-addresses-i-kept-mixing-up.html
  template: cms/templates/posts/posts--via-contact-and-nat-three-sip-addresses-i-kept-mixing-up.tpl
  source: cms/templates/posts/posts--via-contact-and-nat-three-sip-addresses-i-kept-mixing-up.json
---

SIP behind NAT produced some of my most confusing traces because the same message can contain several addresses that look important. The IP header has source and destination addresses, Via describes the signaling path for responses, Contact advertises where future requests should be sent, and SDP may advertise an entirely different address for media. NAT can make any of those values disagree with what the far side can actually reach.

I started with registration because it is easy to observe. A phone on a private address sent REGISTER through a router. The server saw the packet arriving from the router's public mapping, but the Contact header still contained the phone's private SIP URI. If the registrar later tried to send an INVITE literally to that unreachable Contact, the registration looked successful while incoming calls failed.

The Via header has another job. Responses use the Via chain to travel back through SIP hops. Parameters such as `received` and `rport` help a server account for the address and port from which a request actually arrived. That does not automatically fix Contact, and neither mechanism fixes an SDP address that points RTP toward a private interface.

This was the point where I stopped using 'NAT issue' as a complete diagnosis. I began asking which layer had the wrong address. Is the SIP response returning to the wrong transport tuple? Is the next in-dialog request using an unreachable Contact? Is media being sent to a private SDP connection address? Those are related to NAT, but they are not the same failure.

A useful lab was to register a softphone from behind NAT, inspect the registration location stored by the server, then place calls in both directions. I compared the packet source with Via, Contact and SDP. I also changed the NAT mapping by restarting the client and watched how the observed source port changed. That made registration expiry and keepalive behavior more meaningful because stale NAT state could invalidate an otherwise valid-looking contact.

Kamailio has modules and helper functions for NAT detection and contact handling, but I found it dangerous to copy a block of NAT configuration without understanding the addresses it was correcting. A function name can hide several assumptions about transport, endpoint behavior and topology.

The best debugging question became very literal: if the server sends a UDP packet to the address written here, can it actually reach the intended device? Repeating that question for the IP header, Via, Contact and SDP turned a messy SIP trace into a set of specific reachability checks.
