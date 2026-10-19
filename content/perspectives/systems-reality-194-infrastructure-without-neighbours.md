---
title: "Infrastructure Without Neighbours"
date: '2026-10-20'
draft: false
language: en
url: /posts/systems-reality-194-infrastructure-without-neighbours.html
topic: technology-and-systems
tags:
- infrastructure
- software
- networks
- evolution
featured: false
read_time: 4
excerpt: "An isolated service may work reliably, but what kinds of discovery become impossible when systems cannot exchange capabilities?"
series: systems-of-reality
series_index: 194
editorial_mode: science-philosophy
---

Imagine a server that never communicates with another server. It receives no updates, imports no libraries, exchanges no data and learns nothing from the failures of its peers. If its workload is fixed and its resources are sufficient, it may operate for years. It might even be exceptionally reliable. But reliability and open-ended development are different achievements.

Infrastructure is usually built as a network of specialisations. One service stores records; another authenticates users; another routes messages; another watches for failures. Their relationships allow a larger system to do more than any one component could do alone. Shared protocols let independently developed parts coordinate without requiring them to be identical.

This is a kind of neighbourhood, but not biological kinship. A service can communicate with another without sharing a common origin. It can use an interface created by a stranger. The critical question is whether the interaction is defined well enough that each side can predict what the other expects, and what happens when the exchange fails.

What might infrastructure gain from richer relationships? A routing service could learn from a monitoring system that a path is deteriorating. A resource manager could share its tested allocation strategy with another cluster. A voice network could compare failure-recovery policies under controlled simulations. The possibilities lie not in making every system copy every other system, but in allowing useful capabilities to move across boundaries.

The dangers are equally real. Network connections expand the attack surface. Shared dependencies create common points of failure. Automatically importing a neighbour's configuration could spread a defect at machine speed. The biological metaphor of exchange must never be mistaken for a safety argument.

A practical architecture would make relationships explicit. Each capability would declare its interface, assumptions, permissions, resource demands and provenance. Systems could exchange proposals rather than blindly copying live state. A candidate would be tested in isolation, compared against a known baseline, and deployed gradually only after passing functional and security checks. Revocation and rollback would be built in from the beginning.

The result would not be a network that evolves merely because it is connected. Most connected systems simply exchange messages. Evolutionary development requires additional mechanisms: variation, selection, inheritance and evidence that a change improves performance under relevant conditions.

An isolated machine can be excellent at a known task. A neighbourhood of systems can explore a wider space of possible tasks, provided their interactions are governed carefully. The engineering challenge is to create boundaries permeable enough for discovery and strong enough to prevent one neighbour's mistake from becoming everyone's emergency.
