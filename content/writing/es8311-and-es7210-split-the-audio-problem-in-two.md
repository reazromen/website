---
title: ES8311 and ES7210 Split the Audio Problem in Two
url: /posts/es8311-and-es7210-split-the-audio-problem-in-two.html
date: '2026-09-14'
read_time: 1
excerpt: Speaker output and microphone capture travel through different codec responsibilities.
topic: loup-engineering
tags:
- es8311
- es7210
- audio-codec
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Hardware Bring-Up · advanced'
outputs:
- url: /posts/es8311-and-es7210-split-the-audio-problem-in-two.html
  template: cms/templates/posts/posts--es8311-and-es7210-split-the-audio-problem-in-two.tpl
  source: cms/templates/posts/posts--es8311-and-es7210-split-the-audio-problem-in-two.json
---

I reached ES8311 and ES7210 Split the Audio Problem in Two through a repeatable lab problem rather than a design slogan. LOUP uses ES8311 on the playback side and ES7210 on the microphone side, so a call that sounds bad in one direction does not point to one generic audio codec problem.

Downlink faults have to be traced through decoder, sample conversion, I2S output, ES8311, amplifier and speaker. Uplink faults travel through microphones, ES7210 routing, I2S capture, AEC and encoder. Keeping those paths distinct prevented fixes for one direction from being applied blindly to the other.

The useful debugging step was separating signal path, state and timing instead of modifying all three and then guessing which change mattered. Evidence marker: `codec-split`.

Bidirectional audio should be debugged as two pipelines that meet at the call, not as one opaque audio subsystem. That distinction also makes regressions cheaper to isolate when hardware, firmware and infrastructure are changing in parallel.

## Project evidence

LOUP engineering marker: `codec-split`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
