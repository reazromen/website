---
title: What a Switch Actually Learns from a MAC Address
url: /posts/what-a-switch-actually-learns-from-a-mac-address.html
date: '2026-08-28'
read_time: 3
excerpt: A switch learns from source MAC addresses, not destination addresses. Watching
  the table populate makes unknown unicast, flooding and forwarding much easier to
  reason about.
topic: networking
tags:
- ccna
- ethernet
- switching
- mac
draft: false
featured: false
language: en
eyebrow: 2018 Network Foundations · beginner
outputs:
- url: /posts/what-a-switch-actually-learns-from-a-mac-address.html
  template: cms/templates/posts/posts--what-a-switch-actually-learns-from-a-mac-address.tpl
  source: cms/templates/posts/posts--what-a-switch-actually-learns-from-a-mac-address.json
---

One sentence changed how I understood Ethernet switching: a switch learns from the source MAC address of frames it receives. I had previously pictured the switch as looking at a destination, somehow discovering the device, and then remembering where it was. The real process is simpler and more mechanical.

Suppose a switch has an empty MAC address table. A frame enters port Fa0/1 from a host whose source address is 00:11:22:33:44:55. Before deciding what to do with the frame, the switch can associate that source MAC with Fa0/1 in the current VLAN. It does not need any protocol above Ethernet to make that observation. The frame itself provided the evidence.

The destination side is a separate decision. If the destination MAC is already in the table, the switch sends the frame toward the learned port, assuming the outgoing port is different from the incoming one. If the destination is a broadcast address, the frame is flooded within the broadcast domain. If the destination is an unknown unicast, the switch also floods it because it has no better information yet. Flooding is therefore not the same as broadcasting. A broadcast is a property of the destination address; unknown-unicast flooding is a forwarding behavior caused by missing table state.

This is easy to watch in a small lab. Clear the dynamic MAC table, generate traffic from one host, and inspect the table. On Cisco IOS the familiar command is `show mac address-table`. Generate traffic in the opposite direction and the second host appears. Move a host to another access port and, after the switch receives frames from that source on the new port, the entry can be relearned. Dynamic entries also age out when traffic disappears for long enough.

The VLAN association matters. A switch does not maintain one global Layer 2 identity map where a MAC address means the same forwarding path everywhere. The forwarding database is scoped by VLAN. This becomes important later when trunks carry multiple VLANs over the same physical link. The same physical interface can participate in forwarding decisions for many separate Layer 2 domains.

MAC learning also explains a common lab observation: captures on one switch port do not normally show every unicast frame sent by other hosts once the switch has learned the topology. A hub repeats bits to every port. A switch tries to constrain unicast forwarding based on its table. That difference is fundamental to understanding why switched Ethernet scales better than old shared-media designs, even though broadcasts and unknown destinations still create flooded traffic.

The most useful troubleshooting habit here is to ask what the switch has actually learned, not what I intended the cabling to mean. If a host is connected but no source traffic has arrived, its dynamic MAC entry might not exist yet. If the address appears on the wrong port, there may be an unexpected patch, loop, bridge or device in the path. If the entry keeps moving between ports, that is a stronger clue than simply saying the network is unstable.

A MAC table is not a configuration diagram. It is observed forwarding state. That distinction made later switching problems much easier to approach.
