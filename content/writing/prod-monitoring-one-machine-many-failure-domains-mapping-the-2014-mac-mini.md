---
title: 'One Machine, Many Failure Domains: Mapping the 2014 Mac mini'
url: /posts/prod-monitoring-one-machine-many-failure-domains-mapping-the-2014-mac-mini.html
date: '2026-09-15'
read_time: 34
excerpt: 'A production-engineering deep dive into one machine, many failure domains:
  mapping the 2014 mac mini, grounded in the 2014 Mac mini hserver observability stack
  and its accepted runtime evidence.'
topic: observability-monitoring
tags:
- monitoring-architecture
- observability
- failure-model
- sre
draft: false
featured: false
language: en
eyebrow: 'Production Monitoring: Philosophy & Architecture · deep-dive'
outputs:
- url: /posts/prod-monitoring-one-machine-many-failure-domains-mapping-the-2014-mac-mini.html
  template: cms/templates/posts/posts--prod-monitoring-one-machine-many-failure-domains-mapping-the-2014-mac-mini.tpl
  source: cms/templates/posts/posts--prod-monitoring-one-machine-many-failure-domains-mapping-the-2014-mac-mini.json
---

The useful question behind **One Machine, Many Failure Domains: Mapping the 2014 Mac mini** was not whether I could collect another metric. It was whether the metric would reduce uncertainty during a production failure on a very small machine.

The host is 2014 Apple Mac mini running Linux, with roughly 7.1 GiB usable RAM from an 8 GB-class machine. Applications, databases, networking, authentication, OTA, OpenBao, VoIP and the observability stack share the same limited CPU, memory and storage. That makes monitoring part of the workload rather than something outside it. The central failure I am trying to avoid is not merely “a metric went high.” I want enough accepted evidence to tell whether a user-facing service is degrading, which dependency owns the problem, whether the signal is current, and whether the monitoring path itself is still trustworthy.

For this specific problem the primary observation point is `node_thermal_zone_temp and SMART temperature`. The short production note that preceded this article captured the core finding: Thermal data gives hardware context to throttling, fan behavior and storage health that software-only metrics cannot provide. This long-form version goes further: what that signal really proves, which nearby signals can falsify my first hypothesis, how I implement and page condition on it, what it costs on this host, and how I would redesign the same control at larger scale.

The numbers in this article are not generic benchmarks. When I mention 27,578 active Prometheus series, against a 27,414-series acceptance baseline, cAdvisor measured at 428.2 MiB before the low-RAM work and 27.87 MiB in one post-change sample, with an observed steady range around 20–28 MiB, or any other concrete value, I mean the 2026-09-15 acceptance snapshot unless I explicitly say otherwise. If a current value is not present in the accepted accepted evidence, I leave `[CURRENT MEASUREMENT NEEDED]` rather than inventing a number.

## The engineering question specific to this article

The short version of the problem is not “how do I graph One Machine, Many Failure Domains: Mapping the 2014 Mac mini?” It is: **A small Mac mini running many containers can hit thermal constraints before ordinary CPU graphs explain why performance changed.** That failure can be confused with neighboring conditions, which is why the primary observation is `node_thermal_zone_temp and SMART temperature` rather than a generic process-up flag.

The latest production production conclusion is specific: Thermal data gives hardware context to throttling, fan behavior and storage health that software-only metrics cannot provide. I turn that conclusion into an operational practice—hardware telemetry correlation—and into a preventive control: Trend CPU package and SSD temperature with load and disk activity, and page condition on sustained abnormal values rather than isolated sensor noise. Those three layers are intentionally separate. The finding explains what the accepted evidence taught me. The practice describes how I diagnose it. The prevention rule describes how I keep the same ambiguity from returning after the next deployment.

There is also a data-model question. The observation has to retain the dimension that matters without encoding unbounded identity. If the question is per node, the node label matters. If it is fleet capacity, an aggregate may be more useful. If it is an event such as a deadlock or OOM kill, a counter over a time window carries different meaning from a current-state gauge. If it is a cached inventory value, age and refresh success are part of the value's contract.

Finally I decide how close this signal is to user impact. Some topics in this series are direct symptoms; others are explanatory accepted evidence. `One Machine, Many Failure Domains: Mapping the 2014 Mac mini` belongs at the point where it can reduce investigation time without claiming more certainty than the underlying source provides. That classification determines whether it becomes a page, a warning, a NOC surface drill-down or simply retained forensic context.

