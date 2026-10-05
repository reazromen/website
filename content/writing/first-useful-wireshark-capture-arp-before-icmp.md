---
title: 'My First Useful Wireshark Capture: ARP Before ICMP'
url: /posts/first-useful-wireshark-capture-arp-before-icmp.html
date: '2025-02-06'
read_time: 3
excerpt: 'Capturing a simple ping showed that the interesting packet often arrives
  before ICMP: ARP has to resolve the Layer 2 destination first.'
topic: networking
tags:
- wireshark
- arp
- icmp
- packet-capture
draft: false
featured: false
language: en
eyebrow: 2018 Network Foundations · beginner
outputs:
- url: /posts/first-useful-wireshark-capture-arp-before-icmp.html
  template: cms/templates/posts/posts--first-useful-wireshark-capture-arp-before-icmp.tpl
  source: cms/templates/posts/posts--first-useful-wireshark-capture-arp-before-icmp.json
---

Wireshark became useful to me when I stopped opening it just to watch a wall of packets. The first capture that taught me something concrete was a simple ping between two hosts on the same subnet. I expected to see ICMP echo requests and replies. I did see them, but only after ARP had done the work required to build the Ethernet frame.

The setup was intentionally small. Two hosts shared one Layer 2 network. Before starting the test I cleared or waited out the relevant ARP entry so the sender did not already know the destination MAC address. Then I started the capture and sent one ping. The first important frame was an ARP request asking who had the target IPv4 address. That request used the Ethernet broadcast destination because the sender did not yet know which MAC address belonged to the IP.

The target answered with an ARP reply containing its MAC address. After that exchange, the ICMP echo request could be sent inside a unicast Ethernet frame. The IP destination stayed the same throughout the test, but the Ethernet destination depended on what the sender had learned. That made the division between Layer 2 and Layer 3 much clearer than a diagram did.

The capture also showed why filters matter. A display filter such as `arp || icmp` reduced the noise enough that I could follow the sequence. Later, filtering by host address, protocol or port became normal practice. The important point was not memorizing Wireshark syntax. It was learning to ask a narrow question before opening the capture. What address is the host trying to resolve? Did a reply come back? Did the ICMP request leave? Was there an echo reply?

I also learned to distinguish capture location from network truth. A packet not visible on my interface does not automatically mean it never existed anywhere. Switched Ethernet forwards known unicast frames selectively, so a third host connected to another access port may not see the conversation at all. Capturing on the sender, receiver, a mirrored switch port, or a routed hop can produce very different evidence. The capture point is part of the experiment.

Repeating the test with a remote destination added another useful detail. When the target IP is outside the local subnet, the sender does not ARP for the remote host. It ARPs for the default gateway's local interface because the Ethernet frame only needs to reach the next hop. The IP packet still names the final destination. Watching that happen made routing feel less like a separate chapter and more like an extension of the same forwarding process.

That small ARP-plus-ICMP trace became my reference for packet analysis. Start with a controlled topology, clear cached state when necessary, capture as close to the endpoint as possible, and follow the packet dependencies in order. Wireshark is much less intimidating when the capture has a question behind it.
