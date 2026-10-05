---
title: Weather Models and Field Observations Are Different Kinds of Data
date: '2026-09-06'
draft: false
language: en
url: /posts/bn-weather-observation-model.html
topic: environmental-systems
tags:
- environment
- data-quality
featured: false
read_time: 2
excerpt: >-
  Before interpreting a temperature for a location, first ask where the number came from.
  A nearby station observation, a model grid value, and a later reanalysis product are not
  the same kind of evidence.
editorial_batch: 20261003-100-niches
---

Before interpreting a temperature for a location, first ask where the number came from. A nearby station observation, a model grid value, and a later reanalysis product are not the same kind of evidence. They exist for different purposes and have different limits.

Suppose two sources disagree on temperature. It is difficult to declare one wrong immediately. Location, elevation, time, and data-generation method all matter. Two values carrying the same city name do not necessarily describe the exact same physical point.

A dashboard should preserve source name, timestamp, and data type. Calling a model output a direct measurement—or calling an observation a forecast—creates a larger claim than the data supports.

For me, the first responsibility of an environmental data interface is preserving the identity of the number. Beautiful visualization cannot compensate for losing how the data was produced. Multiple sources become most valuable when their differences remain visible.

Source: [official reference](https://open-meteo.com/en/docs/historical-weather-api).
