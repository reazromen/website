---
title: SSH Failure Alerts Need Warning and Critical Bursts
url: /posts/ssh-failure-alerts-need-burst-levels.html
date: '2024-09-05'
read_time: 1
excerpt: A few failed SSH logins are normal on an administered server, while a rapid
  burst can indicate brute-force activity or a broken automation credential.
topic: observability-monitoring
tags:
- ssh
- security
- journald
- alerting
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Logs & Security · advanced'
outputs:
- url: /posts/ssh-failure-alerts-need-burst-levels.html
  template: cms/templates/posts/posts--ssh-failure-alerts-need-burst-levels.tpl
  source: cms/templates/posts/posts--ssh-failure-alerts-need-burst-levels.json
---

A few failed SSH logins are normal on an administered server, while a rapid burst can indicate brute-force activity or a broken automation credential. The monitoring mistake would be to read one metric in isolation. `SSH failure increases over five minutes with warning and critical thresholds` is useful because it narrows the question, and rate-based burst detection reduces noise from isolated mistakes while still escalating sustained authentication failures quickly.

In software operations this falls under behavioral security monitoring. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Use separate severity thresholds, retain the journal context, and correlate with source addresses and successful logins before blocking legitimate operators. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `b65d5d4`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
