---
title: Image Storage Growth Is Different from Runtime Data Growth
url: /posts/image-storage-growth-different-from-runtime-data.html
date: '2020-11-22'
read_time: 1
excerpt: Docker images can quietly accumulate through repeated deployments even when
  application volumes and databases remain stable.
topic: observability-monitoring
tags:
- docker-images
- disk-usage
- capacity
- cleanup
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Storage & I/O · advanced'
outputs:
- url: /posts/image-storage-growth-different-from-runtime-data.html
  template: cms/templates/posts/posts--image-storage-growth-different-from-runtime-data.tpl
  source: cms/templates/posts/posts--image-storage-growth-different-from-runtime-data.json
---

Docker images can quietly accumulate through repeated deployments even when application volumes and databases remain stable. The monitoring mistake would be to read one metric in isolation. `Docker image storage bytes and image count` is useful because it narrows the question, and image cache growth consumes root filesystem capacity but has different remediation than persistent data growth because old images are usually rebuildable.

In software operations this falls under capacity classification. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Monitor images separately from volumes and writable layers so cleanup automation never confuses disposable artifacts with state that needs backup. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `218300b`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
