---
title: Why Voice Processing and Web Serving Should Fail Independently
url: /posts/why-voice-processing-and-web-serving-should-fail-independently.html
date: '2023-12-07'
read_time: 2
excerpt: Using deployment separation to reduce cross-component blast radius.
topic: voiceware-engineering
tags:
- voiceware
- audio
- web-app
- fault-isolation
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Voice Services · deep-dive'
outputs:
- url: /posts/why-voice-processing-and-web-serving-should-fail-independently.html
  template: cms/templates/posts/posts--why-voice-processing-and-web-serving-should-fail-independently.tpl
  source: cms/templates/posts/posts--why-voice-processing-and-web-serving-should-fail-independently.json
---

The architecture question is **using deployment separation to reduce cross-component blast radius**.

## Start with the boundary, not the tool

I deployed the web app and audio-fork as separate Helm applications so they could fail and restart independently.

## Runtime view

```
voice/telephony event -> integration or audio service -> application/background processing -> resulting action
```

## Responsibilities

For this topic, the relevant responsibility is using deployment separation to reduce cross-component blast radius. The boundary is good when each side can be described without hand-waving: what it receives, what it produces, what it depends on, and what happens if it disappears.

## Interfaces and failure isolation

The failure I explicitly design against is: A memory leak or restart loop in a media component should not necessarily recycle the user-facing web process. That is why I care about the interface, not only whether both pods are currently green.

## Scaling implications

The signals I would attach to this boundary are request or event latency, backlog, process availability, dependency errors, quality-specific metrics when available.

## Architecture review questions

- Do not use pod liveness as the only media-health signal.
- Keep voice-specific services independently restartable where useful.
- Verify internal endpoint contracts provider-to-consumer.
- Separate observed repository facts from protocol assumptions.
- Protect interactive work from batch backlog.

The design rule I keep is **Failure isolation is one of the strongest practical reasons to separate runtime responsibilities.** The tool is secondary. The contract between layers is what makes the system operable.