## Competing hypotheses before I touch production

I try to write down multiple explanations before making a change. For **One Machine, Many Failure Domains: Mapping the 2014 Mac mini**, the candidate set I would test includes: **the desired configuration differs from runtime**; **the monitoring path is consuming enough resources to worsen the incident**; **the component is healthy but a dependency path is broken**; **the primary observation is stale rather than healthy**; and **the local observer shares the same failure domain as the service**. The point is not that all five are equally likely. It is to stop the first plausible graph from becoming the conclusion.

The primary observation `node_thermal_zone_temp and SMART temperature` should eliminate some of those hypotheses, not all of them. I choose the next query or log source by information gain: which check can separate the most remaining explanations at the lowest operational cost? A fresh internal probe versus a failed public probe immediately moves suspicion toward the edge. High memory utilization with low pressure and stable swap activity moves me away from a memory-emergency diagnosis. A stale FreeSWITCH heartbeat with a running container moves the problem from process liveness into worker readiness.

This habit is especially useful on a single host because many symptoms are correlated. Storage pressure can slow databases, logs and containers simultaneously. Host memory pressure can make the monitoring stack itself late. A router or Internet failure can make every public service look broken while the applications are healthy. Explicit competing hypotheses keep correlation from being mistaken for independent failures.

## The observation contract I expect this signal to keep

For `node_thermal_zone_temp and SMART temperature` I want a written contract even if it is only a few lines in a runbook. The contract says who produces the data, what unit it uses, which labels are bounded and meaningful, how often it should update, what reset behavior exists, and what missing data means. Without those details an old metric can survive long after its interpretation has changed.

The contract also names the strongest claim the signal supports. Thermal data gives hardware context to throttling, fan behavior and storage health that software-only metrics cannot provide. That sentence is intentionally narrower than “the service is healthy.” It leaves room for independent accepted evidence and tells future maintainers not to reuse the metric for a stronger conclusion without re-validating it.

Freshness belongs in the contract whenever the producer is not scraped directly. Cache-backed Docker inventory, textfile metrics, heartbeat state and backup timestamps can all remain syntactically valid after the producer stops. I therefore prefer either an explicit age metric or a timestamp from which age can be derived. For direct Prometheus targets, `up` is part of the collection contract but still not the service-health contract.

Finally, the contract includes data sensitivity. Labels and log content must not turn operational telemetry into a secret-disclosure channel. If the observation cannot be collected safely with bounded identity and least privilege, I redesign the observation path rather than assuming the monitoring network is trusted.

## Start with the failure, not the exporter

The breakage pathl for this article is: **A small Mac mini running many containers can hit thermal constraints before ordinary CPU graphs explain why performance changed.** That wording matters because it describes the operational ambiguity I need to remove. A raw metric has no value until I know what claim I am trying to make from it.

The obvious monitoring mistake is to collapse several layers into one binary state. A process can exist while the application is unusable. A observation path can return a number that is already stale. A public service can correctly return a redirect or authorization error and still be healthy. A database can accept a TCP connection while lock contention makes useful queries stall. A host can report high memory utilization while reclaimable page cache means applications are not under pressure. The same general problem appears repeatedly: one layer's “up” is only accepted evidence about that layer.

I therefore map each failure to at least three questions. First, what is the earliest useful signal that something is changing? Second, what is the strongest user-visible symptom I can observe independently? Third, what accepted evidence tells me the monitoring path is alive enough to trust the first two answers? For `One Machine, Many Failure Domains: Mapping the 2014 Mac mini`, `node_thermal_zone_temp and SMART temperature` belongs in that chain, but it is never allowed to stand alone if the failure can be confirmed from another layer.

This is also how I decide whether an page condition belongs on a metric. A signal may be excellent for diagnosis and terrible for paging. Context switches, container block-I/O bytes or database size trends can be valuable accepted evidence without being reasons to interrupt an operator immediately. Conversely, a public probe failure or no-healthy-worker condition may deserve much more direct attention because it is already close to user impact.

## Where this sits in the hserver observability architecture

