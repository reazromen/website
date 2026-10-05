---
title: PCF and Policy Control Made 5G Sessions Feel Less Static
url: /posts/pcf-and-policy-control-made-5g-sessions-feel-less-static.html
date: '2024-11-24'
read_time: 1
excerpt: Policy is not just a config file on the gateway; in 5GC it can actively influence
  session behavior through dedicated network functions.
topic: mobile-networks
tags:
- pcf
- smf
- policy
- 5g-core
draft: false
featured: false
language: en
eyebrow: 2023 Mobile and 5G Notes · advanced
outputs:
- url: /posts/pcf-and-policy-control-made-5g-sessions-feel-less-static.html
  template: cms/templates/posts/posts--pcf-and-policy-control-made-5g-sessions-feel-less-static.tpl
  source: cms/templates/posts/posts--pcf-and-policy-control-made-5g-sessions-feel-less-static.json
---

In small labs it is easy to make a PDU session look static: a subscriber asks for a DNN, the core creates the session, and packets flow. That hides the policy machinery that becomes important in real networks.

The PCF gave me a better model. Policy decisions can depend on subscriber context, service requirements and network conditions, while the SMF applies those decisions to session management. That means the eventual user-plane rules are not necessarily a fixed result of one configuration file.

This also connected the 5G architecture back to things I had seen in LTE with PCRF and Gx. The interfaces and network functions changed, but the underlying problem remained familiar: the network needs a control point that decides how a session should be treated, and another component has to enforce that decision.

For troubleshooting, I started asking whether a bad session was a forwarding problem or a policy outcome. If the SMF intentionally installed different rules because of policy, changing routes on the UPF would only mask the real issue. Following the decision chain was slower at first, but much more reliable.
