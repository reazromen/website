---
title: An OTA Download Finishing Does Not Mean the Update Is Finished
date: '2022-07-07'
draft: false
language: en
url: /posts/bn-ota-download-not-update.html
topic: ota-fleet
tags:
- ota
- state
featured: false
read_time: 2
excerpt: >-
  A full OTA progress bar proves that a file transfer completed. It does not yet prove
  that the device booted the image successfully or that the required product functions
  still work. Update success spans several states.
editorial_batch: 20261003-100-niches
---

A full OTA progress bar proves that a file transfer completed. It does not yet prove that the device booted the image successfully or that the required product functions still work. Update success spans several states rather than one moment.

Suppose the new image downloads, the device restarts, and audio never comes back. The transfer log is successful, but a critical product function has failed. If health validation tests only for boot, the system may mark a bad image as good. Boot confirmation and usability confirmation should remain separate.

OTA design also needs rules for when rollback is allowed, when a new image becomes accepted, and what evidence supports that decision. Before updating the whole fleet, it is useful to observe a small group first. Tests should reflect the actual firmware, bootloader, and partition constraints of the device.

Writing *success* on a dashboard is easy; defining what that word means is the real work. Separating download, boot, and functional validation lets an operator see where an update actually stands instead of treating a completed transfer as a completed release.

Source: [official reference](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/ota.html).
