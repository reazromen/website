---
title: Do Not Leave Decrypted DR Payloads Behind After Verification
url: /posts/do-not-leave-decrypted-dr-payloads-after-verification.html
date: '2024-08-25'
read_time: 1
excerpt: A recovery drill can create a new sensitive-data exposure if decrypted database
  dumps remain on disk by default.
topic: disaster-recovery
tags:
- dr
- plaintext
- data-minimization
- backup
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Backup and DR · advanced'
outputs:
- url: /posts/do-not-leave-decrypted-dr-payloads-after-verification.html
  template: cms/templates/posts/posts--do-not-leave-decrypted-dr-payloads-after-verification.tpl
  source: cms/templates/posts/posts--do-not-leave-decrypted-dr-payloads-after-verification.json
---

The DR verifier decrypted and unpacked recovery data for format checks, then copied database payloads into a persistent drill directory. That was convenient for manual testing but extended the lifetime of plaintext sensitive data.

Verification and artifact retention had been coupled. The workflow needed temporary plaintext to inspect the backup, but did not always need to preserve that plaintext after the check completed. The verifier now removes temporary decrypted data by default and only retains a drill bundle when `HS_DR_KEEP_DRILL_BUNDLE=1` is explicitly requested.

This is data minimization: keep sensitive material only for the duration and purpose required. Security controls should apply to recovery tooling as strongly as they apply to the live database. Use secure temporary directories, restrictive umasks and explicit retention flags. A successful DR test should not leave behind an undocumented second copy of production data. The concrete hserver evidence is commit 886f854, so this note is tied to an actual production change rather than a hypothetical failure.
