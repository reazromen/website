---
title: "GDB and OpenOCD: A Repeatable Workflow for Embedded Debugging"
draft: false
date: '2023-02-06'
language: en
url: /posts/gdb-openocd-embedded-debugging.html
read_time: 2
excerpt: >-
  With a supported probe and OpenOCD, GDB can halt a target, inspect registers and memory, and show where execution went wrong.
eyebrow: "Perspectives · Debugging"
tags: ["gdb","openocd","firmware"]
---

With a supported probe and OpenOCD, GDB can halt a target, inspect registers and memory, and show where execution went wrong. Build with debug symbols and preserve the exact ELF that matches the flashed image; mismatched symbols can make source lines misleading.

Capture the call stack first, then inspect relevant registers and documented fault-status registers. Treat a damaged backtrace as evidence, not certainty. Check in a launch configuration or runbook covering target, probe, reset behavior, and connection steps. Conditional breakpoints and watchpoints can reveal who changed a value, not merely where execution stopped.
