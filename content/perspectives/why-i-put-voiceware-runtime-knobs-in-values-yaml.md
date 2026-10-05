---
title: Why I Put Voiceware Runtime Knobs in values.yaml
url: /posts/why-i-put-voiceware-runtime-knobs-in-values-yaml.html
date: '2022-07-01'
read_time: 1
excerpt: Separating reusable Kubernetes structure from service-specific image, replica,
  and port settings.
topic: voiceware-engineering
tags:
- voiceware
- helm
- values
- kubernetes
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Helm · deep-dive'
outputs:
- url: /posts/why-i-put-voiceware-runtime-knobs-in-values-yaml.html
  template: cms/templates/posts/posts--why-i-put-voiceware-runtime-knobs-in-values-yaml.tpl
  source: cms/templates/posts/posts--why-i-put-voiceware-runtime-knobs-in-values-yaml.json
---

Here is the simplest way I explain **separating reusable Kubernetes structure from service-specific image, replica, and port settings**.

## The analogy

```
values.yaml + templates -> rendered manifest -> ArgoCD/Kubernetes
```

## How it appeared in Voiceware

I kept image repository, tag, pull policy, replica count, and service settings in values.yaml instead of hard-coding them into templates.

## Why it matters

Hard-coding environment-specific values inside templates makes every change a template edit and increases drift between charts.

## A concrete way to reason about it

If the signals helm template output, missing nested values, conditional branches, required service ports, rendered container commands agree with the expected flow, I can move to application-specific behavior. If they disagree, I stay at the infrastructure boundary until the mismatch is understood.

## Practical test

- Render the chart before sync.
- Fail early when required values are absent.
- Use defaults only when a default is genuinely safe.
- Keep conditionals shallow and test both branches.
- Treat rendered YAML as a build artifact worth reviewing.

The short version is **Values files work best when they expose intentional operational choices rather than every possible YAML field.** The goal is not more Kubernetes. The goal is less ambiguity.
