---
title: Volume Stuck Near 80 Percent Was a Gain-Path Problem, Not a UI Problem
url: /posts/volume-stuck-near-80-percent-was-a-gain-path-problem-not-a-ui-problem.html
date: '2021-10-01'
read_time: 1
excerpt: A slider value is meaningless until every digital and analog gain stage is
  mapped.
topic: loup-engineering
tags:
- volume
- gain-staging
- codec
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Audio Pipeline · advanced'
outputs:
- url: /posts/volume-stuck-near-80-percent-was-a-gain-path-problem-not-a-ui-problem.html
  template: cms/templates/posts/posts--volume-stuck-near-80-percent-was-a-gain-path-problem-not-a-ui-problem.tpl
  source: cms/templates/posts/posts--volume-stuck-near-80-percent-was-a-gain-path-problem-not-a-ui-problem.json
---

I stopped treating this part of LOUP as a black box while working on Volume Stuck Near 80 Percent Was a Gain-Path Problem, Not a UI Problem. Early LOUP builds appeared to stop changing loudness meaningfully near the top of the volume range.

The visible volume control had to be traced through application scaling, codec volume, amplifier behavior and speaker headroom. If two stages saturate or quantize early, the final 20 percent of UI range can become numerically different and acoustically identical. Measuring output level by step is more useful than inspecting the slider code.

Logs and measurements were used to decide whether the fault lived before or after the boundary, then the smallest falsifiable change was tested. Evidence marker: `volume-stuck-80`.

Gain staging should be designed end to end. A user control is only as linear as the stages it drives. The resulting test is small enough to rerun after later changes, which is what turns one successful experiment into engineering evidence.

## Project evidence

LOUP engineering marker: `volume-stuck-80`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
