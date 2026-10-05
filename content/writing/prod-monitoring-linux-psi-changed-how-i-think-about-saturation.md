---
title: Linux PSI Changed How I Think About Saturation
url: /posts/prod-monitoring-linux-psi-changed-how-i-think-about-saturation.html
date: '2026-05-24'
read_time: 35
excerpt: A production-engineering deep dive into linux psi changed how i think about
  saturation, grounded in the 2014 Mac mini hserver observability stack and its accepted
  runtime evidence.
topic: observability-monitoring
tags:
- linux
- host-monitoring
- performance
- prometheus
draft: false
featured: false
language: en
eyebrow: 'Production Monitoring: Linux Host Observability · deep-dive'
outputs:
- url: /posts/prod-monitoring-linux-psi-changed-how-i-think-about-saturation.html
  template: cms/templates/posts/posts--prod-monitoring-linux-psi-changed-how-i-think-about-saturation.tpl
  source: cms/templates/posts/posts--prod-monitoring-linux-psi-changed-how-i-think-about-saturation.json
---

I did not add this signal because My goal ised another graph. I added it because `Linux PSI Changed How I Think About Saturation` describes a incident shape that the rest of the stack could not explain cleanly.

The host is 2014 Apple Mac mini running Linux, with roughly 7.1 GiB usable RAM from an 8 GB-class machine. Applications, databases, networking, authentication, OTA, OpenBao, VoIP and the observability stack share the same limited CPU, memory and storage. That makes monitoring part of the workload rather than something outside it. The central failure I am trying to avoid is not merely “a metric went high.” My goal is enough evidence to tell whether a user-facing service is degrading, which dependency owns the problem, whether the signal is current, and whether the monitoring path itself is still trustworthy.

For this specific problem the primary observation point is `node_memory_MemAvailable_bytes and PSI memory pressure`. The short the live system note that preceded this article captured the core finding: Available memory shows what the kernel can still reclaim, while pressure shows whether workloads are actually stalling for memory. This long-form version goes further: what that signal really proves, which nearby signals can falsify my first hypothesis, how I implement and notification rule on it, what it costs on this host, and how I would redesign the same control at larger scale.

The numbers in this article are not generic benchmarks. When I mention 27,578 active Prometheus series, against a 27,414-series acceptance baseline, cAdvisor measured at 428.2 MiB before the low-RAM work and 27.87 MiB in one post-change sample, with an observed steady range around 20–28 MiB, or any other concrete value, I mean the 2026-09-15 acceptance snapshot unless I explicitly say otherwise. If a current value is not present in the accepted evidence, I leave `[CURRENT MEASUREMENT NEEDED]` rather than inventing a number.

## The engineering question specific to this article

The short version of the problem is not “how do I graph Linux PSI Changed How I Think About Saturation?” It is: **The host looked busy enough that a simple percentage could easily become the whole diagnosis, but Linux memory reclaim makes that misleading.** That failure can be confused with neighboring conditions, which is why the primary observation is `node_memory_MemAvailable_bytes and PSI memory pressure` rather than a generic process-up flag.

The the live system the live system conclusion is specific: Available memory shows what the kernel can still reclaim, while pressure shows whether workloads are actually stalling for memory. I turn that conclusion into an operational practice—capacity monitoring plus pressure-based diagnosis—and into a preventive control: Alert on sustained high utilization, then confirm with PSI, swap activity and OOM evidence before blaming a service. Those three layers are intentionally separate. The finding explains what the evidence taught me. The practice describes how I diagnose it. The prevention rule describes how I keep the same ambiguity from returning after the next deployment.

There is also a data-model question. The observation has to retain the dimension that matters without encoding unbounded identity. If the question is per node, the node label matters. If it is fleet capacity, an aggregate may be more useful. If it is an event such as a deadlock or OOM kill, a counter over a time window carries different meaning from a current-state gauge. If it is a cached inventory value, age and refresh success are part of the value's contract.

Finally I decide how close this signal is to user impact. Some topics in this series are direct symptoms; others are explanatory evidence. `Linux PSI Changed How I Think About Saturation` belongs at the point where it can reduce investigation time without claiming more certainty than the underlying source provides. That classification determines whether it becomes a page, a warning, a visualization drill-down or simply retained forensic context.

## Competing hypotheses before I touch the live system

