---
title: TLS Protected My SIP Signaling, Not My RTP
url: /posts/tls-protected-my-sip-signaling-not-my-rtp.html
date: '2026-09-14'
read_time: 2
excerpt: A secure SIP transport and encrypted media are separate decisions. TLS can
  protect signaling while RTP remains completely visible on the wire.
topic: telecom-voip
tags:
- sip
- tls
- srtp
- rtp
draft: false
featured: false
language: en
eyebrow: 2021 SIP Infrastructure · intermediate
outputs:
- url: /posts/tls-protected-my-sip-signaling-not-my-rtp.html
  template: cms/templates/posts/posts--tls-protected-my-sip-signaling-not-my-rtp.tpl
  source: cms/templates/posts/posts--tls-protected-my-sip-signaling-not-my-rtp.json
---

After getting SIP over TLS working, I made an assumption that is easy to make: the call was now encrypted. A packet capture corrected that quickly. The SIP messages were inside TLS, but the RTP stream was still ordinary RTP and the audio payload remained visible to anyone able to capture the media path.

That distinction is architectural. SIP signaling and media normally use different flows. TLS protects the signaling transport between two SIP hops. It can hide credentials, headers and SDP from passive observers on that segment, but it does not automatically transform the media protocol negotiated inside SDP.

For encrypted media, SRTP is a separate mechanism. The endpoints need to agree on keys and crypto parameters using an appropriate key-management method. Depending on the system, that might involve SDES information carried in SDP or a negotiation such as DTLS-SRTP. The security properties differ, so simply seeing `RTP/SAVP` or a crypto attribute is not enough to make broad claims about end-to-end security.

The lab was straightforward. I placed a call using SIP over TLS and captured traffic on the PBX host. Wireshark could not decode the signaling without access to the TLS session secrets, but it immediately identified the UDP media flow. Repeating the call with SRTP changed what was visible in the media packets. The packet timing and addresses were still observable, but the audio payload was no longer plain RTP content.

A media relay complicates the trust boundary further. An rtpengine deployment can terminate one media security context and create another. That can be useful when bridging an SRTP-capable WebRTC endpoint to a legacy RTP endpoint, but it means the relay is a trusted point with access to clear media internally. 'Encrypted call' is therefore incomplete unless I specify between which components the encryption applies.

This also changed how I documented systems. Instead of one checkbox called secure VoIP, I started listing signaling transport, authentication, media transport and termination points separately. SIP over TLS, SRTP, certificate validation and endpoint identity are related controls, but each protects a different part of the call.

The packet capture was a useful reality check. Security claims are easier to evaluate when I can point to a specific flow and say exactly what is protected on that hop and what is not.
