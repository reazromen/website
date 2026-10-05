---
title: The Device Is the Source of Truth for a Firmware Release
date: '2025-10-28'
draft: false
language: en
url: /posts/bn-firmware-release-device-evidence.html
topic: firmware-release-engineering
tags:
- firmware
- observability
featured: false
read_time: 2
excerpt: >-
  A new firmware image being uploaded to the server tells us the state of the server. The
  image actually running on a device is a different claim. A successful deploy command
  cannot prove the second one by itself.
editorial_batch: 20261003-100-niches
---

A new firmware image being uploaded to the server tells us the state of the server. The image actually running on a device is a different claim. A successful deploy command cannot prove the second one by itself. Build identity and active-state evidence need to come back from the device.

In a fleet, some devices may be offline, some may reject an update, and others may roll back to an older image. Showing the new version beside every device at once would display intent rather than reality. Desired state and observed state should remain separate.

A useful report shows which build is targeted, which build the device most recently reported, and how old that report is. Version data without freshness can still mislead. An image that was active last week is not proof of what is running today.

The same principle applies outside embedded systems. Evidence should come from the layer where the change was supposed to occur. A release is strongest when control-plane intent and data-plane observation agree.

Source: [official reference](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/app_image_format.html).
