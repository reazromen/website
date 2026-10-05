---
title: A Clean Checkout Must Contain Every Local Build and Config Reference
url: /posts/clean-checkout-must-contain-every-local-reference.html
date: '2022-07-26'
read_time: 1
excerpt: Infrastructure source is incomplete if Compose points at files that only
  exist on the current server.
topic: production-engineering
tags:
- reproducibility
- compose
- ci
- git
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Production Acceptance · advanced'
outputs:
- url: /posts/clean-checkout-must-contain-every-local-reference.html
  template: cms/templates/posts/posts--clean-checkout-must-contain-every-local-reference.tpl
  source: cms/templates/posts/posts--clean-checkout-must-contain-every-local-reference.json
---

The production-readiness review found that the observability stack referenced required local files or directories that were not all present in Git. A normal `docker compose up` on the current host could still work because those files existed live. The repository did not fully capture the build graph. Runtime residue was masking a missing source dependency.

The stack was marked blocked for destructive redeploy and CI requirements were added to prove that managed Compose definitions render with all local references available from a clean checkout.

Run clean-checkout validation in CI and periodically rebuild noncritical copies from scratch so missing local assumptions surface before disaster recovery. Reproducibility means another machine can reconstruct the release from declared inputs. Hidden host files violate that property even if they are harmless during day-to-day operation. The concrete hserver evidence is commit 9d36c75, so this note is tied to an actual production change rather than a hypothetical failure.
