---
title: Kubernetes Gateway API Is Not Just a New Ingress YAML
url: /posts/kubernetes-gateway-api-not-new-ingress-yaml.html
date: '2023-09-09'
read_time: 9
excerpt: Gateway API changes who owns the network boundary, how routes attach, and
  what a migration has to prove. Treating it as an Ingress syntax upgrade misses the
  important part.
topic: ''
tags:
- kubernetes
- gateway-api
- ingress
- platform-engineering
draft: false
featured: false
language: en
eyebrow: Infrastructure & Networking · systems note
outputs:
- url: /posts/kubernetes-gateway-api-not-new-ingress-yaml.html
  template: cms/templates/posts/posts--kubernetes-gateway-api-not-new-ingress-yaml.tpl
  source: cms/templates/posts/posts--kubernetes-gateway-api-not-new-ingress-yaml.json
---

The easiest way to misunderstand Gateway API is to compare two YAML files.

You put an `Ingress` on the left, an `HTTPRoute` on the right, map `host` to `hostnames`, move some paths around, and conclude that Kubernetes has invented a more verbose way to configure a reverse proxy.

That misses the architectural change. Gateway API is less interesting as a new syntax than as a new ownership model for the traffic boundary.

## Ingress compressed several jobs into one object[#](#ingress-compressed-several-jobs-into-one-object)

Ingress gave applications a portable way to describe basic HTTP routing, but the API stayed deliberately small. Real installations then accumulated annotations for rewrites, timeouts, TLS behavior, load-balancer features, authentication, canaries, and controller-specific switches.

The object looked portable while much of the behavior lived somewhere else.

It also blurred responsibilities. The same application manifest could describe hostnames and paths while indirectly causing infrastructure to provision or reconfigure a shared data plane. Different controllers merged multiple Ingress objects differently because the API did not fully prescribe conflict resolution.

Gateway API makes those boundaries explicit.

```
GatewayClass  -> implementation / infrastructure contract
Gateway       -> listener and traffic-entry ownership
HTTPRoute     -> application routing intent
Service       -> workload destination
```

The important thing in that chain is not the number of CRDs. It is that an infrastructure team can own the Gateway and its listeners while an application team owns the HTTPRoute that is permitted to attach to it.

## Attachment is a contract, not an accident[#](#attachment-is-a-contract-not-an-accident)

An `HTTPRoute` has `parentRefs`. A Gateway listener can constrain which Routes are allowed to attach. Hostnames have to intersect correctly. Cross-namespace relationships use explicit mechanisms such as `ReferenceGrant`.

That means the network edge can finally express a question platform teams already had to answer operationally: who is allowed to publish a route here?

With Ingress, the answer was often hidden in admission policy, namespace conventions, controller flags, or human process. Gateway API moves more of that relationship into the resource model itself.

## The CRDs are part of your platform lifecycle[#](#the-crds-are-part-of-your-platform-lifecycle)

Gateway API resources are custom resources, not native built-in Kubernetes kinds. That means installing a Gateway implementation is not just installing a Deployment. You are also managing API definitions, release channels, controller compatibility, and upgrades.

This is one reason I would not describe migration as “replace Ingress with HTTPRoute.” The cluster now has an additional API lifecycle that has to be owned deliberately.

A useful production checklist is:

- Which Gateway API version and channel are installed?
- Which controller version is conformant with that version?
- Who upgrades the CRDs?
- What happens to Routes when the controller is upgraded first, or the CRDs are upgraded first?
- Which Extended features does the implementation actually support?

The official conformance model matters here. “Supports Gateway API” is too vague; the useful question is which resources, features, and conformance profiles are supported by the controller you are operating.

## Annotations are where migrations stop being mechanical[#](#annotations-are-where-migrations-stop-being-mechanical)

The happy migration demo is a host, a path, and a Service. Production Ingresses are rarely that clean.

They carry controller annotations for redirects, regex matching, buffering, timeouts, header manipulation, source restrictions, authentication, rate limits, sticky sessions, body-size limits, and certificate behavior.

Some map to Gateway API filters or policies. Some map to implementation-specific extension resources. Some need to be redesigned.

So I would inventory behavior, not YAML.

```
Ingress rule
+ annotations
+ controller ConfigMap
+ admission policy
+ TLS automation
+ cloud load-balancer settings
= actual edge behavior
```

If you only convert the first line, the new manifest can validate and still behave differently.

## A safe migration proves two control planes at once[#](#a-safe-migration-proves-two-control-planes-at-once)

There are really two things to validate: Kubernetes object state and data-plane behavior.

Object state means the Route is accepted, references resolve, the listener accepts attachment, and the controller reports the expected Conditions. Data-plane behavior means real requests see the same redirects, TLS chain, headers, routing, retries, timeouts, and failure behavior as before.

I would run both stacks in parallel where the environment allows it. Give the Gateway API path a separate hostname or load-balancer address, replay representative requests, verify status Conditions, then move traffic deliberately.

The migration guide itself is careful about this: converting resources is not the same thing as preparing a live migration.

## The real benefit is organizational[#](#the-real-benefit-is-organizational)

Gateway API can express more networking features, but that is not the part I find most important.

The biggest improvement is that infrastructure ownership and application routing can be separate without being disconnected.

A platform team can own listeners, addresses, certificates, allowed namespaces, and controller lifecycle. An application team can own the hostname/path/backend rules it needs. The attachment between them is visible and machine-checkable.

That is a much stronger model than “put the right annotations on this Ingress and hope everybody agrees what they mean.”

So no, Gateway API is not just the next Ingress YAML. It is Kubernetes admitting that the edge is shared infrastructure and modeling that fact directly.

## Sources and further reading[#](#sources-and-further-reading)

- [Gateway API: Migrating from Ingress](https://gateway-api.sigs.k8s.io/guides/getting-started/migrating-from-ingress/)
- [Kubernetes: Gateway API overview](https://kubernetes.io/docs/concepts/services-networking/gateway/)
- [Gateway API: HTTPRoute reference](https://gateway-api.sigs.k8s.io/reference/api-types/httproute/)
- [Gateway API: Getting started](https://gateway-api.sigs.k8s.io/guides/getting-started/introduction/)
