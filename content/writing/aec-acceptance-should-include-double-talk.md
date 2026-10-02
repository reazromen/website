---
title: AEC Acceptance Should Include Double-Talk
url: /posts/aec-acceptance-should-include-double-talk.html
date: '2026-09-14'
read_time: 1
excerpt: A speakerphone must handle the user talking while the far end is also active.
topic: loup-engineering
tags:
- aec
- double-talk
- speech
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: AEC & DSP · advanced'
outputs:
- url: /posts/aec-acceptance-should-include-double-talk.html
  template: cms/templates/posts/posts--aec-acceptance-should-include-double-talk.tpl
  source: cms/templates/posts/posts--aec-acceptance-should-include-double-talk.json
---

The practical ownership question in AEC Acceptance Should Include Double-Talk was simple to state and harder to prove. Single-speaker echo tests are useful but incomplete because real calls include overlapping speech.

During double-talk the microphone contains local speech plus far-end leakage. An aggressive adaptive filter can mistake local speech for echo and distort the user, while a conservative filter may leave more residual echo. Acceptance therefore needs controlled overlap tests at several speaker volumes, not only silence-versus-far-end playback.

The debugging order stayed conservative: verify wiring and state transitions first, then tune performance only after correctness had been established. Evidence marker: `aec-double-talk`.

A voice algorithm should be tested in the conversational condition that is hardest for its assumptions. The broader result is a system that can be changed incrementally because each layer has a measurable responsibility and a known recovery path.

## Project evidence

LOUP engineering marker: `aec-double-talk`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
