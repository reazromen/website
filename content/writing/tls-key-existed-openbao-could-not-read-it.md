---
title: The TLS Key Existed, but OpenBao Still Could Not Read It
url: /posts/tls-key-existed-openbao-could-not-read-it.html
date: '2026-09-14'
read_time: 2
excerpt: A file can have the right contents and still be unusable when directory traversal
  or group permissions are wrong.
topic: security-secrets
tags:
- openbao
- tls
- permissions
- linux
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Permissions and Secrets · advanced'
outputs:
- url: /posts/tls-key-existed-openbao-could-not-read-it.html
  template: cms/templates/posts/posts--tls-key-existed-openbao-could-not-read-it.tpl
  source: cms/templates/posts/posts--tls-key-existed-openbao-could-not-read-it.json
---

OpenBao had the expected TLS key on disk, yet the service could not consume it reliably at runtime. Checking the file alone made the failure look mysterious because the path existed and the certificate material was valid.

The problem was Unix path traversal and ownership, not cryptography. A process needs execute permission on each parent directory and enough file permission on the final object, so an unreadable path can fail even when the key itself looks correct from a root shell. We separated the secret file permission from the directory permission: the TLS directory became traversable by the intended service context, the private key stayed group-readable rather than world-readable, and public certificates remained broadly readable.

This is classic boundary-first debugging: verify identity, path traversal, ownership and effective permissions before changing the application. OWASP least-privilege guidance also favors granting the narrowest access needed instead of weakening the entire tree. Deployment scripts now enforce the required modes explicitly so a redeploy cannot silently recreate the same mismatch. Permission checks belong in acceptance tests because they are part of the runtime contract, not a post-install detail. The concrete hserver evidence is commit 7843fb3, so this note is tied to an actual production change rather than a hypothetical failure.
