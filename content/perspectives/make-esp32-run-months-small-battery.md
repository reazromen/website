---
title: "How to Make an ESP32 Run for Months on a Small Battery"
draft: false
date: '2024-01-19'
language: en
url: /posts/make-esp32-run-months-small-battery.html
read_time: 10
excerpt: >-
  Long battery life is a system-level property. Deep sleep helps, but radio activity, sensors, regulators, wake-up schedules, and battery behavior determine whether an ESP32 device lasts days or months.
eyebrow: "Perspectives · Embedded Systems"
tags: ["esp32", "low-power", "iot", "battery", "embedded-systems"]
---

# How to Make an ESP32 Run for Months on a Small Battery

A battery-powered ESP32 can run for a long time, but selecting deep sleep in software does not guarantee months of operation. Battery life is determined by the average current of the entire product: microcontroller, regulator, sensors, display, LEDs, pull-ups, and any circuit that remains powered while the processor sleeps.

The correct workflow is to define the duty cycle, measure the board, and remove unnecessary energy costs one at a time.

## Start with an energy budget

Suppose a device spends most of its time asleep and wakes periodically to measure a sensor and send a short update. Its average current can be estimated from the current and duration of each operating state:

`I_{avg} = (I_{sleep}t_{sleep} + I_{active}t_{active})/(t_{sleep}+t_{active})`

If active work takes only a few seconds but occurs every several minutes, the sleep current becomes especially important. Conversely, a device that connects to Wi-Fi for a long time or retries a failed network operation may use much more energy than the original estimate.

Convert battery capacity into a rough runtime only after accounting for usable capacity, temperature, battery chemistry, regulator losses, self-discharge, and current peaks. A battery's printed capacity is not a guarantee that the full amount is available under every load.

## Measure the whole board

Many development boards consume more current than the bare chip because of USB-to-serial converters, power LEDs, voltage regulators, and other components. A low-power firmware setting cannot switch off components that remain connected to the battery.

Measure current in active and sleep states with an instrument appropriate for the expected range. Some meters have burden voltage or slow sampling that can obscure short radio peaks. A power analyzer or a well-designed shunt measurement may be needed for accurate results.

Test the complete product, not just a module on a bench. A sensor breakout board may contain a regulator or indicator LED that dominates sleep current.

## Design the wake-up cycle

Use deep sleep when the device can safely stop most CPU activity between jobs. Choose a wake-up source—timer, GPIO, or another supported mechanism—that matches the application. On wake, initialize only what is required, take the measurement, transmit or store the result, and return to sleep.

Avoid reconnecting to a network unnecessarily if the product architecture allows batching or a more efficient communication method. However, keeping a radio association alive can itself cost energy, so compare measured alternatives rather than assuming that persistent connectivity is always better.

Bound retries. A device that repeatedly attempts to join an unavailable Wi-Fi network can drain its battery rapidly. Use backoff, a maximum retry window, and a policy for returning to sleep when the network is absent.

## Power-gate peripherals where appropriate

Sensors, amplifiers, displays, and external modules may draw current even when not in use. If the device permits it, switch their supply with a suitable load switch or transistor. Check startup time, required power sequencing, and whether signal pins can back-power an unpowered device through protection diodes.

Select regulator quiescent current carefully. A regulator with excellent peak efficiency may still waste energy during long sleep periods if its no-load current is high. Also consider leakage through pull-up resistors, voltage dividers, level shifters, and charging circuitry.

## Radio and firmware decisions

Wi-Fi is convenient but can have significant current peaks and connection overhead. BLE, a low-power wide-area radio, or a wired interface may be more suitable depending on range, throughput, infrastructure, and latency. Choose the communication system at the product level.

Use the vendor's power-management features correctly, and confirm which clocks, peripherals, and memory domains remain active in each sleep mode. Avoid unnecessary logging and LED activity in production. Ensure wake-up code does not accidentally leave a timer, task, or peripheral running.

## Validate under real conditions

Measure a complete cycle: sleep, wake, sensor stabilization, computation, transmission, retry behavior, and return to sleep. Repeat with weak Wi-Fi, failed requests, cold starts, and low battery voltage. Estimate battery life from observed energy per cycle and the actual schedule.

For example, reducing active time by half may be less valuable than fixing a regulator that draws several milliamps continuously. The measurement tells you where the energy goes.

Months of operation are achievable only when the entire circuit and its behavior are designed around a power budget. Deep sleep is one tool in that design—not a substitute for measurement.
