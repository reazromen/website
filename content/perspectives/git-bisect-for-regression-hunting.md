---
title: "Git Bisect: Find the Commit That Introduced a Firmware Regression"
draft: false
date: '2024-06-02'
language: en
url: /posts/git-bisect-for-regression-hunting.html
read_time: 2
excerpt: >-
  Git bisect performs a binary search through commit history.
eyebrow: "Perspectives · Developer Tools"
tags: ["git","debugging"]
---

Git bisect performs a binary search through commit history. Mark a known-broken revision bad and a known-working revision good; test each midpoint and report the result. Each answer eliminates roughly half the candidates.

First establish a reliable pass/fail test. Keep board revision, compiler, configuration, and dependencies consistent, since flaky hardware tests can misclassify commits. Mark unbuildable historical revisions as skipped rather than guessing. After bisect identifies a candidate, reproduce the failure on its parent and on the candidate itself. The commit narrows the investigation; it does not automatically prove the defective line.