The deployed topology started from failure domains, not from a shopping list of observability products. The host can fail as hardware, as a Linux system, as a Docker runtime, as an application platform, as a network endpoint, and as the place where the monitoring stack itself lives. Those layers overlap but they do not fail identically. A process can be alive while a service is unusable; a service can be healthy internally while its public route is broken; the local monitoring stack can be perfect until the whole Mac mini loses power. That is why the design combines kernel metrics, container metrics, application metrics, logs, synthetic probes, state checks, recovery accepted evidence and an external observer. Each signal is a claim of a particular strength. The point is to know what the claim proves and what it cannot prove.

The resource constraint matters because it prevents observability from becoming an unpriced luxury. On this small production machine, monitoring competes with databases, authentication, OTA, VoIP, secret management and the applications themselves. A metric therefore has acquisition cost, storage cost, query cost and human interpretation cost. A NOC surface has cognitive cost. An page condition has interruption cost. My model treats those costs as part of production capacity. This is also why I prefer layered accepted evidence: cheap signals should identify the failure domain, and expensive inspection should happen after the search space is smaller.

For this article, the component boundary matters as much as the metric. The latest production accepted observability stack includes Prometheus, Grafana, Loki, Alloy, Alertmanager, Blackbox Exporter, Node Exporter, cAdvisor, SMART collection, Docker inventory and deep host/database observation paths, plus application-native and external synthetic signals. The latest acceptance artifact records 52/52 accepted Prometheus targets UP, 106 page condition/recording rules loaded, 15 provisioned NOC surfaces and 10/10 public probes UP.

I intentionally avoid interpret those counts as a maturity score. More targets and more rules can make a system worse if they add noise or cost without reducing uncertainty. The useful part is that the inventory is explicit and accepted. When I add a control for `One Machine, Many Failure Domains: Mapping the 2014 Mac mini`, I can ask which existing layer already sees part of the problem, whether a new metric is necessary, and how the new observation will be validated after deployment.

## The decision this monitor should let me make

If this telemetry cannot change a decision, it should not automatically consume always-on budget. For **One Machine, Many Failure Domains: Mapping the 2014 Mac mini**, the decisions fall into four categories. I may need to intervene immediately because a service contract is already broken. I may need to schedule capacity work because margin is shrinking. I may need to isolate a dependency during incident diagnosis. Or I may decide that the condition is normal and explicitly avoid action.

That last outcome is important. Monitoring is partly a system for proving when *not* to react. Page cache, historical swap, a 302 authentication redirect, a controlled restart, or a busy response from a SIP endpoint can look abnormal without representing infrastructure failure. The metric model should carry enough context to distinguish those cases.

I keep a second constraint: want the monitor to make rollback decisions safer. If a deployment changes `node_thermal_zone_temp and SMART temperature`, I should be able to compare the new state with the accepted baseline and decide whether the change is intended. That is why provenance `b65d5d4` stays attached to the topic. A production metric without a known configuration history is harder to use as change accepted evidence.

At scale this decision-centric approach becomes even more important. Hundreds of hosts can produce unlimited telemetry; operator time remains finite. The series therefore treats observability as a decision system rather than a storage system.

## Why this particular collection path won

There are usually several ways to obtain the state behind **One Machine, Many Failure Domains: Mapping the 2014 Mac mini**: scrape an existing exporter, query an application API, run a SQL statement, parse logs, inspect the Docker API, read a Linux kernel interface, or publish a small custom metric through the textfile path. I choose among them by authority, cost, security and failure independence.

The closest source is not always the best source. A Docker container metric can tell me process resource use but not whether PostgreSQL sessions are waiting. A log parser can count authentication failures but is a weaker source for current service readiness than a direct state query. A raw TCP probe is cheap but deliberately shallow. A deep query may be authoritative but require credentials or create load. The implementation behind `node_thermal_zone_temp and SMART temperature` is valuable because it sits at the layer that owns the state I need to interpret.

I keep a second constraint: prefer collection paths with visible failure. A custom script that exits silently and leaves yesterday's textfile metric behind is worse than a observation path that exports its own success and age. A cache should expose refresh result and age. A database observation path should expose whether its query succeeded. A log pipeline should expose drops. The observer has to be observable.

The chosen path therefore reflects more than convenience. It is part of the breakage pathl: which component can lie, which credential can expire, which namespace the query sees, and what remains observable when another layer breaks.

## How I reason about a threshold for this topic

