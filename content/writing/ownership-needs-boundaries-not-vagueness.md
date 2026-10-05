---
title: Ownership Needs Boundaries, Not Vagueness
url: /posts/ownership-needs-boundaries-not-vagueness.html
date: '2022-06-05'
read_time: 1
excerpt: Shared responsibility works only when teams also know which decisions they
  actually own.
topic: devops-culture
tags:
- ownership
- raci
- architecture
draft: false
featured: false
language: en
eyebrow: 'DevOps Culture: Ownership & Collaboration · advanced'
outputs:
- url: /posts/ownership-needs-boundaries-not-vagueness.html
  template: cms/templates/posts/posts--ownership-needs-boundaries-not-vagueness.tpl
  source: cms/templates/posts/posts--ownership-needs-boundaries-not-vagueness.json
---

“Everyone owns production” can become another way of saying nobody knows who decides. Useful ownership has explicit domains and clear escalation paths.

On hserver, source-ownership records distinguish Git-controlled configuration from runtime state and secrets. In LOUP, firmware stays under LOUP control while Minewing owns hardware, mechanical, RF, acoustic and factory execution within reviewed interfaces.

The cultural principle is shared outcomes with bounded authority. Teams collaborate across the boundary without erasing technical accountability or making every decision everybody’s job.

Good ownership reduces waiting because people know which changes they can make, which contracts they must respect and where review is required.

## Engineering evidence

Repository/project evidence for this note: `source-ownership`. The point is the operating model behind the change, not the commit number itself.
