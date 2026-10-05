---
title: Firmware Has a Version; Configuration Needs One Too
date: '2024-12-07'
draft: false
language: en
url: /posts/bn-device-config-version.html
topic: firmware-release-engineering
tags:
- firmware
- configuration
featured: false
read_time: 2
excerpt: >-
  A device can receive new firmware while keeping old configuration. If new code reads
  that stored data with a different meaning, behavior can change after the update. Two
  devices on the same firmware may then behave differently because their stored history differs.
editorial_batch: 20261003-100-niches
---

A device can receive new firmware while keeping old configuration. If new code reads that stored data with a different meaning, behavior can change after the update. Two devices on the same firmware may then behave differently because their stored history differs.

Imagine a setting that used to be a number and later becomes an enum. Flashing new firmware does not automatically transform the old value into the new structure. A configuration schema version and migration rules let the software know what it is actually reading.

Migration failure also needs a defined outcome. If half the data is rewritten while the rest stays in the old format, the next boot can enter an ambiguous state. Preparing the new state first and then committing it is one useful pattern, although the exact strategy depends on storage and product constraints.

Debug reports should therefore include configuration version as well as build identity. A release is a relationship between code and data. Keeping code history while losing the history of what stored data means makes behavior difficult to reproduce.

Source: [official reference](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/storage/nvs_flash.html).