I intentionally avoid begin with a round number. I begin with the consequence I am trying to avoid and how much reaction time exists. Capacity thresholds such as disk or connection utilization should leave enough margin to investigate before exhaustion. Pressure thresholds should remain high long enough to distinguish real contention from transient scheduling noise. Certificate thresholds are measured in days because the repair process is administrative, not millisecond-sensitive. External availability failures can justify much faster response.

For **One Machine, Many Failure Domains: Mapping the 2014 Mac mini**, the next threshold review should use the historical distribution plus the component's configured limit and the time needed to act. If that distribution is not captured in the latest accepted runtime artifact, the honest value is **[CURRENT MEASUREMENT NEEDED]**. I intentionally avoid derive a production page from an attractive number in a blog post.

I keep a second constraint: test both sides of the boundary. A warning threshold should actually enter pending/firing state when a fixture crosses it, and it should resolve when the signal recovers. A critical threshold should not be inhibited by the warning in a way that loses the more serious state. If the signal is a counter, the window should contain enough events to be meaningful. If it is a gauge, the `for` duration and freshness semantics matter more than counter reset behavior.

Thresholds are therefore versioned policy. When topology, workload, resource limits or observation path semantics change, I expect the threshold to be reviewed alongside the code.

## Draw the data path before trusting the panel

For this part of the system I keep a simple failure-domain drawing in mind:

```
failure -> local metric/log -> Prometheus/Loki -> rule/NOC surface -> Alertmanager
     \-> internal synthetic probe
     \-> public probe -> external GitHub watcher (outside hserver failure domain)
```

The diagram matters because every arrow can fail independently. Collection can succeed while storage or rule evaluation fails. An internal probe can succeed while the public path fails. A public probe running on hserver still shares the host failure domain even if it reaches a public URL. A database exporter can be healthy while its engine query permission is broken. A log observation path can be alive while the write path drops entries.

For `One Machine, Many Failure Domains: Mapping the 2014 Mac mini`, I identify the authoritative source on the left, every transformation before the NOC surface or page condition, and which component owns persistence. Then I decide where failure should become visible. If a transformation silently converts “unknown” into zero, the diagram has an observability gap. If both the service and its observer depend on the same process or credential, the diagram has a shared failure domain.

This exercise is cheap and often catches problems before PromQL is written. It additionally explains why I retained both internal and public probes, why the external watcher lives on hosted runners, and why backup accepted evidence has multiple stages rather than one success bit.

## What would make this monitor lie?

I ask this question explicitly because most monitoring failures are not fabricated numbers; they are numbers interpreted outside their validity. `node_thermal_zone_temp and SMART temperature` can become misleading if its observation path is stale, labels change, the underlying source resets, the query aggregates away the failing member, the scrape path observes a different network namespace, or the monitored component changes semantics after an upgrade.

Caching creates another class of lies. The Docker storage inventory is deliberately cached because continuous filesystem inspection was too expensive. A cache-backed metric is only trustworthy when cache age and refresh success are visible. Textfile metrics have the same issue if the producer stops updating them. Database-derived metrics can lie by omission if the observation path account loses access to a system view. Log-derived metrics can go quiet because Alloy or Loki is dropping data rather than because the event stopped happening.

Authentication and synthetic probes can lie through overly permissive expectations. Following redirects blindly may turn an application failure into a successful login-page response. Accepting every status code may hide a broken route. Requiring only 200 may create the opposite error and call a healthy access-control response an outage. The probe has to encode the intended contract.

My response to these risks is not distrust of monitoring. It is meta-monitoring, freshness, independent accepted evidence and explicit UNKNOWN states when the observation path cannot make a strong claim.

## The hserver case that shaped this part of the design

The external dead-man design is the clearest architecture case. Local Prometheus and Alertmanager cannot report a total host death because they share the host's power, kernel, storage and network failure domains. The GitHub-hosted watcher deliberately moves scheduling and incident state outside hserver, probes public accepted evidence without hserver credentials, and was exercised through a forced failure/recovery cycle. That one design decision is stronger accepted evidence of failure-model thinking than another dozen local NOC surfaces.

I prefer that case as a guardrail for `One Machine, Many Failure Domains: Mapping the 2014 Mac mini` because it prevents the discussion from becoming a generic monitoring tutorial. The interesting question is not whether another platform supports the same metric. It is what decision the signal enabled on this constrained production host, what cost it imposed, and what accepted evidence proved that the change improved rather than merely rearranged the system.

