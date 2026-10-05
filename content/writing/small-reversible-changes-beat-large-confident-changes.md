---
title: Small Reversible Changes Beat Large Confident Changes
url: /posts/small-reversible-changes-beat-large-confident-changes.html
date: '2023-08-25'
read_time: 1
excerpt: Reducing change size lowers diagnosis time and makes rollback a practical
  control instead of a theoretical option.
topic: devops-culture
tags:
- deployment
- rollback
- change-size
draft: false
featured: false
language: en
eyebrow: 'DevOps Culture: Delivery & Reliability · advanced'
outputs:
- url: /posts/small-reversible-changes-beat-large-confident-changes.html
  template: cms/templates/posts/posts--small-reversible-changes-beat-large-confident-changes.tpl
  source: cms/templates/posts/posts--small-reversible-changes-beat-large-confident-changes.json
---

Large changes feel efficient because many improvements move together, but they create a wide search space when something fails. Small changes preserve causality.

The hserver workflow increasingly separates authentication, monitoring, backup and publishing changes into reviewed units with independent acceptance. LOUP firmware experiments also use known-good baselines and A/B variants instead of changing the entire audio pipeline at once.

This is risk reduction through batch size. A reversible change can be tested quickly, observed clearly and undone without reconstructing the previous system from memory.

Speed comes from shortening the feedback loop, not from maximizing how much code crosses the boundary at once, because smaller batches preserve causality and rollback options.

## Engineering evidence

Repository/project evidence for this note: `fa3c478`. The point is the operating model behind the change, not the commit number itself.
