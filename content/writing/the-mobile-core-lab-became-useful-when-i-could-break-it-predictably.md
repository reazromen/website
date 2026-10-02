---
title: The Mobile Core Lab Became Useful When I Could Break It Predictably
url: /posts/the-mobile-core-lab-became-useful-when-i-could-break-it-predictably.html
date: '2026-09-14'
read_time: 1
excerpt: A working lab proves very little. A lab becomes valuable when failures can
  be introduced, observed and explained on demand.
topic: engineering-notes
tags:
- open5gs
- lab
- failure-testing
- mobile-core
draft: false
featured: false
language: en
eyebrow: 2023 Mobile and 5G Notes · all
outputs:
- url: /posts/the-mobile-core-lab-became-useful-when-i-could-break-it-predictably.html
  template: cms/templates/posts/posts--the-mobile-core-lab-became-useful-when-i-could-break-it-predictably.tpl
  source: cms/templates/posts/posts--the-mobile-core-lab-became-useful-when-i-could-break-it-predictably.json
---

A green dashboard is a satisfying end to a build, but it is not a strong test of understanding. The mobile-core lab became much more useful when I could deliberately create failures and predict what the trace should look like.

Removing subscriber data should fail in a different place from breaking the N3 path. A wrong DNN should not look like a radio failure. Stopping the UPF should affect user-plane establishment differently from stopping the AMF. Changing an IMS authentication parameter should not be diagnosed from GTP counters.

I started keeping a small failure matrix: what I changed, which protocol should show the first symptom, what the UE should report, and which component log should confirm it. When the observed result did not match the prediction, that was usually where the real learning happened.

This approach also made the lab less fragile. Instead of being afraid to change a working configuration, I had a known-good baseline and a repeatable way back. The goal was no longer to keep everything green. It was to understand the path well enough that red states were useful information.
