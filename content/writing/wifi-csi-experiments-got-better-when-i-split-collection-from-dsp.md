---
title: Wi-Fi CSI Experiments Got Better When I Split Collection from DSP
url: /posts/wifi-csi-experiments-got-better-when-i-split-collection-from-dsp.html
date: '2026-09-14'
read_time: 1
excerpt: Keeping the ESP32 focused on reliable CSI capture and moving heavier analysis
  elsewhere made the sensing pipeline easier to debug.
topic: radio-iot
tags:
- wi-fi-csi
- esp32-s3
- dsp
- sensing
draft: false
featured: false
language: en
eyebrow: 2026 Production Voice Systems · advanced
outputs:
- url: /posts/wifi-csi-experiments-got-better-when-i-split-collection-from-dsp.html
  template: cms/templates/posts/posts--wifi-csi-experiments-got-better-when-i-split-collection-from-dsp.tpl
  source: cms/templates/posts/posts--wifi-csi-experiments-got-better-when-i-split-collection-from-dsp.json
---

Trying to collect CSI and do every stage of signal processing on the same small device made the experiment harder to reason about.

I got a cleaner architecture by making the ESP32 responsible for timestamped CSI collection and transport, while a larger machine handled filtering, windowing, feature extraction and visualization. That kept radio timing and data capture close to the hardware without forcing the microcontroller to carry the analysis workload.

The split also improved reproducibility. Raw or lightly processed samples can be replayed through different DSP pipelines without repeating the RF experiment every time. If a classifier behaves strangely, I can determine whether the problem started in collection or analysis.

For sensing work that boundary is valuable. The radio endpoint should be boring and reliable; the experimental part can evolve quickly on the analysis side.
