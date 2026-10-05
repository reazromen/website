---
title: N2 and N3 Helped Me Draw a 5G Call Path Without Hand-Waving
url: /posts/n2-and-n3-helped-me-draw-a-5g-call-path-without-hand-waving.html
date: '2021-10-09'
read_time: 2
excerpt: Separating N2 signalling from N3 user traffic made the gNB-to-core boundary
  much easier to troubleshoot.
topic: mobile-networks
tags:
- n2
- n3
- ngap
- gtp-u
draft: false
featured: false
language: en
eyebrow: 2023 Mobile and 5G Notes · advanced
outputs:
- url: /posts/n2-and-n3-helped-me-draw-a-5g-call-path-without-hand-waving.html
  template: cms/templates/posts/posts--n2-and-n3-helped-me-draw-a-5g-call-path-without-hand-waving.tpl
  source: cms/templates/posts/posts--n2-and-n3-helped-me-draw-a-5g-call-path-without-hand-waving.json
---

The 5G diagrams became much more useful once I stopped labeling the entire gNB-to-core connection as one link. N2 and N3 carry very different things. N2 connects the gNB to the AMF for control-plane signalling, while N3 carries user-plane traffic between the gNB and UPF.

That split gives a clean troubleshooting boundary. A UE can attach to the radio, exchange NGAP over N2, authenticate and register while still having no usable data path on N3. Conversely, a user-plane issue does not automatically mean the AMF registration procedure is broken.

When looking at captures, NGAP messages on N2 explain registration, mobility and session-related signalling. GTP-U on N3 carries the subscriber packets once the session is established. The tunnel endpoint identifiers and addresses in the control plane need to match the user-plane state that eventually appears on N3.

This sounds simple on paper, but it changed how I drew incidents. Instead of one arrow from gNB to core, I started drawing signalling and user traffic separately. That made failed PDU sessions, wrong tunnel addresses and firewall mistakes much easier to localize. The same habit had already helped with SIP versus RTP; 5G simply applies the separation on a larger scale.
