---
title: 'Trunk Ports: The Part of VLANs I Initially Misunderstood'
url: /posts/trunk-ports-the-part-of-vlans-i-initially-misunderstood.html
date: '2026-09-14'
read_time: 3
excerpt: A trunk does not merge VLANs. It preserves multiple Layer 2 domains across
  one physical link by carrying VLAN identity with the frame.
topic: networking
tags:
- ccna
- vlan
- 802-1q
- trunking
draft: false
featured: false
language: en
eyebrow: 2018 Network Foundations · beginner
outputs:
- url: /posts/trunk-ports-the-part-of-vlans-i-initially-misunderstood.html
  template: cms/templates/posts/posts--trunk-ports-the-part-of-vlans-i-initially-misunderstood.tpl
  source: cms/templates/posts/posts--trunk-ports-the-part-of-vlans-i-initially-misunderstood.json
---

After access ports made sense, trunk ports were the next place where my mental model broke. I understood that VLAN 10 and VLAN 20 were separate Layer 2 domains, but I was not clear on how one cable between two switches could carry both without mixing them together. The answer is that the link carries extra VLAN information with the Ethernet traffic so each switch can preserve the original forwarding domain.

With IEEE 802.1Q, a switch can insert a VLAN tag into an Ethernet frame before sending it across a trunk. The receiving switch reads that tag and associates the frame with the correct VLAN. A VLAN 10 broadcast arriving over the trunk is still a VLAN 10 broadcast; it is not flooded into VLAN 20 merely because both VLANs share the same physical cable. The trunk is multiplexing Layer 2 domains over one link, not collapsing them.

That distinction helped me understand why an access port and a trunk port behave differently. An ordinary endpoint connected to an access port usually sends and receives untagged Ethernet frames. The switch maps those frames into the access VLAN internally. A trunk is intended to connect devices that understand the VLAN context, such as another switch, a router-on-a-stick interface, a virtualization host, or an access point carrying multiple SSIDs.

The native VLAN made the picture slightly more complicated because 802.1Q trunks can carry one VLAN untagged, depending on the configuration. That means both sides of a trunk need to agree on the native VLAN. A mismatch does not always produce a clean, obvious failure. Some traffic may work while untagged traffic lands in different VLANs on opposite ends. That kind of partial behavior is more dangerous than a link that is simply down.

A useful Packet Tracer lab used two switches. Each switch had one PC in VLAN 10 and another PC in VLAN 20. The inter-switch link was configured as a trunk. The two VLAN 10 hosts could communicate across the trunk, and the two VLAN 20 hosts could do the same, but traffic still did not cross between VLANs without routing. That single topology demonstrated the purpose of the tag more clearly than memorizing trunk commands.

The `show interfaces trunk` and `show vlan brief` style of verification also taught me to separate configuration intent from operational state. A port may be configured as expected, but I still want to know which VLANs are active, which VLANs are allowed on the trunk, and whether the interface is actually trunking. When a VLAN works on one switch but disappears across an uplink, the allowed-VLAN list and trunk state are obvious places to look.

The broader lesson was that a physical link does not define a single logical network. Tags, tunnels and encapsulation let one physical path carry many logical contexts. 802.1Q was my first practical example of that idea, and the same pattern appears much later in overlays, VPNs, virtual switching and service-provider networks.
