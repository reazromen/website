---
title: V115 Stayed Valuable Because It Was Preserved as a Known-Good Artifact
url: /posts/v115-stayed-valuable-because-it-was-preserved-as-a-known-good-artifact.html
date: '2022-01-19'
read_time: 1
excerpt: An old build can be more useful than a new branch when a regression removes
  the reference point.
topic: loup-engineering
tags:
- v115
- release
- known-good
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: OTA & Release Engineering · advanced'
outputs:
- url: /posts/v115-stayed-valuable-because-it-was-preserved-as-a-known-good-artifact.html
  template: cms/templates/posts/posts--v115-stayed-valuable-because-it-was-preserved-as-a-known-good-artifact.tpl
  source: cms/templates/posts/posts--v115-stayed-valuable-because-it-was-preserved-as-a-known-good-artifact.json
---

The first engineering constraint behind V115 Stayed Valuable Because It Was Preserved as a Known-Good Artifact was concrete: LOUP preserved `LOUP_V115_QUIET_AB_V1_APP_ONLY_0x20000.bin` after it eliminated the major downlink stall and stayed stable in long calls.

That artifact became a control sample for later audio work. If a new build crackled, lagged or lost echo control, flashing V115 answered whether the board and PBX could still reproduce the earlier behaviour. Preservation also prevented source changes from rewriting history.

I kept the experiment narrow by changing one variable, capturing the observable result, and comparing it with a preserved working build before moving on. Evidence marker: `v115-quiet-ab`.

A firmware team needs immutable reference binaries, not only branches that can keep moving. In practice that keeps the next LOUP change measurable because the baseline remains available for comparison.

## Project evidence

LOUP engineering marker: `v115-quiet-ab`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
