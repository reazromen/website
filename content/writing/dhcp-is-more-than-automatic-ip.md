---
title: DHCP Is More Than Automatic IP
url: /posts/dhcp-is-more-than-automatic-ip.html
date: '2026-09-14'
read_time: 3
excerpt: DHCP is easier to troubleshoot when treated as a timed client-server exchange
  that delivers an address plus the parameters a host needs to participate in the
  network.
topic: networking
tags:
- dhcp
- ccna
- udp
- broadcast
draft: false
featured: false
language: en
eyebrow: 2018 Network Foundations · beginner
outputs:
- url: /posts/dhcp-is-more-than-automatic-ip.html
  template: cms/templates/posts/posts--dhcp-is-more-than-automatic-ip.tpl
  source: cms/templates/posts/posts--dhcp-is-more-than-automatic-ip.json
---

I originally thought of DHCP as the thing that gives a computer an IP address. That description is not wrong, but it hides most of the useful behavior. DHCP is a client-server protocol that can provide an address, subnet mask, default gateway, DNS servers, lease time and other options. More importantly, the client often starts with almost no usable network identity, so the early exchange has to work before ordinary unicast communication is available.

The common sequence is remembered as DORA: Discover, Offer, Request, Acknowledge. A new client sends a DHCPDISCOVER because it does not yet know which DHCP server to contact. The server responds with an offer. The client requests the offered configuration, and the server acknowledges the lease. The exchange uses UDP, traditionally server port 67 and client port 68. In the early stages, broadcasts are common because the client may not yet have a usable address or server information.

Seeing this in a capture is much better than only memorizing the acronym. The Discover contains a client identifier or hardware information and a list of requested parameters. The Offer includes an address the server is willing to lease. The Request tells the network which offer the client intends to accept, and the ACK confirms the final parameters. Once I could identify those messages in Wireshark, a failed DHCP configuration became a sequence problem rather than a vague state called 'no IP'.

The broadcast behavior also explains why DHCP works easily inside one VLAN but needs help across routed boundaries. Routers do not normally forward local Layer 2 broadcasts between subnets. If the DHCP server sits in another network, a relay agent can receive the client's broadcast and forward the request toward the server as routable traffic. In Cisco labs this appears as an `ip helper-address` configuration on the Layer 3 interface serving the client subnet.

Lease timing matters too. An address is not simply assigned forever. The client attempts to renew before the lease expires. That makes DHCP stateful enough that intermittent server failures can be confusing: existing clients may continue working because their leases are still valid while new clients fail to obtain configuration. Looking only at one working laptop could therefore give the wrong impression about server health.

I found it useful to test DHCP failures deliberately. Put the client in the wrong VLAN, stop the DHCP service, remove the relay configuration, or exhaust a small address pool. Each case can lead to 'no address', but the packet capture tells a different story. No Discover leaving the client points in one direction. Repeated Discovers with no Offer point elsewhere. An Offer that never becomes a successful lease suggests another part of the exchange is failing.

The key change in my understanding was to stop treating DHCP as background automation. It is a visible protocol with a clear conversation. Once the conversation is observable, troubleshooting becomes much less dependent on clicking renew and hoping the address appears.
