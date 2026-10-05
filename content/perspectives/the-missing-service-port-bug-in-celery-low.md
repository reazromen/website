---
title: The Missing service.port Bug in celery-low
url: /posts/the-missing-service-port-bug-in-celery-low.html
date: '2022-06-16'
read_time: 1
excerpt: Why one absent value can break an otherwise familiar chart pattern.
topic: voiceware-engineering
tags:
- voiceware
- helm
- celery
- debugging
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Helm · deep-dive'
outputs:
- url: /posts/the-missing-service-port-bug-in-celery-low.html
  template: cms/templates/posts/posts--the-missing-service-port-bug-in-celery-low.tpl
  source: cms/templates/posts/posts--the-missing-service-port-bug-in-celery-low.json
---

## Symptom

I hit this on `celery-low`: its values were missing `service.port`, so I added the missing service contract.

The symptom pointed at the wrong layer. Copying a chart pattern without copying its required value contract produces failures that look like template problems but are really configuration-schema problems.

## My first rule: identify the stage of failure

```
values.yaml + templates -> rendered manifest -> ArgoCD/Kubernetes
```

## What I checked

I checked Helm template output, missing nested values, conditional branches, required service ports, rendered container commands before changing anything.

## Where the problem actually was

What this came down to was this: Copying a chart pattern without copying its required value contract produces failures that look like template problems but are really configuration-schema problems. From that I kept one rule: Every reusable chart pattern needs an explicit set of required values and a validation path.

## Prevention checklist

- Treat rendered YAML as a build artifact worth reviewing.
- Render the chart before sync.
- Fail early when required values are absent.
- Use defaults only when a default is genuinely safe.
- Keep conditionals shallow and test both branches.
