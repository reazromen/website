---
title: V117 Was Useful Because It Failed Clearly
url: /posts/v117-was-useful-because-it-failed-clearly.html
date: '2023-02-03'
read_time: 1
excerpt: A bad experimental build can be valuable when it changes a small set of variables
  and is easy to revert.
topic: loup-engineering
tags:
- v117
- regression
- aec
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: AEC & DSP · advanced'
outputs:
- url: /posts/v117-was-useful-because-it-failed-clearly.html
  template: cms/templates/posts/posts--v117-was-useful-because-it-failed-clearly.tpl
  source: cms/templates/posts/posts--v117-was-useful-because-it-failed-clearly.json
---

The useful question in V117 Was Useful Because It Failed Clearly was where the behaviour actually originated. The V117 rebuffer, AEC and volume patch produced bad crackle and was reverted instead of being patched repeatedly in place.

Combining several changes made the result poor enough to reject, but preservation of the previous known-good branch prevented the regression from becoming the new baseline. The next work could then reintroduce ideas one at a time rather than debugging an unstable stack of changes.

I treated the known-good configuration as a control sample, changed only the layer under investigation, and recorded the regression or improvement before the next experiment. Evidence marker: `v117-bad-crackle`.

Reversion is an engineering tool. A failed experiment should narrow the search space, not become permanent technical debt. Keeping the rule explicit means the same decision can be checked again on the next board revision or firmware branch.

## Project evidence

LOUP engineering marker: `v117-bad-crackle`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
