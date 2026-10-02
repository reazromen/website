---
title: Docker Networks Hid Less Once I Drew the Packet Path
url: /posts/docker-networks-hid-less-once-i-drew-the-packet-path.html
date: '2026-09-14'
read_time: 1
excerpt: Container networking stopped feeling magical when I separated host routing,
  bridge interfaces, NAT and the application socket.
topic: linux-homelab
tags:
- docker
- linux
- networking
- voip
draft: false
featured: false
language: en
eyebrow: 2024 Telecom and Embedded Notes · intermediate
outputs:
- url: /posts/docker-networks-hid-less-once-i-drew-the-packet-path.html
  template: cms/templates/posts/posts--docker-networks-hid-less-once-i-drew-the-packet-path.tpl
  source: cms/templates/posts/posts--docker-networks-hid-less-once-i-drew-the-packet-path.json
---

Docker made services easy to start and sometimes harder to reason about. The cure was to stop thinking in container names and draw the packet path.

A SIP packet arriving at the host may hit a published port, a bridge interface and a container socket before the application sees it. Return traffic can be translated again on the way out. RTP adds a second problem because signalling can advertise addresses that do not match the actual path.

I started checking the host route table, Docker bridge addresses, published ports and application bind addresses separately. If the service listened only inside the container, the host firewall was not the first problem. If signalling reached the container but SDP advertised the wrong address, the Docker port mapping was not enough to fix media.

This was one of the first places where infrastructure and VoIP debugging became inseparable for me. Containers do not remove networking; they add another network boundary that has to be made explicit.
