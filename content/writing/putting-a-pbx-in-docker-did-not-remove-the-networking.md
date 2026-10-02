---
title: Putting a PBX in Docker Did Not Remove the Networking
url: /posts/putting-a-pbx-in-docker-did-not-remove-the-networking.html
date: '2026-09-14'
read_time: 2
excerpt: Containerizing a SIP service added another address and NAT boundary, which
  made port publishing, advertised addresses and RTP ranges more important rather
  than less important.
topic: linux-homelab
tags:
- docker
- sip
- rtp
- linux
draft: false
featured: false
language: en
eyebrow: 2020 VoIP Foundations · intermediate
outputs:
- url: /posts/putting-a-pbx-in-docker-did-not-remove-the-networking.html
  template: cms/templates/posts/posts--putting-a-pbx-in-docker-did-not-remove-the-networking.tpl
  source: cms/templates/posts/posts--putting-a-pbx-in-docker-did-not-remove-the-networking.json
---

I expected Docker to make a PBX deployment cleaner because the application and its dependencies could be packaged together. It did make installation repeatable, but it also inserted another networking layer into a protocol that already carried addresses and ports inside its messages. A container can be healthy, the SIP socket can be listening, and the outside endpoint can still receive unusable SDP because the application believes its container address is externally reachable.

The signaling port was the easy part. Publishing a UDP port from the host to the container allowed REGISTER and INVITE traffic to reach the service. RTP was more awkward because media typically uses a range of UDP ports selected dynamically. That range had to be configured consistently in the PBX and exposed through the container networking setup. Opening only the SIP port produced a system that looked alive until a call answered and no media crossed the boundary.

Container addresses also forced me to think carefully about advertised identity. Inside a bridge network, the PBX might see an address such as 172.x.x.x that should never appear in SDP sent to a remote endpoint. The application needs to know which external or host-side address represents it from the client's point of view. This is the same NAT problem as a PBX behind a router, but Docker makes the translation boundary easy to forget because it exists on the same physical machine.

Host networking simplified some labs because it removed the extra bridge and port-publishing layer, but it also reduced isolation and made port conflicts more direct. Bridge networking offered cleaner separation but required explicit handling of signaling and media exposure. There was no universally correct mode; the useful question was which network boundary I wanted and how SIP and RTP should traverse it.

The main lesson was that containers do not abstract networking away. They create another network environment with namespaces, interfaces, routes and translations. For ordinary HTTP services that can be mostly transparent. For SIP and RTP, where messages can advertise contact and media addresses, the difference between container address, host address and public address becomes part of the application behavior. Containerizing the service therefore made protocol knowledge more important, not less.
