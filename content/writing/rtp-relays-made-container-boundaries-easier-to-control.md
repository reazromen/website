---
title: RTP Relays Made Container Boundaries Easier to Control
url: /posts/rtp-relays-made-container-boundaries-easier-to-control.html
date: '2024-05-07'
read_time: 1
excerpt: Anchoring media at a deliberate boundary reduced the number of private addresses
  that leaked into SDP and simplified firewall policy.
topic: telecom-voip
tags:
- rtp
- rtpengine
- docker
- nat
draft: false
featured: false
language: en
eyebrow: 2025 Voice and Infrastructure Notes · advanced
outputs:
- url: /posts/rtp-relays-made-container-boundaries-easier-to-control.html
  template: cms/templates/posts/posts--rtp-relays-made-container-boundaries-easier-to-control.tpl
  source: cms/templates/posts/posts--rtp-relays-made-container-boundaries-easier-to-control.json
---

Containerized PBX stacks become confusing when every component advertises an address from its own network namespace. SIP can be fixed with header rewriting and still leave RTP pointed at an unreachable private address.

A media relay gives the architecture a deliberate anchor. Endpoints send media to addresses owned by the relay, and the relay forwards between legs. That makes the SDP path predictable and keeps media policy in one place.

The trade-off is that the relay now sits directly in the media path, so capacity, port ranges and monitoring matter. It also does not fix signalling mistakes automatically. I still need correct dialog routing and a consistent view of which addresses are public, private and container-internal.

The value was not that relaying is always better. It was that the network boundary became explicit instead of being discovered accidentally through broken audio.
