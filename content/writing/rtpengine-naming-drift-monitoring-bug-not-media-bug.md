---
title: RTPengine Naming Drift Was a Monitoring Bug, Not a Media Bug
url: /posts/rtpengine-naming-drift-monitoring-bug-not-media-bug.html
date: '2023-09-20'
read_time: 1
excerpt: When a sentinel references yesterday's container name, the monitoring system
  becomes the failed component.
topic: telecom-voip
tags:
- rtpengine
- monitoring
- docker
- naming
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Production Acceptance · intermediate'
outputs:
- url: /posts/rtpengine-naming-drift-monitoring-bug-not-media-bug.html
  template: cms/templates/posts/posts--rtpengine-naming-drift-monitoring-bug-not-media-bug.tpl
  source: cms/templates/posts/posts--rtpengine-naming-drift-monitoring-bug-not-media-bug.json
---

Monitoring configuration is production code. False alerts deserve root-cause treatment because noisy gates reduce operator trust and increase the chance that a future real warning is bypassed. The media relay was running under `voip-platform-rtpengine`, while the change-window script still searched for `rtpengine`. The resulting failure looked like a production dependency outage even though media service state was fine. Operational tooling had a hard-coded identifier that no longer matched the runtime source of truth. This is observability drift.

The sentinel name was corrected immediately and committed as its own fix so the safety gate reflected the current deployment. Where possible, derive runtime identifiers from reviewed service catalogs or Compose metadata instead of maintaining duplicate hard-coded lists. The concrete hserver evidence is commit dfe9992, so this note is tied to an actual production change rather than a hypothetical failure.
