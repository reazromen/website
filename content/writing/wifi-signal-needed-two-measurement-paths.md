---
title: Wi-Fi Signal Needed Two Measurement Paths, Not One Assumption
url: /posts/wifi-signal-needed-two-measurement-paths.html
date: '2026-09-14'
read_time: 1
excerpt: Hardware and drivers expose radio state differently, so a production metric
  may need a fallback without hiding uncertainty.
topic: observability
tags:
- wi-fi
- nmcli
- iw
- metrics
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Observability · intermediate'
outputs:
- url: /posts/wifi-signal-needed-two-measurement-paths.html
  template: cms/templates/posts/posts--wifi-signal-needed-two-measurement-paths.tpl
  source: cms/templates/posts/posts--wifi-signal-needed-two-measurement-paths.json
---

Robust instrumentation distinguishes 'measurement unavailable' from 'system failed'. Multiple evidence sources can be useful when each has known limitations and the fallback semantics are explicit. The host metrics collector originally relied on `iw` output for signal and connectivity. On the production Wi-Fi stack, that path did not always provide the complete state needed for reliable dashboards.

The collector assumed one tool represented the authoritative interface state across driver and NetworkManager behavior. That assumption made the metric brittle even though the underlying link was fine.

The collector retains `iw` dBm parsing when available and adds NetworkManager signal percentage as another observation path. Connectivity falls back carefully instead of treating missing output as a hard disconnect. Expose collector success and avoid turning parser failure into a user-facing outage signal. Metrics code should be tested against real production command output, not only idealized fixtures. The concrete hserver evidence is commit 218300b, so this note is tied to an actual production change rather than a hypothetical failure.
