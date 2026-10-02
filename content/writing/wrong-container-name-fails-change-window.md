---
title: A Wrong Container Name Can Fail a Change Window Even When VoIP Is Healthy
url: /posts/wrong-container-name-fails-change-window.html
date: '2026-09-14'
read_time: 1
excerpt: A preflight sentinel is only useful if it names the runtime object that actually
  exists today.
topic: telecom-voip
tags:
- rtpengine
- preflight
- docker
- voip
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Git and Provenance · intermediate'
outputs:
- url: /posts/wrong-container-name-fails-change-window.html
  template: cms/templates/posts/posts--wrong-container-name-fails-change-window.tpl
  source: cms/templates/posts/posts--wrong-container-name-fails-change-window.json
---

The production change-window script checked for a container named `rtpengine`, while the live deployment used `voip-platform-rtpengine`. The media service was running, but the safety check reported it missing.

Safety automation must be versioned with the runtime definition and tested against live inventory. A false negative in a gate is safer than a false positive, but repeated false alarms train operators to distrust the gate. The sentinel encoded a stale runtime identifier. Monitoring and preflight code can drift from the system it watches just like application configuration can drift. The sentinel list was updated to the current container name so the preflight tests the actual VoIP topology.

Derive sentinel names from an ownership catalog where possible, and include a CI or staging test that compares preflight expectations with the declared Compose service names. The concrete hserver evidence is commit dfe9992, so this note is tied to an actual production change rather than a hypothetical failure.
