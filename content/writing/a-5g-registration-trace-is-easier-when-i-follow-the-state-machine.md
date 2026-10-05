---
title: A 5G Registration Trace Is Easier When I Follow the State Machine
url: /posts/a-5g-registration-trace-is-easier-when-i-follow-the-state-machine.html
date: '2023-01-27'
read_time: 1
excerpt: Following registration as a state transition is more useful than memorizing
  a long list of NAS messages.
topic: mobile-networks
tags:
- 5g
- nas
- amf
- registration
draft: false
featured: false
language: en
eyebrow: 2023 Mobile and 5G Notes · advanced
outputs:
- url: /posts/a-5g-registration-trace-is-easier-when-i-follow-the-state-machine.html
  template: cms/templates/posts/posts--a-5g-registration-trace-is-easier-when-i-follow-the-state-machine.tpl
  source: cms/templates/posts/posts--a-5g-registration-trace-is-easier-when-i-follow-the-state-machine.json
---

A 5G registration trace can look like a dense list of NAS messages if I read it line by line without a model. The better approach is to ask what state the UE and core are trying to establish at each point.

The UE starts by identifying itself and requesting registration. The AMF may need identity clarification, authentication, security-mode setup and subscriber context before it can accept the registration. Each message exists because some piece of state is missing, untrusted or needs confirmation.

Authentication and security are especially important boundaries. If authentication fails, there is little value debugging PDU session establishment. If security mode never completes, later messages may be absent by design. Registration Accept only appears after enough context has been established for the network to consider the UE registered.

This state-machine view made packet captures much faster to read. I mark the last successful state, then inspect the next expected transition. Instead of asking “which message is missing?” in isolation, I ask “what condition would allow the next state?” That same method works surprisingly well across SIP registration, IMS AKA and mobile-core procedures.
