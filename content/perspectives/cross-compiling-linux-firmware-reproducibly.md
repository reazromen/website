---
title: "Cross-Compiling Firmware and Linux Utilities Without Losing Track of the Toolchain"
draft: false
date: '2021-01-16'
language: en
url: /posts/cross-compiling-linux-firmware-reproducibly.html
read_time: 2
excerpt: >-
  Cross-compilation builds software on one machine for a different target architecture.
eyebrow: "Perspectives · Build Systems"
tags: ["cross-compilation","linux","toolchains"]
---

Cross-compilation builds software on one machine for a different target architecture. Record the target triple, compiler, sysroot, ABI, C library, SDK, and flags. Mixing host headers with target libraries can produce confusing link failures or binaries that cannot run on the device. In CMake, use a toolchain file to separate target settings from project logic.

Inspect artifacts with `file`, `readelf`, and `objdump` rather than trusting a successful build. Confirm architecture, ABI, and dynamic dependencies. Pin toolchain versions, automate clean builds, and test on the target or a representative emulator. The goal is an artifact that deploys and runs in the intended environment.
