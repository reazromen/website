---
title: Swap Provides Space, but Time Is the Price
date: '2025-11-02'
draft: false
language: en
url: /posts/bn-swap-time-tradeoff.html
topic: linux-homelab
tags:
- linux
- storage
featured: false
read_time: 2
excerpt: >-
  Swap is sometimes treated as a direct replacement for RAM, but memory moved to storage
  has to be read back when active work needs it again. Swap creates room while introducing
  a time cost.
editorial_batch: 20261003-100-niches
---

Swap is sometimes treated as a direct replacement for RAM, but memory moved to storage has to be read back when active work needs it again. Swap creates room while introducing a time cost. Its existence does not remove physical memory limits.

Moving rarely used pages out can create useful RAM for other workloads. But if active work repeatedly needs those pages again, the machine spends more time moving data between memory and storage. The system may technically remain alive while becoming painful to use.

When testing, look at movement as well as occupancy. How much data is sitting in swap, and how much is actively being swapped in and out? Storage performance, workload behavior, and acceptable response time all affect the answer.

I see swap as a tradeoff. It can keep a machine functional under some forms of pressure, but it does not erase limited RAM for free. A good capacity plan accounts for both space and time.

Source: [official reference](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html).
