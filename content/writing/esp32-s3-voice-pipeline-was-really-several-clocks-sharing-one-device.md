---
title: The ESP32-S3 Voice Pipeline Was Really Several Clocks Sharing One Device
url: /posts/esp32-s3-voice-pipeline-was-really-several-clocks-sharing-one-device.html
date: '2025-09-05'
read_time: 1
excerpt: Microphone sampling, RTP packetization, network arrival and speaker playout
  each have their own timing domain.
topic: embedded-firmware
tags:
- esp32-s3
- i2s
- rtp
- audio
draft: false
featured: false
language: en
eyebrow: 2025 Voice and Infrastructure Notes · advanced
outputs:
- url: /posts/esp32-s3-voice-pipeline-was-really-several-clocks-sharing-one-device.html
  template: cms/templates/posts/posts--esp32-s3-voice-pipeline-was-really-several-clocks-sharing-one-device.tpl
  source: cms/templates/posts/posts--esp32-s3-voice-pipeline-was-really-several-clocks-sharing-one-device.json
---

A voice pipeline on the ESP32-S3 looked linear on paper: microphone to codec, codec to RTP, RTP over Wi-Fi, then the reverse path for playback. The bugs made more sense when I stopped treating it as one timeline.

The microphone samples from a hardware clock. RTP packets are grouped on a packetization interval. The network adds variable arrival time. The speaker consumes audio on another hardware clock. If those rates differ slightly, buffers drift even when there is no packet loss.

That explains why a call can sound good for thirty seconds and then slowly begin to underrun or accumulate latency. The fix is not always a larger buffer. I need one part of the system to own playout timing and explicit policies for drift, rebuffering and late packets.

Once I viewed the pipeline as clock domains connected by buffers, audio debugging became much less random. The traces started matching what I could hear instead of leaving me to guess between network and codec problems.
