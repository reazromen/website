---
title: Where Are You Drawing the Boundary of the System?
date: '2025-09-28'
draft: false
language: en
url: /posts/bn-boundary-defines-system.html
topic: systems-thinking
tags:
- architecture
- systems-thinking
featured: false
read_time: 2
excerpt: >-
  Before talking about a system, it helps to say where its boundary is. An application
  can be treated as the system, or the application, database, network, and user workflow
  can be considered together. Changing the boundary changes the explanation.
editorial_batch: 20261003-100-niches
---

Before talking about a system, it helps to say where its boundary is. An application can be treated as the system, or the application, database, network, and user workflow can be considered together. Changing the boundary changes the explanation.

Suppose the application responded quickly but the user never received the result. Inside the application boundary, the operation succeeded. Across the whole communication path, it failed. Both reports can be true because they are measuring different systems.

An investigation often needs both larger and smaller boundaries. Start with the end-to-end path, then isolate the suspected component. Avoid turning a truth about one layer into a guarantee about another.

For me, systems thinking does not begin by making everything larger. It begins by choosing the relationships that answer the question at hand. Once the boundary is explicit, words like success and failure become much more meaningful.

Source: [official reference](https://kubernetes.io/docs/concepts/architecture/).
