---
title: "Using a Logic Analyzer to Debug Firmware That Talks to Hardware"
draft: false
date: '2020-04-29'
language: en
url: /posts/logic-analyzer-for-firmware-bugs.html
read_time: 2
excerpt: >-
  A logic analyzer shows what actually appeared on the wires.
eyebrow: "Perspectives · Tools"
tags: ["Logic Analyzer","I2C","SPI"]
---

A logic analyzer shows what actually appeared on the wires. Capture the smallest failing transaction and verify probe points, ground, voltage compatibility, and sample rate. For I2C, inspect addresses, acknowledgements, clock stretching, and stop conditions. For SPI, verify chip select, clock polarity and phase, bit order, and transfer length.

Compare successful and failing captures. A decoded label is useful, but the raw waveform remains authoritative when decoder settings are wrong. Logic analyzers reveal digital sequence and timing; they do not replace an oscilloscope when voltage quality, ringing, or slow edges are suspect. Pair captures with firmware logs to connect a transaction to the software state that initiated it.
