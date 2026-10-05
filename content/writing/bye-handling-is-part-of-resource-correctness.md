---
title: BYE Handling Is Part of Resource Correctness
url: /posts/bye-handling-is-part-of-resource-correctness.html
date: '2020-08-30'
read_time: 1
excerpt: A call that starts and carries audio but does not terminate cleanly can leak
  state across the device and PBX.
topic: loup-engineering
tags:
- sip
- bye
- dialog-state
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: SIP & RTP · advanced'
outputs:
- url: /posts/bye-handling-is-part-of-resource-correctness.html
  template: cms/templates/posts/posts--bye-handling-is-part-of-resource-correctness.tpl
  source: cms/templates/posts/posts--bye-handling-is-part-of-resource-correctness.json
---

The important detail in BYE Handling Is Part of Resource Correctness was not the component name but the contract around it. LOUP call acceptance has to include remote hangup, local hangup and teardown after abnormal signalling, not only successful setup.

BYE must target the established dialog and cause audio tasks, RTP sockets, UI state and PBX resources to close exactly once. Errors such as a 481 response usually point toward dialog identity or routing state rather than microphone or codec behaviour.

The acceptance test was written around observable behaviour rather than whether a task, container or peripheral merely reported that it had started. Evidence marker: `bye-dialog-lifecycle`.

Teardown is part of the protocol contract. Resource leaks often live in the path teams test least. That gives the team a concrete acceptance condition and a rollback point rather than a subjective sense that the build is probably better.

## Project evidence

LOUP engineering marker: `bye-dialog-lifecycle`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
