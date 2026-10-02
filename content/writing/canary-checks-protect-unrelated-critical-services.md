---
title: Canary Checks Should Protect Unrelated Critical Services Too
url: /posts/canary-checks-protect-unrelated-critical-services.html
date: '2026-09-14'
read_time: 1
excerpt: A successful target deployment is not a full success if the change quietly
  damages another workload on the same host.
topic: production-engineering
tags:
- canary
- blast-radius
- voip
- deployment
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Production Acceptance · advanced'
outputs:
- url: /posts/canary-checks-protect-unrelated-critical-services.html
  template: cms/templates/posts/posts--canary-checks-protect-unrelated-critical-services.tpl
  source: cms/templates/posts/posts--canary-checks-protect-unrelated-critical-services.json
---

Change-window preflight and production acceptance include critical sentinel workloads and host posture in addition to the target application's own health checks.

hserver is a shared production machine: OTA, Operations, observability, publishing and VoIP stacks coexist. A change to networking, authentication or resource limits can affect services that were not part of the deployment plan. Acceptance scoped only to the changed service would miss collateral regressions on shared dependencies and host resources.

Canary thinking applies to infrastructure changes as well as application versions. Validate both intended improvement and absence of unacceptable side effects.

Maintain a small set of critical cross-service invariants—VoIP sentinels, disk headroom, backup freshness, auth reachability—and run them before and after every production change. The concrete hserver evidence is commit 9e6f8a5, so this note is tied to an actual production change rather than a hypothetical failure.
