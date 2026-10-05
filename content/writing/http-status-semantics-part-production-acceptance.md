---
title: HTTP Status Semantics Are Part of Production Acceptance
url: /posts/http-status-semantics-part-production-acceptance.html
date: '2025-05-19'
read_time: 1
excerpt: A service can be reachable and still be routed through the wrong authentication
  or application layer.
topic: production-engineering
tags:
- http
- acceptance
- ingress
- contract-testing
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Production Acceptance · advanced'
outputs:
- url: /posts/http-status-semantics-part-production-acceptance.html
  template: cms/templates/posts/posts--http-status-semantics-part-production-acceptance.tpl
  source: cms/templates/posts/posts--http-status-semantics-part-production-acceptance.json
---

The OTA public endpoint needed different expected responses for health, invalid machine payloads, unauthorized artifacts and human admin access. A single 'curl succeeded' check could not distinguish correct routing from SSO interception.

Contract tests should verify failure behavior as carefully as success behavior. Negative responses often provide stronger evidence that authentication, validation and routing boundaries are intact. Reachability is weaker than protocol correctness. Each route has an expected status class that identifies which boundary processed the request.

The acceptance script asserts 200 for health, 422 for invalid machine JSON, 401/403/404 for invalid artifact access and 302 for the admin SSO path.

Encode status expectations in version-controlled checks and run them after proxy, tunnel, auth or API changes. The concrete hserver evidence is commit 8940954, so this note is tied to an actual production change rather than a hypothetical failure.
