---
title: "Linux Core Dumps and GDB: Reconstruct a Crash After It Happens"
draft: false
date: '2018-12-07'
language: en
url: /posts/gdb-core-dumps-linux-crash-analysis.html
read_time: 2
excerpt: >-
  A core dump preserves a process snapshot for post-mortem analysis when a crash cannot be reproduced under a debugger.
eyebrow: "Perspectives · Debugging"
tags: ["linux","gdb","crash-analysis"]
---

A core dump preserves a process snapshot for post-mortem analysis when a crash cannot be reproduced under a debugger. On systemd systems, `coredumpctl` can help locate dumps; limits, service settings, containers, and core-pattern configuration affect collection. Keep the exact executable and debug symbols alongside release metadata.

Open the dump in GDB and inspect every thread’s backtrace, arguments, and relevant memory. A crash near a null pointer may be the final symptom of earlier corruption. Core files can contain secrets and private data, so restrict access and retention. Capture binary version, platform, configuration, and preceding events to connect the dump to a reproducible investigation.