I try to write down multiple explanations before making a change. For **Linux PSI Changed How I Think About Saturation**, the candidate set I would test includes: **one workload is creating host-wide contention**; **storage or network pressure is masquerading as CPU/load trouble**; **the physical device or clock is the failing dependency**; **the kernel is reclaiming cache normally**; and **tasks are genuinely stalled for CPU, memory or I/O**. The point is not that all five are equally likely. It is to stop the first plausible graph from becoming the conclusion.

The primary observation `node_memory_MemAvailable_bytes and PSI memory pressure` should eliminate some of those hypotheses, not all of them. I choose the next query or log source by information gain: which check can separate the most remaining explanations at the lowest operational cost? A fresh internal probe versus a failed public probe immediately moves suspicion toward the edge. High memory utilization with low pressure and stable swap activity moves me away from a memory-emergency diagnosis. A stale FreeSWITCH heartbeat with a running container moves the problem from process liveness into worker readiness.

This habit is especially useful on a single host because many symptoms are correlated. Storage pressure can slow databases, logs and containers simultaneously. Host memory pressure can make the monitoring stack itself late. A router or Internet failure can make every public service look broken while the applications are healthy. Explicit competing hypotheses keep correlation from being mistaken for independent failures.

## The observation contract I expect this signal to keep

For `node_memory_MemAvailable_bytes and PSI memory pressure` My goal is a written contract even if it is only a few lines in a runbook. The contract says who produces the data, what unit it uses, which labels are bounded and meaningful, how often it should update, what reset behavior exists, and what missing data means. Without those details an old metric can survive long after its interpretation has changed.

The contract also names the strongest claim the signal supports. Available memory shows what the kernel can still reclaim, while pressure shows whether workloads are actually stalling for memory. That sentence is intentionally narrower than “the service is healthy.” It leaves room for independent evidence and tells future maintainers not to reuse the metric for a stronger conclusion without re-validating it.

Freshness belongs in the contract whenever the producer is not scraped directly. Cache-backed Docker inventory, textfile metrics, heartbeat state and backup timestamps can all remain syntactically valid after the producer stops. I therefore prefer either an explicit age metric or a timestamp from which age can be derived. For direct Prometheus targets, `up` is part of the collection contract but still not the service-health contract.

Finally, the contract includes data sensitivity. Labels and log content must not turn operational telemetry into a secret-disclosure channel. If the observation cannot be collected safely with bounded identity and least privilege, I redesign the collector rather than assuming the monitoring network is trusted.

## Start with the failure, not the exporter

The incident shapel for this article is: **The host looked busy enough that a simple percentage could easily become the whole diagnosis, but Linux memory reclaim makes that misleading.** That wording matters because it describes the operational ambiguity I need to remove. A raw metric has no value until I know what claim I am trying to make from it.

The obvious monitoring mistake is to collapse several layers into one binary state. A process can exist while the application is unusable. A collector can return a number that is already stale. A public service can correctly return a redirect or authorization error and still be healthy. A database can accept a TCP connection while lock contention makes useful queries stall. A host can report high memory utilization while reclaimable page cache means applications are not under pressure. The same general problem appears repeatedly: one layer's “up” is only evidence about that layer.

I therefore map each failure to at least three questions. First, what is the earliest useful signal that something is changing? Second, what is the strongest user-visible symptom I can observe independently? Third, what evidence tells me the monitoring path is alive enough to trust the first two answers? For `Linux PSI Changed How I Think About Saturation`, `node_memory_MemAvailable_bytes and PSI memory pressure` belongs in that chain, but it is never allowed to stand alone if the failure can be confirmed from another layer.

This is also how I decide whether an notification rule belongs on a metric. A signal may be excellent for diagnosis and terrible for paging. Context switches, container block-I/O bytes or database size trends can be valuable evidence without being reasons to interrupt an operator immediately. Conversely, a public probe failure or no-healthy-worker condition may deserve much more direct attention because it is already close to user impact.

## Where this sits in the hserver observability architecture

Linux host monitoring became useful only after I stopped equating utilization with distress. Linux deliberately uses otherwise-idle memory as page cache, so a red “used RAM” gauge can be alarming while the machine is healthy. MemAvailable is a better capacity clue, but even that is not enough by itself: active swap movement, reclaim behavior, OOM evidence and memory PSI tell me whether applications are actually being delayed. The same pattern appears elsewhere. CPU percentage says how time is being consumed, while load and CPU pressure tell me about runnable work waiting for service. Disk throughput says how many bytes move, while latency and I/O pressure tell me whether applications are stalled.

