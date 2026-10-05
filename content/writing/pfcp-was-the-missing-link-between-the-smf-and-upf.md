---
title: PFCP Was the Missing Link Between the SMF and UPF
url: /posts/pfcp-was-the-missing-link-between-the-smf-and-upf.html
date: '2022-12-11'
read_time: 2
excerpt: 5G user-plane programming became clearer once I followed PFCP instead of
  treating the UPF as a static router.
topic: mobile-networks
tags:
- pfcp
- smf
- upf
- 5g-core
draft: false
featured: false
language: en
eyebrow: 2023 Mobile and 5G Notes · advanced
outputs:
- url: /posts/pfcp-was-the-missing-link-between-the-smf-and-upf.html
  template: cms/templates/posts/posts--pfcp-was-the-missing-link-between-the-smf-and-upf.tpl
  source: cms/templates/posts/posts--pfcp-was-the-missing-link-between-the-smf-and-upf.json
---

The UPF made more sense when I stopped thinking of it as a router with some mobile-networking features bolted on. In a 5G Core, the control plane needs a way to tell the user plane what to do with each subscriber session. PFCP is the protocol that carries much of that instruction between the SMF and UPF.

The useful objects are not ordinary routes. Packet Detection Rules identify traffic, Forwarding Action Rules say where or how to forward it, and related rules can handle QoS, buffering and usage reporting. That model explains why a UE can register successfully while data still fails: the subscriber may exist in the control plane but the UPF may not have the correct session state.

In a lab I found it more productive to inspect PFCP session establishment and modification messages than to stare at the Linux routing table first. If the SMF never installs the expected rules, the UPF cannot invent them. If the rules exist, then ordinary forwarding, tunnel state and host networking become the next suspects.

PFCP also exposed the value of separating control-plane intent from forwarding-plane state. The SMF owns session logic; the UPF executes it. That division shows up repeatedly in telecom systems and later made policy, charging and multi-UPF designs easier to understand.
