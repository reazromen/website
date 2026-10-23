---
title: "Watchdog Timers: Detect Hangs Without Hiding the Root Cause"
draft: false
date: '2020-10-31'
language: en
url: /posts/watchdog-timers-and-deadlock-diagnosis.html
read_time: 2
excerpt: >-
  A watchdog can recover a device from a stalled task, but a badly designed one can hide evidence.
eyebrow: "Perspectives · Firmware Reliability"
tags: ["firmware","watchdogs","deadlocks"]
---

A watchdog can recover a device from a stalled task, but a badly designed one can hide evidence. Feed it only when meaningful progress occurs; if any active task can feed a shared watchdog regardless of system health, a critical subsystem may remain stuck indefinitely.

Before reset, preserve a compact failure record when safe: reset reason, task or state identifier, last-progress timestamp, queue depth, and fault registers. Avoid blocking logging in a critical path. Test controlled hangs, starvation, and deadlocks, then verify recovery time and diagnostic value. Watchdogs complement timeouts, bounded queues, and health checks; they do not replace them.
