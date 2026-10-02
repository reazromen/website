---
title: APNs, PGW Selection and the Path to the Data Network
url: /posts/apns-pgw-selection-and-the-path-to-the-data-network.html
date: '2026-09-14'
read_time: 2
excerpt: An APN is more than a label on the handset; it influences how a subscriber
  session reaches a packet gateway and an external data network.
topic: mobile-networks
tags:
- apn
- pgw
- lte
- open5gs
- epc
draft: false
featured: false
language: en
eyebrow: 2022 Mobile Core and IMS · intermediate
outputs:
- url: /posts/apns-pgw-selection-and-the-path-to-the-data-network.html
  template: cms/templates/posts/posts--apns-pgw-selection-and-the-path-to-the-data-network.tpl
  source: cms/templates/posts/posts--apns-pgw-selection-and-the-path-to-the-data-network.json
---

I used to think of the APN as the mobile equivalent of a Wi-Fi network name. That analogy falls apart quickly. In the EPC, the APN is part of session selection and policy. It identifies the packet data network the subscriber wants to reach and influences which gateway and configuration should be used for the session.

In a small Open5GS lab I could make this visible by defining more than one APN and giving them different address pools or downstream routes. The UE requested an APN during session establishment, the core selected the corresponding packet data path, and the subscriber eventually received an IP address associated with that context. A wrong or unsupported APN could therefore produce a failure even though authentication had already succeeded.

That distinction helped separate subscriber identity from data-service authorization. The HSS may know who the subscriber is, but that does not automatically mean every APN or service is valid for that subscriber. The session still has to be created using configuration and policy that the core accepts.

The packet gateway side also reminded me that the mobile core ultimately has to interact with normal IP routing. After GTP-U is decapsulated, the subscriber packet still needs a route to whatever external network it is trying to reach, and the return path has to know how to reach the subscriber address pool. NAT may be used in some lab designs, but it is not a substitute for understanding the underlying routes.

One of my more useful tests was to give the subscriber a working attach and deliberately break only the route beyond the PGW. The UE still looked registered and the core still showed an active session, but data failed. A capture at the user-plane function showed the inner subscriber packet leaving the tunnel and then going nowhere useful. That made the boundary between mobile-core session state and ordinary IP forwarding very clear.

The APN therefore became another example of why service names should not be treated as cosmetic configuration. It participates in a real selection process that affects address allocation, policy and forwarding. When data service fails after a successful attach, checking the requested APN, the selected session parameters and the downstream route is a much better starting point than resetting the radio side.
