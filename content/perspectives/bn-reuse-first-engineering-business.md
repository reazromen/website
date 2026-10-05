---
title: Reuse Is an Engineering Decision Too
date: '2024-02-17'
draft: false
language: en
url: /posts/bn-reuse-first-engineering-business.html
topic: production-engineering
tags:
- reuse
- product-thinking
featured: false
read_time: 2
excerpt: >-
  Building from scratch is a great way to learn, but existing software may solve a user's
  problem faster and more reliably. Reuse does not remove engineering judgment; it changes
  what must be evaluated.
editorial_batch: 20261003-100-niches
---

Building from scratch is a great way to learn, but existing software may solve a user's problem faster and more reliably. Reuse does not remove engineering judgment. You still need to know which parts fit the requirement and which constraints become part of your own system.

Suppose the real need is a specific form and a publishing path. Building an entire new platform immediately creates responsibility for authentication, storage, editing, deployment, and maintenance. Reusing a smaller existing system can solve the immediate problem while revealing the real requirements earlier.

Reuse still has dependencies. Versioning, licenses, maintenance, data flow, and replacement cost matter. A component that is convenient today may be expensive to replace later. Total control and delivering useful work to the user are not the same objective.

I do not think of reuse as a lesser shortcut. Good reuse requires reading boundaries, matching interfaces, and reducing the problem to what actually needs to be built. The quality of an engineering solution is not measured by how much new code it contains.
