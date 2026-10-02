---
title: Spanning Tree Stopped Looking Weird Once I Built a Loop on Purpose
url: /posts/spanning-tree-stopped-looking-weird-once-i-built-a-loop-on-purpose.html
date: '2026-09-14'
read_time: 3
excerpt: 'STP made more sense after I created the failure it is designed to prevent:
  a Layer 2 loop with no TTL to save the network.'
topic: networking
tags:
- ccna
- stp
- switching
- ethernet
draft: false
featured: false
language: en
eyebrow: 2019 Routing, Linux & First VoIP · intermediate
outputs:
- url: /posts/spanning-tree-stopped-looking-weird-once-i-built-a-loop-on-purpose.html
  template: cms/templates/posts/posts--spanning-tree-stopped-looking-weird-once-i-built-a-loop-on-purpose.tpl
  source: cms/templates/posts/posts--spanning-tree-stopped-looking-weird-once-i-built-a-loop-on-purpose.json
---

Spanning Tree was one of those topics I could answer in a multiple-choice question before I really understood why it existed. The diagrams showed redundant switch links, a root bridge, port roles and one interface sitting in a blocking state. It looked like a protocol that deliberately disabled perfectly good links. That feels wasteful until you actually build a Layer 2 loop and watch what ordinary Ethernet does with a broadcast frame.

I used three switches in a triangle and put a host on one edge. With spanning tree operating normally, one of the redundant paths was not forwarding user traffic. When I removed the loop protection in a lab and generated broadcast traffic, the problem became obvious. Ethernet frames do not carry a hop count like IP packets do. A broadcast can be forwarded by one switch, arrive at another, then come back around the redundant path. The switches can also keep relearning the same source MAC on different ports. The network does not need much traffic to become unstable.

That gave the root bridge election a reason to exist. STP needs a consistent reference point so every switch can make compatible decisions about which paths should forward and which path should remain available but blocked. Bridge ID combines priority and MAC information, and the lowest value wins the root election. Once the root is chosen, each non-root switch calculates its best path toward it. The terms root port, designated port and blocked or alternate port started to describe actual forwarding choices instead of vocabulary to memorize.

A useful verification command in Cisco-style labs is `show spanning-tree`. I stopped reading only the final state and started checking the root ID, the local bridge ID, root cost and which interface had which role. If I expected a certain switch to become root but another device won, the topology could still converge, just not in the way I intended. Changing bridge priority then became a design decision rather than a cosmetic command.

The other thing that clicked was that STP is not a routing protocol. It is not finding an IP path. It is controlling a Layer 2 topology so Ethernet forwarding does not contain loops. If two VLANs have separate spanning-tree instances, they can make different forwarding decisions even while using the same physical switches. That matters later when trunks carry several VLANs across the same links.

I still prefer small STP labs. Three switches are enough to see the root election, redundant path and reconvergence after a link failure. Larger diagrams make the protocol look more sophisticated than the problem really is. At the center, STP is solving a very specific issue: Ethernet redundancy is useful, but a forwarding loop is destructive, so one path has to wait until it is needed.