The host is also old physical hardware, so software telemetry is not the whole story. SMART state, SSD temperature, CPU thermal sensors, clock synchronization, network drops and TCP retransmits all belong beside CPU and memory. A filesystem can run out of inodes while gigabytes remain free. A disk can have capacity while latency makes databases unusable. NTP loss can corrupt the meaning of certificate ages, TOTP windows, log ordering and backup freshness. Host observability is therefore a model of kernel and hardware behavior, not a single “system utilization” visualization.

For this article, the component boundary matters as much as the metric. The the live system accepted observability stack includes Prometheus, Grafana, Loki, Alloy, Alertmanager, Blackbox Exporter, Node Exporter, cAdvisor, SMART collection, Docker inventory and deep host/database collectors, plus application-native and external synthetic signals. The latest acceptance artifact records 52/52 accepted Prometheus targets UP, 106 notification rule/recording rules loaded, 15 provisioned visualizations and 10/10 public probes UP.

I deliberately do not interpret those counts as a maturity score. More targets and more rules can make a system worse if they add noise or cost without reducing uncertainty. The useful part is that the inventory is explicit and accepted. When I add a control for `Linux PSI Changed How I Think About Saturation`, I can ask which existing layer already sees part of the problem, whether a new metric is necessary, and how the new observation will be validated after deployment.

## The decision this monitor should let me make

If this telemetry cannot change a decision, it should not automatically consume always-on budget. For **Linux PSI Changed How I Think About Saturation**, the decisions fall into four categories. I may need to intervene immediately because a service contract is already broken. I may need to schedule capacity work because margin is shrinking. I may need to isolate a dependency during incident diagnosis. Or I may decide that the condition is normal and explicitly avoid action.

That last outcome is important. Monitoring is partly a system for proving when *not* to react. Page cache, historical swap, a 302 authentication redirect, a controlled restart, or a busy response from a SIP endpoint can look abnormal without representing infrastructure failure. The metric model should carry enough context to distinguish those cases.

I keep a second constraint: want the monitor to make rollback decisions safer. If a deployment changes `node_memory_MemAvailable_bytes and PSI memory pressure`, I should be able to compare the new state with the accepted baseline and decide whether the change is intended. That is why provenance `b65d5d4` stays attached to the topic. A the live system metric without a known configuration history is harder to use as change evidence.

At scale this decision-centric approach becomes even more important. Hundreds of hosts can produce unlimited telemetry; operator time remains finite. The series therefore treats observability as a decision system rather than a storage system.

## Why this particular collection path won

There are usually several ways to obtain the state behind **Linux PSI Changed How I Think About Saturation**: scrape an existing exporter, query an application API, run a SQL statement, parse logs, inspect the Docker API, read a Linux kernel interface, or publish a small custom metric through the textfile path. I choose among them by authority, cost, security and failure independence.

The closest source is not always the best source. A Docker container metric can tell me process resource use but not whether PostgreSQL sessions are waiting. A log parser can count authentication failures but is a weaker source for current service readiness than a direct state query. A raw TCP probe is cheap but deliberately shallow. A deep query may be authoritative but require credentials or create load. The implementation behind `node_memory_MemAvailable_bytes and PSI memory pressure` is valuable because it sits at the layer that owns the state I need to interpret.

I keep a second constraint: prefer collection paths with visible failure. A custom script that exits silently and leaves yesterday's textfile metric behind is worse than a collector that exports its own success and age. A cache should expose refresh result and age. A database collector should expose whether its query succeeded. A log pipeline should expose drops. The observer has to be observable.

The chosen path therefore reflects more than convenience. It is part of the incident shapel: which component can lie, which credential can expire, which namespace the query sees, and what remains observable when another layer breaks.

## How I reason about a threshold for this topic

I deliberately do not begin with a round number. I begin with the consequence I am trying to avoid and how much reaction time exists. Capacity thresholds such as disk or connection utilization should leave enough margin to investigate before exhaustion. Pressure thresholds should remain high long enough to distinguish real contention from transient scheduling noise. Certificate thresholds are measured in days because the repair process is administrative, not millisecond-sensitive. External availability failures can justify much faster response.

