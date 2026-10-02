---
title: Reading My First SIP REGISTER and INVITE in Wireshark
url: /posts/reading-first-sip-register-and-invite-wireshark.html
date: '2026-09-14'
read_time: 3
excerpt: SIP became much less mysterious once I stopped reading it as 'phone system
  traffic' and followed it as a text-based request and response protocol with explicit
  state transitions.
topic: telecom-voip
tags:
- sip
- wireshark
- asterisk
- voip
draft: false
featured: false
language: en
eyebrow: 2019 Routing, Linux & First VoIP · intermediate
outputs:
- url: /posts/reading-first-sip-register-and-invite-wireshark.html
  template: cms/templates/posts/posts--reading-first-sip-register-and-invite-wireshark.tpl
  source: cms/templates/posts/posts--reading-first-sip-register-and-invite-wireshark.json
---

By the end of the year I was spending more time looking at SIP packets than PBX configuration screens. The protocol helped because it is readable. A REGISTER or INVITE contains headers that look closer to an email or HTTP-style message than to a binary telecom protocol. That made packet capture a practical way to learn what the endpoints and server were actually asking each other to do.

REGISTER was the first message I followed properly. The client sends a REGISTER toward its SIP domain or registrar with an Address of Record in the `To` and `From` headers and a `Contact` header describing where that user can currently be reached. Authentication usually adds another exchange: the server challenges the client, and the client repeats the request with authorization information. A successful response tells me the registrar accepted the binding; it does not establish a phone call.

INVITE starts a different transaction. The Request-URI identifies the target of the session, while headers such as `Via`, `From`, `To`, `Call-ID`, `CSeq` and `Contact` help route and identify the dialog and transaction. I did not try to memorize every header. I followed one call and asked what each value was doing. `Call-ID` was especially useful because Wireshark could show messages belonging to the same call even when several SIP exchanges were happening at once.

The provisional responses made the ringing process less mysterious. A server or endpoint can return responses such as 100 Trying or 180 Ringing before the final answer. A successful 200 response to the INVITE is followed by ACK. That sequence showed why a SIP call is not one request followed by one response. There are transactions inside a longer dialog, and different methods handle different pieces of the session.

SDP inside the SIP message was where networking came back into the picture. The signaling packet could tell the other side which IP address, UDP port and codec to use for media. I could have a perfectly valid 200 OK while the SDP advertised an unreachable address. The result was a call that looked established in SIP but had no useful RTP path. That was the first time I really understood why reading only the SIP status code is not enough for audio troubleshooting.

Wireshark's SIP flow view and RTP analysis were helpful, but the raw packet still mattered. I wanted to know what address was advertised, what source address carried the packet, whether NAT had changed one but not the other, and which side selected the media port. A graphical ladder is convenient after the basic message fields make sense.

This was probably the point where VoIP stopped looking like a separate specialty and started looking like another networked system with its own application protocol. The same troubleshooting habits still applied: capture at a known point, separate signaling from media, check the return path, and read what the protocol actually says before changing configuration.
