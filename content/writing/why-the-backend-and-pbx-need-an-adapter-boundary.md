---
title: Why the Backend and PBX Need an Adapter Boundary
url: /posts/why-the-backend-and-pbx-need-an-adapter-boundary.html
date: '2026-03-02'
read_time: 1
excerpt: Identity and parental policy should not be embedded inside SIP routing rules.
topic: loup-engineering
tags:
- backend
- pbx-adapter
- architecture
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Product Architecture · advanced'
outputs:
- url: /posts/why-the-backend-and-pbx-need-an-adapter-boundary.html
  template: cms/templates/posts/posts--why-the-backend-and-pbx-need-an-adapter-boundary.tpl
  source: cms/templates/posts/posts--why-the-backend-and-pbx-need-an-adapter-boundary.json
---

I stopped treating this part of LOUP as a black box while working on Why the Backend and PBX Need an Adapter Boundary. The LOUP backend knows users, pairing and approved contacts; the PBX knows registrations, dialogs and media routing. Those are different domains.

An adapter between them can translate approved application state into telephony configuration without making Asterisk the source of truth for product identity. The same separation also keeps the parent app from needing direct knowledge of SIP extensions, RTP ports or PBX internals.

Logs and measurements were used to decide whether the fault lived before or after the boundary, then the smallest falsifiable change was tested. Evidence marker: `backend-pbx-adapter`.

Good boundaries let each system own the data model it understands and exchange only the minimum contract needed for the next layer. The resulting test is small enough to rerun after later changes, which is what turns one successful experiment into engineering evidence.

## Project evidence

LOUP engineering marker: `backend-pbx-adapter`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