For **Linux PSI Changed How I Think About Saturation**, the next threshold review should use the historical distribution plus the component's configured limit and the time needed to act. If that distribution is not captured in the the live system acceptance artifact artifact, the honest value is **[CURRENT MEASUREMENT NEEDED]**. I deliberately do not derive a the live system page from an attractive number in a blog post.

I keep a second constraint: test both sides of the boundary. A warning threshold should actually enter pending/firing state when a fixture crosses it, and it should resolve when the signal recovers. A critical threshold should not be inhibited by the warning in a way that loses the more serious state. If the signal is a counter, the window should contain enough events to be meaningful. If it is a gauge, the `for` duration and freshness semantics matter more than counter reset behavior.

Thresholds are therefore versioned policy. When topology, workload, resource limits or collector semantics change, I expect the threshold to be reviewed alongside the code.

## The mechanism underneath the graph

Most host metrics ultimately come from kernel interfaces such as `/proc`, `/sys`, netlink or device-specific APIs. Their semantics matter. CPU counters are cumulative time by mode; rates convert them into activity. Load average is a scheduler/work-queue signal, not CPU percentage. `MemAvailable` is an estimate informed by reclaimable memory rather than a count of unused pages. PSI accumulates time in which tasks are stalled for CPU, memory or I/O. Disk latency is derived from cumulative operation and service-time counters, so low-rate windows need care to avoid unstable ratios.

That mechanism matters for `Linux PSI Changed How I Think About Saturation` because two visually similar graphs can have very different semantics. A cumulative counter should normally be turned into a rate or increase over a time window. A gauge can be read directly but still needs freshness. A ratio is meaningless if its denominator is missing, zero or describes a different capacity boundary. A status value needs an explicit state model. A log-derived count depends on the reliability of ingestion and parsing. A synthetic probe depends on where the probe originates and which route it exercises.

I try to preserve units all the way from collection to the panel and notification rule. Seconds should not silently become milliseconds. Bytes should not be compared with decimal “GB” labels without deciding which convention is in use. Percentages should identify their denominator. Ages should be derived from timestamps in a timezone-independent way. These details look small in configuration review and become large during incidents, when the operator is making decisions from the graph under time pressure.

The other subtlety is reset behavior. Counters restart with processes. Container identities change on recreation. database cumulative statistics can reset after engine restart. A visualization that uses raw cumulative values can therefore interpret restart as recovery or huge negative activity. Query functions and labels need to match the lifecycle of the component being measured.

## Implementation: make the observation cheap and reproducible

The implementation is deliberately smaller than the explanation. My goal is the collection path to be boring: deterministic configuration in Git, bounded work on the host, a clear scrape or evaluation cadence, and a result that can be checked after deployment. Repository evidence associated with this topic is `b65d5d4`.

A representative query or configuration fragment is:

```
# Use the node/container PSI series exported by the accepted collectors.
# Exact series selection is deployment-specific; correlate CPU, memory and I/O pressure
# with utilization and latency rather than notification ruleing on percentage alone.
```

The fragment is not meant to be copied blindly into another system. Labels, device names, mount points, job names and custom metric families are deployment-specific. The important point is the shape of the control. Ratios need denominators. Counters need rates or increases over windows. Slow-changing inventory should not be polled at CPU-metric cadence. Authentication-aware probes need status semantics. Freshness-sensitive collectors need age checks. Expensive queries should be recorded or sampled at a cadence that matches the decision they support.

I keep a second constraint: keep configuration ownership separate from runtime evidence. Prometheus rules, scrape configuration, visualizations and collector code live in the reviewed source tree. Runtime acceptance data records what the live system actually observed. Secret values stay out of both metrics and public documentation. This lets me reproduce the monitoring design without turning the monitoring repository into a credential store.

## Query semantics: small expression mistakes become large operational mistakes

The implementation fragment earlier is intentionally small, but even small PromQL or LogQL expressions carry assumptions. Counter queries need a window long enough to contain useful events but short enough to react. Ratios need both numerator and denominator to describe the same population. Aggregation labels decide whether a single bad instance disappears inside a fleet average. `sum`, `avg`, `max` and `count` answer different questions; choosing one because it makes the panel look cleaner is not query engineering.

