---
title: When One VLAN Would Not Cross the Trunk
url: /posts/when-one-vlan-would-not-cross-the-trunk.html
date: '2024-01-25'
read_time: 3
excerpt: A trunk can be up while one VLAN is still broken. That lab pushed me to verify
  allowed VLANs and operational state instead of assuming the link was simply good
  or bad.
topic: networking
tags:
- ccna
- vlan
- trunking
- troubleshooting
draft: false
featured: false
language: en
eyebrow: 2019 Routing, Linux & First VoIP · intermediate
outputs:
- url: /posts/when-one-vlan-would-not-cross-the-trunk.html
  template: cms/templates/posts/posts--when-one-vlan-would-not-cross-the-trunk.tpl
  source: cms/templates/posts/posts--when-one-vlan-would-not-cross-the-trunk.json
---

One of my more useful VLAN labs failed in a way that looked inconsistent. Two switches were connected by a trunk. Hosts in VLAN 10 could communicate across the link, but hosts in VLAN 20 could not. The physical interface was up and the trunk existed, so my first assumption was that the VLAN configuration on one of the access ports was wrong. It was not.

The mistake was in the trunk's allowed VLAN list. I had permitted VLAN 10 but not VLAN 20 on one side. That is a good example of why 'the trunk is up' is not a complete operational statement. A trunk is a transport for multiple VLANs, and each VLAN can effectively have a different reachability result depending on the allowed list, local VLAN database and spanning-tree state.

`show interfaces trunk` was much more useful than repeatedly checking `show running-config`. I wanted to know which interfaces were actually trunking, which encapsulation was in use, what the native VLAN was, and which VLANs were allowed and forwarding. Configuration tells me what I asked the switch to do. Operational commands tell me what state the switch reached.

I also started checking whether the VLAN existed on both switches. An access port can reference a VLAN locally while the remote switch has no corresponding active VLAN. Depending on the platform and configuration, the trunk may still be functioning for other VLANs. That partial success makes the problem easy to misread as an endpoint issue. The same is true for spanning tree: a VLAN can be blocked on a particular path while another VLAN forwards.

The native VLAN was another source of subtle trouble. If the two ends disagree about which VLAN is native, untagged frames can be associated with different Layer 2 domains at each side. Some management traffic or protocols may still appear, so the link does not necessarily fail cleanly. I learned to treat a native VLAN mismatch as a configuration error even if basic traffic happened to pass.

My troubleshooting order became fairly mechanical: verify the endpoint access VLAN, verify the VLAN exists locally, verify the uplink is operationally a trunk, verify the VLAN is allowed, verify spanning-tree state for that VLAN, then inspect MAC learning on both switches. If the source MAC appears on the local access port but never appears across the trunk, the problem is already narrowed down considerably.

The useful part of this lab was not the command that fixed it. It was seeing that a shared physical link can be healthy while one logical network carried over it is broken. That idea appears everywhere later: tunnels, VRFs, VPNs, virtual switches and service-provider links all create cases where 'the interface is up' tells only a small part of the story.
