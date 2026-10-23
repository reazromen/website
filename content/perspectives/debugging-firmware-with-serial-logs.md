---
title: "Debugging Firmware with Serial Logs Without Drowning in Output"
draft: false
date: '2021-08-11'
language: en
url: /posts/debugging-firmware-with-serial-logs.html
read_time: 2
excerpt: >-
  A log should answer a question, not narrate every line of code.
eyebrow: "Perspectives · Firmware"
tags: ["firmware","debugging"]
---

A log should answer a question, not narrate every line of code. Use consistent levels, subsystem labels, timestamps, and structured values that explain decisions. Never log credentials or private payloads.

Printing can change timing. In latency-sensitive paths, record compact events in a ring buffer and let a lower-priority task transmit them. Compare failing traces with known-good traces, narrow instrumentation to distinguish hypotheses, and remove temporary noise when the cause is understood. Logs are most useful when they expose system decisions while respecting the runtime budget.