For `Linux PSI Changed How I Think About Saturation`, I review whether the query behaves during restart, missing series, zero traffic and partial fleet failure. A rate over an idle counter may legitimately be zero. A ratio with no denominator needs protection. `absent()` or target-state logic may be more appropriate than treating missing data as zero. Freshness checks may be required for textfile or cache-backed metrics. A histogram, if present, needs bucket semantics and enough observations before a quantile is meaningful.

I keep a second constraint: avoid encoding the entire diagnosis into one unreadable PromQL expression. Recording rules can name intermediate concepts, make visualizations cheaper and give notification rules a reviewed semantic layer. The cost is extra stored series and another rule dependency, so I work with them where the expression is repeatedly valuable, not merely because the query language permits it.

The same principle applies to logs: a regex that happens to match today's message format is not a durable security signal unless the source and parser are tested. Queries are the live system code when notification rules and incident decisions depend on them.

## Walk the failure from symptom back to cause

A productive way to review this monitor is to imagine a failure and force myself to predict what each layer would show. I deliberately do not claim the following sequence happened unless it is part of the recorded evidence; it is a design exercise for the control.

Start with the user-visible symptom related to **Linux PSI Changed How I Think About Saturation**. The top-level probe or service metric changes first or eventually. I then ask whether the host is still reachable, whether the target is still being scraped, and whether `node_memory_MemAvailable_bytes and PSI memory pressure` is fresh. If the target is down, an old threshold value is no longer the primary evidence; target failure becomes the first branch. If the target is up, I compare the signal with its nearest independent corroborator.

From there I trace downward. A host-pressure signal leads to per-container attribution and kernel logs. A container symptom leads to host resource state and application health. A database symptom leads from reachability to connection, wait, lock and engine state. A public probe failure is compared with the internal probe, DNS/TLS phases and edge logs. A VoIP symptom is separated into signaling, worker and media evidence. A backup symptom is followed through job, artifact, checksum and restore state.

The useful end state is not to prove that every incident follows one tree. It is to make sure each metric has a place in an investigation. If a signal cannot tell me which branch to take next, I question whether it belongs in the always-on monitoring budget.

## How I debug this signal when it looks wrong

I work with a layered debugging order because the fastest way to waste time is to treat the first abnormal graph as the root cause. For **Linux PSI Changed How I Think About Saturation**, I start by proving that the sample is current. I check target or collector health, the timestamp/freshness path, and whether a recent deployment changed labels or collection cadence. If the value can be generated from a custom collector, I compare the exported value with the underlying operating-system, Docker, database or application state.

Next I look for a neighboring signal that should move if my hypothesis is correct. Memory pressure should have some relationship to MemAvailable, swap activity, OOM evidence or workload latency. Storage latency should have some relationship to I/O pressure or application waits. Container I/O should reconcile with host disk activity. A database saturation hypothesis should be visible in connection, wait or lock state. A public availability failure should be compared with an internal probe so I can separate application failure from DNS, TLS, tunnel or edge failure.

Only after that do I broaden into logs. Logs are best when the failure domain is already smaller: kernel OOM records, Docker daemon warnings, authentication failures, Alloy/Loki pipeline errors, database messages or VoIP-specific events. This keeps me from searching an unbounded log corpus for an event I have not yet defined.

The last step is to check the monitoring system itself. A quiet visualization can be caused by a missing target. A stable line can be a stale sample. A zero-notification rule page can coexist with rule-evaluation failures. My goal is evidence that the observer is alive before I trust the observation.

## The false-positive and false-negative traps

Every monitoring decision has at least two ways to be wrong. A false positive declares a failure when the system is operating within its intended semantics. A false negative keeps the visualization green while the service contract is broken. `Linux PSI Changed How I Think About Saturation` is useful only if I can describe both.

A common false positive is reading a state without duration or context. Non-zero swap can be historical. High CPU can be productive work. A protected HTTP endpoint can return 302, 401 or 403 because authentication is functioning. A brief container restart can be a deployment. A temporarily high database connection count can be harmless if capacity and latency remain healthy. These cases need windows, denominators or state semantics before they become incidents.

The false negative is usually more dangerous. A target can scrape successfully while its downstream dependency is broken. A stale custom metric can remain below threshold after its collector died. A database socket can accept connections while waits or locks stop useful work. A FreeSWITCH process can run while the worker heartbeat is stale. A backup archive can exist while restore verification has not succeeded. Those failures are why the architecture uses independent layers instead of treating one green signal as global truth.

