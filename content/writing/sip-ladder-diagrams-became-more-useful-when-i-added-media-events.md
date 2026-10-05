---
title: SIP Ladder Diagrams Became More Useful When I Added Media Events
url: /posts/sip-ladder-diagrams-became-more-useful-when-i-added-media-events.html
date: '2024-05-11'
read_time: 1
excerpt: A signalling-only ladder can say a call succeeded while the user heard silence;
  adding SDP and RTP events fixes that blind spot.
topic: telecom-voip
tags:
- sip
- sdp
- rtp
- troubleshooting
draft: false
featured: false
language: en
eyebrow: 2024 Telecom and Embedded Notes · advanced
outputs:
- url: /posts/sip-ladder-diagrams-became-more-useful-when-i-added-media-events.html
  template: cms/templates/posts/posts--sip-ladder-diagrams-became-more-useful-when-i-added-media-events.tpl
  source: cms/templates/posts/posts--sip-ladder-diagrams-became-more-useful-when-i-added-media-events.json
---

I used to draw SIP ladders with REGISTER, INVITE, provisional responses, 200 OK, ACK and BYE, then stop. That is enough to explain the dialog and not enough to explain the call.

The missing information is media state. I now annotate where SDP offers and answers appear, which addresses and ports are negotiated, when RTP should begin, and whether a media relay rewrites the path. A 200 OK is then no longer the end of the story; it is the point where I can compare negotiated media against observed packets.

This matters most for partial failures. A call can ring, answer and clear normally while audio is one-way. The SIP ladder looks healthy. The media annotations immediately show whether the problem is a bad advertised address, blocked RTP range, codec disagreement or missing relay state.

The improvement is small but it changed incident notes. The ladder describes both control and media expectations, so someone reading it later can see where the user experience diverged from signalling success.
