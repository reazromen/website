---
title: A Connected Call and Delivered Audio Are Different Events
date: '2022-10-28'
draft: false
language: en
url: /posts/bn-call-connected-media-journey.html
topic: telecom-voip
tags:
- sip
- rtp
featured: false
read_time: 2
excerpt: >-
  When the call timer starts, we tend to assume communication has succeeded. But SIP can
  establish the signaling state while the path that carries audio is still broken. Who
  is talking to whom and how the media packets reach them are not answered by the same
  process.
editorial_batch: 20261003-100-niches
---

When the call timer starts, we tend to assume communication has succeeded. But the timer represents only a small part of the whole event. SIP can establish agreement between both sides while the path that carries audio is still broken. Who is talking to whom and how the media packets reach them are not answered by the same process. That is why registration alone is not enough evidence when a call has one-way audio.

Imagine a PBX behind NAT. Signaling arrives correctly, but SDP advertises an address that the remote phone cannot reach. The phone will still try to send audio to that address. From the server's point of view the call is alive; from the user's point of view the conversation is dead. Before changing codecs, check where packets are being sent, whether media is arriving in both directions, and whether the firewall allows the required ports.

I find it useful to treat a call as a journey. First comes the call request, then negotiation about media addresses, then bidirectional media. Each stage needs its own evidence. A SIP trace explains signaling; RTP packet counts, sequence numbers, and arrival times explain the media path. One green status cannot prove the health of the entire journey.

Telephony monitoring should therefore ask questions close to the user's experience. Did audio arrive in both directions? Were there long gaps? Why did the call end? The number of registered phones is useful, but it is not a substitute for conversation quality. The system succeeds not when the protocols merely agree, but when sound reaches the people using it.

Source: [official reference](https://www.rfc-editor.org/rfc/rfc3550.html).
