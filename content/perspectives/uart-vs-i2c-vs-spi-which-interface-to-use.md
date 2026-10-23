---
title: "UART vs I²C vs SPI: The Difference That Actually Matters in Real Projects"
draft: false
date: '2023-02-11'
language: en
url: /posts/uart-vs-i2c-vs-spi-which-interface-to-use.html
read_time: 8
excerpt: >-
  UART, I²C, and SPI solve different communication problems. Their wiring diagrams are only the beginning; topology, timing, addressing, electrical limits, and error handling determine which one fits a design.
eyebrow: "Perspectives · Embedded Systems"
tags: ["uart", "i2c", "spi", "embedded-systems", "electronics"]
---

# UART vs I²C vs SPI: The Difference That Actually Matters in Real Projects

A microcontroller rarely works alone. It exchanges bytes with sensors, displays, audio codecs, radios, storage chips, debug consoles, and other controllers. UART, I²C, and SPI are three common interfaces, but they have different assumptions about how devices connect and how data moves.

Choosing one because it has fewer wires can create problems later. Start with the device datasheets and the shape of the system.

## UART: a simple serial link

UART usually sends data over transmit and receive signals, with a shared ground. The endpoints agree on parameters such as baud rate, data bits, parity, and stop bits. The line idles at a defined logic level, and each character is framed with start and stop bits.

A typical UART link is point-to-point. It is useful for console logs, GPS receivers, modems, bootloaders, and communication with another controller. It does not require a shared clock line, which makes wiring straightforward.

But UART is not itself a complete multi-device network protocol. It does not inherently provide device addressing, packet boundaries, authentication, or robust error recovery. Those functions must be added by a higher-level protocol when needed. Also distinguish logic-level UART from RS-232 and RS-485 electrical standards; their voltage levels and physical-layer characteristics are not interchangeable.

## I²C: a shared two-wire bus

I²C uses a serial data line (SDA) and a serial clock line (SCL). Devices share the bus, and transfers include addressing and acknowledgment. The lines are typically open-drain or open-collector and require pull-up resistors.

This makes I²C useful when several low-to-moderate-speed peripherals need to share two signal wires: temperature sensors, real-time clocks, small displays, GPIO expanders, and configuration devices are common examples. Multiple devices can coexist if their addresses and electrical characteristics are compatible.

The pull-ups matter. Values that are too weak can make edges too slow; values that are too strong increase current and may violate device limits. Bus capacitance, wire length, voltage, and the selected speed all affect reliability. Address collisions, clock stretching, stuck-low lines, and mixed-voltage devices can also complicate a design.

## SPI: separate data paths and a clock

SPI commonly uses a clock, controller-to-peripheral data, peripheral-to-controller data, and a chip-select signal for each peripheral. It often supports higher throughput than basic I²C arrangements and can be straightforward for streaming data.

Displays, flash memory, ADCs, DACs, and radio modules frequently use SPI. Full-duplex transfers are possible because transmit and receive data can travel on separate lines at the same time, though the device protocol determines how those transfers are used.

SPI has no single universal specification covering every detail. Clock polarity, clock phase, bit order, maximum frequency, chip-select timing, and command format depend on the peripheral. More devices may require more chip-select wiring, and long or poorly routed wires can create signal-integrity problems.

## The practical trade-off

| Requirement | Often a good fit |
|---|---|
| Debug console or simple peer-to-peer serial | UART |
| Several low-speed sensors on shared wiring | I²C |
| Higher-throughput peripheral with precise timing | SPI |
| Long-distance multidrop industrial link | Consider RS-485 with a suitable protocol |
| Robust network between many nodes | Consider CAN or another purpose-built bus |

These are starting points, not absolute rules. A particular device may only offer one interface, or the board layout may make another choice more sensible.

## Common mistakes

First, check voltage compatibility. A 5 V peripheral may not tolerate a 3.3 V controller's assumptions, and a 3.3 V output may not meet a 5 V input's logic-high requirement. Never assume that a breakout board includes level shifting.

Second, inspect pin multiplexing and peripheral assignment. A microcontroller may support multiple serial peripherals, but pins can conflict with boot functions, flash, USB, or other hardware.

Third, do not confuse a working bench test with a robust link. Validate the bus under the intended cable length, electrical noise, clock speed, and device count. Add timeouts and recovery behavior where the protocol and application require them.

## Choose at the system level

UART is simple for a link between two endpoints. I²C is efficient for a collection of compatible peripherals sharing a short bus. SPI is attractive when a peripheral needs faster transfers and the design can accommodate its wiring.

The decisive questions are not merely “How many wires?” and “Which is fastest?” Ask how much data must move, how far it travels, how many devices share the connection, what the chip supports, and how failures will be detected and recovered. That is how a serial-interface choice becomes an engineering decision rather than a habit.
