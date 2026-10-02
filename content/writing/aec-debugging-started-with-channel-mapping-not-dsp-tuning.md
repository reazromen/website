---
title: AEC Debugging Started with Channel Mapping, Not DSP Tuning
url: /posts/aec-debugging-started-with-channel-mapping-not-dsp-tuning.html
date: '2026-09-14'
read_time: 1
excerpt: Before tuning echo cancellation I verified that the algorithm was receiving
  the microphone and far-end reference channels I thought it was.
topic: embedded-firmware
tags:
- aec
- i2s
- es7210
- audio
draft: false
featured: false
language: en
eyebrow: 2026 Production Voice Systems · advanced
outputs:
- url: /posts/aec-debugging-started-with-channel-mapping-not-dsp-tuning.html
  template: cms/templates/posts/posts--aec-debugging-started-with-channel-mapping-not-dsp-tuning.tpl
  source: cms/templates/posts/posts--aec-debugging-started-with-channel-mapping-not-dsp-tuning.json
---

Echo cancellation can waste days if the signal plumbing is wrong. The algorithm may run, CPU usage may look normal, and the result may still be useless because the reference channel does not contain the far-end signal.

I moved channel verification to the start of the process. Capture the individual I2S channels, identify which one is microphone audio, identify the playback reference, and verify their timing. Only then does it make sense to tune filter length, adaptation or suppression.

This also caught assumptions introduced by codec routing. A channel index in the application is not proof of what the codec placed on that slot. Hardware mapping, TDM configuration and firmware channel order all have to agree.

Once the reference was correct, echo behavior changed in a way that tuning could actually improve. That was a useful reminder that DSP problems are often ordinary integration problems first.
