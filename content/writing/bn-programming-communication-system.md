---
title: Programming Can Start With a Communication System
date: '2026-07-14'
draft: false
language: en
url: /posts/bn-programming-communication-system.html
topic: engineering-notes
tags:
- programming
- protocols
featured: false
read_time: 2
excerpt: >-
  If programming begins as syntax memorization, the relationships inside a system can
  arrive late. A tiny communication system introduces useful questions immediately:
  who asks, who answers, and what happens when no answer arrives?
editorial_batch: 20261003-100-niches
---

If programming begins as syntax memorization, the relationships inside a system can arrive late. A tiny communication system introduces useful questions immediately: who asks, who answers, and what happens when no answer arrives? Those questions connect code to behavior.

Imagine two processes exchanging a message. They need a message format, a destination, and rules for failure. Even a few lines of code quickly introduce protocol and state.

This does not mean starting with a huge distributed system. Finish one small interaction first, then add boundaries gradually: local communication, then a network, then identity, then retries.

For me, much of the joy of programming comes from building these relationships. Code is not merely a list of instructions; it is a way to connect behavior to events outside the program. Once the path of the work is clear, the syntax gains a reason to exist.

Source: [official reference](https://www.rfc-editor.org/rfc/rfc9110.html).
