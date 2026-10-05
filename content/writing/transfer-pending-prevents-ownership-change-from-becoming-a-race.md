---
title: Transfer Pending Prevents Ownership Change from Becoming a Race
url: /posts/transfer-pending-prevents-ownership-change-from-becoming-a-race.html
date: '2022-04-18'
read_time: 1
excerpt: Moving a device between accounts needs an intermediate state while old and
  new authority are resolved.
topic: loup-engineering
tags:
- device-transfer
- ownership
- state-machine
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Provisioning & Backend · advanced'
outputs:
- url: /posts/transfer-pending-prevents-ownership-change-from-becoming-a-race.html
  template: cms/templates/posts/posts--transfer-pending-prevents-ownership-change-from-becoming-a-race.tpl
  source: cms/templates/posts/posts--transfer-pending-prevents-ownership-change-from-becoming-a-race.json
---

I stopped treating this part of LOUP as a black box while working on Transfer Pending Prevents Ownership Change from Becoming a Race. LOUP includes transfer\_pending rather than switching ownership in one unobservable database update.

An intermediate state can freeze sensitive actions, require approval or cleanup, rotate credentials and make the new owner relationship explicit before returning the unit to active. It also provides a recovery point if the transfer process is interrupted.

Logs and measurements were used to decide whether the fault lived before or after the boundary, then the smallest falsifiable change was tested. Evidence marker: `transfer-pending`.

Multi-step ownership changes deserve their own state. Atomic-looking UI actions often hide several security-sensitive operations. The resulting test is small enough to rerun after later changes, which is what turns one successful experiment into engineering evidence.

## Project evidence

LOUP engineering marker: `transfer-pending`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
