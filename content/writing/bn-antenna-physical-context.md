---
title: The Antenna Does Not End at the Edge of the Board
date: '2023-06-25'
draft: false
language: en
url: /posts/bn-antenna-physical-context.html
topic: pcb-bringup-hardware
tags:
- radio
- hardware
featured: false
read_time: 2
excerpt: >-
  A board antenna gives clues about expected behavior, but in a real product the surrounding
  objects become part of the system. The enclosure, cables, metal parts, and device placement
  can all change the result. An open-board test is not a guarantee for the finished enclosure.
editorial_batch: 20261003-100-niches
---

A board antenna gives clues about expected behavior, but in a real product the surrounding objects become part of the system. The enclosure, cables, metal parts, and device placement can all change the result. An open-board test is not a guarantee for the finished enclosure.

Suppose a device works well on a desk, but the result changes when someone holds it or places it near a wall. Firmware is not the only suspect. The physical context of real use has to be part of the test.

It helps to change one variable at a time. If the board revision, enclosure, and placement all change together, it becomes difficult to identify what actually changed the result. Multiple measurements under the same method and in the same location are more useful.

This is one of the things I like about hardware: the lines on a schematic do not end when they meet the physical world. The environment in which the product lives becomes part of the effective circuit story. Radio testing therefore continues long after the software has been flashed.

Source: [official reference](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/index.html).
