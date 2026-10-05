---
title: Two OpenBao Services on One Host Are Still Not High Availability
url: /posts/raft-snapshot-is-backup-one-node-not-ha.html
date: '2026-08-10'
read_time: 1
excerpt: Separating the main secret authority from the Transit seal service improves
  trust boundaries, but both still share the same physical host failure domain.
topic: security-identity
tags:
- openbao
- transit
- raft
- high-availability
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: OIDC, Trust & Recovery · advanced'
outputs:
- url: /posts/raft-snapshot-is-backup-one-node-not-ha.html
  template: cms/templates/posts/posts--raft-snapshot-is-backup-one-node-not-ha.tpl
  source: cms/templates/posts/posts--raft-snapshot-is-backup-one-node-not-ha.json
---

The updated CSL topology now has two OpenBao services with different jobs. The main service owns application secrets, policies, AppRole and audit state. The seal service owns only the Transit key used to wrap and unwrap the main OpenBao root key.

That separation is valuable because compromise of one interface does not automatically grant every capability of the other. The seal API is not host-published, the Transit token is narrowly scoped, and the main service can restart and auto-unseal without an operator typing key material.

It is still not high availability. Both services and both Raft stores currently live on the same Mac mini. A power, disk, kernel or host-network failure can remove both at once. Two containers are two security roles, not two independent availability zones.

Raft snapshots and encrypted off-host recovery prove recoverability. Real HA requires independent nodes and quorum across independent failure domains. The architecture document is explicit about that distinction so convenience is not confused with resilience.

## Engineering evidence

The hserver repository evidence for this note is commit `04e75703`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
