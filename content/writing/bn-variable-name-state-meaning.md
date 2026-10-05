---
title: Variable Names Preserve the Meaning of State
date: '2023-04-04'
draft: false
language: en
url: /posts/bn-variable-name-state-meaning.html
topic: engineering-notes
tags:
- programming
- state
featured: false
read_time: 2
excerpt: >-
  Knowing that a variable contains a number is not the same as knowing what the number
  means. A name that preserves unit, time, or state reduces the amount of context a future
  reader has to reconstruct.
editorial_batch: 20261003-100-niches
---

Knowing that a variable contains a number is not the same as knowing what the number means. If the name is simply *value*, the next reader has to search elsewhere to reconstruct its context. A name that preserves unit, time, or state reduces that work.

Imagine a timeout whose unit is unclear: seconds or milliseconds. The wrong number can still be syntactically valid while producing incorrect behavior. A compiler cannot catch every semantic mistake. Naming and type rules can make some of those mistakes harder to create.

A very long name is not a substitute for every explanation either. The code still needs to reveal when the state changes and who is allowed to change it. A good name makes that relationship easier to follow.

I do not think of naming as decoration. It is communication with a future reader, and that future reader may simply be me a few months later. The clearer the meaning, the less unnecessary inference the code demands.
