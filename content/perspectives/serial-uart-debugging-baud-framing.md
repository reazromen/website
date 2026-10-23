---
title: "UART Debugging: Baud Rate, Framing Errors, and Electrical Reality"
draft: false
date: '2018-07-29'
language: en
url: /posts/serial-uart-debugging-baud-framing.html
read_time: 2
excerpt: >-
  Garbled UART output can come from mismatched baud rates, data bits, parity, stop bits, swapped wires, or incompatible voltage levels.
eyebrow: "Perspectives · Hardware Interfaces"
tags: ["UART","Serial"]
---

Garbled UART output can come from mismatched baud rates, data bits, parity, stop bits, swapped wires, or incompatible voltage levels. Cross TX and RX, connect grounds, and verify the board’s electrical specification. RS-232 voltage levels are not directly compatible with 3.3 V or 5 V TTL UART pins.

If configuration looks correct, inspect the waveform with a logic analyzer or oscilloscope. Confirm bit duration, idle polarity, start bits, and stop bits. Failures under load may indicate interrupt latency or insufficient buffering. Begin with a known test pattern, then add framing, checksums, sequence numbers, and error counters where reliability requires them.
