---
title: PBX Timer Underrun Can Sound Like an Endpoint Bug
url: /posts/pbx-timer-underrun-can-sound-like-an-endpoint-bug.html
date: '2023-05-14'
read_time: 1
excerpt: Server scheduling can inject media timing problems even when embedded firmware
  has not changed.
topic: loup-engineering
tags:
- asterisk
- timer
- rtp
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: PBX & Network · advanced'
outputs:
- url: /posts/pbx-timer-underrun-can-sound-like-an-endpoint-bug.html
  template: cms/templates/posts/posts--pbx-timer-underrun-can-sound-like-an-endpoint-bug.tpl
  source: cms/templates/posts/posts--pbx-timer-underrun-can-sound-like-an-endpoint-bug.json
---

PBX Timer Underrun Can Sound Like an Endpoint Bug became a separate note because the failure crossed more than one subsystem. During LOUP testing the Asterisk timer under-ticked during a call, and restarting the PBX improved the observed behaviour.

That observation mattered because audio defects were easy to attribute to the ESP32-S3. Comparing endpoint logs with PBX timing and then repeating the call after a server restart helped isolate a server-side contribution.

The fix came from assigning one owner to the behaviour and refusing to hide a hardware or network fault with an unrelated firmware workaround. Evidence marker: `asterisk-timer-undertick`.

Distributed real-time systems can fail at either endpoint or in the middle. Keep server timing in the audio-debugging evidence. The value is not only the fix itself; it is having a repeatable way to prove the same class of failure has not returned.

## Project evidence

LOUP engineering marker: `asterisk-timer-undertick`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
