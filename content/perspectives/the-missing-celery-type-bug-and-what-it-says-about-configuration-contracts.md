---
title: The Missing celery.type Bug and What It Says About Configuration Contracts
url: /posts/the-missing-celery-type-bug-and-what-it-says-about-configuration-contracts.html
date: '2025-07-03'
read_time: 1
excerpt: How conditional behavior depends on values being present and semantically
  correct.
topic: voiceware-engineering
tags:
- voiceware
- helm
- configuration
- celery
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Helm · deep-dive'
outputs:
- url: /posts/the-missing-celery-type-bug-and-what-it-says-about-configuration-contracts.html
  template: cms/templates/posts/posts--the-missing-celery-type-bug-and-what-it-says-about-configuration-contracts.tpl
  source: cms/templates/posts/posts--the-missing-celery-type-bug-and-what-it-says-about-configuration-contracts.json
---

## Symptom

`celery-low` also needed an explicit `celery.type`, so I added it to the values file and made the command path unambiguous.

The symptom pointed at the wrong layer. A valid YAML file can still be operationally incomplete when templates expect semantic fields that are not documented or validated.

## My first rule: identify the stage of failure

```
values.yaml + templates -> rendered manifest -> ArgoCD/Kubernetes
```

## What I checked

I checked Helm template output, missing nested values, conditional branches, required service ports, rendered container commands before changing anything.

## Where the problem actually was

The issue was this: A valid YAML file can still be operationally incomplete when templates expect semantic fields that are not documented or validated. After that, I treated this as a rule: Configuration should have a schema, defaults, or tests so missing semantics fail early and clearly.

## Prevention checklist

- Render the chart before sync.
- Fail early when required values are absent.
- Use defaults only when a default is genuinely safe.
- Keep conditionals shallow and test both branches.
- Treat rendered YAML as a build artifact worth reviewing.
