---
title: Least-Privilege Backup Receipts Let Operators Verify Without Reading the Backups
url: /posts/least-privilege-backup-receipts-operator-verification.html
date: '2020-08-02'
read_time: 1
excerpt: Operators need evidence that backups succeeded without necessarily gaining
  access to the protected data itself.
topic: disaster-recovery
tags:
- receipts
- least-privilege
- backup
- ops-portal
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Backup and DR · advanced'
outputs:
- url: /posts/least-privilege-backup-receipts-operator-verification.html
  template: cms/templates/posts/posts--least-privilege-backup-receipts-operator-verification.tpl
  source: cms/templates/posts/posts--least-privilege-backup-receipts-operator-verification.json
---

The safe operator job needed to report backup posture while the underlying backup directories remained protected. Granting the runner broad read access would have solved observability by weakening the data boundary.

This is separation of evidence from sensitive payload. Least privilege is easier when systems publish purpose-built attestations rather than forcing monitoring identities to inspect raw protected state. The monitoring principal needed assurance metadata, not backup contents. Those are different information classes and should not share the same access requirement.

Root-managed backup processes write limited success receipts into a location the operator checker can read. The receipt contains completion time and set metadata without exposing database dumps or secret-bearing archives.

Keep receipts minimal, tamper-resistant through ownership and validation, and cross-check them periodically against full privileged restore verification so metadata cannot drift from reality. The concrete hserver evidence is commit f199743, so this note is tied to an actual production change rather than a hypothetical failure.
