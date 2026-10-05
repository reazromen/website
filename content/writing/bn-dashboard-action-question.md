---
title: Ask the Operational Question Before Building the Dashboard
date: '2024-10-24'
draft: false
language: en
url: /posts/bn-dashboard-action-question.html
topic: observability-monitoring
tags:
- observability
- dashboards
featured: false
read_time: 2
excerpt: >-
  Adding a graph is easy; deciding what action that graph should support is harder. A
  dashboard can contain every metric and still leave an operator unsure where to begin
  during an incident.
editorial_batch: 20261003-100-niches
---

Adding a graph is easy; deciding what action that graph should support is harder. A dashboard can contain every metric and still leave an operator unsure where to begin during an incident. I prefer to write the operational question before choosing the panel.

Suppose phone calls are failing. Registration count, media failures, and network latency are all useful signals, but they answer different questions. Which panel should come first depends on the symptom being investigated. Giving every number equal visual weight can hide the relationship that matters.

Try writing the purpose of a panel as a sentence: if this value changes, what will I check next? If there is no answer, the panel may be useful for context rather than direct decision-making. That distinction is worth making visible.

A good dashboard is not defined by having few panels or many. Its job is to guide an investigation. Layout matters, but the connection between visible numbers and operational action is what makes the dashboard useful.

Source: [official reference](https://prometheus.io/docs/practices/instrumentation/).
