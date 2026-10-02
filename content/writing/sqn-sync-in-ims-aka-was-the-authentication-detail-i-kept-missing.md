---
title: SQN Sync in IMS AKA Was the Authentication Detail I Kept Missing
url: /posts/sqn-sync-in-ims-aka-was-the-authentication-detail-i-kept-missing.html
date: '2026-09-14'
read_time: 2
excerpt: IMS AKA stopped looking like a simple password check once I traced the sequence
  number and resynchronization path.
topic: mobile-networks
tags:
- ims
- aka
- sqn
- authentication
draft: false
featured: false
language: en
eyebrow: 2023 Mobile and 5G Notes · advanced
outputs:
- url: /posts/sqn-sync-in-ims-aka-was-the-authentication-detail-i-kept-missing.html
  template: cms/templates/posts/posts--sqn-sync-in-ims-aka-was-the-authentication-detail-i-kept-missing.tpl
  source: cms/templates/posts/posts--sqn-sync-in-ims-aka-was-the-authentication-detail-i-kept-missing.json
---

The IMS authentication flow looked straightforward until I paid attention to the sequence number. I had been treating AKA as a challenge-response exchange: the network sends a challenge, the UE calculates a response, and authentication either passes or fails. That model is incomplete because both sides also maintain freshness state. The sequence number, SQN, is part of that state and it can get out of sync.

In the normal path the network obtains an authentication vector and the UE validates the AUTN using its secret key and the expected sequence range. If the cryptographic checks are good and the sequence number is acceptable, the UE can produce the response and continue registration. The interesting failure appears when the network and UE disagree about where the sequence should be. The credentials can be correct and the subscriber can still fail authentication.

The resynchronization mechanism finally made this clear. When the UE detects that the network sequence is stale, it can return an authentication failure containing AUTS. That is not the same as a generic bad-password failure. AUTS lets the home side recover a usable sequence relationship without exposing the long-term key. Following that path through the IMS REGISTER exchange made the failure much easier to classify.

The practical lesson was to stop reading every 401/403-style outcome as the same thing. In an IMS trace I now look at the AKA parameters, the failure cause, whether AUTS appears, and what the HSS or authentication backend does next. A subscriber that repeatedly enters resynchronization points to a different problem than one producing a wrong response.

This was also a good reminder that telecom authentication is distributed state. The SIM or ISIM, IMS core and subscriber database all participate. A packet capture at the P-CSCF shows only part of the story; Diameter logs and subscriber state can be just as important. Once I treated SQN as state rather than a mysterious field, IMS AKA became much easier to reason about.
