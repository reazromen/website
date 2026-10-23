---
title: "tcpdump for Linux Network Debugging: Capture Only What Matters"
draft: false
date: '2020-07-03'
language: en
url: /posts/tcpdump-network-debugging-on-linux.html
read_time: 2
excerpt: >-
  A timeout can come from DNS, routing, firewall policy, TCP setup, TLS, or the application.
eyebrow: "Perspectives · Linux Tools"
tags: ["Linux","Networking"]
---

A timeout can come from DNS, routing, firewall policy, TCP setup, TLS, or the application. `tcpdump` helps show which packets enter and leave a Linux host. Select the correct interface and filter by host, port, or protocol; inspect whether a SYN leaves, a reply returns, or retransmissions continue.

A missing packet does not prove the remote host never sent it—the capture may be on the wrong interface or affected by offload behavior. Encrypted payloads remain encrypted, and broad captures may contain private information. Compare both ends when possible and pair packet evidence with socket state, service logs, DNS checks, and request timing.
