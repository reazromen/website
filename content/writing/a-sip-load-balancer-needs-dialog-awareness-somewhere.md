---
title: A SIP Load Balancer Needs Dialog Awareness Somewhere
url: /posts/a-sip-load-balancer-needs-dialog-awareness-somewhere.html
date: '2026-09-14'
read_time: 1
excerpt: Distributing initial INVITEs is easy; keeping in-dialog requests on a valid
  path is where the architecture starts to matter.
topic: telecom-voip
tags:
- sip
- load-balancing
- kamailio
- freeswitch
draft: false
featured: false
language: en
eyebrow: 2025 Voice and Infrastructure Notes · advanced
outputs:
- url: /posts/a-sip-load-balancer-needs-dialog-awareness-somewhere.html
  template: cms/templates/posts/posts--a-sip-load-balancer-needs-dialog-awareness-somewhere.tpl
  source: cms/templates/posts/posts--a-sip-load-balancer-needs-dialog-awareness-somewhere.json
---

A round-robin list of FreeSWITCH servers looks like a SIP load balancer until the first re-INVITE or BYE takes a path that no longer understands the dialog.

The system needs a routing story for sequential requests. That can involve Record-Route in a proxy, topology state, dispatcher behavior, consistent dialog ownership, or an architecture where the application servers remain reachable through the same signalling edge.

Failure handling makes the problem more interesting. A dead backend should stop receiving new calls, but existing dialogs may still have media and state tied to it. Moving a live call is very different from routing the next INVITE elsewhere.

This is why I stopped evaluating SIP load balancing only with registration counts or calls per second. Correct dialog routing and predictable failure behavior matter before scale numbers do.
