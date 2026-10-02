---
title: WebRTC Connectivity Is Not “STUN or TURN” — It Is an ICE Candidate Selection
  Problem
url: /posts/webrtc-ice-candidate-selection-not-stun-turn.html
date: '2026-09-26'
read_time: 9
excerpt: STUN discovers reachability information and TURN provides a relay, but ICE
  is the algorithm that gathers candidates, checks candidate pairs, prioritizes working
  paths, and nominates the connection media actually uses.
topic: ''
tags:
- webrtc
- ice
- stun
- turn
draft: false
featured: false
language: en
eyebrow: Real-Time Networking · systems note
outputs:
- url: /posts/webrtc-ice-candidate-selection-not-stun-turn.html
  template: cms/templates/posts/posts--webrtc-ice-candidate-selection-not-stun-turn.tpl
  source: cms/templates/posts/posts--webrtc-ice-candidate-selection-not-stun-turn.json
---

WebRTC connectivity is often explained as a binary:

```
STUN if NAT works
TURN if NAT is hard
```

That shortcut is useful for a first lesson and harmful for debugging.

The real system is ICE: gather possible addresses, exchange them, form candidate pairs, run connectivity checks, and nominate a path that works.

## A candidate is one possible way to reach an agent[#](#a-candidate-is-one-possible-way-to-reach-an-agent)

ICE can work with several candidate types.

A host candidate represents a local interface address. A server-reflexive candidate represents an address mapping learned through STUN. A peer-reflexive candidate can be discovered during connectivity checks. A relay candidate is allocated through TURN.

The candidate list is not a decision. It is a set of hypotheses.

## ICE checks pairs[#](#ice-checks-pairs)

After peers exchange candidates through signaling, ICE forms local/remote candidate pairs and sends STUN connectivity checks.

A pair that looks reasonable from SDP can still fail because a NAT mapping is endpoint-dependent, filtering blocks the reverse traffic, a firewall rejects UDP, or the route is asymmetric.

This is why reading a candidate list does not prove media reachability.

## “Symmetric NAT” hides useful details[#](#symmetric-nat-hides-useful-details)

The old symmetric-NAT label compresses several mapping/filtering behaviors into one phrase.

Operationally, what matters is whether the public mapping learned when talking to the STUN server is usable when a different remote peer sends traffic, and whether inbound packets are accepted under the NAT's filtering behavior.

ICE testing discovers that empirically.

A Stack Overflow discussion about two peers behind restrictive NATs illustrates the point: the usable outcome depends on candidate pairs and TURN permissions, not on a rule that “both sides always need two TURN servers.”

## TURN is a candidate source and relay service[#](#turn-is-a-candidate-source-and-relay-service)

TURN gives a client a relay allocation reachable by the peer. Media can flow through the relay when direct candidate pairs fail.

One side using a relay candidate can be enough for a working pair in many topologies. In the most restrictive cases, the nominated pair can be relay-to-relay.

That is an ICE result, not a configuration slogan.

## Candidate priority does not guarantee success[#](#candidate-priority-does-not-guarantee-success)

ICE prefers candidate types and pairs according to priority rules, but high priority only determines which checks are attempted/preferred. A lower-priority pair can win because the higher-priority route is not reachable.

When debugging, I want to know the nominated pair:

```
local candidate type / IP / port
remote candidate type / IP / port
transport
ICE state transitions
selected/nominated pair
RTT / packet loss on that pair
```

That immediately tells you whether the call is actually direct or relayed.

## Signaling success is not media success[#](#signaling-success-is-not-media-success)

WebRTC signaling can exchange SDP and ICE candidates perfectly while connectivity checks fail.

Similarly, one candidate pair can succeed while DTLS, SRTP, codec negotiation, or application media still fails later.

Keep the state machines separate:

```
signaling
 -> ICE connectivity
 -> DTLS
 -> SRTP/media
 -> application playback
```

## Trickle ICE changes timing[#](#trickle-ice-changes-timing)

Candidates do not always arrive as one completed set. With trickle ICE, peers can begin connectivity checks while more candidates are still being gathered.

This reduces setup time but makes logs more temporal: a host pair may be tested first, a server-reflexive candidate may appear later, and TURN candidates may arrive after that.

A static SDP snapshot can miss the sequence that explains why connection establishment took two seconds.

## Test from hostile networks[#](#test-from-hostile-networks)

A LAN-to-LAN success case proves almost nothing about internet reachability.

I would test from mobile networks, CGNAT, enterprise Wi-Fi, UDP-blocked networks, IPv6, and deliberately restrictive firewall environments.

Then measure relay percentage. If TURN usage is unexpectedly high, either direct connectivity is genuinely impossible for that population or some part of ICE/STUN/firewall configuration is unnecessarily blocking it.

## The useful abstraction is path selection[#](#the-useful-abstraction-is-path-selection)

STUN and TURN are tools inside the connectivity process.

ICE is the mechanism that compares possible paths and proves reachability with checks.

Once you debug WebRTC as candidate-pair selection rather than “STUN versus TURN,” NAT problems become packet-flow problems instead of folklore.

## Sources and further reading[#](#sources-and-further-reading)

- [RFC 8445: Interactive Connectivity Establishment (ICE)](https://www.rfc-editor.org/rfc/rfc8445.html)
- [RFC 8489: Session Traversal Utilities for NAT (STUN)](https://www.rfc-editor.org/rfc/rfc8489.html)
- [RFC 8656: Traversal Using Relays around NAT (TURN)](https://www.rfc-editor.org/rfc/rfc8656.html)
- [Stack Overflow: ICE with peers behind restrictive NATs](https://stackoverflow.com/questions/54796460/will-ice-negotiations-between-peers-behind-two-symmetric-nats-result-in-requiri)
