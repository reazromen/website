---
title: A SHA256SUMS File Turns Backup Corruption into a Detectable Failure
url: /posts/sha256sums-turns-backup-corruption-detectable.html
date: '2026-09-14'
read_time: 1
excerpt: Checksums do not replace restore tests, but they catch silent byte changes
  before a disaster forces you to discover them.
topic: disaster-recovery
tags:
- sha256
- backup
- integrity
- checksums
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Backup and DR · intermediate'
outputs:
- url: /posts/sha256sums-turns-backup-corruption-detectable.html
  template: cms/templates/posts/posts--sha256sums-turns-backup-corruption-detectable.tpl
  source: cms/templates/posts/posts--sha256sums-turns-backup-corruption-detectable.json
---

Checksums provide integrity verification for stored artifacts. They are one layer in a recovery chain that should also include format validation and actual restore drills. A backup set can have every expected filename and still contain truncated or modified data. File presence alone therefore gave the operator more confidence than the evidence justified.

Structural validation was present, but content integrity was not. Storage errors, interrupted copies or accidental edits can preserve names while changing bytes.

Backup sets include SHA-256 manifests and the posture check runs `sha256sum -c` before reporting a visible set as healthy. Generate the manifest only after all backup members are closed, store it with the set, and verify it both during routine posture checks and before a restore begins. The concrete hserver evidence is commit f10f5c7, so this note is tied to an actual production change rather than a hypothetical failure.
