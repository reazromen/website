---
title: VLANs Made Sense When I Stopped Thinking of Them as Extra Networks
url: /posts/vlans-made-sense-when-i-stopped-thinking-of-them-as-extra-networks.html
date: '2024-11-22'
read_time: 3
excerpt: A VLAN is first a Layer 2 boundary. IP subnets often map to VLANs, but keeping
  those two concepts separate makes switching and routing much easier to reason about.
topic: networking
tags:
- ccna
- vlan
- switching
- ethernet
draft: false
featured: false
language: en
eyebrow: 2018 Network Foundations · beginner
outputs:
- url: /posts/vlans-made-sense-when-i-stopped-thinking-of-them-as-extra-networks.html
  template: cms/templates/posts/posts--vlans-made-sense-when-i-stopped-thinking-of-them-as-extra-networks.tpl
  source: cms/templates/posts/posts--vlans-made-sense-when-i-stopped-thinking-of-them-as-extra-networks.json
---

VLANs confused me when I treated them as another way to create IP networks. The diagrams usually showed VLAN 10 with one subnet and VLAN 20 with another, so it was easy to merge the Layer 2 and Layer 3 ideas into one concept. The cleaner model is that a VLAN creates a separate Ethernet broadcast domain. IP addressing is normally designed to match that boundary, but the VLAN itself exists at Layer 2.

Consider one physical switch with four access ports. If ports 1 and 2 belong to VLAN 10 and ports 3 and 4 belong to VLAN 20, a broadcast received on port 1 is flooded within VLAN 10, not into VLAN 20. From an Ethernet forwarding point of view, those are separate logical switches sharing the same hardware. A host in VLAN 10 cannot send an Ethernet frame directly to a host in VLAN 20 just because both cables terminate on the same box.

The IP design normally reinforces that separation. I might use 192.168.10.0/24 for VLAN 10 and 192.168.20.0/24 for VLAN 20. A host at 192.168.10.10 sees 192.168.20.10 as remote because the destination is outside its /24. It therefore sends the packet toward its default gateway rather than ARPing directly for the destination host. Routing between the VLANs requires a Layer 3 device or a Layer 3 switch interface configured for those networks.

This is why assigning two IP subnets to ports in the same unsegmented VLAN is not equivalent to creating two VLANs. Hosts may make different Layer 3 decisions based on their masks, but the Ethernet broadcast domain is still shared. ARP broadcasts and other Layer 2 broadcasts can still reach the entire VLAN. Conversely, putting two hosts in different VLANs keeps them separated at Layer 2 even if someone mistakenly gives them addresses that appear to belong to the same IP subnet. The addressing would be wrong, but the VLAN boundary would still exist.

On a Cisco-style switch, an access port belongs to one data VLAN for ordinary untagged client traffic. The switch associates incoming frames on that port with the configured VLAN internally. The host does not need to know the VLAN number. That is useful because normal endpoints can remain unaware of the switching design. The VLAN becomes visible only when a link needs to carry traffic for multiple VLANs, which leads to trunking and 802.1Q tagging.

A simple lab made the boundary obvious. I placed two PCs in the same IP subnet but assigned their switch ports to different VLANs. They could not ARP for each other across the VLAN boundary. Then I put the ports in the same VLAN and connectivity returned. After that, I used different IP subnets and added a router interface for each VLAN. Now traffic crossed the boundary through routing instead of direct Layer 2 forwarding.

The useful mental model is therefore: VLAN first defines who shares Ethernet broadcasts; the IP subnet defines who a host considers directly reachable at Layer 3. Good designs usually align one subnet with one VLAN, but understanding why they are different prevents a lot of configuration mistakes.
