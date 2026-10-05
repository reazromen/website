---
title: Why Voiceware Needed More Than Docker Compose Thinking
url: /posts/why-voiceware-needed-more-than-docker-compose-thinking.html
date: '2023-06-25'
read_time: 2
excerpt: The conceptual shift from “start these containers” to declaring desired state
  and independent service lifecycles.
topic: voiceware-engineering
tags:
- voiceware
- docker
- kubernetes
- platform-engineering
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Platform Architecture · deep-dive'
outputs:
- url: /posts/why-voiceware-needed-more-than-docker-compose-thinking.html
  template: cms/templates/posts/posts--why-voiceware-needed-more-than-docker-compose-thinking.tpl
  source: cms/templates/posts/posts--why-voiceware-needed-more-than-docker-compose-thinking.json
---

The interesting part of Voiceware was not the number of YAML files. It was the number of decisions hidden behind those files: what runs separately, what is internal, what is exposed, what Git controls, and how failures are contained.

## The tempting shortcut

I split the runtime into the web app, audio-fork, Celery Beat, high/standard/low workers, ESL, Filebeat, Nginx, and Redis.

## Why it breaks

The failure mode was: Compose-style thinking is excellent for local composition but does not by itself solve drift, reconciliation, rollout ownership, or cluster service discovery. In practice, that kind of mismatch often produces misleading symptoms one layer away from the root cause. A networking-looking problem may start as a selector mismatch; an application-looking problem may actually be an image-resolution failure; a Kubernetes-looking problem may be a Helm render error.

## How I would test it

After that, my rule was: Kubernetes migration is mainly an operational-model change, not a syntax conversion exercise. If I could not check a decision from a rendered manifest, controller status, endpoint list, process command, or workload-specific signal, it was still too vague to operate.

## Rule of thumb

When I work on this area, my practical checks are:

- Render the Helm chart and inspect the concrete manifest before syncing it.
- Check ArgoCD source revision/path and compare desired state with live state.
- Verify dependency reachability from the same network context as the workload.
- Use immutable release identifiers when reproducibility and rollback matter.

For Voiceware, the important lesson is not that one particular YAML shape is universally correct. It is that **Kubernetes migration is mainly an operational-model change, not a syntax conversion exercise.** The broader lesson is that boring, inspectable infrastructure usually outperforms clever infrastructure during incidents.
