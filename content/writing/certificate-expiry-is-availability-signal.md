---
title: Certificate Expiry Is an Availability Signal
url: /posts/certificate-expiry-is-availability-signal.html
date: '2026-09-14'
read_time: 1
excerpt: TLS can work perfectly today and still have a known future outage date embedded
  in the certificate.
topic: observability-monitoring
tags:
- tls
- certificates
- blackbox-exporter
- availability
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Network & Edge · advanced'
outputs:
- url: /posts/certificate-expiry-is-availability-signal.html
  template: cms/templates/posts/posts--certificate-expiry-is-availability-signal.tpl
  source: cms/templates/posts/posts--certificate-expiry-is-availability-signal.json
---

TLS can work perfectly today and still have a known future outage date embedded in the certificate. I ended up treating `probe_ssl_earliest_cert_expiry with 14-day warning and 7-day critical thresholds` as the useful observation point rather than relying on a generic service-up indicator. Expiry monitoring turns a predictable failure into scheduled maintenance rather than a surprise public outage.

This is a good example of proactive certificate lifecycle monitoring. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Alert well before expiry, track the minimum days remaining across endpoints, and verify renewed certificates from the external probe path. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `b65d5d4` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
