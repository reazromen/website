---
title: "Using strace to Understand What a Linux Program Is Really Doing"
draft: false
date: '2022-12-14'
language: en
url: /posts/linux-strace-debugging-system-calls.html
read_time: 2
excerpt: >-
  When an application reports a vague error, system calls can expose the concrete reason.
eyebrow: "Perspectives · Linux Tools"
tags: ["Linux","strace"]
---

When an application reports a vague error, system calls can expose the concrete reason. `strace` records file opens, reads, writes, network operations, and process creation. Look for repeated `ENOENT` errors, permission failures, unexpected paths, or a process blocked on a read that never completes.

Trace a focused command or attach to an authorized process, filtering calls when output is too large. A trace changes timing and may contain sensitive filenames or request details, so limit scope and retention. Combine it with service logs and process status: a trace shows what the program asks the kernel to do, while application evidence helps explain why.
