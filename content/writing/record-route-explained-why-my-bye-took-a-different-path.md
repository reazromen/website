---
title: Record-Route Explained Why My BYE Took a Different Path
url: /posts/record-route-explained-why-my-bye-took-a-different-path.html
date: '2026-09-14'
read_time: 3
excerpt: Initial SIP routing and in-dialog routing are different problems. Record-Route
  was the mechanism that made the proxy stay on the path after the call was established.
topic: telecom-voip
tags:
- sip
- kamailio
- record-route
- dialog
draft: false
featured: false
language: en
eyebrow: 2021 SIP Infrastructure · intermediate
outputs:
- url: /posts/record-route-explained-why-my-bye-took-a-different-path.html
  template: cms/templates/posts/posts--record-route-explained-why-my-bye-took-a-different-path.tpl
  source: cms/templates/posts/posts--record-route-explained-why-my-bye-took-a-different-path.json
---

I had a call setup working through Kamailio and assumed the rest of the call would naturally pass through the same proxy. Then I found a BYE taking a different path. The INVITE had used my routing logic correctly, but the endpoints had enough information to address later requests without necessarily returning through the proxy. That was the point where Record-Route stopped looking like an obscure SIP header.

The initial INVITE establishes the route toward the called party. A proxy that wants to remain in the signaling path can insert itself into the route set using Record-Route. The endpoints then use that route set for later in-dialog requests. Those later requests normally contain Route headers derived from the Record-Route information learned during dialog establishment.

In Kamailio, the important idea was not the exact function call but when to apply it. I wanted the proxy on the path for the initial dialog-forming request, then I wanted sequential requests such as BYE, re-INVITE and UPDATE to follow loose routing based on the existing route set. Treating every in-dialog request like a brand-new call setup produced ugly routing logic and made loops easier to create.

A packet trace made the behavior obvious. The first INVITE passed through the proxy and accumulated the routing information. The 200 OK returned. The ACK and later BYE then carried routing information that kept Kamailio involved. When I removed Record-Route from the initial handling, the endpoints behaved differently because the established route set changed.

This also clarified the role of Contact. Contact identifies where a user agent wants to receive future requests for that dialog or registration context, while Record-Route is used by proxies to establish the signaling path. I had previously blurred those responsibilities because both fields contain SIP URIs and both influence later message delivery.

The practical troubleshooting method became: check the initial INVITE for Record-Route, check the final response for the route set seen by the other side, then inspect Route and Contact on the later request. If BYE bypasses the proxy, I no longer start by changing firewall rules. I first ask whether the dialog was built with the proxy in its route set.

That small distinction became important later with topology hiding, SBC behavior and multi-proxy designs. A SIP call is not just one request finding one destination. It creates routing information that affects the signaling path for the lifetime of the dialog.
