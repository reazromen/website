---
title: The Call Connected but Only One Side Had Audio
url: /posts/the-call-connected-but-only-one-side-had-audio.html
date: '2021-09-07'
read_time: 2
excerpt: One-way audio was my first VoIP problem where the signaling looked healthy
  and the real fault was the address and port information used for RTP.
topic: telecom-voip
tags:
- rtp
- nat
- sip
- troubleshooting
draft: false
featured: false
language: en
eyebrow: 2020 VoIP Foundations · intermediate
outputs:
- url: /posts/the-call-connected-but-only-one-side-had-audio.html
  template: cms/templates/posts/posts--the-call-connected-but-only-one-side-had-audio.tpl
  source: cms/templates/posts/posts--the-call-connected-but-only-one-side-had-audio.json
---

The first one-way-audio problem I worked through was useful because it forced me to stop treating a call as one end-to-end connection. Both phones rang, the call answered, and the SIP trace showed the expected 200 OK and ACK. One side could hear the other perfectly. The reverse direction was silent. That symptom narrowed the problem much more than I initially realized: signaling had established the call, at least one RTP direction worked, and the failure was directional.

The next step was to read the SDP from both sides and write down the advertised media addresses and ports. One endpoint was behind NAT and advertised a private address that was not reachable from the other network. The PBX knew where the SIP messages had actually arrived from, but the media description still contained an address that only made sense inside the endpoint's local LAN. RTP packets in one direction reached the PBX, while packets in the other direction followed the unusable SDP information.

A packet capture made the asymmetry obvious. Instead of filtering only for SIP, I looked at the negotiated RTP ports and compared both directions. One stream had a steady sequence of UDP packets. The reverse stream was either missing or being sent toward the wrong address. That was much better evidence than repeatedly changing codecs, which had been my first instinct because the symptom was 'no sound'. Codec negotiation matters, but a codec cannot help packets that never arrive.

NAT makes VoIP awkward because SIP payloads can carry IP addresses and ports inside the application message while the IP and UDP headers are also being translated by the network. A simple header translation does not automatically make the addresses inside SDP correct. PBXs and endpoints therefore need NAT-aware behavior, and some deployments use STUN, symmetric RTP, media relays, or other techniques depending on the topology. The exact feature is less important than understanding which address each side believes it should send media to.

The troubleshooting sequence I kept was straightforward: confirm the dialog, inspect both SDP bodies, identify the expected RTP endpoints, capture the media, then compare the actual packet path with the advertised path. One-way audio stopped being a mysterious telephony problem and became a directional UDP reachability problem with signaling metadata that could be inspected directly.