It additionally keeps causality honest. A before/after measurement is accepted evidence for this configuration at that time. It is not a universal benchmark for cAdvisor, Prometheus, Docker, OpenBao or any database engine. When the article makes a recommendation, the recommendation is about the engineering method—measure, isolate cost, preserve the useful signal, verify the new breakage paths—not about assuming another machine will reproduce the same number.

## An accepted evidence ledger for this monitor

I find it useful to write down the accepted evidence hierarchy explicitly rather than leaving it implicit in a NOC surface. For **One Machine, Many Failure Domains: Mapping the 2014 Mac mini**, the ledger starts with the primary signal `node_thermal_zone_temp and SMART temperature` and the repository/runtime accepted evidence `b65d5d4`. Beside it I record the nearest independent corroborator, the user-visible symptom that would make the condition important, the freshness requirement, and the monitoring failure that would make the accepted evidence unavailable.

That ledger prevents two common mistakes. My first is treating a derived metric as authoritative when the source has changed. The second is treating absence of an page condition as proof of health when the rule, target or notification path is broken. A trustworthy green state is therefore composite: expected targets are present, relevant rules evaluate, the sample is fresh, the value is inside policy, and the delivery path is not reporting failure.

I keep a second constraint: record which accepted evidence is historical acceptance rather than live truth. The 27,578-series point, cAdvisor 27.87 MiB sample, 52/52 targets and 106 rules all belong to a dated accepted state. They are useful comparison points. They should not be copied into future incident notes as though they describe the current second. If this article needs a current value during an investigation, the operator must query production again.

This sounds bureaucratic until something changes. Once labels, exporters, versions and topology evolve, the ledger tells me which assumption an old graph depended on. Monitoring ages like code; provenance is how I keep old conclusions from becoming folklore.

## The obvious alternatives I did not choose

My first rejected alternative is usually **collect everything at the fastest cadence**. That maximizes raw visibility and minimizes discipline. On this small production machine it also increases samples, series, disk writes, log volume and exporter work without guaranteeing faster diagnosis. I prefer deliberate sampling and the ability to run a deeper command or query during investigation.

The second alternative is **replace semantics with one generic health endpoint**. Health endpoints are useful, but they collapse state. They cannot tell me whether Linux is reclaiming memory, whether PostgreSQL sessions are waiting, whether an RTP leg is failing while SIP is healthy, or whether an OpenBao seal state violates the expected operating mode. I keep coarse health for orchestration and synthetic checks, then retain subsystem accepted evidence for diagnosis.

The third alternative is **page on every abnormal-looking value**. That would turn `node_thermal_zone_temp and SMART temperature` into an interruption mechanism even when the signal is only contextual. I would rather reserve paging for service symptoms, dangerous saturation and predictive failures with a clear response. Diagnostic metrics remain available without waking anyone.

Finally, I avoid solving a local observation problem by adding another heavyweight service automatically. A custom textfile metric or a reviewed query inside an existing database container can be safer and cheaper than maintaining another exporter, another credential, another image and another update lifecycle. Exporter sprawl is still infrastructure sprawl.

## Anti-patterns I now reject

I no longer accept **“there is a NOC surface for it”** as monitoring coverage. A NOC surface that depends on manual inspection has no detection contract. I keep a second constraint: reject **“the container is running”** as application availability, **“the port accepts TCP”** as database health, **“the backup job exited zero”** as recoverability, and **“the service returned non-200”** as a universal definition of outage.

Another anti-pattern is **metric accumulation without deletion**. Exporters get enabled, NOC surfaces import hundreds of panels, and nobody removes series after architecture changes. That creates cost and ambiguity. The accepted configuration explicitly checks that dead synthetic references are gone; I apply the same hygiene to unused metrics and stale log streams.

I keep a second constraint: avoid **page conditioning on implementation details without user consequence or operator action**. High context-switch rate, image count, database size or a busy disk may explain an incident without deserving a page. The right place can be a drill-down NOC surface or a warning tied to capacity trend. Paging is reserved for conditions where time matters.

