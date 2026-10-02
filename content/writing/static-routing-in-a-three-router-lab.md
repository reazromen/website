---
title: Static Routing in a Three-Router Lab
url: /posts/static-routing-in-a-three-router-lab.html
date: '2026-09-14'
read_time: 3
excerpt: 'A three-router topology is enough to show the most important routing lesson:
  reachability is directional, and the return path matters just as much as the forward
  path.'
topic: networking
tags:
- ccna
- routing
- static-route
- ipv4
draft: false
featured: false
language: en
eyebrow: 2018 Network Foundations · beginner
outputs:
- url: /posts/static-routing-in-a-three-router-lab.html
  template: cms/templates/posts/posts--static-routing-in-a-three-router-lab.tpl
  source: cms/templates/posts/posts--static-routing-in-a-three-router-lab.json
---

A three-router static-routing lab was the first topology where I could see that a route is a local decision, not a property of the whole network. Router A can know how to reach a LAN behind Router C while Router C has no idea how to return traffic to the LAN behind Router A. The forward path can be correct and the ping can still fail because routing has to work in both directions.

A simple topology is enough. Router A has LAN 192.168.10.0/24, Router B sits in the middle, and Router C has LAN 192.168.30.0/24. Point-to-point transit networks connect A to B and B to C. Each router automatically knows only its directly connected networks. Nothing about the physical diagram causes A to learn 192.168.30.0/24.

On Router A I can add a static route for 192.168.30.0/24 through Router B's next-hop address. Router B needs routes toward both edge LANs if they are not directly connected, and Router C needs a route back to 192.168.10.0/24. Once every hop has enough information for the forward and return directions, the end hosts can communicate.

The routing table is the important evidence. `show ip route` on a Cisco router or `ip route` on Linux tells me which prefixes are known and how a matching packet will be forwarded. The router chooses the most specific matching route, which is the basis of longest-prefix matching. A default route is simply a very broad match used when no more specific entry applies.

This lab also exposed a common mistake: assuming that because the middle router can ping both edge routers, the edge LANs must be able to reach each other. The router interfaces may be directly connected while the end-user subnets are not present in all required routing tables. Testing router-to-router addresses and testing end-to-end host connectivity answer different questions.

Traceroute became useful here because it shows where the forwarding path stops progressing. If traffic reaches Router B and then fails, I inspect B's route for the destination. If the request reaches Router C but no reply returns, I inspect the reverse direction. A failed ping by itself does not say which half of the path is broken.

Static routes are not a scalable way to operate a large changing network, but that is exactly why they are good for learning. There is no routing protocol hiding the control-plane work. Every route exists because I entered it or because the network is directly connected. When the topology changes, the limitations are obvious. That makes the transition to OSPF and other dynamic routing protocols easier to understand: those protocols automate the exchange and calculation of reachability information that this lab required me to manage by hand.
