---
title: Building a Small Home Lab from an Old PC and a Cheap Switch
url: /posts/building-a-small-home-lab-from-an-old-pc-and-a-cheap-switch.html
date: '2023-07-03'
read_time: 3
excerpt: A useful home lab does not need enterprise hardware. A spare PC, a small
  switch and a few isolated network experiments are enough to learn a lot about real
  interfaces, routes and services.
topic: linux-homelab
tags:
- homelab
- linux
- ethernet
- ccna
draft: false
featured: false
language: en
eyebrow: 2018 Network Foundations · beginner
outputs:
- url: /posts/building-a-small-home-lab-from-an-old-pc-and-a-cheap-switch.html
  template: cms/templates/posts/posts--building-a-small-home-lab-from-an-old-pc-and-a-cheap-switch.tpl
  source: cms/templates/posts/posts--building-a-small-home-lab-from-an-old-pc-and-a-cheap-switch.json
---

My idea of a home lab used to be much bigger than what I could actually justify. Rack servers, managed switches and a pile of routers looked like the proper way to learn. In practice, the first useful lab was much smaller: an old PC, a basic Ethernet switch, a laptop, and enough discipline not to mix every experiment into the normal home network.

The old PC was valuable because it gave me a machine I could break without worrying about daily work. I could reinstall Linux, change interface configuration, stop services, add routes, or lock myself out and simply start again. That freedom is more useful for learning than expensive hardware that I am afraid to touch. The switch did not need many features at first. Even an unmanaged switch is enough to work with link state, ARP, addressing, DHCP and packet captures. A managed switch becomes more useful once VLANs and trunks enter the picture.

I kept the first topology deliberately boring. The lab host and laptop sat on the same small Layer 2 segment. One interface could reach the normal network when I needed packages or documentation, while the lab-facing interface could be configured with static addresses. The important rule was to know which interface was supposed to carry which traffic. When a machine has more than one interface, a surprising amount of confusion comes from assuming the operating system will choose the path I had in mind.

On Linux, `ip addr` and `ip route` became the first two commands I checked. `ip addr` shows whether the interface is up and what addresses are assigned. `ip route` shows the kernel's forwarding decisions. If the host has `192.168.50.10/24` on one interface and a route for `192.168.50.0/24` through that interface, a peer such as `192.168.50.20` should be directly reachable at Layer 3. If a default route points somewhere unexpected, traffic to external networks may leave through a different interface.

The lab became more useful when I started running small services instead of only pinging. An SSH server made remote access practical. A simple HTTP server gave me TCP traffic to inspect. DNS queries produced UDP traffic with an obvious request/response pattern. None of those services required a large platform, but together they turned the network from an abstract diagram into something carrying real application traffic.

Isolation mattered more as the experiments became less predictable. A bad static address is annoying. Accidentally running a second DHCP server on the household LAN is worse. The safe pattern is to keep experimental broadcast domains separate when possible, and to understand exactly when a lab interface is bridged, routed or NATed into the rest of the network. Even before I had a sophisticated setup, thinking in terms of failure containment was useful.

The main lesson from this period was that a home lab is not defined by hardware quantity. It is defined by whether I can create a condition, observe what the network does, change one variable, and repeat the test. A small environment that I understand completely is a better learning tool than a large environment built mostly from copied configurations.
