---
title: The Age of "Live" Environmental Data
date: '2024-04-22'
draft: false
language: en
url: /posts/bn-environment-data-age.html
topic: environmental-systems
tags:
- environment
- freshness
featured: false
read_time: 2
excerpt: >-
  When an interface says live, people naturally assume the data represents the present.
  But source update interval, observation time, ingestion time, and display time are all
  different clocks. Opening a page now does not make its data current.
editorial_batch: 20261003-100-niches
---

When an interface says *live*, people naturally assume the data represents the present. But source update interval, observation time, ingestion time, and display time are all different clocks. Opening a page now does not make its data current.

Suppose a panel keeps showing the latest known value after the upstream source stops updating. The number may still be historically correct, but it is no longer current. Without its age, stale information can become the basis for a new decision.

Keeping observation time, collection time, and presentation time separate helps locate delay. If a fallback source is being used, that should be visible too. Alternate data can be useful, but its identity should not disappear.

I think of *live* as a promise that a product needs to define. Once update cadence and acceptable data age are visible, the user can judge how much confidence to place in the number right now.

Source: [official reference](https://open-meteo.com/en/docs).
