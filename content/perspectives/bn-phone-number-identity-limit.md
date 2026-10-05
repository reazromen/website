---
title: A Phone Number Is a Communication Address, Not a Complete Identity
date: '2022-06-01'
draft: false
language: en
url: /posts/bn-phone-number-identity-limit.html
topic: security-identity
tags:
- identity
- telephony
featured: false
read_time: 2
excerpt: >-
  We often treat a phone number as if it were a permanent identity. In reality, it is a
  communication address whose user can change, whose access can be lost, and whose
  presentation can be misleading.
editorial_batch: 20261003-100-niches
---

We often treat a phone number as if it were a permanent identity. In reality, it is a communication address whose user can change, whose access can be lost, and whose presentation can be misleading. Reaching a number and reliably identifying the person behind it are different claims. Security systems built around telephony can become overconfident when that distinction disappears.

Caller ID often triggers immediate recognition, but before trusting the displayed number we need to know where that information came from and how it was verified. Mechanisms such as SIP Identity can add verification to specific protocol claims. Even then, cryptographic or protocol verification cannot measure the intentions or honesty of the person on the other end. Address authenticity and behavioral trust are separate.

Suppose an urgent request for sensitive information arrives from a number associated with an organization. The number matching should not be the only basis for the decision. High-impact actions may require another verification path, limited permissions, and context about the requested operation. The goal is not to teach permanent suspicion; it is to define how far one identity signal should be trusted.

This boundary matters in system design. Interfaces often display a small identity signal and then allow very large decisions to rest on it. If the signal appears to mean more than it can actually prove, the interface teaches false confidence. A good identity system communicates not only the name, but also which claim was verified and what remains unverified.

Source: [official reference](https://www.rfc-editor.org/rfc/rfc8224.html).
