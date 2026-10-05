---
title: Calibration Is Not a Number; It Is a Contract With an Environment
date: '2025-07-01'
draft: false
language: en
url: /posts/bn-calibration-environment-contract.html
topic: radio-iot
tags:
- sensing
- calibration
featured: false
read_time: 2
excerpt: >-
  Setting a calibration value does not guarantee that every future measurement will remain
  correct. The environment, reference, and operating range in which that value was created
  are part of its meaning. Calibration is a rule for interpreting a measurement.
editorial_batch: 20261003-100-niches
---

Setting a calibration value does not guarantee that every future measurement will remain correct. The environment, reference, and operating range in which that value was created are part of its meaning. Calibration is a rule for interpreting a measurement. If the conditions behind that rule disappear, confidence in the number should fall too.

Suppose a device learns a threshold in one physical setup. Later its placement, power supply, or surrounding environment changes. The same threshold may no longer represent the same event, and that has to be tested rather than assumed.

That is why an interface can benefit from recording when and under what conditions calibration happened. A successful write is not enough. Which reference was used? How much change is acceptable? When should calibration be checked again? Those details help someone make a better operational decision.

I prefer sensor values to travel with their conditions. That does not weaken the measurement; it makes the claim precise. The quality of a measurement depends not only on the sensor but also on preserving the context in which the measurement became meaningful.

Source: [official reference](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/adc_calibration.html).
