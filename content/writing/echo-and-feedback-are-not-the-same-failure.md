---
title: Echo and Feedback Are Not the Same Failure
url: /posts/echo-and-feedback-are-not-the-same-failure.html
date: '2026-09-14'
read_time: 1
excerpt: A delayed copy of far-end speech and an unstable acoustic loop require different
  diagnosis.
topic: loup-engineering
tags:
- echo
- feedback
- acoustics
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: AEC & DSP · advanced'
outputs:
- url: /posts/echo-and-feedback-are-not-the-same-failure.html
  template: cms/templates/posts/posts--echo-and-feedback-are-not-the-same-failure.tpl
  source: cms/templates/posts/posts--echo-and-feedback-are-not-the-same-failure.json
---

I stopped treating this part of LOUP as a black box while working on Echo and Feedback Are Not the Same Failure. LOUP speakerphone testing needed to distinguish ordinary far-end echo from howl, ringing or gain instability.

Echo is primarily a correlated delayed version of playback returning through the microphone path. Feedback is a closed-loop gain problem that can self-amplify at resonant frequencies. An AEC can attack correlated echo, while feedback margin depends heavily on acoustic gain, placement and level.

Logs and measurements were used to decide whether the fault lived before or after the boundary, then the smallest falsifiable change was tested. Evidence marker: `echo-vs-feedback`.

Name the acoustic failure correctly before selecting the algorithm. Similar symptoms can belong to different control problems. The resulting test is small enough to rerun after later changes, which is what turns one successful experiment into engineering evidence.

## Project evidence

LOUP engineering marker: `echo-vs-feedback`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
