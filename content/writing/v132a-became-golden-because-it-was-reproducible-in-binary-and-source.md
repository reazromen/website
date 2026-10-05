---
title: V132A Became Golden Because It Was Reproducible in Binary and Source
url: /posts/v132a-became-golden-because-it-was-reproducible-in-binary-and-source.html
date: '2026-02-16'
read_time: 1
excerpt: A release is stronger when the exact app image and the source snapshot both
  survive.
topic: loup-engineering
tags:
- v132a
- golden-build
- release
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: OTA & Release Engineering · advanced'
outputs:
- url: /posts/v132a-became-golden-because-it-was-reproducible-in-binary-and-source.html
  template: cms/templates/posts/posts--v132a-became-golden-because-it-was-reproducible-in-binary-and-source.tpl
  source: cms/templates/posts/posts--v132a-became-golden-because-it-was-reproducible-in-binary-and-source.json
---

I reached V132A Became Golden Because It Was Reproducible in Binary and Source through a repeatable lab problem rather than a design slogan. The stable LOUP build was preserved as app-only and partition artifacts together with a source snapshot marked for production and the committed AEC reference path.

The app length, flash offset and partition context were recorded so the binary could be reflashed without reconstructing an old build environment. The source snapshot provided the code-side explanation for that artifact instead of relying on memory about which branch was stable.

The useful debugging step was separating signal path, state and timing instead of modifying all three and then guessing which change mattered. Evidence marker: `v132a-golden`.

Golden releases should be recoverable as both executable evidence and reviewable source. That distinction also makes regressions cheaper to isolate when hardware, firmware and infrastructure are changing in parallel.

## Project evidence

LOUP engineering marker: `v132a-golden`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
