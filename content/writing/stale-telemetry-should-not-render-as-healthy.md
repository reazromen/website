---
title: Stale Telemetry Should Not Render as Healthy
url: /posts/stale-telemetry-should-not-render-as-healthy.html
date: '2023-12-24'
read_time: 1
excerpt: A last-known-good value becomes misleading when the system does not show
  how old the evidence is.
topic: observability
tags:
- telemetry
- freshness
- sre
- ops-portal
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Observability · intermediate'
outputs:
- url: /posts/stale-telemetry-should-not-render-as-healthy.html
  template: cms/templates/posts/posts--stale-telemetry-should-not-render-as-healthy.tpl
  source: cms/templates/posts/posts--stale-telemetry-should-not-render-as-healthy.json
---

The Fleet and Command Center views could display reassuring state even when the runner or storage observation had not refreshed recently. The number itself was valid when collected, but the UI did not make evidence age prominent enough.

SRE monitoring depends on trustworthy evidence, not just positive values. Freshness is part of the signal contract, especially for safety gates and release decisions. State and freshness had been collapsed into one concept. A green health result from an hour ago is not equivalent to a green result from thirty seconds ago when the underlying service can change quickly.

Telemetry runners gained explicit states such as STALE and NEVER\_SEEN, storage observations carry timestamps, and the operator UI flags stale data instead of presenting it as current truth.

Every derived health signal should have an age budget. If the evidence exceeds that budget, downgrade the state to stale or unknown and require a new observation before high-risk actions proceed. The concrete hserver evidence is commit be4f22b, so this note is tied to an actual production change rather than a hypothetical failure.
