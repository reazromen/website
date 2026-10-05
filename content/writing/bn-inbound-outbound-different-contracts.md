---
title: Inbound and Outbound Calls Are Not Two Names for the Same Test
date: '2023-09-21'
draft: false
language: en
url: /posts/bn-inbound-outbound-different-contracts.html
topic: telecom-voip
tags:
- sip
- testing
featured: false
read_time: 2
excerpt: >-
  It is easy to assume that if a system can place an outbound call, inbound calling must
  work too. But the two directions can have different routing, authentication, numbering,
  NAT, and reachability requirements.
editorial_batch: 20261003-100-niches
---

It is easy to assume that if a system can place an outbound call, inbound calling must work too. But the two directions can have different routing, authentication, numbering, NAT, and reachability requirements. Outbound traffic starts from inside the system; inbound traffic has to find its way in from somewhere else. Success in one direction is not proof of readiness in the other.

For a PBX, think separately about which number is presented outbound, which DID is accepted inbound, and where an accepted inbound call should route. Outbound number presentation and inbound DID matching are different contracts. If a phone never rings, assuming the handset is at fault can hide a routing problem. First establish whether the inbound INVITE reached the system at all.

The test matrix should separate signaling and media in both directions. Call initiation, ringing, answer, two-way audio, DTMF, and call teardown can each be recorded independently. A small matrix like this can be more useful than a large dashboard because it makes the claim under test explicit.

This is a general networking lesson as well. Being able to reach out and being reachable from outside are different properties. Webhooks, email delivery, and device commands all have similar asymmetry. Unless both directions are tested, one half of connectivity can easily be mistaken for the whole thing.

Source: [official reference](https://www.rfc-editor.org/rfc/rfc3261.html).