Finally, I reject **false precision**. If the current system has not measured a latency percentile, per-component RAM split, database footprint or recovery duration, I intentionally avoid invent one for a polished article. `[CURRENT MEASUREMENT NEEDED]` is a better engineering statement than a believable number with no accepted evidence.

## Cross-layer dependencies I intentionally avoid want this monitor to hide

The primary observation in this article belongs to one layer, but incidents cross layers. A memory-pressure page condition can be caused by a container leak, a database cache change, observability cardinality growth or an unrelated batch job. A public HTTP failure can be application, reverse proxy, authentication, DNS, TLS, tunnel, router or Internet path. A database latency symptom can be locks, storage, memory reclaim or connection saturation. A VoIP symptom can cross registration, SIP transaction, worker health, DNS/SQL dependency and RTP media.

That is why I avoid NOC surfaces grouped only by exporter. Exporters reflect collection technology; incidents follow dependencies. `One Machine, Many Failure Domains: Mapping the 2014 Mac mini` should link naturally to the next accepted evidence domain. The host view links to containers and storage. Database panels link to host I/O and container limits. Public probes link to internal probes and edge logs. Alert-delivery panels link back to rule health. Backup panels link to disk headroom, job logs and restore verification.

This cross-layer model also changes page condition grouping. If one host failure makes ten applications disappear, the application probes are still useful symptoms, but the operator should not receive ten unrelated pages. Conversely, if the host is healthy and only one public route fails, collapsing everything into “host healthy” would hide the actual service outage. Correlation is therefore contextual, not a reason to suppress independent accepted evidence.

## The monitoring tax for this signal

On this machine, collection cost is part of the design review. The latest production host has roughly 7.1 GiB of usable RAM, and the observability stack has occupied a meaningful fraction of that budget in different acceptance snapshots. The low-RAM artifact recorded the low-RAM acceptance artifact recorded a 726.2 MiB observability-memory sample; another aggregate runtime field recorded 841,814,016 bytes, so My model treats both as snapshot accepted evidence rather than a universal footprint. Those snapshots cover different accounting views, so I intentionally avoid collapse them into one magic “monitoring uses X MiB” claim. I prefer them to prove that observability is large enough to manage deliberately.

The cAdvisor case is the clearest example: cAdvisor measured at 428.2 MiB before the low-RAM work and 27.87 MiB in one post-change sample, with an observed steady range around 20–28 MiB. That improvement came from removing work whose cost exceeded its operational value, not from disabling container observability. The same reasoning applies to `One Machine, Many Failure Domains: Mapping the 2014 Mac mini`. I ask how often the state can meaningfully change, how quickly I need to react, how many series or log streams the observation creates, whether a cheaper observation path can answer the same question, and whether the query belongs at scrape time, recording-rule time or investigation time.

There is also a human monitoring tax. Every page condition that cannot lead to an action consumes attention. Every NOC surface panel that lacks a clear question makes incidents slower. Every high-cardinality label creates future storage and query work. The resource budget therefore includes RAM, CPU, disk, network, series count, log streams and operator cognition.

On a larger host I might tolerate a more expensive observation path to gain richer diagnostics. On this small production machine the default is the opposite: collect the smallest reliable signal that preserves the failure accepted evidence I need, then keep deeper inspection available on demand.

## Turning the observation into an page condition without creating noise

Not every article in this series ends with a page. Some of the best signals are diagnostic. When I do page condition, I separate **prediction**, **saturation**, and **symptom**. Prediction covers conditions such as disk capacity or certificate expiry where action before failure is possible. Saturation covers sustained pressure or exhausted pools. Symptoms cover conditions such as a failed public probe, no healthy SIP worker, or unsuccessful restore verification where the service contract is already affected.

The rule duration has to fit the failure. A single scrape miss or short deployment restart should not create an incident. A total public outage should not sit pending for an arbitrary long `for:` window simply because another resource rule uses ten minutes. Warning and critical labels are response contracts: warning means investigate or schedule action before the margin disappears; critical means the operating state is already outside the tolerated envelope or approaching it fast enough to require immediate attention.

I keep a second constraint: ask what other page condition will fire at the same time. If host loss makes every public service fail, paging separately for Grafana, OTA, authentication, gateway and VoIP adds noise without information. Grouping and inhibition should preserve useful symptoms while making the likely root event obvious. Resolution is part of the lifecycle too. The latest accepted notification accepted evidence recorded external notification counters in the acceptance artifact: 13 success, 0 failure, 6 resolved; that is a snapshot of delivery behavior, not an SLA claim.

