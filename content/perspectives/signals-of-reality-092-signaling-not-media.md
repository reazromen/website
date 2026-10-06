---
title: Signaling Is Not Media
url: /posts/signals-of-reality-092-signaling-not-media.html
date: '2026-01-04'
read_time: 7
excerpt: SIP establishes, modifies, and ends sessions, while RTP commonly carries the audio or video. A successful signaling dialog does not prove that media can flow.
topic: telecom-voip
tags:
- sip
- rtp
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Protocols Lie Carefully'
editorial_batch: signals-of-reality-200
---

The call screen says connected.

The timer is counting.

Nobody can hear anything.

This is one of the cleanest demonstrations that signaling is not media.

SIP can successfully establish a session while the audio path fails completely.

## SIP negotiates and coordinates

SIP handles session signaling.

An INVITE proposes a session.

Responses report progress and outcome.

An ACK completes the INVITE transaction.

BYE tears the dialog down.

Session descriptions carried with SIP can negotiate media parameters.

But SIP messages are not the audio stream.

They are control-plane messages about the session.

## RTP commonly carries the voice

Real-time audio is often transported separately using RTP.

The media packets may take a different network path.

They use different ports.

They can face NAT and firewall rules unrelated to SIP signaling.

They can be anchored by an RTP proxy or sent directly between endpoints.

This separation is architecturally useful.

It also creates a classic failure mode: signaling succeeds while RTP fails.

## A 200 OK proves less than users think

A SIP 200 OK to an INVITE indicates the invitation was accepted under SIP semantics.

It does not prove:

audio packets are reaching both endpoints,

the negotiated codec is actually handled correctly,

the microphone works,

the speaker works,

the advertised IP addresses are reachable,

NAT mappings are correct,

or packet loss is acceptable.

The status belongs to signaling.

The user experience belongs to the combined path.

## One-way audio is a topology clue

If A hears B but B cannot hear A, media is not simply "down."

One direction works.

That narrows the investigation.

Check the SDP addresses and ports in each direction.

Check NAT.

Check firewall rules.

Check RTP proxy anchoring.

Check packet captures on both sides.

Check whether the endpoint is sending at all.

The asymmetry is evidence.

A generic "call failed" label throws that evidence away.

## SDP is not the media either

Even when SDP correctly lists codecs, addresses, and ports, it describes intended media behavior.

The network still has to deliver packets.

The endpoint still has to send them.

The receiver still has to decode them.

An SDP exchange can be semantically valid while the advertised address is unreachable from the peer.

Negotiation success is another layer.

## Control and data planes fail differently

This pattern exists far beyond telephony.

Routing protocols can converge while application traffic is blackholed.

A storage control plane can report a volume attached while I/O fails.

A Kubernetes API can show a service object while packets cannot reach pods.

Control-plane truth is not data-plane truth.

Both must be observed.

## Troubleshooting needs two captures

For a voice call, signaling traces answer questions such as:

Who was invited?

Which route was selected?

Which response ended the transaction?

What SDP was offered and answered?

Media traces answer different questions:

Did RTP packets exist?

Which addresses exchanged them?

In which direction?

At what rate?

With what loss and jitter?

Trying to solve a media problem with only SIP logs is like diagnosing a river from the paperwork that authorized the bridge.

Signaling is not media.

A connected dialog is evidence that one part of the call succeeded.

The human conversation still has to cross the network.
