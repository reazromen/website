---
title: The Process Is Running, but Is the Service Useful?
date: '2021-10-01'
draft: false
language: en
url: /posts/bn-process-running-service-useful.html
topic: production-engineering
tags:
- operations
- health-checks
featured: false
read_time: 2
excerpt: >-
  A running process is useful information, but it does not prove the process is completing
  the work it exists to do. A web server can be alive while its required database is
  unreachable.
editorial_batch: 20261003-100-niches
---

A running process is useful information, but it does not prove the process is completing the work it exists to do. A web server can be alive while its required database is unreachable. The user sees failure while the process list still shows life.

Health checks should therefore make their level explicit. Process exists, port responds, dependency is usable, and a real operation completes are different guarantees. A green status is only meaningful when we know which guarantee it represents.

A small functional probe can be more valuable than a shallow heartbeat. It may be possible to perform a limited, safe operation without executing a complete transaction. The probe's own load and side effects still have to be considered.

I want service health to stay close to the service's purpose. Operators do not only need signs of life; they need evidence that user work is likely to succeed. Keeping that distinction reduces false confidence.

Source: [official reference](https://www.freedesktop.org/software/systemd/man/249/systemctl.html).
