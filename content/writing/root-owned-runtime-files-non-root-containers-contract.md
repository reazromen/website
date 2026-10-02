---
title: Root-Owned Runtime Files and Non-Root Containers Need an Explicit Contract
url: /posts/root-owned-runtime-files-non-root-containers-contract.html
date: '2026-09-14'
read_time: 1
excerpt: Dropping container privileges is only safe when mounts, ownership and startup
  scripts are designed for the new identity.
topic: security-secrets
tags:
- docker
- uid
- gid
- permissions
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Permissions and Secrets · advanced'
outputs:
- url: /posts/root-owned-runtime-files-non-root-containers-contract.html
  template: cms/templates/posts/posts--root-owned-runtime-files-non-root-containers-contract.tpl
  source: cms/templates/posts/posts--root-owned-runtime-files-non-root-containers-contract.json
---

We moved permission setup into deployment code, used group-readable secrets where necessary, and kept public material separate from private material. The service starts with only the rights it needs.

Several hserver services intentionally run as non-root while their certificates, configuration and secret files are provisioned by root on the host. The design is secure only if the crossing point between those identities is deliberate. A common failure pattern is to harden the process identity without hardening the file-ownership model at the same time. The result alternates between permission-denied outages and overly broad chmod fixes.

Privilege dropping is a system property, not one Compose field. Effective UID/GID, bind mounts, parent directory traversal, secret rotation and backup/restore ownership all need to agree.

Acceptance checks should run from the service identity and verify actual read/write requirements. That catches permission drift before a restart converts it into an outage. The concrete hserver evidence is commit 7843fb3, so this note is tied to an actual production change rather than a hypothetical failure.
