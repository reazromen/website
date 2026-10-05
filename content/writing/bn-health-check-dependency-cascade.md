---
title: When a Health Check Fails Every Dependency at Once
date: '2025-04-20'
draft: false
language: en
url: /posts/bn-health-check-dependency-cascade.html
topic: production-engineering
tags:
- health-checks
- reliability
featured: false
read_time: 2
excerpt: >-
  Restarting a service whenever one of its dependencies is temporarily unhealthy is not
  always helpful. An external failure may not be fixed by restarting the application,
  and useful in-flight work can be lost in the process.
editorial_batch: 20261003-100-niches
---

Restarting a service whenever one of its dependencies is temporarily unhealthy is not always helpful. An external failure may not be fixed by restarting the application, and useful in-flight work can be lost in the process. The action triggered by a health check is part of the design.

Liveness and readiness answer different questions. Is the process itself stuck? Can it safely accept new work right now? Treating the second condition as if it were the first can create unnecessary restart loops.

Suppose the database becomes slow. The application restarts, reconnects, and immediately adds more work to the already stressed dependency. The health system detected a problem correctly, but its response made the incident worse.

I think of a good health check as part of operational decision-making. Which failures should cause waiting, which should remove traffic, and which should restart a process? Once those rules are explicit, system behavior becomes more meaningful than a simple green or red indicator.

Source: [official reference](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/).
