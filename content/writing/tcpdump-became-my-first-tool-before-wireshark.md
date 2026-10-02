---
title: tcpdump Became My First Tool Before Wireshark
url: /posts/tcpdump-became-my-first-tool-before-wireshark.html
date: '2026-09-14'
read_time: 3
excerpt: On a headless Linux box, tcpdump was faster than moving captures around blindly.
  A narrow capture at the right interface often answered the question immediately.
topic: linux-homelab
tags:
- tcpdump
- linux
- packet-capture
- troubleshooting
draft: false
featured: false
language: en
eyebrow: 2019 Routing, Linux & First VoIP · intermediate
outputs:
- url: /posts/tcpdump-became-my-first-tool-before-wireshark.html
  template: cms/templates/posts/posts--tcpdump-became-my-first-tool-before-wireshark.tpl
  source: cms/templates/posts/posts--tcpdump-became-my-first-tool-before-wireshark.json
---

Wireshark was still my preferred tool when I wanted to inspect a conversation in detail, but `tcpdump` became the tool I reached for first on a Linux server. Most lab machines were running without a desktop, and when something was unreachable I usually wanted one quick answer before opening a large capture: did the packet arrive at this interface, and did anything leave in response?

The simplest useful capture was often something like `tcpdump -ni eth0 host 192.168.50.20`. The `-n` option prevents name resolution from adding noise or delays, and `-i` selects the interface. From there I could narrow by protocol or port: `icmp`, `udp port 53`, `tcp port 22`, or a combination of source and destination conditions. A small filter makes the output readable enough that a terminal can show the sequence in real time.

Capture location became more important as the lab gained routers and multi-interface Linux hosts. If I expected a packet to cross a gateway, I could capture on the ingress interface and the egress interface separately. Seeing the request arrive on one side but never leave the other pointed toward routing, forwarding or firewall state on that host. Seeing it leave but never return moved the investigation farther down the path.

The `-w` option was the bridge back to Wireshark. I could write a pcap file on the server, reproduce the problem for a few seconds, stop the capture, and then inspect the file in Wireshark from another machine. That was especially useful for protocols where header fields mattered more than a one-line summary. The terminal capture gave me confidence that I was collecting the right traffic before I spent time reading it.

I also became more careful about what a capture proves. If tcpdump on an interface shows no packet, that does not automatically mean the sender never transmitted it. The packet may have taken another route, been dropped earlier, or arrived on a different interface. Conversely, seeing a packet arrive does not prove the local application received it. A firewall can drop it after capture, or no process may be listening on the destination port.

For services, I started pairing `tcpdump` with `ss`. If a TCP SYN reached the server on port 22 and `ss -lntp` showed sshd listening on the expected address, the next question was different from a case where no listener existed. Packet evidence and socket state together were much more useful than restarting the service and hoping.

This became a habit that carried into later VoIP work. Signaling and media problems are much easier to reason about when I can capture at the actual server and confirm what entered and left. The protocol changes, but the first question remains the same: what packets did this machine really see?
