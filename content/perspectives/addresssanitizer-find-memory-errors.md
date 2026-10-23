---
title: "AddressSanitizer: Catch Memory Bugs Before They Become Production Incidents"
draft: false
date: '2024-03-25'
language: en
url: /posts/addresssanitizer-find-memory-errors.html
read_time: 2
excerpt: >-
  AddressSanitizer instruments C and C++ code to detect errors such as out-of-bounds access and use-after-free.
eyebrow: "Perspectives · Developer Tools"
tags: ["cpp","memory-safety","testing"]
---

AddressSanitizer instruments C and C++ code to detect errors such as out-of-bounds access and use-after-free. Enable it in a debug or test build using supported compiler and linker flags, preserve symbols, and exercise realistic paths. Read the first diagnostic carefully; later failures may be consequences of the original invalid access.

Sanitizer builds have overhead and may not run on every embedded target. Host-side libraries can still benefit, while hardware-specific paths need other techniques. A clean ASan run does not prove the absence of data races. Add sanitizer jobs to CI where practical, reduce reports to small reproductions, and retain regression tests after fixing the underlying lifetime or bounds error.