When I review a rule or panel, I explicitly ask: what normal condition could make this look bad, and what bad condition could make this look normal? That question often produces a better second metric than adding another threshold to the first one.

## The monitoring tax for this signal

On this machine, collection cost is part of the design review. The the live system host has roughly 7.1 GiB of usable RAM, and the observability stack has occupied a meaningful fraction of that budget in different acceptance snapshots. The low-RAM artifact recorded the low-RAM acceptance artifact recorded a 726.2 MiB observability-memory sample; another aggregate runtime field recorded 841,814,016 bytes, so I classify both as snapshot evidence rather than a universal footprint. Those snapshots cover different accounting views, so I deliberately do not collapse them into one magic “monitoring uses X MiB” claim. I work with them to prove that observability is large enough to manage deliberately.

The cAdvisor case is the clearest example: cAdvisor measured at 428.2 MiB before the low-RAM work and 27.87 MiB in one post-change sample, with an observed steady range around 20–28 MiB. That improvement came from removing work whose cost exceeded its operational value, not from disabling container observability. The same reasoning applies to `Linux PSI Changed How I Think About Saturation`. I ask how often the state can meaningfully change, how quickly I need to react, how many series or log streams the observation creates, whether a cheaper collector can answer the same question, and whether the query belongs at scrape time, recording-rule time or investigation time.

There is also a human monitoring tax. Every notification rule that cannot lead to an action consumes attention. Every visualization panel that lacks a clear question makes incidents slower. Every high-cardinality label creates future storage and query work. The resource budget therefore includes RAM, CPU, disk, network, series count, log streams and operator cognition.

On a larger host I might tolerate a more expensive collector to gain richer diagnostics. For this server the default is the opposite: collect the smallest reliable signal that preserves the failure evidence I need, then keep deeper inspection available on demand.

## Operational limits and thresholds are configuration, not physics

Thresholds in this system are chosen from capacity, consequence and response time. Disk warning/critical bands, certificate windows, notification rule `for:` durations, heartbeat age, memory budgets and SLO burn-rate factors all express policy. I document them as current the live system choices, not constants of Linux or Prometheus.

That distinction matters during growth. If workload changes, a threshold that once provided useful warning may become permanently noisy. If a collector is optimized, an observability-memory budget may be tightened. If a service moves off-host, its failure domain changes and an old notification rule relationship may no longer apply. If public traffic increases, SLO windows may have enough events to use a different statistical model.

For `Linux PSI Changed How I Think About Saturation`, I would review the threshold whenever the component version, workload, resource limit or topology materially changes. I would also inspect the historical distribution before tightening it. A threshold selected only from a desired round number is less defensible than one derived from observed normal behavior plus an explicit safety margin.

Where the the live system acceptance artifact evidence does not contain the distribution needed to justify a new threshold, the article leaves **[CURRENT MEASUREMENT NEEDED]**. That is not an incomplete monitoring practice; it is a refusal to pretend policy has empirical support that has not yet been collected.

## Turning the observation into an notification rule without creating noise

Not every article in this series ends with a page. Some of the best signals are diagnostic. When I do notification rule, I separate **prediction**, **saturation**, and **symptom**. Prediction covers conditions such as disk capacity or certificate expiry where action before failure is possible. Saturation covers sustained pressure or exhausted pools. Symptoms cover conditions such as a failed public probe, no healthy SIP worker, or unsuccessful restore verification where the service contract is already affected.

The rule duration has to fit the failure. A single scrape miss or short deployment restart should not create an incident. A total public outage should not sit pending for an arbitrary long `for:` window simply because another resource rule uses ten minutes. Warning and critical labels are response contracts: warning means investigate or schedule action before the margin disappears; critical means the operating state is already outside the tolerated envelope or approaching it fast enough to require immediate attention.

I keep a second constraint: ask what other notification rule will fire at the same time. If host loss makes every public service fail, paging separately for Grafana, OTA, authentication, gateway and VoIP adds noise without information. Grouping and inhibition should preserve useful symptoms while making the likely root event obvious. Resolution is part of the lifecycle too. The latest accepted notification evidence recorded external notification counters in the acceptance artifact: 13 success, 0 failure, 6 resolved; that is a snapshot of delivery behavior, not an SLA claim.

For `Linux PSI Changed How I Think About Saturation`, the notification rule is successful only if its annotation tells me what was observed, over what window, which visualization or runbook to open next, and what secondary signal can confirm the hypothesis.