For `One Machine, Many Failure Domains: Mapping the 2014 Mac mini`, the page condition is successful only if its annotation tells me what was observed, over what window, which NOC surface or runbook to open next, and what secondary signal can confirm the hypothesis.

## Acceptance: prove the monitor after changing it

I intentionally avoid treat a configuration commit as proof that monitoring works. After meaningful observability changes I compare the desired state in Git with runtime acceptance. The latest production artifact records 52/52 accepted Prometheus targets UP, 106 page condition/recording rules loaded, 0 firing and 0 pending page conditions, 27,578 active Prometheus series, against a 27,414-series acceptance baseline, 10/10 public probes UP, 9/9 database probes UP and 35 monitored configuration files with zero drift in the latest runtime sample. Those numbers are useful because they make blind spots and accidental cardinality growth measurable after deployment.

The validation depends on the feature. A scrape change should prove the target is UP and the expected series exists. A relabel change should prove the required NOC surface and page condition queries still return data. A log-pipeline change should prove cursor continuity and check drop counters. A public probe should be exercised against both healthy and intentionally invalid behavior. A backup control should be followed by checksum and restore accepted evidence. A notification change should send a synthetic page condition and verify both firing and resolved delivery.

Where safe, I prefer failure injection to passive confidence. The external dead-man watcher was tested by forcing a synthetic outage: the hosted workflow failed, an incident issue was created, recovery later passed and the issue closed. That sequence proved more than reading the workflow YAML. The same idea scales down to small controls: temporarily make a test target fail, expire a synthetic sample, or use a fixture that triggers the rule without damaging production.

## Change management and rollback for monitoring itself

Monitoring changes can cause outages indirectly. A bad Prometheus rule can increase evaluation load. A label change can break every NOC surface and page condition that joins on the old label. A log relabel rule can drop security accepted evidence. A Blackbox change can generate false incidents. A database probe can even change engine counters, as the removed raw MySQL TCP probe demonstrated by incrementing `Aborted_connects`.

I therefore treat observability changes like production software. Before a risky change I preserve the relevant configuration and acceptance state. I validate syntax and rule files before deployment. After deployment I verify target count, rule count/evaluation health, expected query results, NOC surface rendering, series/cardinality movement and the resource budget. If those checks fail, rollback should restore the previous known configuration rather than “fix forward” while the monitoring system is partially blind.

The latest production source-of-truth model helps here: reviewed configuration lives in Git; runtime acceptance and config hashes tell me what was actually deployed. `b65d5d4` is associated with this article for the same reason. Provenance is not decoration. When an page condition behaves differently weeks later, I want to know which configuration decision created that behavior.

## What another engineer would need to operate this without me

An accepted evidence-collection system is fragile if only the person who built it understands why a threshold exists. For each important control I want enough context in Git, NOC surfaces and runbooks that another engineer can answer five things: what failure the signal represents, where the data comes from, what normal exceptions exist, what corroborating accepted evidence to inspect, and how to change or roll back the rule safely.

That requirement shapes article writing too. I include the architecture and the rejected alternatives because a bare PromQL expression does not preserve the decision. If someone later sees `node_thermal_zone_temp and SMART temperature`, they should understand why that signal was selected over a simpler metric and which assumptions would invalidate it.

The acceptance artifact is part of that handoff. It records a dated state—targets, rules, probes, drift, series count, DR verification, low-RAM settings—so future changes have a reference. It does not replace live inspection, but it prevents operations from depending on oral history.

At larger organizational scale I would turn more of these controls into automated policy tests and service ownership metadata. On one small server, explicit source ownership, reproducible configs and documented accepted evidence already provide most of the cultural benefit: production state should be reconstructable from artifacts, not from memory.

## What the current accepted system says

The 2026-09-15 acceptance snapshot gives me a concrete reference point while writing this series. It records 52/52 accepted Prometheus targets UP, 106 page condition/recording rules loaded, 0 firing and 0 pending page conditions, and 15 provisioned NOC surfaces. Prometheus reported 27,578 active Prometheus series, against a 27,414-series acceptance baseline. Public probing reported 10/10 public probes UP; database probing reported 9/9 database probes UP. The accepted configuration manifest reported 35 monitored configuration files with zero drift in the latest runtime sample.

