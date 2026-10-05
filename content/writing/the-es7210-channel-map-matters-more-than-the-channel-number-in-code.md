---
title: The ES7210 Channel Map Matters More Than the Channel Number in Code
url: /posts/the-es7210-channel-map-matters-more-than-the-channel-number-in-code.html
date: '2021-05-03'
read_time: 1
excerpt: AEC depends on what signal actually lands in each TDM slot.
topic: loup-engineering
tags:
- es7210
- tdm
- channel-mapping
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Hardware Bring-Up · advanced'
outputs:
- url: /posts/the-es7210-channel-map-matters-more-than-the-channel-number-in-code.html
  template: cms/templates/posts/posts--the-es7210-channel-map-matters-more-than-the-channel-number-in-code.tpl
  source: cms/templates/posts/posts--the-es7210-channel-map-matters-more-than-the-channel-number-in-code.json
---

The useful question in The ES7210 Channel Map Matters More Than the Channel Number in Code was where the behaviour actually originated. The application expected the far-end reference on channel 0 and microphone audio on channel 1 or 3, but hardware routing had to be verified rather than assumed.

Codec configuration, board wiring and firmware slot order can each change what a numeric channel means. Capturing raw channels and identifying their content was necessary before trusting an AEC reference. A channel index that compiles correctly can still carry the wrong physical signal.

I treated the known-good configuration as a control sample, changed only the layer under investigation, and recorded the regression or improvement before the next experiment. Evidence marker: `aec-ref-ch0-mic-ch1-ch3`.

Signal identity has to be proven at the boundary where hardware becomes samples. DSP tuning cannot repair a mislabeled input. Keeping the rule explicit means the same decision can be checked again on the next board revision or firmware branch.

## Project evidence

LOUP engineering marker: `aec-ref-ch0-mic-ch1-ch3`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
