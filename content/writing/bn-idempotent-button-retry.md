---
title: If the Same Button Is Pressed Twice, Should the Work Run Twice?
date: '2023-05-04'
draft: false
language: en
url: /posts/bn-idempotent-button-retry.html
topic: production-engineering
tags:
- idempotency
- api
featured: false
read_time: 2
excerpt: >-
  When a network response disappears, a user may retry even though the first operation
  already succeeded on the server. Whether the second request creates new work or returns
  the result of the first operation is part of the application's contract.
editorial_batch: 20261003-100-niches
---

When a network response disappears, a user may retry even though the first operation already succeeded on the server. Whether the second request creates new work or returns the result of the first operation is part of the application's contract.

Imagine pressing a button to start a device update. The interface never receives a response, so the button is pressed again. Should two update commands run concurrently? Disabling the button in the UI does not solve every network failure or retry path.

Keeping an operation identity can help the server recognize the same intent, but the design still needs an expiration policy, a definition of which result is preserved, and protection against accidentally treating different requests as identical. Idempotency is a concrete behavior, not a decorative term.

I prefer to design retry semantics from the beginning. Failed communication is normal. The important property is that repeating the same intent does not create unnecessary duplicate side effects.

Source: [official reference](https://www.rfc-editor.org/rfc/rfc9110.html).
