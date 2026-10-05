---
title: The Voice Product Stack Was Finally One System, Not Three Projects
url: /posts/the-voice-product-stack-was-finally-one-system-not-three-projects.html
date: '2023-02-14'
read_time: 1
excerpt: Firmware, backend and telephony stopped being separate workstreams once their
  failure states and deployment policies were designed together.
topic: engineering-notes
tags:
- architecture
- firmware
- voip
- operations
draft: false
featured: false
language: en
eyebrow: 2025 Voice and Infrastructure Notes · all
outputs:
- url: /posts/the-voice-product-stack-was-finally-one-system-not-three-projects.html
  template: cms/templates/posts/posts--the-voice-product-stack-was-finally-one-system-not-three-projects.tpl
  source: cms/templates/posts/posts--the-voice-product-stack-was-finally-one-system-not-three-projects.json
---

For a long time I could think about firmware, backend and PBX independently. That stopped working once releases and incidents crossed all three.

A device registration problem might be bad Wi-Fi, stale backend credentials or a PBX account issue. A call-quality problem might be RTP timing in firmware, a media relay path, or server load. OTA can change behavior that the backend and monitoring need to understand immediately.

The architecture became more useful when every subsystem exposed state in a form the others could consume. Device identity remained in the backend. SIP credentials were provisioned rather than hard-coded. Firmware reported version and health. The telephony layer exposed registration and call metrics. Release management connected them.

At that point the product was no longer an embedded device plus some servers. It was a distributed voice system with a physical endpoint, which is a much better description of the engineering problem.
