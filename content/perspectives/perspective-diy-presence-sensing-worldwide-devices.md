---
title: "DIY Presence Sensing in Context: PIR, mmWave, ESPHome and Commercial Devices"
url: /posts/diy-presence-sensing-worldwide-devices.html
date: '2026-10-17'
read_time: 6
excerpt: "A practical comparison of DIY ESP8266 experiments, PIR and mmWave sensing, ESPHome, Home Assistant and dedicated presence products—without confusing detection with reliability."
topic: radio-iot
tags:
  - presence
  - sensors
  - wifi
  - automation
  - embedded
  - hardware
draft: false
featured: true
language: en
eyebrow: IoT · ecosystem notes
---

# DIY Presence Sensing in Context: PIR, mmWave, ESPHome and Commercial Devices

Presence sensing is becoming a familiar part of home automation, but the category covers different technologies and very different expectations. A simple PIR sensor, a millimetre-wave radar module, a DIY ESP8266 node and a finished commercial presence sensor should not be treated as interchangeable devices.

My own experiment starts from a narrow use case: decide when a desk is probably empty long enough to request a computer sleep action. Looking at the wider ecosystem helps clarify which parts are worth building, which parts are better bought, and where reliability comes from.

## PIR and mmWave solve different sensing problems

A passive infrared (PIR) sensor detects changes in infrared energy, commonly associated with a moving warm body. It is inexpensive and useful for motion-triggered lighting, but a person sitting almost motionless may stop generating detectable changes. Placement, field of view and the environment all matter.

Millimetre-wave radar can detect small movements and is often used for room-presence sensing where a stationary person should remain detectable. It introduces its own tuning challenges: mounting position, reflections, sensitivity, interference from fans or moving objects, and the distinction between a human presence signal and other motion. Radar does not magically eliminate false positives.

The right choice depends on the behavior needed. For a hallway light, PIR may be enough. For a desk where someone can sit still for an hour, mmWave may be worth evaluating. In either case, a grace period and an explicit state machine are more useful than pretending the raw sensor output is perfect.

## The software ecosystem matters too

ESPHome lets supported microcontrollers expose sensors and controls to a broader home-automation setup, often alongside Home Assistant. This reduces the amount of firmware plumbing a DIY builder has to maintain. It can also make sensor values, configuration and automations easier to inspect.

A custom ESP8266 project gives more control over the exact logic and can stay deliberately small. The trade-off is that the builder owns updates, connectivity handling, diagnostics and integration. Home Assistant can provide a central view and automations, but if a particular automation requires Home Assistant to be online, that dependency should be understood and tested.

Dedicated devices such as Everything Presence One and products in Shelly's presence-sensing range represent another path: buy a more integrated unit rather than assemble every part yourself. Their exact sensors, firmware, connectivity and features differ by model and hardware revision, so current specifications should be checked before making a purchasing decision. A product name alone is not a reliability guarantee.

## Build versus buy is a question of ownership

DIY makes sense when the goal is to learn, experiment, customize the control loop or integrate with hardware that a commercial product does not support. A finished product is often preferable when installation time, polished configuration, enclosure quality, support and predictable updates matter more than control over every detail.

There is also a middle path: use a known sensor module, run ESPHome or a small custom firmware, and keep the policy layer independent from the dashboard. This preserves flexibility without requiring every layer to be invented from scratch.

## Reliability lives beyond detection accuracy

For my PC power-saving use case, a presence event is only the beginning. The system must decide how long to wait, cancel a pending sleep when occupancy returns, handle a missing listener, avoid repeating stale commands and expose the reason for its current state. A sensor can be accurate in a laboratory and still produce a frustrating automation if these transitions are poorly designed.

I would evaluate any solution using the same practical tests: Does it detect a stationary person? Does it recover after Wi-Fi loss? Can I see when the last valid event arrived? What happens if the controller restarts? Can I override the automation immediately? And can I measure whether the complete setup saves energy in real use?

## The useful comparison

PIR, mmWave, ESPHome, Home Assistant and commercial presence products occupy different layers of the problem. Some detect motion, some package hardware and firmware, and some coordinate automations. Comparing them fairly means separating those roles rather than ranking them as if they were identical products.

The best setup is the simplest one that meets the real requirement. For a learning project, that may be an ESP8266 and a sensor. For a busy home, an integrated product may save maintenance. For a critical action such as putting a work computer to sleep, both need conservative timing, visible state and a recovery path.
