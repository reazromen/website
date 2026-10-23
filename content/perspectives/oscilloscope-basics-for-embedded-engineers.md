---
title: "What an Oscilloscope Reveals That Firmware Logs Cannot"
draft: false
date: '2019-09-22'
language: en
url: /posts/oscilloscope-basics-for-embedded-engineers.html
read_time: 2
excerpt: >-
  A firmware log may report a peripheral timeout but cannot show a microsecond supply dip.
eyebrow: "Perspectives · Tools"
tags: ["Oscilloscope","Electronics"]
---

A firmware log may report a peripheral timeout but cannot show a microsecond supply dip. An oscilloscope reveals voltage over time. Trigger on a rail drop during resets, or inspect a signal at the receiving pin during communication failures. Check rise times, overshoot, ringing, and logic thresholds against component specifications.

Probe technique matters: long ground leads can introduce misleading ringing. Use appropriate attenuation and bandwidth, and avoid loading sensitive nodes. Correlate captures with software events, perhaps by toggling a GPIO before a risky operation. The purpose is to test a hypothesis—such as motor startup causing brownout—not merely collect waveforms.
