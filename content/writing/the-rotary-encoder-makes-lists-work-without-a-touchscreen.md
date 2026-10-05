---
title: The Rotary Encoder Makes Lists Work Without a Touchscreen
url: /posts/the-rotary-encoder-makes-lists-work-without-a-touchscreen.html
date: '2020-08-19'
read_time: 1
excerpt: Infinite scroll plus push maps naturally to small menu selection when the
  display is not interactive.
topic: loup-engineering
tags:
- rotary-encoder
- input
- ui
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: E-Paper UI & Controls · advanced'
outputs:
- url: /posts/the-rotary-encoder-makes-lists-work-without-a-touchscreen.html
  template: cms/templates/posts/posts--the-rotary-encoder-makes-lists-work-without-a-touchscreen.tpl
  source: cms/templates/posts/posts--the-rotary-encoder-makes-lists-work-without-a-touchscreen.json
---

The useful question in The Rotary Encoder Makes Lists Work Without a Touchscreen was where the behaviour actually originated. LOUP specifies a mouse-wheel-style infinite rotary control with push for navigating contacts and confirming selection.

The firmware needs debounced relative movement, acceleration policy and a click event that remains distinct from rotation. The UI then has one clear focus item and can update only the selection region as the wheel moves.

I treated the known-good configuration as a control sample, changed only the layer under investigation, and recorded the regression or improvement before the next experiment. Evidence marker: `rotary-click`.

A simple input device becomes effective when its event model and visual focus model are designed together. Keeping the rule explicit means the same decision can be checked again on the next board revision or firmware branch.

## Project evidence

LOUP engineering marker: `rotary-click`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
