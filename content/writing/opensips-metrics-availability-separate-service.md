---
title: OpenSIPS Metrics Availability Is Separate from OpenSIPS Availability
url: /posts/opensips-metrics-availability-separate-service.html
date: '2026-09-14'
read_time: 1
excerpt: OpenSIPS can continue processing calls while the MI metrics collector fails,
  leaving the service healthy but observability blind.
topic: observability-monitoring
tags:
- opensips
- mi
- meta-monitoring
- voip
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: VoIP · advanced'
outputs:
- url: /posts/opensips-metrics-availability-separate-service.html
  template: cms/templates/posts/posts--opensips-metrics-availability-separate-service.tpl
  source: cms/templates/posts/posts--opensips-metrics-availability-separate-service.json
---

OpenSIPS can continue processing calls while the MI metrics collector fails, leaving the service healthy but observability blind. On hserver the first signal I use for this question is `hserver_opensips_scrape_success`. The monitoring path is a dependency of operations rather than call processing, so its failure needs a warning that does not falsely declare the SIP service down.

The important part is interpretation rather than collecting another graph. meta-monitoring for service exporters. That gives the metric a specific operational job instead of making it another number on a dashboard.

The practical control is straightforward: Alert when metrics disappear, keep an independent service probe, and repair telemetry without triggering unnecessary traffic failover. This also gives me a repeatable check after deployments, exporter changes, or capacity tuning.

Repository evidence for this monitoring behavior is commit `b65d5d4`. I keep that reference with the note because a monitoring conclusion is stronger when the configuration and runtime decision that produced it can be inspected later.
