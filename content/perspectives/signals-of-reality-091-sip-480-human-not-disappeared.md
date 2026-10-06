---
title: SIP 480 Does Not Mean the Human Disappeared
url: /posts/signals-of-reality-091-sip-480-human-not-disappeared.html
date: '2026-09-12'
read_time: 7
excerpt: SIP 480 Temporarily Unavailable reports reachability in signaling terms. It does not tell us what the human is doing, where they are, or whether every route has failed.
topic: telecom-voip
tags:
- sip
- status-codes
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Protocols Lie Carefully'
editorial_batch: signals-of-reality-200
---

A call fails with:

480 Temporarily Unavailable.

To a caller, the message can sound personal.

The person is unavailable.

But SIP does not have direct access to a person's life.

It has signaling state.

[RFC 3261](https://www.rfc-editor.org/rfc/rfc3261.html) defines 480 for cases where the callee's end system was contacted successfully but the callee is currently unavailable, with examples such as not logged in or a status making communication impossible.

That is already more careful than the human-language interpretation.

## Presence and personhood are different layers

A SIP registrar can know that no current contact is registered.

A proxy can know that registered contacts failed.

An endpoint can know that local policy rejects the invitation.

None of those facts tells the system where the human is.

They may be standing beside the phone while Wi-Fi is disconnected.

They may be online in an application that is not registered to this SIP domain.

They may deliberately disable calls.

The protocol reports communication reachability, not human existence.

## Temporary is also a protocol judgment

The word *temporarily* does not come with a guarantee that the user will become reachable in five minutes.

It distinguishes the condition from more permanent forms of failure.

The duration may be unknown.

A registration could return in seconds.

A device could remain offline for days.

A route could be reconfigured.

The response keeps retry conceptually possible without predicting when success will occur.

## Intermediaries can generate the response

A PBX, proxy, SBC, or gateway may generate 480 based on its own state.

For example, no contacts are registered.

Or a downstream network returned a condition that was mapped into 480.

The caller sees one code.

The infrastructure may have seen a longer story.

This is why call debugging begins with the signaling path, not the final display text.

## One response can hide several causes

480 can emerge from different operational conditions.

No registered device.

A device that cannot currently receive the session.

A temporary routing condition.

A policy mapping.

That ambiguity is intentional enough for routing logic but insufficient for root-cause analysis.

The protocol status tells clients how to behave.

Observability tells operators why this case happened.

Those are different jobs.

## A human-readable label can overclaim

Phones and PBXs often translate SIP responses into friendly messages:

Unavailable.

Offline.

Not reachable.

The friendlier the label, the easier it is to forget the underlying uncertainty.

A support engineer then asks the user, "Why were you offline?" when the real problem was stale registration state.

The label has converted an infrastructure observation into a claim about a person.

That is epistemically sloppy and operationally expensive.

## Preserve protocol wording when diagnosing

A good diagnostic record keeps the actual response code, source hop, transaction, timestamp, and routing context.

Then it can add interpretation.

Received 480 from registrar-facing proxy because no active contacts were found.

That sentence is much stronger than:

User was unavailable.

The first identifies observer and mechanism.

The second invents human state.

SIP 480 does not mean the human disappeared.

It means the signaling system, from a particular point of view at a particular moment, could not complete the invitation under conditions represented as temporary.

That is less dramatic.

It is also much closer to what the network actually knows.
