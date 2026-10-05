---
title: Changing Codecs Changes the Work Behind the Audio
date: '2022-01-13'
draft: false
language: en
url: /posts/bn-codec-conversion-hidden-work.html
topic: telecom-voip
tags:
- audio
- capacity
featured: false
read_time: 2
excerpt: >-
  If a codec is treated as nothing more than an audio format, a large part of the cost
  inside a phone system stays hidden. When two sides cannot use the same codec, audio may
  need to be decoded and encoded again in the middle.
editorial_batch: 20261003-100-niches
---

If a codec is treated as nothing more than an audio format, a large part of the cost inside a phone system stays hidden. When two sides cannot use the same codec, audio may need to be decoded and encoded again in the middle. That transcoding consumes compute, buffering, and time. The number of calls can stay the same while the server workload changes because the codec combinations changed.

Suppose a phone speaks codec A while the trunk expects codec B. If the PBX performs the translation, every media frame takes an extra processing path. Counting registered endpoints will not reveal that work. Capacity planning needs to know which calls are transcoded, which are passed through, and whether processing is required in one or both directions.

Lower bandwidth does not automatically mean lower total cost either. Smaller packets sent more frequently can increase header overhead. More compression can reduce network traffic while increasing encoder work. The best tradeoff depends on the limits of the devices, network, and server.

Codec selection should therefore be tested across a real call path. Is the audio intelligible? What is the delay? Where is CPU pressure created? What happens on a weak network? Humanly acceptable sound and sustainable system behavior are related. Calling the newest codec the best solution before measuring that relationship is premature.

Source: [official reference](https://www.rfc-editor.org/rfc/rfc3551.html).
