---
title: Why 0600 Was Too Strict for a Containerized Private Key
url: /posts/why-0600-was-too-strict-for-containerized-private-key.html
date: '2026-09-14'
read_time: 1
excerpt: The strictest-looking file mode is not automatically the safest usable mode
  when a non-root service must read the key.
topic: security-secrets
tags:
- linux
- containers
- tls
- least-privilege
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Permissions and Secrets · advanced'
outputs:
- url: /posts/why-0600-was-too-strict-for-containerized-private-key.html
  template: cms/templates/posts/posts--why-0600-was-too-strict-for-containerized-private-key.tpl
  source: cms/templates/posts/posts--why-0600-was-too-strict-for-containerized-private-key.json
---

A private key set to mode 0600 looked secure, but the container process was intentionally not running as root. The result was a secure file that the intended service identity could not read, which is still an availability failure. Security had been reduced to a numeric mode instead of an access model. The correct question was which principal must read the key, which group should represent that trust boundary, and which principals must remain excluded.

The key was changed to 0640 with controlled group ownership while the containing directory was limited to 0750. That preserved confidentiality while allowing the production service to start without root privileges.

For every secret mount, the service record should document expected UID, GID, directory mode and file mode. A deployment verifier can then test effective access using the same identity that the service uses. Least privilege means sufficient privilege, not zero privilege. File ownership, supplemental groups and container UID/GID mapping need to be designed together so the application can perform its required operation and nothing more. The concrete hserver evidence is commit 7843fb3, so this note is tied to an actual production change rather than a hypothetical failure.
