---
title: One Missing Semicolon Broke HTML Escaping in the Command Center
url: /posts/missing-semicolon-broke-html-escaping-command-center.html
date: '2023-11-04'
read_time: 1
excerpt: Tiny output-encoding defects matter more in admin surfaces because they render
  operational data from many sources.
topic: web-control-plane
tags:
- html-escaping
- xss
- frontend
- ops-portal
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Safe Automation · intermediate'
outputs:
- url: /posts/missing-semicolon-broke-html-escaping-command-center.html
  template: cms/templates/posts/posts--missing-semicolon-broke-html-escaping-command-center.tpl
  source: cms/templates/posts/posts--missing-semicolon-broke-html-escaping-command-center.json
---

The entity was corrected to `&quot;` and the regression was committed independently rather than bundled into unrelated UI work. The Command Center escape helper encoded double quotes as `&quot` without the terminating semicolon. It was a one-character regression inside a compact JavaScript helper used across operator-rendered values. Security-sensitive encoding logic had become compressed enough that a small typo was hard to see in review. The UI aggregates service, request and audit data, so output encoding is not cosmetic.

Output encoding should use well-tested primitives and receive direct tests. Admin interfaces are still web applications and must treat operational text as untrusted display data.

Avoid clever minified helper code in source, add representative escaping tests and keep security fixes small enough that reviewers can verify the exact change. The concrete hserver evidence is commit 54279de, so this note is tied to an actual production change rather than a hypothetical failure.
