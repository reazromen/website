---
title: What Survives When a Static Site's Origin Goes Offline?
date: '2021-04-18'
draft: false
language: en
url: /posts/bn-static-site-origin-offline.html
topic: web-control-plane
tags:
- cache
- architecture
featured: false
read_time: 2
excerpt: >-
  One attraction of static publishing is that the authoring server may not need to stay
  online for readers to receive already-published files. But the boundary of that independence
  needs to be clear.
editorial_batch: 20261003-100-niches
---

One attraction of static publishing is that the authoring server may not need to stay online for readers to receive already-published files. But the boundary of that independence needs to be clear. HTML and images remaining available does not mean every dynamic feature still works.

A page may depend on an external API, search service, or authentication system. The main files can remain at the edge while those dependencies fail. Works offline therefore needs a definition of which functions are expected to survive.

Think separately about reading, authoring, publishing, and fetching live data. Readers may still access the site while editors cannot publish. That distinction does not hide weakness; it shows which responsibilities were deliberately decoupled.

For me, static delivery is valuable because it separates the fate of the authoring environment from the reading environment. But claims of independence should be limited to what has actually been tested.

Source: [official reference](https://developers.cloudflare.com/pages/).
