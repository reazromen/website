---
title: Audit Logs Matter Because Secret Reads Are Security Events
url: /posts/openbao-audit-logs-secret-reads-security-events.html
date: '2020-05-29'
read_time: 1
excerpt: A successful secret request is operationally normal and still important enough
  to leave durable evidence.
topic: security-identity
tags:
- openbao
- audit
- hmac
- security
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: OpenBao Secrets · advanced'
outputs:
- url: /posts/openbao-audit-logs-secret-reads-security-events.html
  template: cms/templates/posts/posts--openbao-audit-logs-secret-reads-security-events.tpl
  source: cms/templates/posts/posts--openbao-audit-logs-secret-reads-security-events.json
---

Most application logs focus on failures. Secret infrastructure needs a different mindset because a successful read may be the event I need to investigate later.

The hserver OpenBao configuration enables a persistent file audit device. OpenBao records request activity while protecting sensitive request and response fields with HMAC by default rather than dumping raw secret values into the audit trail.

That gives two useful properties at the same time: I can answer which identity used which path and when, while avoiding an audit file that becomes a second plaintext secret database. Audit storage itself remains restricted and enters the operational monitoring and backup model as security evidence.

An audit log is not prevention. It is accountability and forensic context. When combined with narrow policies and short-lived tokens, it makes abnormal secret access easier to distinguish from expected workload behavior.

## Engineering evidence

The hserver repository evidence for this note is commit `1f583b4`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
