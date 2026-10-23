---
title: "Designing Firmware Updates That Survive Power Loss"
draft: false
date: '2022-06-21'
language: en
url: /posts/firmware-update-rollback-and-power-loss.html
read_time: 2
excerpt: >-
  An update is not complete when a download finishes.
eyebrow: "Perspectives · Firmware Reliability"
tags: ["ota","bootloader","reliability"]
---

An update is not complete when a download finishes. The device must validate the image, select it safely, boot, and confirm health. A bootloader-managed staging area or separate image slots can allow rollback if the new application fails to confirm within a bounded number of attempts.

Integrity checks detect corruption; cryptographic signatures establish that an image was authorized. Plan for interrupted downloads, insufficient storage, incompatible configuration migrations, and bad releases. Test power loss during download, staging, boot, and confirmation, plus invalid signatures and truncated images. The state machine should recover to a known-good version and preserve diagnostic information.
