---
title: Off-Host Encrypted Backups Change the Failure Domain
url: /posts/off-host-encrypted-backups-change-failure-domain.html
date: '2024-03-17'
read_time: 1
excerpt: A backup on the same disk protects against application mistakes better than
  it protects against host or disk loss.
topic: disaster-recovery
tags:
- off-host-backup
- encryption
- dr
- failure-domain
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Backup and DR · advanced'
outputs:
- url: /posts/off-host-encrypted-backups-change-failure-domain.html
  template: cms/templates/posts/posts--off-host-encrypted-backups-change-failure-domain.tpl
  source: cms/templates/posts/posts--off-host-encrypted-backups-change-failure-domain.json
---

Local backups were useful but still shared too much fate with the Mac mini hosting production. Disk failure, theft, catastrophic filesystem damage or destructive host changes could affect both primary state and local recovery copies.

CISA recommends offline or otherwise isolated encrypted backups and regular recovery testing. The important concept is independent failure domains, not simply counting copies. The backup existed without enough failure-domain separation. Redundancy is strongest when the copy does not depend on the same hardware, credentials and runtime path as the original.

The DR workflow creates encrypted recovery sets, pulls them off-host and records verification receipts so the Operations Portal can distinguish recent off-host evidence from local backup state.

Track where each backup lives, how it is encrypted, how credentials are recovered and how recently an independent copy was verified. The concrete hserver evidence is commit b9b9027, so this note is tied to an actual production change rather than a hypothetical failure.
