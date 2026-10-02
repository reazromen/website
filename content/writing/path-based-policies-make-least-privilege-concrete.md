---
title: Path-Based Policies Make Least Privilege Concrete
url: /posts/path-based-policies-make-least-privilege-concrete.html
date: '2026-09-14'
read_time: 1
excerpt: The difference between operator, runtime and backup identities is visible
  in the exact OpenBao paths and capabilities they receive.
topic: security-identity
tags:
- openbao
- policy
- acl
- least-privilege
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: OpenBao Secrets · advanced'
outputs:
- url: /posts/path-based-policies-make-least-privilege-concrete.html
  template: cms/templates/posts/posts--path-based-policies-make-least-privilege-concrete.tpl
  source: cms/templates/posts/posts--path-based-policies-make-least-privilege-concrete.json
---

Least privilege is easy to say and hard to review when permissions are hidden inside application code. OpenBao policies make the boundary declarative.

The current `runtime-read` policy grants read access to production KV data and read/list access to metadata. The operator policy can create, update, delete and patch those application secret paths but does not receive blanket control over auth methods, audit devices or the OpenBao root namespace. The backup policy is narrower still: read the Raft snapshot endpoint and inspect its own token.

These distinctions matter during incidents. A compromised runtime identity should not be able to rotate secrets. A backup automation should not become an application-secret browser. An operator workflow should not silently gain root-equivalent control because one API call was convenient.

I prefer policies that can be read like architecture diagrams. The permitted paths explain the trust boundary without needing to execute the system.

## Engineering evidence

The hserver repository evidence for this note is commit `1f583b4`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
