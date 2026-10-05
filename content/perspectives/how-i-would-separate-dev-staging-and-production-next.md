---
title: How I Would Separate Dev, Staging, and Production Next
url: /posts/how-i-would-separate-dev-staging-and-production-next.html
date: '2026-04-24'
read_time: 2
excerpt: Turning the current single-destination pattern into an environment promotion
  model.
topic: voiceware-engineering
tags:
- voiceware
- environments
- argocd
- gitops
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Operations & Lessons · deep-dive'
outputs:
- url: /posts/how-i-would-separate-dev-staging-and-production-next.html
  template: cms/templates/posts/posts--how-i-would-separate-dev-staging-and-production-next.tpl
  source: cms/templates/posts/posts--how-i-would-separate-dev-staging-and-production-next.json
---

The architecture question is **turning the current single-destination pattern into an environment promotion model**.

## Start with the boundary, not the tool

In the first pass I kept the environment model simple: ArgoCD pointed at HEAD and deployed into the default namespace.

## Runtime view

```
change -> review -> deploy -> observe -> diagnose -> recover -> document
```

## Responsibilities

For this topic, the relevant responsibility is turning the current single-destination pattern into an environment promotion model. The boundary is good when each side can be described without hand-waving: what it receives, what it produces, what it depends on, and what happens if it disappears.

## Interfaces and failure isolation

I traced this as **change -> review -> deploy -> observe -> diagnose -> recover -> document** and checked change diff, deployment status, product behavior, recovery time, repeatability from clean state at each handoff. That kept the debugging path concrete.

The failure I explicitly design against is: As environments multiply, branch, values, namespace, secret, and promotion differences can become accidental drift. That is why I care about the interface, not only whether both pods are currently green.

## Scaling implications

The signals I would attach to this boundary are change diff, deployment status, product behavior, recovery time, repeatability from clean state.

## Architecture review questions

- Define rollback before the risky change.
- Keep secrets out of plaintext Git.
- Document what is implemented versus what remains a hardening next step.
- Change one layer at a time during migration.
- Review infrastructure by blast radius, not line count.

The design rule I keep is **Choose one explicit environment strategy and automate promotion rather than copying manifests by hand.** Once the boundary is explicit, both automation and debugging get simpler.
