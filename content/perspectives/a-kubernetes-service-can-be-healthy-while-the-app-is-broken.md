---
title: A Kubernetes Service Can Be Healthy While the App Is Broken
url: /posts/a-kubernetes-service-can-be-healthy-while-the-app-is-broken.html
date: '2023-02-27'
read_time: 2
excerpt: A layered method for checking pods, endpoints, ports, and application behavior
  separately.
topic: voiceware-engineering
tags:
- voiceware
- kubernetes
- debugging
- services
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Kubernetes · deep-dive'
outputs:
- url: /posts/a-kubernetes-service-can-be-healthy-while-the-app-is-broken.html
  template: cms/templates/posts/posts--a-kubernetes-service-can-be-healthy-while-the-app-is-broken.tpl
  source: cms/templates/posts/posts--a-kubernetes-service-can-be-healthy-while-the-app-is-broken.json
---

## Symptom

I kept Deployments and Services separate, so process state and network reachability could be checked independently.

The symptom pointed at the wrong layer. “Service exists” is not signal that endpoints are ready or that the process behind them is useful.

## My first rule: identify the stage of failure

```
Deployment -> Pod -> label -> Service selector -> Endpoint -> listening process
```

## What I checked

I checked pod phase and events, Service endpoints, label/selector matches, listener and target ports, external exposure path before changing anything.

I traced this as **Deployment -> Pod -> label -> Service selector -> Endpoint -> listening process** and checked pod phase and events, Service endpoints, label/selector matches, listener and target ports, external exposure path at each handoff. That kept the debugging path concrete.

## Where the problem actually was

At the core, it was “Service exists” is not signal that endpoints are ready or that the process behind them is useful. The useful lesson was simple: Debug from resource state to endpoints to transport to application protocol instead of jumping randomly between logs.

## Prevention checklist

- List endpoints; a Service with zero endpoints is not routing anywhere.
- Trace port -> targetPort -> process listener.
- Separate internal service discovery from external exposure.
- Inspect pod events before application logs.
- Compare Service selectors with pod labels.
