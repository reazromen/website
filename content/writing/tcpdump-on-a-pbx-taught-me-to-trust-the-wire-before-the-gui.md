---
title: tcpdump on a PBX Taught Me to Trust the Wire Before the GUI
url: /posts/tcpdump-on-a-pbx-taught-me-to-trust-the-wire-before-the-gui.html
date: '2020-10-06'
read_time: 2
excerpt: 'On a headless PBX, a narrow tcpdump capture often answered the important
  question faster than a full GUI trace: did the signaling or media packet actually
  reach the server?'
topic: linux-homelab
tags:
- tcpdump
- sip
- rtp
- linux
draft: false
featured: false
language: en
eyebrow: 2020 VoIP Foundations · intermediate
outputs:
- url: /posts/tcpdump-on-a-pbx-taught-me-to-trust-the-wire-before-the-gui.html
  template: cms/templates/posts/posts--tcpdump-on-a-pbx-taught-me-to-trust-the-wire-before-the-gui.tpl
  source: cms/templates/posts/posts--tcpdump-on-a-pbx-taught-me-to-trust-the-wire-before-the-gui.json
---

Running VoIP services on a Linux server made packet capture feel less optional. Desktop tools were useful for analysis, but the PBX itself was often the best capture point because that was where I needed to know whether a packet had actually arrived. `tcpdump` became the first check when an endpoint claimed it had sent something and the application log did not make the path obvious.

For SIP I could start with a narrow filter around the signaling port and the relevant host, write the packets to a pcap file, and open that file later in Wireshark if the conversation required deeper inspection. For RTP I used the media port range or the specific ports learned from SDP. Keeping the capture focused mattered because a busy server can produce enough unrelated traffic to hide the event I am trying to understand.

The location of the capture changes the meaning of the result. If the endpoint shows an outbound REGISTER but the PBX interface never sees it, the problem is somewhere between those two points. If tcpdump sees the packet but Asterisk does not log it, the question moves toward local firewall rules, socket binding or application configuration. If the application receives signaling but the RTP port remains silent, the investigation moves again. One capture cannot explain the entire network, but it can prove what crossed one interface.

I also learned not to confuse `any` with perfect visibility. Capturing on all interfaces is convenient, especially on a host with loopback, LAN and bridge interfaces, but it can show duplicate views of traffic or hide interface-specific details that matter. When the topology became confusing, I went back to a named interface and followed the packet one boundary at a time. That approach was slower than applying a broad filter everywhere, but the evidence was easier to interpret.

The useful habit was to treat logs and captures as complementary. Application logs explain what the process thought it was doing. A packet capture shows what crossed the observed network interface. When those stories disagree, the gap between them is usually where the problem lives. That became especially valuable with SIP and RTP because the signaling process, firewall, NAT state and media sockets can all be correct or broken independently.
