---
title: The Runner Is a Privilege-Separation Boundary, Not Just a Worker
url: /posts/runner-privilege-separation-boundary.html
date: '2026-09-14'
read_time: 1
excerpt: Keeping host execution outside the portal containers limits what a web compromise
  can directly control.
topic: security-secrets
tags:
- runner
- privilege-separation
- docker
- security
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Safe Automation · advanced'
outputs:
- url: /posts/runner-privilege-separation-boundary.html
  template: cms/templates/posts/posts--runner-privilege-separation-boundary.tpl
  source: cms/templates/posts/posts--runner-privilege-separation-boundary.json
---

The portal containers intentionally do not receive the Docker socket, root filesystem mounts or root SSH keys. Yet some approved operations still need host-level observation or controlled execution.

Privilege separation reduces blast radius by splitting trust domains. A web compromise should not automatically become unrestricted host execution. Putting host power inside the web application would combine Internet-facing parsing, authentication, business logic and privileged execution in one compromise domain.

A dedicated systemd runner identity claims reviewed jobs, reads narrowly scoped secrets and returns bounded results while the API remains separated from direct host control.

Keep the runner interface narrow, rotate its token, validate its ACLs and resist convenience features that move Docker socket or root credentials back into the portal container. The concrete hserver evidence is commit 8f76eb2, so this note is tied to an actual production change rather than a hypothetical failure.
