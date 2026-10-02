---
title: RTP Is Not SIP, and That Difference Explains a Lot of Broken Calls
url: /posts/rtp-is-not-sip-and-that-difference-explains-broken-calls.html
date: '2026-09-14'
read_time: 2
excerpt: Signaling and media usually take different paths, use different ports and
  fail for different reasons, so a working SIP registration says very little about
  RTP health.
topic: telecom-voip
tags:
- rtp
- sip
- udp
- voip
draft: false
featured: false
language: en
eyebrow: 2020 VoIP Foundations · intermediate
outputs:
- url: /posts/rtp-is-not-sip-and-that-difference-explains-broken-calls.html
  template: cms/templates/posts/posts--rtp-is-not-sip-and-that-difference-explains-broken-calls.tpl
  source: cms/templates/posts/posts--rtp-is-not-sip-and-that-difference-explains-broken-calls.json
---

One of the easiest mistakes in early VoIP troubleshooting is to say that a phone is connected to the PBX and assume the call path is therefore healthy. SIP registration may be working on port 5060 while the audio uses a completely different set of UDP ports. The protocols solve different problems. SIP handles signaling such as registration, call setup and teardown. RTP carries the media stream after the endpoints have negotiated where that stream should go.

In a basic Asterisk setup, SIP signaling might arrive on one well-known listening port, while RTP is allocated dynamically from a configured port range. The actual destination port is learned through SDP. That means a firewall can allow every REGISTER and INVITE while silently dropping all audio packets. It also means packet captures taken only with a SIP display filter can show a perfect call while completely hiding the failing media plane.

RTP itself is intentionally lightweight. The header carries fields such as sequence number, timestamp, synchronization source identifier and payload type. The sequence number helps a receiver identify packet ordering and loss. The timestamp relates packets to media sampling time. Payload type tells the receiver how to interpret the media according to the negotiated codec mapping. None of this performs call control; RTP assumes the session details were established elsewhere.

The first useful test was to capture a short call and separate signaling from media. I would confirm the INVITE, 200 OK and ACK, note the SDP addresses and ports, then filter for UDP traffic matching those media ports. If packets existed in both directions, I could move on to codec or endpoint playback issues. If packets moved only one direction, NAT or firewall behavior became much more likely. If there were no media packets at all, I went back to the SDP and PBX configuration.

This separation also made network design clearer. A SIP proxy can participate heavily in signaling without carrying RTP. A media relay or PBX may deliberately anchor the RTP path. Two endpoints can therefore have a signaling path through several servers and a media path that is shorter, longer, or completely different. Once I stopped picturing the call as one connection, the architecture became easier to understand and troubleshoot.
