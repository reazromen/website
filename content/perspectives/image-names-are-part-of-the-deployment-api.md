---
title: Image Names Are Part of the Deployment API
url: /posts/image-names-are-part-of-the-deployment-api.html
date: '2024-08-28'
read_time: 2
excerpt: Why repository, tag, and pull policy deserve review like any other runtime
  contract.
topic: voiceware-engineering
tags:
- voiceware
- containers
- helm
- releases
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Containers · deep-dive'
outputs:
- url: /posts/image-names-are-part-of-the-deployment-api.html
  template: cms/templates/posts/posts--image-names-are-part-of-the-deployment-api.tpl
  source: cms/templates/posts/posts--image-names-are-part-of-the-deployment-api.json
---

I learned more from the small Voiceware failures than from the clean architecture diagram. The final repository looks organized, but the useful engineering story is in the boundaries that had to be discovered and corrected.

The architecture question is **why repository, tag, and pull policy deserve review like any other runtime contract**.

## Start with the boundary, not the tool

I exposed image repository, tag, and pull policy through Helm values for each service.

## Runtime view

```
source -> image build -> registry identity -> Helm value -> node runtime pull -> container start
```

## Responsibilities

For this topic, the relevant responsibility is why repository, tag, and pull policy deserve review like any other runtime contract. The boundary is good when each side can be described without hand-waving: what it receives, what it produces, what it depends on, and what happens if it disappears.

## Interfaces and failure isolation

The failure I explicitly design against is: A chart can be perfectly templated but still deploy the wrong artifact if image identity is vague. That is why I care about the interface, not only whether both pods are currently green.

## Scaling implications

The signals I would attach to this boundary are image reference, registry reachability, node pull events, image digest, running container image ID.

## Architecture review questions

- Promote the same built artifact across environments.
- Use an explicit registry/repository path.
- Prefer immutable tags or digests for releases.
- Verify the node can pull the artifact.
- Do not pair mutable latest tags with assumptions about reproducibility.

The design rule I keep is **Treat image coordinates as immutable inputs to a release, not incidental strings.** That lesson has been more reusable for me than any particular YAML pattern.
