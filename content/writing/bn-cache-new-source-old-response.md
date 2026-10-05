---
title: The Source Changed, So Why Are People Still Seeing the Old Page?
date: '2025-03-22'
draft: false
language: en
url: /posts/bn-cache-new-source-old-response.html
topic: web-control-plane
tags:
- cache
- deployment
featured: false
read_time: 2
excerpt: >-
  A source-code change can make a release feel finished, but several deployment and cache
  layers may still sit between the repository and a user's browser. A new file, a newly
  published artifact, and a newly observed response are three different pieces of evidence.
editorial_batch: 20261003-100-niches
---

A source-code change can make a release feel finished, but several deployment and cache layers may still sit between the repository and a user's browser. A new file, a newly published artifact, and a newly observed response are three different pieces of evidence.

Suppose the origin has the new page but the edge still has an older copy. Or the edge may already have the new HTML while the browser is still running an old script. Those are different failure locations and require different fixes. Re-deploying again does not, by itself, tell you where the stale response came from.

It helps to expose a build identity and inspect response headers during verification. Versioned static asset names make old and new artifacts easier to distinguish. HTML cache policy should also match how quickly that HTML needs to change.

The final test of a release should therefore happen not only in source control but along the delivery path to the user. A cache is not inherently wrong; it is a copy from a particular point in time. Problems shrink when the rules for replacing that copy are explicit.

Source: [official reference](https://developers.cloudflare.com/cache/concepts/revalidation/).
