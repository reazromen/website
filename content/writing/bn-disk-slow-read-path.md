---
title: When a Disk Looks Slow, Inspect the Whole Read Path
date: '2024-10-12'
draft: false
language: en
url: /posts/bn-disk-slow-read-path.html
topic: disaster-recovery
tags:
- storage
- debugging
featured: false
read_time: 2
excerpt: >-
  When opening a file is slow, the disk is an obvious suspect. But data may cross a
  filesystem, mount, network gateway, and application layer before reaching the user.
  The symptom does not prove that storage is where the delay began.
editorial_batch: 20261003-100-niches
---

When opening a file is slow, the disk is an obvious suspect. But data may cross a filesystem, mount, network gateway, and application layer before reaching the user. The symptom does not prove that storage is where the delay began.

Suppose reading the file directly is fast while the web interface is slow. Replacing the hard drive would be an early conclusion. If the direct read is also slow, then lower layers deserve closer inspection. Small tests that divide the path are useful.

A failing disk should not be stressed with unnecessary scans either. First establish which data matters, what errors already exist, and what work the device is currently doing. Health indicators are useful evidence, but they do not predict every failure perfectly.

When investigating slowness, I try to reduce the question: up to which boundary was the operation still fast, and what was added at the next boundary? That turns one large complaint into several measurable relationships.

Source: [official reference](https://www.kernel.org/doc/html/latest/accounting/psi.html).
