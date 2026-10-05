---
title: Wi-Fi CSI Looked Like a Sensor Hidden Inside the Radio
url: /posts/wifi-csi-looked-like-a-sensor-hidden-inside-the-radio.html
date: '2026-07-04'
read_time: 1
excerpt: Channel State Information exposes how multipath changes, which turns ordinary
  Wi-Fi links into crude environmental sensors.
topic: radio-iot
tags:
- wi-fi-csi
- rf
- sensing
- esp32
draft: false
featured: false
language: en
eyebrow: 2025 Voice and Infrastructure Notes · advanced
outputs:
- url: /posts/wifi-csi-looked-like-a-sensor-hidden-inside-the-radio.html
  template: cms/templates/posts/posts--wifi-csi-looked-like-a-sensor-hidden-inside-the-radio.tpl
  source: cms/templates/posts/posts--wifi-csi-looked-like-a-sensor-hidden-inside-the-radio.json
---

RSSI gives one rough number for received power. CSI is more interesting because it describes the channel across subcarriers and, depending on the hardware, multiple spatial paths.

Movement changes multipath. A person walking through a room changes reflections and phase relationships even when the transmitter and receiver stay fixed. That means the radio link contains information about the environment in addition to carrying data.

The difficult part is separating useful motion from normal channel noise. Raw CSI needs calibration, filtering and a stable collection setup before a classifier means anything. Different rooms, antenna positions and devices can shift the baseline dramatically.

I treated the first experiments as signal-processing work rather than an AI problem. Plot amplitude and phase, look for repeatable structure, understand the sampling path, then decide whether a model is justified. The radio already gives a lot of information before machine learning enters the picture.
