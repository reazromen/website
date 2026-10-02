---
title: Router-on-a-Stick Was My First Clean Inter-VLAN Routing Lab
url: /posts/router-on-a-stick-first-clean-inter-vlan-routing-lab.html
date: '2026-09-14'
read_time: 3
excerpt: One router interface, an 802.1Q trunk and a few subinterfaces were enough
  to connect separate VLANs without hiding what was happening at Layer 2 and Layer
  3.
topic: networking
tags:
- ccna
- inter-vlan-routing
- 802-1q
- routing
draft: false
featured: false
language: en
eyebrow: 2019 Routing, Linux & First VoIP · intermediate
outputs:
- url: /posts/router-on-a-stick-first-clean-inter-vlan-routing-lab.html
  template: cms/templates/posts/posts--router-on-a-stick-first-clean-inter-vlan-routing-lab.tpl
  source: cms/templates/posts/posts--router-on-a-stick-first-clean-inter-vlan-routing-lab.json
---

Router-on-a-stick is not the design I would choose for a large network, but it was an excellent lab for understanding inter-VLAN routing. Until then I had VLANs on the switch and routing on the router as separate exercises. This topology joins the two in a way that is easy to observe: several VLANs reach one physical router interface over an 802.1Q trunk, and the router uses one logical subinterface per VLAN.

I used VLAN 10 for 192.168.10.0/24 and VLAN 20 for 192.168.20.0/24. The switch uplink toward the router was configured as a trunk. On the router I created subinterfaces such as `G0/0.10` and `G0/0.20`, assigned the appropriate 802.1Q VLAN IDs, and gave them gateway addresses 192.168.10.1 and 192.168.20.1. Hosts used the subinterface address in their own VLAN as the default gateway.

The packet path is what made the lab worthwhile. A host in VLAN 10 sending to another host in VLAN 10 stays within the Layer 2 domain; the router is not involved. If that same host sends to 192.168.20.20, its /24 mask tells it the destination is remote. It ARPs for 192.168.10.1, sends the IP packet in a frame addressed to the router, and the switch carries that frame over the trunk with VLAN 10 context.

The router removes the incoming Layer 2 header, performs a routing-table lookup on the IP destination, and chooses the VLAN 20 subinterface. It then needs the destination MAC in VLAN 20, builds a new Ethernet frame, tags it for VLAN 20 on the trunk, and sends it back toward the switch. The switch removes the tag before delivering it through the destination access port. The IP packet is routed; the Ethernet frame is replaced at the Layer 3 boundary.

Most of my failures were simple. I forgot the `encapsulation dot1q` statement on a subinterface, used the wrong VLAN ID, left the switch uplink as an access port, or gave a host the wrong default gateway. Because the topology is small, each mistake has a fairly obvious observation point. `show interfaces trunk`, the router interface configuration, ARP tables and a packet capture can account for the whole path.

This lab also made asymmetric thinking more natural. If VLAN 10 can reach the router but VLAN 20 has the wrong gateway, the routing configuration may be fine while the return traffic never reaches the router. End-to-end connectivity requires both endpoint configuration and the Layer 3 forwarding path to agree.

Later, a multilayer switch with switched virtual interfaces is a more scalable way to perform the same logical job at high speed. But router-on-a-stick exposes the boundary nicely. It shows exactly where an Ethernet broadcast domain ends, where an IP routing decision begins, and how a trunk can carry several separate Layer 2 networks to one routing device.
