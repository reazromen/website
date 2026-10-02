---
title: Incoming Call UI Has a Hard Timing Requirement Even on E-Paper
url: /posts/incoming-call-ui-has-a-hard-timing-requirement-even-on-e-paper.html
date: '2026-09-14'
read_time: 1
excerpt: The user must see caller identity before deciding whether to answer, despite
  slow display behavior.
topic: loup-engineering
tags:
- incoming-call
- e-paper
- latency
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: E-Paper UI & Controls · advanced'
outputs:
- url: /posts/incoming-call-ui-has-a-hard-timing-requirement-even-on-e-paper.html
  template: cms/templates/posts/posts--incoming-call-ui-has-a-hard-timing-requirement-even-on-e-paper.tpl
  source: cms/templates/posts/posts--incoming-call-ui-has-a-hard-timing-requirement-even-on-e-paper.json
---

I stopped treating this part of LOUP as a black box while working on Incoming Call UI Has a Hard Timing Requirement Even on E-Paper. LOUP incoming-call state combines signalling, ringtone or alert behavior, contact identity and a display update on e-paper.

The screen should prepare a compact caller view that can be rendered quickly, while physical answer/reject control remains available immediately. The call path should not wait on a full decorative refresh before accepting input.

Logs and measurements were used to decide whether the fault lived before or after the boundary, then the smallest falsifiable change was tested. Evidence marker: `incoming-call-ui`.

User-visible latency budgets should follow the action. Answering a call is time-critical; a perfect full-screen redraw is not. The resulting test is small enough to rerun after later changes, which is what turns one successful experiment into engineering evidence.

## Project evidence

LOUP engineering marker: `incoming-call-ui`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
