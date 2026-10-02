---
title: Cookie Domain and SameSite Settings Are Part of SSO Architecture
url: /posts/cookie-domain-samesite-part-of-sso-architecture.html
date: '2026-09-14'
read_time: 1
excerpt: Cross-subdomain authentication only works predictably when cookie scope and
  redirect boundaries match the domain design.
topic: web-control-plane
tags:
- cookies
- samesite
- authelia
- sso
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Authentication and Ingress · advanced'
outputs:
- url: /posts/cookie-domain-samesite-part-of-sso-architecture.html
  template: cms/templates/posts/posts--cookie-domain-samesite-part-of-sso-architecture.tpl
  source: cms/templates/posts/posts--cookie-domain-samesite-part-of-sso-architecture.json
---

Authentication cookies should be scoped to the smallest domain set that satisfies the architecture and should use deliberate SameSite behavior. Browser cookie policy is part of the security boundary, not frontend trivia. The hserver dashboards live on multiple `reazromen.com` subdomains behind one authentication portal. Session behavior depends on whether the browser sends the right cookie across those protected origins.

Cookie scope is a routing rule for credentials. A too-narrow domain breaks SSO, while an unnecessarily broad or permissive cookie scope increases exposure.

The Authelia configuration uses the reviewed parent domain, `same_site: lax`, the canonical authentication URL and explicit redirection defaults for the protected dashboard family. Test real browser flows across every protected subdomain after auth changes, including fresh login, remembered login, logout and redirect back to the original application. The concrete hserver evidence is commit aa114a5, so this note is tied to an actual production change rather than a hypothetical failure.
