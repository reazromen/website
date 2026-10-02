---
title: 'Linux Routing Tables: The Moment `ip route` Replaced Guessing'
url: /posts/linux-routing-tables-ip-route-replaced-guessing.html
date: '2026-09-14'
read_time: 3
excerpt: Once I started reading Linux routes as prefix decisions instead of interface
  settings, multi-interface hosts and lab gateways became much easier to debug.
topic: linux-homelab
tags:
- linux
- iproute2
- routing
- homelab
draft: false
featured: false
language: en
eyebrow: 2019 Routing, Linux & First VoIP · intermediate
outputs:
- url: /posts/linux-routing-tables-ip-route-replaced-guessing.html
  template: cms/templates/posts/posts--linux-routing-tables-ip-route-replaced-guessing.tpl
  source: cms/templates/posts/posts--linux-routing-tables-ip-route-replaced-guessing.json
---

A Linux machine with one Ethernet interface can hide a lot of networking detail. Add a second interface for a lab network, a VPN, or a virtual bridge and assumptions start breaking. I spent enough time changing addresses before realizing that the routing table was often the more important piece of state. The system can have the correct addresses and still send traffic through a path I did not expect.

`ip route` became the command I checked before editing configuration. A connected route such as `192.168.50.0/24 dev enp3s0 src 192.168.50.10` tells me that destinations in that prefix are directly reachable through the interface. A default route such as `default via 192.168.1.1 dev enp2s0` tells me where unmatched traffic goes. If both interfaces have gateways, route selection can get more interesting very quickly.

The longest-prefix rule is the same routing behavior I had been learning on routers. A route for 10.20.30.0/24 is more specific than 10.20.0.0/16, so it wins for a destination inside 10.20.30.0/24. Metric can influence selection between otherwise comparable routes, but specificity comes first. Seeing Linux make the same basic prefix decision as a router helped remove the artificial boundary between 'server networking' and 'networking networking'.

I used `ip route get` to ask the kernel how it would reach a specific destination. That was useful on a multi-interface host because it showed the chosen route, next hop, outgoing interface and source address. If a connection left with the wrong source address, the remote side might have no valid return path even though the destination route looked fine at first glance.

Adding a temporary static route was straightforward: `ip route add 10.50.0.0/16 via 192.168.50.1`. The important word there is temporary. Runtime changes disappear after reboot unless the persistent network configuration also describes them. That separation between current kernel state and persistent configuration became a recurring theme with Linux services.

Forwarding was another separate switch. A Linux machine with routes to two networks does not automatically behave as a router for traffic received from other hosts. IP forwarding has to be enabled, and firewall rules may still control the transit traffic. This was useful preparation for later home-lab gateways and container hosts, where Linux often sits in the middle even when it does not look like a traditional router.

The biggest change was diagnostic. Instead of saying 'this interface has Internet' or 'traffic should use this NIC', I started asking what prefix matches the destination, what next hop the kernel chose, and what source address it selected. Those questions are less intuitive at first, but they are much harder to argue with than a network diagram in my head.
