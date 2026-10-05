---
title: Wi-Fi Signal Needed a Fallback Path
url: /posts/wifi-signal-needed-fallback-path.html
date: '2022-03-06'
read_time: 1
excerpt: The host collector originally relied on `iw`, but driver and interface behavior
  did not always expose the active connection signal consistently.
topic: observability-monitoring
tags:
- wi-fi
- nmcli
- iw
- telemetry
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Network & Edge · advanced'
outputs:
- url: /posts/wifi-signal-needed-fallback-path.html
  template: cms/templates/posts/posts--wifi-signal-needed-fallback-path.tpl
  source: cms/templates/posts/posts--wifi-signal-needed-fallback-path.json
---

The host collector originally relied on `iw`, but driver and interface behavior did not always expose the active connection signal consistently. I ended up treating `hserver_wifi_signal_dbm plus hserver_wifi_signal_percent from nmcli` as the useful observation point rather than relying on a generic service-up indicator. Using both low-level radio data and NetworkManager's active-network view made the signal metric more robust without pretending the two scales are identical.

This is a good example of defensive telemetry collection. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Collect dBm when available, expose percentage as a separate metric, and make missing data visible rather than silently substituting one unit for another. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `218300b` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
