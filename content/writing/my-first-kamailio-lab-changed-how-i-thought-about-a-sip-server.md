---
title: My First Kamailio Lab Changed How I Thought About a SIP Server
url: /posts/my-first-kamailio-lab-changed-how-i-thought-about-a-sip-server.html
date: '2026-06-13'
read_time: 2
excerpt: Kamailio made it obvious that SIP routing, registration and media handling
  do not have to live inside one PBX process.
topic: telecom-voip
tags:
- kamailio
- sip
- proxy
- voip
draft: false
featured: false
language: en
eyebrow: 2020 VoIP Foundations · intermediate
outputs:
- url: /posts/my-first-kamailio-lab-changed-how-i-thought-about-a-sip-server.html
  template: cms/templates/posts/posts--my-first-kamailio-lab-changed-how-i-thought-about-a-sip-server.tpl
  source: cms/templates/posts/posts--my-first-kamailio-lab-changed-how-i-thought-about-a-sip-server.json
---

Asterisk and FreeSWITCH had trained me to think of the SIP server as the place where endpoints register, calls are routed, dialplan logic runs and media may be anchored. Kamailio challenged that picture because it is fundamentally a SIP routing engine rather than a traditional PBX. It can receive, inspect and forward signaling at high scale without automatically becoming the media endpoint for the call.

My first useful lab was deliberately limited to two SIP clients and a proxy path. The goal was not to build a carrier platform; it was to watch an INVITE pass through Kamailio and understand which headers changed and which stayed end-to-end. Via and Record-Route became much more important because the proxy needed responses and in-dialog requests to follow the correct signaling path. That made earlier work on transactions and dialogs immediately relevant.

Registration also looked different once I separated registrar behavior from call processing. A location service can store the current contact for a user, while routing logic decides how an incoming request should be handled. Those functions can be composed rather than hidden behind one monolithic PBX configuration. That architecture starts to matter when multiple application servers, trunks or routing policies need to share the same SIP edge.

The media path was the most important change in perspective. Kamailio did not need to carry RTP merely because it handled the INVITE. If the endpoints could exchange media directly, the proxy could remain signaling-only. If NAT, topology hiding or policy required media anchoring, a separate RTP relay could be introduced. Signaling and media were now visibly independent components instead of two features inside one application.

The lab did not make PBXs obsolete; it clarified their role. Asterisk and FreeSWITCH are excellent when call applications, media features and dialplan behavior belong together. A SIP proxy is useful when the problem is routing, registration, policy or scale at the signaling layer. By the end of 2020, that distinction was the most important change in how I viewed VoIP architecture, and it set up the questions I wanted to explore next: proxies, media relays, TLS, WebRTC and multi-server routing.
