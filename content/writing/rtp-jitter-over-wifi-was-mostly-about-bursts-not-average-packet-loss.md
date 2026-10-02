---
title: RTP Jitter over Wi-Fi Was Mostly About Bursts, Not Average Packet Loss
url: /posts/rtp-jitter-over-wifi-was-mostly-about-bursts-not-average-packet-loss.html
date: '2026-09-14'
read_time: 1
excerpt: A low average loss rate can still sound terrible when packets arrive in short
  bursts separated by long gaps.
topic: telecom-voip
tags:
- rtp
- wi-fi
- jitter
- audio
draft: false
featured: false
language: en
eyebrow: 2025 Voice and Infrastructure Notes · advanced
outputs:
- url: /posts/rtp-jitter-over-wifi-was-mostly-about-bursts-not-average-packet-loss.html
  template: cms/templates/posts/posts--rtp-jitter-over-wifi-was-mostly-about-bursts-not-average-packet-loss.tpl
  source: cms/templates/posts/posts--rtp-jitter-over-wifi-was-mostly-about-bursts-not-average-packet-loss.json
---

I had calls with very low packet loss that still sounded broken. The missing metric was burst structure, because the speaker only cares whether the next frame arrives before its playout deadline, not whether the average loss counter looks respectable.

RTP audio is consumed on a fixed playout schedule. Ten packets arriving close together after a 150 ms gap do not help the speaker during the gap. Average loss and average throughput hide that timing problem.

I started measuring inter-arrival time and grouping late packets into bursts. That immediately made buffer behavior easier to explain. A small jitter buffer handles normal variation and fails on long gaps; a huge buffer hides more gaps but adds conversational delay.

The useful number was not simply 'loss percent'. It was how often the network produced gaps longer than the playout margin. That measure connected packet traces directly to what I heard.
