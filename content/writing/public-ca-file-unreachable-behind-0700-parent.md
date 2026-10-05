---
title: A Public CA File Can Be Unreachable Behind a 0700 Parent Directory
url: /posts/public-ca-file-unreachable-behind-0700-parent.html
date: '2024-01-29'
read_time: 1
excerpt: Publishing a certificate means every directory in its path must support the
  intended reader, even if neighboring secrets remain private.
topic: security-secrets
tags:
- tls
- linux-permissions
- ca
- trust
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Authentication and Ingress · intermediate'
outputs:
- url: /posts/public-ca-file-unreachable-behind-0700-parent.html
  template: cms/templates/posts/posts--public-ca-file-unreachable-behind-0700-parent.tpl
  source: cms/templates/posts/posts--public-ca-file-unreachable-behind-0700-parent.json
---

Filesystem trees should reflect data classification. Public certificates and private keys have different confidentiality requirements even when they share an administrative namespace. The exported Caddy CA certificates were intentionally public material, but `/etc/hserver` had mode 0700. Non-root readers could not traverse the parent path to reach files that were themselves safe to distribute.

The directory policy treated the whole tree as secret even though it contained mixed-sensitivity children. Parent traversal overrode the child file's intended visibility.

The parent became root-owned 0755 while secret child directories retained restrictive permissions. Public trust material could then be read without broadening access to private state. Separate public and private subtrees where practical, and test access using an unprivileged identity rather than assuming child modes determine reachability. The concrete hserver evidence is commit 2aead37, so this note is tied to an actual production change rather than a hypothetical failure.
