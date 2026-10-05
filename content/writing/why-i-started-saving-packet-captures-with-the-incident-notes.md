---
title: Why I Started Saving Packet Captures with the Incident Notes
url: /posts/why-i-started-saving-packet-captures-with-the-incident-notes.html
date: '2026-02-23'
read_time: 1
excerpt: A short pcap plus context is often more useful six months later than a page
  of remembered conclusions.
topic: engineering-notes
tags:
- pcap
- wireshark
- documentation
- troubleshooting
draft: false
featured: false
language: en
eyebrow: 2023 Mobile and 5G Notes · all
outputs:
- url: /posts/why-i-started-saving-packet-captures-with-the-incident-notes.html
  template: cms/templates/posts/posts--why-i-started-saving-packet-captures-with-the-incident-notes.tpl
  source: cms/templates/posts/posts--why-i-started-saving-packet-captures-with-the-incident-notes.json
---

I used to write down the conclusion of a lab and discard most of the raw evidence. That was fine until I came back months later and could not remember why I had decided a particular component was at fault.

Packet captures fixed part of that problem. A small pcap around the failure preserves message order, addresses, transaction identifiers and timing. The capture still needs context, so I save a short note with the topology, software versions, expected result and the exact point where behavior changed.

This became especially useful once labs involved SIP, Diameter, GTP and PFCP at the same time. A screenshot of one error line loses the relationship between protocols. A timestamped capture lets me correlate events across interfaces and verify whether my old explanation was actually correct.

I do not keep everything forever. The useful artifact is a minimal reproducer: enough traffic to show the problem, plus the config and notes required to understand the environment. That habit made later debugging faster and also made technical writing more precise because I could return to evidence instead of relying on memory.
