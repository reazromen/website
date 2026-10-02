---
title: An Operations Portal Should Not Become a Web Terminal
url: /posts/operations-portal-should-not-become-web-terminal.html
date: '2026-09-14'
read_time: 1
excerpt: Convenient arbitrary shell access would collapse the separation between reviewed
  operations and unrestricted host control.
topic: web-control-plane
tags:
- ops-portal
- security
- automation
- least-privilege
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Safe Automation · advanced'
outputs:
- url: /posts/operations-portal-should-not-become-web-terminal.html
  template: cms/templates/posts/posts--operations-portal-should-not-become-web-terminal.tpl
  source: cms/templates/posts/posts--operations-portal-should-not-become-web-terminal.json
---

The hserver Operations Portal needed to execute real maintenance tasks without turning a browser session into root shell access. A generic terminal would have been easy to build and difficult to constrain safely.

Human convenience and operational control were pulling in opposite directions. Arbitrary commands bypass code review, parameter validation, audit semantics and the least-privilege runner model. The portal exposes only reviewed job definitions from Git, while a dedicated host runner re-opens those definitions and executes fixed commands outside the web containers.

This is command whitelisting and privilege separation. High-value automation should expose capabilities, not a general interpreter, so the attack surface matches the intended operational actions. Keep arbitrary shell input out of the API, require new operations to arrive as reviewed definitions, and treat any request for a generic execution primitive as a security-design change. The concrete hserver evidence is commit 9e6f8a5, so this note is tied to an actual production change rather than a hypothetical failure.
