---
title: QCI 5 for IMS Signalling and QCI 1 for Voice Made QoS Concrete
url: /posts/qci-5-signalling-qci-1-voice-made-qos-concrete.html
date: '2026-09-14'
read_time: 2
excerpt: VoLTE QoS became easier to understand when I separated the persistent IMS
  signalling bearer from the dedicated low-latency bearer created for voice media.
topic: mobile-networks
tags:
- volte
- qci
- ims
- qos
- lte
draft: false
featured: false
language: en
eyebrow: 2022 Mobile Core and IMS · intermediate
outputs:
- url: /posts/qci-5-signalling-qci-1-voice-made-qos-concrete.html
  template: cms/templates/posts/posts--qci-5-signalling-qci-1-voice-made-qos-concrete.tpl
  source: cms/templates/posts/posts--qci-5-signalling-qci-1-voice-made-qos-concrete.json
---

QoS tables used to feel like values to memorize until I mapped them onto an actual VoLTE call. The useful distinction was between IMS signalling and the voice media itself. They have different traffic characteristics, so treating them as one bearer with one priority model would make little sense.

IMS signalling is commonly carried using a bearer associated with QCI 5. That traffic includes SIP registration and call-control messages. It needs reliable signalling behavior, but it is not the continuous real-time audio stream. The voice media is normally carried on a dedicated bearer using QCI 1, which is designed around conversational voice requirements such as low delay.

The timing of the dedicated bearer made the architecture more concrete. The UE can already be attached and registered to IMS before a voice call exists. When a VoLTE session is established, policy and bearer-control procedures can create the media bearer needed for the call. After the call ends, that dedicated media resource does not need to remain in the same way the IMS signalling connectivity does.

This also helped me separate SIP success from bearer success. A call can progress through SIP signalling while media setup encounters a QoS or bearer problem. From the user's perspective that may look like a connected call with missing or broken audio. The signalling trace alone does not prove that the radio and core established the expected media path.

In a lab, I found it useful to line up three timelines: SIP messages, bearer-control events and RTP packets. The SIP INVITE and 200 OK show session negotiation. The bearer events show when network resources are created or modified. The RTP stream shows whether media is actually moving. When all three are aligned, VoLTE stops looking like "SIP over LTE" and starts looking like coordinated application signalling plus mobile bearer management.

QCI values therefore became less interesting as numbers and more useful as labels for different forwarding treatment. QCI 5 and QCI 1 represent different service expectations inside the LTE QoS model. The important troubleshooting question is not whether I remember the table, but whether the correct bearer exists for the traffic the session is trying to carry.
