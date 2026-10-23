---
title: "Why Embedded Projects Fail After the Prototype Works—and How to Build Reliable Firmware"
draft: false
date: '2023-11-08'
language: en
url: /posts/why-embedded-prototypes-fail-in-real-products.html
read_time: 10
excerpt: >-
  A successful bench demo proves that a path can work once. Reliable firmware must also survive bad power, missing devices, network outages, memory pressure, updates, and the unexpected states of real use.
eyebrow: "Perspectives · Embedded Systems"
tags: ["embedded-systems", "reliability", "firmware", "testing", "iot"]
---

# Why Embedded Projects Fail After the Prototype Works—and How to Build Reliable Firmware

A prototype can look finished when the main feature works on a desk. A sensor reports a number, a motor turns, or an audio call succeeds. Then the device is moved to another room, left running for a week, exposed to a weak power supply, or updated remotely—and it fails.

This gap is not surprising. A demonstration usually proves that one expected path can work. A product must handle the paths that are delayed, interrupted, malformed, unavailable, or repeated.

## Power is part of the software environment

Voltage dips, noisy loads, poor grounding, and marginal regulators can cause resets that appear to be firmware bugs. Wireless transmissions and motors can produce current peaks that a bench supply hides. Cable length and connector resistance can change the behavior in the final enclosure.

Measure the supply during worst-case activity. Record reset reasons where the MCU supports them, and distinguish watchdog resets from brownouts or deliberate software restarts. Make startup safe even if the previous operation ended abruptly.

## Every external dependency can fail

Sensors can be disconnected, buses can become stuck, network access can disappear, and remote services can time out. A driver that assumes every transaction succeeds may wait forever or use stale data.

Define timeouts and recovery policies. Decide whether to retry, reset a peripheral, mark data invalid, enter a safe mode, or ask for user intervention. Retries should be bounded and spaced appropriately; a tight retry loop can consume power and prevent recovery.

Treat external input as untrusted. Validate lengths, ranges, checksums, protocol states, and version fields before acting on received data.

## Memory and timing problems accumulate

A device that runs for a few minutes may not reveal a memory leak or fragmentation problem. A system tested with one task may fail when networking, audio, logging, and user input run together. Interrupt handlers that are harmless in isolation may cause latency under heavy event load.

Track minimum free heap, task stack high-water marks, queue occupancy, dropped packets, retry counts, and maximum operation duration. Instrumentation should be useful in production but should not consume so much CPU, memory, or flash endurance that it creates the problem it is meant to detect.

## Design for recovery, not only success

A watchdog can recover from a deadlock or stalled control path, but it must be configured thoughtfully. If the watchdog is fed unconditionally from a timer, a broken application can appear healthy forever. Prefer health checks tied to meaningful progress and define what the device should do after a restart.

For persistent configuration, use validation and a recovery default. If power fails during an update, the device should not be left with an unusable configuration. Firmware updates should include image validation, a recovery path, and—where supported—rollback if the new version cannot boot successfully.

## Test failure paths deliberately

A reliable test plan should include:

- Repeated cold starts and resets during activity.
- Power dips and low-battery behavior within safe test limits.
- Missing or unresponsive sensors and peripherals.
- Network loss, high latency, and malformed responses.
- Long-duration runs that expose leaks and drift.
- Full memory, queue, and buffer conditions.
- Interrupted firmware updates and recovery.
- Simultaneous operation of the system's major features.

Hardware-in-the-loop tests can automate some of these scenarios. Even a simple fixture that power-cycles a board, presses inputs, and captures serial logs can reveal failures that manual testing misses.

## Define observable behavior

When something goes wrong, a product should provide evidence. Record reset cause, firmware version, critical fault codes, and selected counters. Use bounded logs and avoid writing flash on every event. If the device is connected, send diagnostics carefully, respecting privacy and bandwidth constraints.

A failure should lead to a defined state. For example, a communication device might disable an unsafe output, show a clear fault indicator, and attempt a bounded reconnection. It should not silently continue with stale state if that could mislead the user or damage equipment.

## Reliability is an architectural property

Watchdogs, retries, tests, and logs are useful, but no single feature makes firmware reliable. Reliability comes from clear state machines, defined timeouts, explicit resource ownership, safe electrical design, validated updates, and tests that include failure.

A prototype answers, “Can it work?” Product engineering asks, “What happens when it does not?” That second question is where dependable embedded systems are built.
