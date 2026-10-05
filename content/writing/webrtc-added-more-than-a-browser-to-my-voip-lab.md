---
title: WebRTC Added More Than a Browser to My VoIP Lab
url: /posts/webrtc-added-more-than-a-browser-to-my-voip-lab.html
date: '2022-09-04'
read_time: 2
excerpt: WebRTC forced me to deal with WSS, ICE, DTLS-SRTP and browser security assumptions
  instead of treating a browser as just another SIP phone.
topic: telecom-voip
tags:
- webrtc
- wss
- ice
- freeswitch
draft: false
featured: false
language: en
eyebrow: 2021 SIP Infrastructure · intermediate
outputs:
- url: /posts/webrtc-added-more-than-a-browser-to-my-voip-lab.html
  template: cms/templates/posts/posts--webrtc-added-more-than-a-browser-to-my-voip-lab.tpl
  source: cms/templates/posts/posts--webrtc-added-more-than-a-browser-to-my-voip-lab.json
---

The first time I connected a browser-based client to a VoIP lab, I expected the main change to be the user interface. It was not. WebRTC introduced a different transport and media-security model, and the browser enforced rules that a normal SIP softphone often let me ignore.

The signaling side used WebSocket Secure instead of plain UDP SIP. That meant I needed a valid TLS configuration on the WebSocket listener and a hostname the browser accepted. A self-signed certificate that was convenient for a softphone became more awkward in a browser because certificate validation was part of the normal security model.

The media side was even more different. Browser media expected ICE for candidate discovery and DTLS-SRTP for secure media. A legacy SIP endpoint on the other side might be advertising ordinary RTP. That made FreeSWITCH or rtpengine useful as an interworking point because the system could terminate the WebRTC-facing security and transport requirements while presenting conventional SIP/RTP toward the older endpoint.

I spent most of the debugging time in three places: the browser console, the SIP trace and the media relay logs. The browser console showed WebSocket or ICE failures. SIP traces confirmed whether REGISTER and INVITE reached the server. Media statistics showed whether ICE had selected a usable candidate pair and whether RTP or SRTP packets were actually moving.

NAT made ICE relevant in a way that plain LAN labs had not. A browser can have several candidate addresses: local interface addresses, server-reflexive addresses learned through STUN, and relay candidates if TURN is used. The chosen candidate pair determines where media actually goes. Looking only at the endpoint's local IP is therefore not enough.

The most useful lesson was that WebRTC is not 'SIP in JavaScript'. SIP can be one signaling choice around a WebRTC application, but the browser media stack brings its own transport, encryption and NAT traversal expectations. Once I treated those as separate components, the setup became easier to reason about.

That lab also prepared me for mixed environments. Real networks rarely replace every endpoint at once. Being able to bridge a browser client to a traditional SIP phone made the role of media gateways and signaling adapters much more concrete.
