---
title: A Clean Checkout Is the Real Test of Infrastructure Reproducibility
url: /posts/clean-checkout-real-test-infrastructure-reproducibility.html
date: '2024-08-16'
read_time: 1
excerpt: Live files that are absent from Git are technical debt even when the service
  is currently healthy.
topic: production-engineering
tags:
- gitops
- observability
- recovery
- configuration
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Reproducibility · advanced'
outputs:
- url: /posts/clean-checkout-real-test-infrastructure-reproducibility.html
  template: cms/templates/posts/posts--clean-checkout-real-test-infrastructure-reproducibility.tpl
  source: cms/templates/posts/posts--clean-checkout-real-test-infrastructure-reproducibility.json
---

The service was explicitly marked BLOCKED for destructive redeploy until the exact live configuration could be recovered into Git. That prevented a well-intentioned cleanup from destroying an environment that could not yet be recreated.

The production-readiness audit found an uncomfortable state: the observability runtime existed and worked, but parts of the Compose build, provisioning or configuration tree required for a clean redeploy were absent from the authoritative source. Operational success had been mistaken for reproducibility. The live host contained knowledge that the repository did not, so the system could not be trusted to survive a destructive rebuild.

This is configuration drift and source-of-truth integrity. OpenGitOps describes drift as divergence between actual and desired state; a missing desired-state definition is an even stronger warning because reconciliation has nothing complete to converge toward.

Acceptance should include a clean-checkout reconstruction test for every managed stack. A running container is runtime evidence, not proof that its source definition is complete. The concrete hserver evidence is commit 9d36c75, so this note is tied to an actual production change rather than a hypothetical failure.
