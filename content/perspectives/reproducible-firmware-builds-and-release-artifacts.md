---
title: "Reproducible Firmware Builds: Know Exactly What You Flashed"
draft: false
date: '2019-04-05'
language: en
url: /posts/reproducible-firmware-builds-and-release-artifacts.html
read_time: 2
excerpt: >-
  A reliable release process connects source code to the binary that was tested and flashed.
eyebrow: "Perspectives · Release Engineering"
tags: ["firmware","ci","release-engineering"]
---

A reliable release process connects source code to the binary that was tested and flashed. Record the source commit, compiler and SDK versions, configuration, bootloader, partition layout, and build environment. Retain checksums, the map file, and the ELF with the flashable image so a field failure can be matched to the correct symbols and memory layout.

Reproducible builds aim for identical inputs to produce identical outputs; timestamps and absolute paths can interfere. Pinned dependencies and automated clean builds improve traceability. Test the actual release artifact, including boot, upgrade, and rollback paths, and preserve it instead of rebuilding silently during deployment.
