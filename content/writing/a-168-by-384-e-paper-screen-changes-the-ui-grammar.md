---
title: A 168 by 384 E-Paper Screen Changes the UI Grammar
url: /posts/a-168-by-384-e-paper-screen-changes-the-ui-grammar.html
date: '2023-11-09'
read_time: 1
excerpt: Portrait monochrome e-paper rewards stable hierarchy and punishes unnecessary
  redraws.
topic: loup-engineering
tags:
- e-paper
- gdey029t71h
- ui
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: E-Paper UI & Controls · advanced'
outputs:
- url: /posts/a-168-by-384-e-paper-screen-changes-the-ui-grammar.html
  template: cms/templates/posts/posts--a-168-by-384-e-paper-screen-changes-the-ui-grammar.tpl
  source: cms/templates/posts/posts--a-168-by-384-e-paper-screen-changes-the-ui-grammar.json
---

The first engineering constraint behind A 168 by 384 E-Paper Screen Changes the UI Grammar was concrete: LOUP uses the Good Display GDEY029T71H with SSD1685, operated as a 168 by 384 portrait interface.

That resolution is enough for contacts, call state, battery, signal and setup information, but the refresh characteristics discourage phone-like animation. Layout has to be readable after a static render and every state transition needs to justify the region it refreshes.

I kept the experiment narrow by changing one variable, capturing the observable result, and comparing it with a preserved working build before moving on. Evidence marker: `gdey029t71h`.

Display technology should shape interaction design from the beginning instead of being treated as a slower LCD at the end. In practice that keeps the next LOUP change measurable because the baseline remains available for comparison.

## Project evidence

LOUP engineering marker: `gdey029t71h`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
