---
title: The Execute Bit on a Directory Is Really a Path Permission
url: /posts/directory-execute-bit-is-path-permission.html
date: '2024-09-20'
read_time: 1
excerpt: A protected parent directory can block a perfectly readable child file because
  directory execute controls traversal.
topic: linux-homelab
tags:
- linux
- acl
- permissions
- debugging
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Permissions and Secrets · intermediate'
outputs:
- url: /posts/directory-execute-bit-is-path-permission.html
  template: cms/templates/posts/posts--directory-execute-bit-is-path-permission.tpl
  source: cms/templates/posts/posts--directory-execute-bit-is-path-permission.json
---

This is a good example of capability decomposition: separate traverse, list, read and write instead of solving every permission error with broader ownership. It also fits least-privilege access-control design. The ops runner had a readable credential file but still failed to open it through the protected secrets hierarchy. From the file listing, the permission looked correct; from the process point of view, the path was inaccessible.

On Linux, directory execute permission means traversal. The runner needed permission to cross the protected parent without gaining permission to list or read unrelated secrets, which is a different requirement from granting read access to the file itself.

We added a narrow traverse-only ACL on the parent path and kept the secret directory and credential file restrictive. That gave the runner exactly the path capability it needed without exposing sibling content. The provisioning code now establishes the ACL as part of runner enrollment and CI validates the invariant. Reproducible permissions are safer than one-time manual chmod commands that disappear from operational memory. The concrete hserver evidence is commit 8f76eb2, so this note is tied to an actual production change rather than a hypothetical failure.
