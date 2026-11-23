---
title: The Call Connected, but Nobody Can Hear
url: /posts/signals-of-reality-094-call-connected-nobody-hears.html
date: '2026-03-12'
read_time: 7
excerpt: A connected SIP dialog with silent audio demonstrates how end-to-end behavior can fail after control-plane success.
topic: telecom-voip
tags:
- sip
- one-way-audio
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Protocols Lie Carefully'
editorial_batch: signals-of-reality-200
---

The phone rings.

Someone answers.

The timer begins.

Silence.

If both sides see the call as connected, the instinct is to say the network is fine.

The silence says otherwise.

This failure is valuable because it separates two systems that user interfaces often collapse into one: call signaling and media transport.

## First prove that RTP exists

Before blaming codecs, NAT, or firewalls, ask a simpler question.

Are RTP packets being sent?

A packet capture on each side can answer.

No packets leaving an endpoint points toward local media generation, device configuration, mute state, or application behavior.

Packets leaving but not arriving point toward the network path.

Packets arriving but no audio points toward decoding, playback, encryption, payload mapping, or device output.

The silence becomes a decision tree.

## Check both directions separately

Two-way audio contains two independent directional paths.

A → B.

B → A.

One-way audio therefore localizes the problem.

If A hears B, then at least one endpoint can send, one path exists, and one receiver can decode.

Do not throw away that information by treating the call as generically broken.

Directionality is a signal.

## NAT turns private truth into public failure

A common cause is SDP containing an address meaningful only inside one network.

The endpoint honestly advertises:

send media to 192.168.x.x.

The remote peer cannot reach it.

From the endpoint's local perspective, the address is real.

From the internet's perspective, it is useless.

NAT traversal mechanisms exist because distributed communication requires addresses that are meaningful from the receiver's location, not merely from the sender's.

This is a perfect example of perspective becoming topology.

## Firewalls can permit SIP and block RTP

SIP might use a known port that the firewall permits.

RTP may use a dynamic UDP range that is blocked.

The call setup succeeds.

The media fails.

A simplistic health check that confirms only SIP registration or signaling reachability can remain green all day.

The product is still broken.

This is why voice infrastructure needs media-path monitoring, not just registration monitoring.

## Relays can solve and create problems

RTP proxies and SBCs help by anchoring media at known public addresses.

They can normalize NAT behavior, provide symmetric paths, and enforce policy.

But they create another component whose advertised addresses, listening ports, routing tables, and firewall rules must be correct.

If the relay receives packets from A but does not forward to B, the endpoints are not the problem.

The media topology has its own observability needs.

## Codec and payload mapping come later

Once packets are proven to arrive, inspect whether both sides interpret them the same way.

Payload type.

Codec.

Clock rate.

Packetization.

Encryption.

RTCP.

A capture can show healthy packet timing while the application still renders silence because the payload is not usable.

Media success is layered too.

## The user's sentence is the best top-level metric

"The call connected, but nobody can hear."

That sentence describes the end-to-end truth better than a signaling dashboard saying 200 OK.

Operationally, the system must preserve both perspectives.

Signaling proves session coordination.

Media proves communication.

The call is not the SIP dialog.

The call is the human experience produced by the entire chain.

When those two truths disagree, the silence is not an absence of evidence.

It is the evidence.
