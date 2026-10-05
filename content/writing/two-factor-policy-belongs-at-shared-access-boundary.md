---
title: Two-Factor Policy Belongs at the Shared Access Boundary
url: /posts/two-factor-policy-belongs-at-shared-access-boundary.html
date: '2021-05-13'
read_time: 1
excerpt: Putting MFA in front of each application separately creates duplicated policy;
  Authelia gives the protected subdomains one identity boundary.
topic: security-identity
tags:
- authelia
- sso
- mfa
- reverse-proxy
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: Authelia SSO · advanced'
outputs:
- url: /posts/two-factor-policy-belongs-at-shared-access-boundary.html
  template: cms/templates/posts/posts--two-factor-policy-belongs-at-shared-access-boundary.tpl
  source: cms/templates/posts/posts--two-factor-policy-belongs-at-shared-access-boundary.json
---

The hserver dashboards are different applications with different internal authentication models, but the operator access rule is the same: members of the admin group need two-factor authentication before they reach the protected surface.

Authelia lets that rule live at the shared access boundary instead of being reimplemented inside Grafana, Portainer, Komodo, OTA and the other applications. The current configuration is default-deny and explicitly lists the protected domains with `policy: two_factor` for `group:admins`.

That does not remove application authorization. It adds a common outer identity gate. An application can still enforce its own roles, API tokens or object permissions after the user crosses the SSO boundary.

This separation reduces configuration drift. MFA policy is changed once, while application permissions remain owned by the application. It also gives the reverse-proxy layer a clear security responsibility: prove the human session before forwarding a protected request.

## Engineering evidence

The hserver repository evidence for this note is commit `aa114a5`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
