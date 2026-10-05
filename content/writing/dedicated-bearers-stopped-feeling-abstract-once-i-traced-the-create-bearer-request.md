---
title: Dedicated Bearers Stopped Feeling Abstract Once I Traced the Create Bearer
  Request
url: /posts/dedicated-bearers-stopped-feeling-abstract-once-i-traced-the-create-bearer-request.html
date: '2021-09-09'
read_time: 1
excerpt: Tracing a Create Bearer Request tied policy, QoS and user-plane classification
  together in one procedure.
topic: mobile-networks
tags:
- lte
- gtpv2-c
- bearer
- qos
draft: false
featured: false
language: en
eyebrow: 2024 Telecom and Embedded Notes · advanced
outputs:
- url: /posts/dedicated-bearers-stopped-feeling-abstract-once-i-traced-the-create-bearer-request.html
  template: cms/templates/posts/posts--dedicated-bearers-stopped-feeling-abstract-once-i-traced-the-create-bearer-request.tpl
  source: cms/templates/posts/posts--dedicated-bearers-stopped-feeling-abstract-once-i-traced-the-create-bearer-request.json
---

Dedicated bearers are one of those LTE concepts that sound simple in a diagram and become clearer only in a trace. The default bearer gives the UE baseline connectivity. A dedicated bearer adds different QoS treatment for selected traffic while remaining associated with the same PDN connection.

The Create Bearer Request is where several earlier topics meet. The control plane identifies the linked bearer, supplies QoS information and includes the TFT that tells the UE which packets belong on the new bearer. That means the message is not merely “create another tunnel”; it carries the classification needed to make the bearer useful.

When debugging I learned to compare three things: the policy decision that requested special treatment, the GTPv2-C bearer procedure, and the actual user traffic. If the bearer exists but no packets match, the problem is probably not bearer establishment. If the procedure never starts, the issue is earlier in policy or session control.

Following the full chain removed a lot of guesswork. It also made later 5G QoS discussions easier because the names changed but the underlying problem remained: identify a flow, assign treatment, and make sure the forwarding plane enforces it.
