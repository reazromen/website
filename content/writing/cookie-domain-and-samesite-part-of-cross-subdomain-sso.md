---
title: Cookie Domain and SameSite Policy Are Part of Cross-Subdomain SSO
url: /posts/cookie-domain-and-samesite-part-of-cross-subdomain-sso.html
date: '2025-08-15'
read_time: 1
excerpt: One identity portal can protect many subdomains only if browser cookie scope
  and request behavior match the intended trust boundary.
topic: security-identity
tags:
- authelia
- cookies
- samesite
- sso
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: Authelia SSO · advanced'
outputs:
- url: /posts/cookie-domain-and-samesite-part-of-cross-subdomain-sso.html
  template: cms/templates/posts/posts--cookie-domain-and-samesite-part-of-cross-subdomain-sso.tpl
  source: cms/templates/posts/posts--cookie-domain-and-samesite-part-of-cross-subdomain-sso.json
---

The user sees one login portal and several protected applications, but the browser sees distinct origins such as `auth`, `grafana`, `ops` and `ota` under the same parent domain.

Our Authelia session cookie is scoped to `reazromen.com` and uses `same_site: lax`. Those values are architecture, not cosmetics. Cookie scope defines where the browser is willing to send session material, while SameSite controls how that material participates in cross-site navigation and request contexts.

Making the cookie too narrow breaks the shared SSO experience. Making it unnecessarily broad increases exposure. The correct boundary should match the set of applications intentionally governed by the identity provider.

When debugging SSO redirects I therefore inspect cookie domain, secure origin, browser policy and redirect target together. A healthy Authelia container cannot fix a cookie the browser refuses to send.

## Engineering evidence

The hserver repository evidence for this note is commit `aa114a5`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