## Acceptance: prove the monitor after changing it

I deliberately do not treat a configuration commit as proof that monitoring works. After meaningful observability changes I compare the desired state in Git with runtime acceptance. The the live system artifact records 52/52 accepted Prometheus targets UP, 106 notification rule/recording rules loaded, 0 firing and 0 pending notification rules, 27,578 active Prometheus series, against a 27,414-series acceptance baseline, 10/10 public probes UP, 9/9 database probes UP and 35 monitored configuration files with zero drift in the latest runtime sample. Those numbers are useful because they make blind spots and accidental cardinality growth measurable after deployment.

The validation depends on the feature. A scrape change should prove the target is UP and the expected series exists. A relabel change should prove the required visualization and notification rule queries still return data. A log-pipeline change should prove cursor continuity and check drop counters. A public probe should be exercised against both healthy and intentionally invalid behavior. A backup control should be followed by checksum and restore evidence. A notification change should send a synthetic notification rule and verify both firing and resolved delivery.

Where safe, I prefer failure injection to passive confidence. The external dead-man watcher was tested by forcing a synthetic outage: the hosted workflow failed, an incident issue was created, recovery later passed and the issue closed. That sequence proved more than reading the workflow YAML. The same idea scales down to small controls: temporarily make a test target fail, expire a synthetic sample, or use a fixture that triggers the rule without damaging the live system.

## Measurements I would capture before changing this again

If I revisit this control, My goal is a before/after dataset rather than a subjective impression. At minimum I would record the primary signal, its update age, target health, the relevant host/container resource cost, Prometheus active-series count and the query or collection duration if available. For a logging change I would also record ingestion/drop counters and Loki storage growth. For a probe change I would preserve phase timing and expected status behavior. For a database change I would capture the engine state that justifies the query cadence.

Some current values are already accepted: 27,578 active Prometheus series, against a 27,414-series acceptance baseline; cAdvisor measured at 428.2 MiB before the low-RAM work and 27.87 MiB in one post-change sample, with an observed steady range around 20–28 MiB; 52/52 accepted Prometheus targets UP; and 106 notification rule/recording rules loaded. Where this article needs a value that the acceptance artifact does not contain—such as an exact current query latency, per-component RAM split, database size, call volume or request rate—the correct value is **[CURRENT MEASUREMENT NEEDED]**. I would rather leave that marker than create false precision in a personal engineering record.

I keep a second constraint: keep measurement windows long enough to catch steady-state behavior. A container immediately after restart can look very different after caches warm. A five-minute resource sample can miss daily batch work. Retention and series changes may need hours to become obvious. The acceptance window should match the phenomenon being evaluated, not the time I am willing to stare at the terminal.

## Capacity math I work with instead of intuition

The simplest capacity calculation is sample multiplication. If a job exports `S` series every `I` seconds, the rough sample count over a day is `S * 86400 / I` before considering churn, compression and block behavior. Halving the scrape interval doubles sample density. Adding a label with ten stable values can multiply a metric family by roughly ten. Turning an unbounded identifier into a label can be far worse because the population grows with traffic rather than with infrastructure.

I deliberately do not use that arithmetic as a precise Prometheus storage estimator; WAL encoding, chunks, label indexes and compression make byte cost more complex. I work with it to compare design choices before deploying them. The the live system acceptance artifact point of 27,578 active series gives me a local baseline. If a small visualization feature adds thousands of active series, that is visible as an architectural cost even before disk use becomes alarming.

Memory budgeting uses the same idea. With roughly 7.1 GiB usable RAM, a 400 MiB monitoring regression is not “only a few hundred megabytes.” It competes with the live system. The cAdvisor before/after evidence showed why percentage-of-host thinking is useful. I track the observability aggregate, large individual processes and host MemAvailable/pressure together rather than assigning one static memory number to the entire stack forever.

For `Linux PSI Changed How I Think About Saturation`, any new collector, label or cadence change should therefore answer two questions: how much additional evidence does it buy, and what the live system resource is being spent to buy it?

## What the current accepted system says

The 2026-09-15 acceptance snapshot gives me a concrete reference point while writing this series. It records 52/52 accepted Prometheus targets UP, 106 notification rule/recording rules loaded, 0 firing and 0 pending notification rules, and 15 provisioned visualizations. Prometheus reported 27,578 active Prometheus series, against a 27,414-series acceptance baseline. Public probing reported 10/10 public probes UP; database probing reported 9/9 database probes UP. The accepted configuration manifest reported 35 monitored configuration files with zero drift in the latest runtime sample.

