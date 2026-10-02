---
title: Why publish technical notes as an onion service?
url: /posts/first-note.html
date: '2026-09-14'
read_time: 1
excerpt: A small engineering blog can be served directly through Tor without opening
  an inbound port on the home router.
topic: engineering-notes
tags:
- tor
- privacy
- systems
draft: false
featured: false
language: en
eyebrow: all
outputs:
- url: /posts/first-note.html
  template: cms/templates/posts/posts--first-note.tpl
  source: cms/templates/posts/posts--first-note.json
---

# Why an onion service?

An onion service gives the site a Tor-native address and lets the server accept visitors without exposing a public inbound web port.

This platform now stores articles in PostgreSQL and serves them through a private application network. The database itself is never published to Tor or the LAN.

## What belongs here

Firmware, networking, VoIP, Linux, radio, protocol experiments, and system-engineering notes.