For storage and retention, Prometheus retention set to about 30 days with a 15 GB size cap; Loki retention set to 168 hours. For hardware accepted evidence, SMART status healthy in the acceptance artifact, with a 49 C device-temperature sample. For recovery, encrypted DR verification PASS, required payload PASS, internal checksum PASS, off-host pull PASS, and restore verification PASS. For OpenBao, main OpenBao initialized and unsealed with Transit auto-unseal; same-host seal node initialized and unsealed with no host-published ports. These values are intentionally described with a date because they are not permanent properties of the architecture. They are accepted evidence that the system reached a known state after a particular round of changes.

This distinction is important for `One Machine, Many Failure Domains: Mapping the 2014 Mac mini`. Monitoring documentation tends to age badly when it turns an observation into a law. I would rather write “27,578 active series in this acceptance snapshot” than imply that 27,578 is a target, a limit or a recommendation. The same applies to cAdvisor memory, disk temperature, NOC surface count and page condition-rule count. The deployed topology should survive changing numbers because the interpretation rules remain explicit.

## What I would change at larger scale

The small-server version optimizes for bounded cost and direct inspectability. At fleet scale I would preserve the semantic model but move some responsibilities. Metrics storage could move off the application host. Long-term retention could use a system designed for remote or object-backed storage. Loki could live on a dedicated node. Exporter and observation path work could be distributed closer to the workloads while query and page condition evaluation stay centralized. High-availability Alertmanager and independent monitoring storage would reduce shared failure domains.

I would not, however, replace `node_thermal_zone_temp and SMART temperature` with a generic “enterprise monitoring” product and call the problem solved. The key question remains what the observation proves. If the signal is about Linux pressure, the kernel semantics remain. If it is about database locks, the engine semantics remain. If it is about SIP versus RTP, the protocol boundaries remain. If it is about dead-man monitoring, the observer still has to live outside the failure domain.

Scale primarily changes collection topology, retention, redundancy and automation. It does not remove the need to define failure semantics. In fact, larger systems punish ambiguous metrics more severely because a noisy or high-cardinality mistake multiplies across more hosts and more operators.

## Deep-dive notes: separating mechanism from policy

A recurring source of monitoring bugs is mixing mechanism with policy. The mechanism answers how the observation is produced: kernel counter, cgroup metric, SQL query, log parser, HTTP probe, application counter or external workflow. Policy answers what the organization does when that observation changes. `node_thermal_zone_temp and SMART temperature` is mechanism. The threshold, window, severity, grouping and escalation path are policy.

Keeping those separate makes the system easier to evolve. I can improve collection without changing the paging contract, or change a warning threshold after capacity review without rewriting the observation path. It additionally makes testing clearer. Collector tests validate units, labels, freshness and failure behavior. Rule tests validate expressions and state transitions. End-to-end tests validate that an actual synthetic condition reaches the operator and resolves correctly.

The same separation applies to desired state and accepted evidence. Git defines reviewed configuration, but Git cannot prove the running system loaded it. Runtime acceptance proves what production observed, but runtime state is not a reproducible configuration source. The latest production manifest model bridges the two by hashing approved monitored configuration and measuring drift without exporting secret values.

For this topic, I would treat a future scale-out as another policy change rather than an excuse to discard the semantic model. A managed metrics backend, Kubernetes, multiple nodes or cloud load balancers change topology. They do not change what memory pressure means, what a deadlock means, what a stale heartbeat means, or why a probe outside the failure domain is stronger accepted evidence of host death than a local NOC surface.

## What I keep from this decision

What survived from this work is not a particular threshold. It is the interpretation contract behind **One Machine, Many Failure Domains: Mapping the 2014 Mac mini** and the accepted evidence required before I trust it. The control is useful because I know its acquisition cost, expected cadence, breakage paths, corroborating signals and response path. That is the standard I now use before adding another metric or page condition to hserver.

The server is still an old Mac mini. That constraint has not stopped the monitoring system from becoming serious. It has forced every layer to be explicit about what it is worth. For me that is the more interesting engineering result: production-grade observability is less about how many products are installed and more about whether the accepted evidence is sufficient, current, independent where necessary, and cheap enough that the observer does not become the outage.
