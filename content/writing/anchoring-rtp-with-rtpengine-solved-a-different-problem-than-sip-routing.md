---
title: Anchoring RTP with rtpengine Solved a Different Problem Than SIP Routing
url: /posts/anchoring-rtp-with-rtpengine-solved-a-different-problem-than-sip-routing.html
date: '2026-03-22'
read_time: 3
excerpt: Kamailio could route the signaling perfectly while media still failed. rtpengine
  made the signaling path and media path explicit instead of treating them as one
  thing.
topic: telecom-voip
tags:
- rtp
- rtpengine
- kamailio
- sdp
draft: false
featured: false
language: en
eyebrow: 2021 SIP Infrastructure · intermediate
outputs:
- url: /posts/anchoring-rtp-with-rtpengine-solved-a-different-problem-than-sip-routing.html
  template: cms/templates/posts/posts--anchoring-rtp-with-rtpengine-solved-a-different-problem-than-sip-routing.tpl
  source: cms/templates/posts/posts--anchoring-rtp-with-rtpengine-solved-a-different-problem-than-sip-routing.json
---

By this point I was comfortable with the idea that SIP and RTP are separate, but I still tended to design them together in my head. A Kamailio proxy could route an INVITE successfully while the endpoints exchanged unusable SDP or tried to send RTP directly across a NAT boundary. Adding rtpengine forced me to make the media path explicit.

The basic lab used Kamailio for signaling and rtpengine as a media relay. On the initial offer, Kamailio passed the SDP to rtpengine so the advertised media address and port could be rewritten toward the relay. When the answer returned, the same process established the opposite side. The endpoints then sent RTP toward the relay instead of directly toward each other.

The important part was not that media now crossed the server. It was understanding why I would choose to anchor it. NAT is an obvious reason, but there are others: hiding endpoint addresses, enforcing a predictable media path, bridging address families, converting between encrypted and clear media domains, or keeping media near a service that needs to record or inspect it. The tradeoff is that the server becomes part of the media data path and must be sized and monitored accordingly.

I verified the setup with three pieces of evidence. The SIP trace showed rewritten SDP. `rtpengine-ctl` showed active media sessions. A packet capture showed RTP entering and leaving the relay on the expected interfaces. If SIP said the call was connected but the media counters stayed at zero, the problem was no longer vaguely described as 'audio broken'. I could tell whether the endpoint was sending anything to the advertised address.

The lab also exposed a common configuration mistake: calling the media-management function only on the offer side. SDP can appear in provisional responses, final responses, re-INVITEs and updates. A real call flow is more than one INVITE and one 200 OK. The media-control logic has to follow the places where SDP can change.

Once rtpengine was in the path, one-way audio became easier to localize. If RTP reached the relay from one endpoint but nothing arrived from the other, I looked at that endpoint's SDP, NAT behavior and firewall. If both streams reached the relay but one side received nothing, I inspected the relay's outgoing path. This separated the call into observable segments.

The broader lesson was architectural: a SIP proxy and a media relay solve different problems. Putting them on the same host does not make them one component. Keeping their responsibilities separate made later scaling and troubleshooting decisions much cleaner.
