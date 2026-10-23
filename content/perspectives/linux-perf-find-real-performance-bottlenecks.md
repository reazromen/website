---
title: "Linux perf: Measure the Bottleneck Before Optimizing Code"
draft: false
date: '2023-10-18'
language: en
url: /posts/linux-perf-find-real-performance-bottlenecks.html
read_time: 2
excerpt: >-
  Profiling replaces guesses with evidence.
eyebrow: "Perspectives · Linux Performance"
tags: ["linux","performance","profiling"]
---

Profiling replaces guesses with evidence. Linux `perf` can sample CPU execution and report hot functions and call paths, subject to kernel configuration, permissions, and symbol availability. Define the symptom, measure a baseline under representative load, and preserve the exact binary and matching debug symbols.

CPU profiles do not explain every kind of slowness. A process waiting on disk, network, locks, or another service may use little CPU while latency remains high. Compare profiles with I/O statistics, process state, metrics, and request timing. Change one meaningful thing, repeat the measurement, and check whether the bottleneck moved.
