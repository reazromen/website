---
title: A VoIP Change Window Should Prove the Media Path Still Exists
url: /posts/voip-change-window-prove-media-path-exists.html
date: '2025-03-19'
read_time: 1
excerpt: Checking only the SIP proxy is not enough when a healthy call depends on
  signaling and media components staying aligned.
topic: telecom-voip
tags:
- voip
- rtpengine
- change-window
- preflight
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Production Acceptance · advanced'
outputs:
- url: /posts/voip-change-window-prove-media-path-exists.html
  template: cms/templates/posts/posts--voip-change-window-prove-media-path-exists.tpl
  source: cms/templates/posts/posts--voip-change-window-prove-media-path-exists.json
---

The hserver change-window preflight treats FreeSWITCH, Drachtio, OpenSIPS and RTPengine as production sentinels. A maintenance change outside the VoIP stack can still affect networking, ports or Docker state that those services depend on.

Telephony availability is a dependency chain rather than one process. Signaling can stay up while media breaks, or a proxy can be reachable while backends are unavailable. Preflight checks enumerate the current signaling and media containers before unrelated production changes proceed, and the RTPengine sentinel was corrected when its runtime name drifted.

This is blast-radius control and change-window validation. Critical unaffected services should be checked before and after a change so collateral damage is detected immediately. Add protocol-level synthetic calls over time, but keep lightweight component sentinels as a fast first gate. The strongest acceptance combines process, endpoint and actual call-path evidence. The concrete hserver evidence is commit dfe9992, so this note is tied to an actual production change rather than a hypothetical failure.