For storage and retention, Prometheus retention set to about 30 days with a 15 GB size cap; Loki retention set to 168 hours. For hardware evidence, SMART status healthy in the acceptance artifact, with a 49 C device-temperature sample. For recovery, encrypted DR verification PASS, required payload PASS, internal checksum PASS, off-host pull PASS, and restore verification PASS. For OpenBao, main OpenBao initialized and unsealed with Transit auto-unseal; same-host seal node initialized and unsealed with no host-published ports. These values are intentionally described with a date because they are not permanent properties of the architecture. They are evidence that the system reached a known state after a particular round of changes.

This distinction is important for `Linux PSI Changed How I Think About Saturation`. Monitoring documentation tends to age badly when it turns an observation into a law. I would rather write “27,578 active series in this acceptance snapshot” than imply that 27,578 is a target, a limit or a recommendation. The same applies to cAdvisor memory, disk temperature, visualization count and notification rule-rule count. This architecture should survive changing numbers because the interpretation rules remain explicit.

## What I would change at larger scale

The small-server version optimizes for bounded cost and direct inspectability. At fleet scale I would preserve the semantic model but move some responsibilities. Metrics storage could move off the application host. Long-term retention could use a system designed for remote or object-backed storage. Loki could live on a dedicated node. Exporter and collector work could be distributed closer to the workloads while query and notification rule evaluation stay centralized. High-availability Alertmanager and independent monitoring storage would reduce shared failure domains.

I would not, however, replace `node_memory_MemAvailable_bytes and PSI memory pressure` with a generic “enterprise monitoring” product and call the problem solved. The key question remains what the observation proves. If the signal is about Linux pressure, the kernel semantics remain. If it is about database locks, the engine semantics remain. If it is about SIP versus RTP, the protocol boundaries remain. If it is about dead-man monitoring, the observer still has to live outside the failure domain.

Scale primarily changes collection topology, retention, redundancy and automation. It does not remove the need to define failure semantics. In fact, larger systems punish ambiguous metrics more severely because a noisy or high-cardinality mistake multiplies across more hosts and more operators.

## Deep-dive notes: separating mechanism from policy

A recurring source of monitoring bugs is mixing mechanism with policy. The mechanism answers how the observation is produced: kernel counter, cgroup metric, SQL query, log parser, HTTP probe, application counter or external workflow. Policy answers what the organization does when that observation changes. `node_memory_MemAvailable_bytes and PSI memory pressure` is mechanism. The threshold, window, severity, grouping and escalation path are policy.

Keeping those separate makes the system easier to evolve. I can improve collection without changing the paging contract, or change a warning threshold after capacity review without rewriting the collector. The design also makes testing clearer. Collector tests validate units, labels, freshness and failure behavior. Rule tests validate expressions and state transitions. End-to-end tests validate that an actual synthetic condition reaches the operator and resolves correctly.

The same separation applies to desired state and evidence. Git defines reviewed configuration, but Git cannot prove the running system loaded it. Runtime acceptance proves what the live system observed, but runtime state is not a reproducible configuration source. The the live system manifest model bridges the two by hashing approved monitored configuration and measuring drift without exporting secret values.

For this topic, I would treat a future scale-out as another policy change rather than an excuse to discard the semantic model. A managed metrics backend, Kubernetes, multiple nodes or cloud load balancers change topology. They do not change what memory pressure means, what a deadlock means, what a stale heartbeat means, or why a probe outside the failure domain is stronger evidence of host death than a local visualization.

## What I keep from this decision

I keep **Linux PSI Changed How I Think About Saturation** in this series because it shows the difference between collecting telemetry and engineering evidence. The control is useful because I know its acquisition cost, expected cadence, incident shapes, corroborating signals and response path. That is the standard I now use before adding another metric or notification rule to hserver.

The server is still an old Mac mini. That constraint has not stopped the monitoring system from becoming serious. It has forced every layer to be explicit about what it is worth. For me that is the more interesting engineering result: the live system-grade observability is less about how many products are installed and more about whether the evidence is sufficient, current, independent where necessary, and cheap enough that the observer does not become the outage.
