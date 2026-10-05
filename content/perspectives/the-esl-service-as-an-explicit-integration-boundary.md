---
title: The ESL Service as an Explicit Integration Boundary
url: /posts/the-esl-service-as-an-explicit-integration-boundary.html
date: '2023-08-27'
read_time: 2
excerpt: Why I prefer to see integration adapters represented directly in the deployment
  graph.
topic: voiceware-engineering
tags:
- voiceware
- esl
- integration
- kubernetes
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Voice Services · deep-dive'
outputs:
- url: /posts/the-esl-service-as-an-explicit-integration-boundary.html
  template: cms/templates/posts/posts--the-esl-service-as-an-explicit-integration-boundary.tpl
  source: cms/templates/posts/posts--the-esl-service-as-an-explicit-integration-boundary.json
---

I learned more from the small Voiceware failures than from the clean architecture diagram. The final repository looks organized, but the useful engineering story is in the boundaries that had to be discovered and corrected.

The architecture question is **why I prefer to see integration adapters represented directly in the deployment graph**.

## Start with the boundary, not the tool

I packaged ESL separately using the voiceware-esl image on port 5000.

## Runtime view

```
voice/telephony event -> integration or audio service -> application/background processing -> resulting action
```

## Responsibilities

For this topic, the relevant responsibility is why I prefer to see integration adapters represented directly in the deployment graph. The boundary is good when each side can be described without hand-waving: what it receives, what it produces, what it depends on, and what happens if it disappears.

## Interfaces and failure isolation

The failure I explicitly design against is: When integration logic is buried inside a large application, connectivity failures are harder to localize and scale independently. That is why I care about the interface, not only whether both pods are currently green.

## Scaling implications

The signals I would attach to this boundary are request or event latency, backlog, process availability, dependency errors, quality-specific metrics when available.

## Architecture review questions

- Keep voice-specific services independently restartable where useful.
- Verify internal endpoint contracts provider-to-consumer.
- Separate observed repository facts from protocol assumptions.
- Protect interactive work from batch backlog.
- Do not use pod liveness as the only media-health signal.

The design rule I keep is **Making an adapter a first-class service turns an implicit dependency into an observable operational boundary.** That lesson has been more reusable for me than any particular YAML pattern.
