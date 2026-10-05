---
title: Which Identity Should Follow a Call Through the System?
date: '2024-10-31'
draft: false
language: en
url: /posts/bn-call-id-story-boundary.html
topic: observability-monitoring
tags:
- sip
- observability
featured: false
read_time: 2
excerpt: >-
  A phone call that crosses several servers leaves pieces of its story in several places.
  Endpoint logs, PBX logs, and trunk logs may all describe it differently. Time proximity
  alone is not enough to prove that two log entries belong to the same call.
editorial_batch: 20261003-100-niches
---

A phone call that crosses several servers leaves pieces of its story in several places. Endpoint logs, PBX logs, and trunk logs may all describe it differently. Time proximity alone is not enough to prove that two log entries belong to the same call. A busy system can process many calls in the same second, so correlation needs an identity—and an understanding of that identity's limits.

A SIP Call-ID is a useful starting point. But an intermediary may terminate one side of the call and create a new leg on the other side. In that case, expecting one identifier to remain unchanged across the entire path is unsafe. The relationship between the legs has to be preserved. If the mapping from an inbound event to the outbound event it created is lost, the story breaks in the middle.

Suppose a user reports that a call dropped suddenly. The phone log shows a BYE, but that does not tell us who made the first decision to end the call. A correlated trace should reveal where the first disconnect occurred, what reason was given, and how the other components reacted. The final log line is not always the root cause; sometimes it is simply the expected consequence of an earlier failure.

Observability is therefore not the same as keeping more logs. One of its central jobs is preserving which events belong to the same piece of work. Identity, time, and leg relationships make investigations smaller. At the same time, there is no reason to create correlation keys from phone numbers or other sensitive data when a safer technical identifier can do the job.

Source: [official reference](https://www.rfc-editor.org/rfc/rfc3261.html).
