---
title: "An ESP8266 Presence Sensor for Smarter PC Power Saving"
url: /posts/esp8266-presence-aware-pc-power-saving.html
date: '2026-10-17'
read_time: 5
excerpt: "A small presence-aware automation experiment explores when a computer should sleep, why timers need care, and how to measure energy savings instead of guessing."
topic: radio-iot
tags:
  - embedded
  - firmware
  - sensors
  - energy
  - automation
draft: false
featured: true
language: en
eyebrow: IoT · field notes
---

# An ESP8266 Presence Sensor for Smarter PC Power Saving

A computer can spend hours powered on while nobody is using it. The obvious response is a schedule: sleep at a fixed time, or shut down after a period of inactivity. But schedules do not know whether someone has stepped away for two minutes or finished work for the day.

I have been experimenting with a small ESP8266-based presence sensor to make that decision more context-aware. The idea is straightforward: observe whether the desk is occupied, wait through a configurable absence interval, and then ask the computer to enter a lower-power state. The useful engineering work is not just detecting a person. It is deciding what the detection should mean.

## Presence is a signal, not a command

A sensor can report movement or presence, but it cannot automatically know the user's intention. Someone may sit still while reading, move out of the sensor's field of view, or leave a desk briefly to collect something. If every missed detection immediately triggers sleep, the automation becomes annoying and people will disable it.

The safer pattern is to treat presence as one input to a state machine:

1. **Occupied:** keep the computer in its normal state.
2. **Recently vacant:** start an absence timer rather than acting immediately.
3. **Vacant for long enough:** request sleep only if the computer is eligible.
4. **Presence returns:** cancel the pending action and, where supported, wake the computer through a deliberate mechanism such as Wake-on-LAN.

A grace period, hysteresis and a clear manual override are not optional polish. They are what make a sensor-driven system usable.

## Keep the hardware's job small

The ESP8266 is well suited to lightweight Wi-Fi sensing and control. It does not need to run a large application stack. It can read a sensor, maintain a small amount of state, expose health information and communicate an event to another component.

The PC-side listener can translate a trusted event into an operating-system action. If the sensor and listener communicate over a network, the design should authenticate commands where practical, reject malformed requests and avoid exposing a power-control endpoint to the public internet. A sensor reporting “vacant” should not be enough to let an arbitrary device shut down a machine.

A dashboard is useful for tuning the absence delay, seeing the last sensor event and understanding why a sleep request did or did not happen. But the dashboard should not become the only place where the automation's essential logic exists.

## How much energy does it actually save?

It is tempting to describe this project as an energy-saving success before measuring it. That would be premature. The result depends on the computer's idle draw, monitor and peripheral power, sleep-state consumption, how often the room is empty, and whether the automation causes unwanted wake-ups.

A credible evaluation needs a baseline and a controlled comparison. Measure watt-hours over comparable workdays with automation disabled and enabled. Record false sleep events, missed presence events, wake-up failures and the time spent in each power state. Keep the workload and measurement window as similar as possible.

Without those measurements, I can describe the design and its intended benefit, but I should not claim a percentage reduction.

## The lesson so far

The most interesting part of this experiment is the boundary between sensing and action. A cheap microcontroller can provide useful context, but reliability comes from the surrounding rules: a grace period, a recoverable state machine, local fallback behavior and evidence about what actually happened.

The goal is not to automate power management at any cost. It is to make the low-power choice when the system has enough evidence, and to fail in a way that does not interrupt the person using it.
