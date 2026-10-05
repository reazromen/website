---
title: SDP Was the Part of SIP Calls I Had Been Ignoring
url: /posts/sdp-was-the-part-of-sip-calls-i-had-been-ignoring.html
date: '2022-10-07'
read_time: 2
excerpt: A SIP call can signal perfectly and still have broken audio because SDP is
  where the endpoints describe media addresses, ports and codecs.
topic: telecom-voip
tags:
- sip
- sdp
- rtp
- codecs
draft: false
featured: false
language: en
eyebrow: 2020 VoIP Foundations · intermediate
outputs:
- url: /posts/sdp-was-the-part-of-sip-calls-i-had-been-ignoring.html
  template: cms/templates/posts/posts--sdp-was-the-part-of-sip-calls-i-had-been-ignoring.tpl
  source: cms/templates/posts/posts--sdp-was-the-part-of-sip-calls-i-had-been-ignoring.json
---

For a while I read SIP traces almost entirely by looking at request methods and response codes. If the INVITE received 200 OK and the ACK followed, I treated signaling as finished and expected audio to work. The missing piece was SDP. SIP establishes and controls the session, but the body carried inside messages often describes how the media should actually be sent. A successful SIP exchange can therefore coexist with completely broken audio.

The SDP body is plain text, which makes it easy to inspect once I know which lines matter. The `c=` line describes the connection address, while the `m=` line describes a media stream, including its port and transport profile. A line such as `m=audio 18462 RTP/AVP 0 8 101` says that audio is expected on UDP port 18462 and lists payload types that the endpoint is willing to use. The `a=rtpmap` attributes can map dynamic payload types to codec names and clock rates.

The offer-answer model helped organize the exchange. One side sends an SDP offer, commonly in the INVITE, describing media it can receive. The other side returns an answer, often in the 200 OK, choosing compatible parameters. If both endpoints agree on a codec but one side advertises an unreachable private address, the SIP dialog may still establish while RTP goes to the wrong place. That was my first strong example of signaling success not being equivalent to service success.

I began checking three things whenever a call had no audio: the advertised media IP, the advertised media port, and the negotiated codec list. If the IP belonged to a private subnet that made no sense from the far side, NAT handling was immediately suspicious. If the port did not fall inside the PBX's expected RTP range, firewall rules became relevant. If there was no common codec, the call might connect while media negotiation failed or required transcoding that the system could not provide.

The important habit was to stop thinking of SDP as decorative SIP payload. It is operational data that tells the media plane where to go. Reading the SIP start line explains who is calling whom; reading the SDP explains where the audio packets are expected to travel. Once I started checking both, one-way audio and no-audio problems became much less mysterious.
