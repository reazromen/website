---
title: SDP Is a Proposal, Not the Actual Media Path
url: /posts/signals-of-reality-093-sdp-proposal-not-media-path.html
date: '2026-06-03'
read_time: 7
excerpt: SDP offer/answer describes desired media parameters and receive addresses. It does not guarantee that packets will traverse the network exactly as described.
topic: telecom-voip
tags:
- sdp
- rtp
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Protocols Lie Carefully'
editorial_batch: signals-of-reality-200
---

An SDP body says:

send audio here,

on this port,

using one of these codecs.

Engineers often read it as if it were a packet capture from the future.

It is not.

[RFC 3264](https://www.rfc-editor.org/rfc/rfc3264.html) defines an offer/answer model in which participants exchange descriptions of desired media streams, formats, addresses, and ports. The goal is to arrive at a common view of the session.

That view is a proposal and agreement.

The network still has to make it real.

## Offer/answer negotiates expectations

One side advertises codecs and a receive address.

The other answers with compatible parameters.

This solves a necessary coordination problem.

Without it, endpoints may disagree about format, direction, or destination.

But agreement in metadata does not establish reachability.

An endpoint can advertise a private address that the peer cannot route to.

A NAT can rewrite mappings.

A firewall can drop UDP.

An SBC can alter SDP.

An RTP relay can intentionally make the actual topology different from the apparent endpoint topology.

## The packet path can be transformed

Consider a call through an SBC with media anchoring.

Endpoint A believes it is sending RTP to the SBC.

Endpoint B also sends RTP to the SBC.

The SBC relays between them.

The endpoints never send directly to each other.

The final physical path is therefore a result of policy and network topology, not just the original SDP text.

Even more complex systems may use ICE, TURN, symmetric RTP behavior, or media relays that adapt after packets begin flowing.

The session description is an input to path construction.

## SDP can be internally correct and operationally useless

A valid SDP offer may contain:

a supported codec,

a syntactically correct IP address,

a legal port,

and the correct media direction.

If that address points to an unreachable interface, the session can remain silent.

The syntax is right.

The intention is coherent.

The topology is wrong.

This is why validators cannot replace packet observation.

## Media direction attributes describe permission and intent

Attributes such as sendrecv, sendonly, recvonly, and inactive help describe intended media direction.

They do not prove that packets will appear.

An endpoint marked sendrecv may have a muted microphone.

A bug may prevent RTP generation.

A downstream relay may drop one direction.

The descriptor constrains expected behavior.

It does not certify runtime behavior.

## Codec agreement is not codec success

Two endpoints may agree on Opus, PCMU, or another codec.

Packets may flow.

Audio may still fail because payload types are mishandled, clocking is wrong, implementation bugs exist, or media is encrypted in a way one side cannot process.

Negotiation only establishes a shared declared format.

Execution remains a separate problem.

## Packet capture is the reality check

When a call has no audio, ask the network directly.

Capture packets near A.

Capture near the relay.

Capture near B.

Compare timestamps, addresses, ports, SSRCs, sequence numbers, and payload types.

Now SDP becomes a prediction:

these are the streams we expected.

The capture becomes evidence:

these are the streams that actually appeared.

The difference is often the bug.

SDP is a proposal, not the actual media path.

That distinction is not pedantry.

It is the difference between configuration and behavior.
