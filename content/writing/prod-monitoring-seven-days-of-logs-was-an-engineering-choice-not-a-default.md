---
title: Seven Days of Logs Was an Engineering Choice, Not a Default
url: /posts/prod-monitoring-seven-days-of-logs-was-an-engineering-choice-not-a-default.html
date: '2026-09-15'
read_time: 35
excerpt: A production-engineering deep dive into seven days of logs was an engineering
  choice, not a default, grounded in the 2014 Mac mini hserver observability stack
  and its accepted runtime evidence.
topic: observability-monitoring
tags:
- loki
- grafana-alloy
- logs
- journald
draft: false
featured: false
language: en
eyebrow: 'Production Monitoring: Loki, Alloy & Logging · advanced'
outputs:
- url: /posts/prod-monitoring-seven-days-of-logs-was-an-engineering-choice-not-a-default.html
  template: cms/templates/posts/posts--prod-monitoring-seven-days-of-logs-was-an-engineering-choice-not-a-default.tpl
  source: cms/templates/posts/posts--prod-monitoring-seven-days-of-logs-was-an-engineering-choice-not-a-default.json
---

The useful question behind **Seven Days of Logs Was an Engineering Choice, Not a Default** was not whether I could collect another metric. It was whether the metric would reduce uncertainty during a the production stack failure on a very small machine.

The host is 2014 Apple Mac mini running Linux, with roughly 7.1 GiB usable RAM from an 8 GB-class machine. Applications, databases, networking, authentication, OTA, OpenBao, VoIP and the observability stack share the same limited CPU, memory and storage. That makes monitoring part of the workload rather than something outside it. The central failure I am trying to avoid is not merely “a metric went high.” I am trying to preserve enough telemetry evidence to tell whether a user-facing service is degrading, which dependency owns the problem, whether the signal is current, and whether the monitoring path itself is still trustworthy.

For this specific problem the primary observation point is `Prometheus 30-day retention plus 15 GB size cap and Loki seven-day retention`. The short the production stack note that preceded this article captured the core finding: Time and size constraints protect different fault conditions: history growth over time and sudden cardinality or ingestion expansion. This long-form version goes further: what that signal really proves, which nearby signals can falsify my first hypothesis, how I implement and detection rule on it, what it costs on this host, and how I would redesign the same control at larger scale.

The numbers in this article are not generic benchmarks. When I mention 27,578 active Prometheus series, against a 27,414-series acceptance baseline, cAdvisor measured at 428.2 MiB before the low-RAM work and 27.87 MiB in one post-change sample, with an observed steady range around 20–28 MiB, or any other concrete value, I mean the 2026-09-15 acceptance snapshot unless I explicitly say otherwise. If a current value is not present in the accepted telemetry evidence, I leave `[CURRENT MEASUREMENT NEEDED]` rather than inventing a number.

## The engineering question specific to this article

The short version of the problem is not “how do I graph Seven Days of Logs Was an Engineering Choice, Not a Default?” It is: **Keeping thirty days of Prometheus data is useful until series growth causes the TSDB to consume more disk than the host can safely spare.** That failure can be confused with neighboring conditions, which is why the primary observation is `Prometheus 30-day retention plus 15 GB size cap and Loki seven-day retention` rather than a generic process-up flag.

The present the production stack conclusion is specific: Time and size constraints protect different fault conditions: history growth over time and sudden cardinality or ingestion expansion. I turn that conclusion into an operational practice—bounded telemetry retention—and into a preventive control: Set retention from incident-investigation needs and host capacity, then monitor actual storage so limits remain appropriate as the system grows. Those three layers are intentionally separate. The finding explains what the telemetry evidence taught me. The practice describes how I diagnose it. The prevention rule describes how I keep the same ambiguity from returning after the next deployment.

There is also a data-model question. The observation has to retain the dimension that matters without encoding unbounded identity. If the question is per node, the node label matters. If it is fleet capacity, an aggregate may be more useful. If it is an event such as a deadlock or OOM kill, a counter over a time window carries different meaning from a current-state gauge. If it is a cached inventory value, age and refresh success are part of the value's contract.

Finally I decide how close this signal is to user impact. Some topics in this series are direct symptoms; others are explanatory telemetry evidence. `Seven Days of Logs Was an Engineering Choice, Not a Default` belongs at the point where it can reduce investigation time without claiming more certainty than the underlying source provides. That classification determines whether it becomes a page, a warning, a monitoring view drill-down or simply retained forensic context.

## Competing hypotheses before I touch the production stack

I try to write down multiple explanations before making a change. For **Seven Days of Logs Was an Engineering Choice, Not a Default**, the candidate set I would test includes: **the source stopped producing events**; **Alloy lost or duplicated position state**; **Docker discovery still references deleted identities**; **Loki accepted data but stream cardinality/storage cost grew unexpectedly**; and **the log-derived detection rule went quiet because the pipeline dropped telemetry evidence**. The point is not that all five are equally likely. It is to stop the first plausible graph from becoming the conclusion.

The primary observation `Prometheus 30-day retention plus 15 GB size cap and Loki seven-day retention` should eliminate some of those hypotheses, not all of them. I choose the next query or log source by information gain: which check can separate the most remaining explanations at the lowest operational cost? A fresh internal probe versus a failed public probe immediately moves suspicion toward the edge. High memory utilization with low pressure and stable swap activity moves me away from a memory-emergency diagnosis. A stale FreeSWITCH heartbeat with a running container moves the problem from process liveness into worker readiness.

This habit is especially useful on a single host because many symptoms are correlated. Storage pressure can slow databases, logs and containers simultaneously. Host memory pressure can make the monitoring stack itself late. A router or Internet failure can make every public service look broken while the applications are healthy. Explicit competing hypotheses keep correlation from being mistaken for independent failures.

## The observation contract I expect this signal to keep

For `Prometheus 30-day retention plus 15 GB size cap and Loki seven-day retention` I am trying to preserve a written contract even if it is only a few lines in a runbook. The contract says who produces the data, what unit it uses, which labels are bounded and meaningful, how often it should update, what reset behavior exists, and what missing data means. Without those details an old metric can survive long after its interpretation has changed.

The contract also names the strongest claim the signal supports. Time and size constraints protect different fault conditions: history growth over time and sudden cardinality or ingestion expansion. That sentence is intentionally narrower than “the service is healthy.” It leaves room for independent telemetry evidence and tells future maintainers not to reuse the metric for a stronger conclusion without re-validating it.

Freshness belongs in the contract whenever the producer is not scraped directly. Cache-backed Docker inventory, textfile metrics, heartbeat state and backup timestamps can all remain syntactically valid after the producer stops. I therefore prefer either an explicit age metric or a timestamp from which age can be derived. For direct Prometheus targets, `up` is part of the collection contract but still not the service-health contract.

Finally, the contract includes data sensitivity. Labels and log content must not turn operational telemetry into a secret-disclosure channel. If the observation cannot be collected safely with bounded identity and least privilege, I redesign the collector rather than assuming the monitoring network is trusted.

## Start with the failure, not the exporter

The fault conditionl for this article is: **Keeping thirty days of Prometheus data is useful until series growth causes the TSDB to consume more disk than the host can safely spare.** That wording matters because it describes the operational ambiguity I need to remove. A raw metric has no value until I know what claim I am trying to make from it.

The obvious monitoring mistake is to collapse several layers into one binary state. A process can exist while the application is unusable. A collector can return a number that is already stale. A public service can correctly return a redirect or authorization error and still be healthy. A database can accept a TCP connection while lock contention makes useful queries stall. A host can report high memory utilization while reclaimable page cache means applications are not under pressure. The same general problem appears repeatedly: one layer's “up” is only telemetry evidence about that layer.

I therefore map each failure to at least three questions. First, what is the earliest useful signal that something is changing? Second, what is the strongest user-visible symptom I can observe independently? Third, what telemetry evidence tells me the monitoring path is alive enough to trust the first two answers? For `Seven Days of Logs Was an Engineering Choice, Not a Default`, `Prometheus 30-day retention plus 15 GB size cap and Loki seven-day retention` belongs in that chain, but it is never allowed to stand alone if the failure can be confirmed from another layer.

This is also how I decide whether an detection rule belongs on a metric. A signal may be excellent for diagnosis and terrible for paging. Context switches, container block-I/O bytes or database size trends can be valuable telemetry evidence without being reasons to interrupt an operator immediately. Conversely, a public probe failure or no-healthy-worker condition may deserve much more direct attention because it is already close to user impact.

## Where this sits in the hserver observability architecture

Logs are event telemetry evidence, not a replacement for metrics. Prometheus is good at answering “is the rate increasing?” or “did a threshold remain exceeded?” Loki is better for the individual SSH attempt, kernel OOM message, Docker daemon warning or authentication failure that explains what happened. Alloy sits in the collection path, reading Docker and systemd journal sources and shipping selected streams to Loki. The pipeline itself has state: journald cursors, Docker discovery state, write queues and dropped-entry counters.

The stale-container incident exposed why discovery correctness matters. Containers are recreated and their IDs disappear. A collector that remembers creation but does not reconcile deletion can repeatedly inspect objects that no longer exist, producing noise from the observability system rather than from the production stack. Label design matters for the same reason it matters in Prometheus. Stable dimensions such as service or source are useful labels; high-cardinality values such as request IDs or source IPs are generally better left in log content. Loki retention is currently seven days, a deliberate disk-versus-forensics decision on a constrained host.

For this article, the component boundary matters as much as the metric. The present accepted observability stack includes Prometheus, Grafana, Loki, Alloy, Alertmanager, Blackbox Exporter, Node Exporter, cAdvisor, SMART collection, Docker inventory and deep host/database collectors, plus application-native and external synthetic signals. The latest acceptance artifact records 52/52 accepted Prometheus targets UP, 106 detection rule/recording rules loaded, 15 provisioned monitoring views and 10/10 public probes UP.

I make a point not to interpret those counts as a maturity score. More targets and more rules can make a system worse if they add noise or cost without reducing uncertainty. The useful part is that the inventory is explicit and accepted. When I add a control for `Seven Days of Logs Was an Engineering Choice, Not a Default`, I can ask which existing layer already sees part of the problem, whether a new metric is necessary, and how the new observation will be validated after deployment.

## The decision this monitor should let me make

If this telemetry cannot change a decision, it should not automatically consume always-on budget. For **Seven Days of Logs Was an Engineering Choice, Not a Default**, the decisions fall into four categories. I may need to intervene immediately because a service contract is already broken. I may need to schedule capacity work because margin is shrinking. I may need to isolate a dependency during incident diagnosis. Or I may decide that the condition is normal and explicitly avoid action.

That last outcome is important. Monitoring is partly a system for proving when *not* to react. Page cache, historical swap, a 302 authentication redirect, a controlled restart, or a busy response from a SIP endpoint can look abnormal without representing infrastructure failure. The metric model should carry enough context to distinguish those cases.

I add one more check: want the monitor to make rollback decisions safer. If a deployment changes `Prometheus 30-day retention plus 15 GB size cap and Loki seven-day retention`, I should be able to compare the new state with the accepted baseline and decide whether the change is intended. That is why provenance `b65d5d4` stays attached to the topic. A the production stack metric without a known configuration history is harder to use as change telemetry evidence.

At scale this decision-centric approach becomes even more important. Hundreds of hosts can produce unlimited telemetry; operator time remains finite. The series therefore treats observability as a decision system rather than a storage system.

## Why this particular collection path won

There are usually several ways to obtain the state behind **Seven Days of Logs Was an Engineering Choice, Not a Default**: scrape an existing exporter, query an application API, run a SQL statement, parse logs, inspect the Docker API, read a Linux kernel interface, or publish a small custom metric through the textfile path. I choose among them by authority, cost, security and failure independence.

The closest source is not always the best source. A Docker container metric can tell me process resource use but not whether PostgreSQL sessions are waiting. A log parser can count authentication failures but is a weaker source for current service readiness than a direct state query. A raw TCP probe is cheap but deliberately shallow. A deep query may be authoritative but require credentials or create load. The runtime mechanism behind `Prometheus 30-day retention plus 15 GB size cap and Loki seven-day retention` is valuable because it sits at the layer that owns the state I need to interpret.

I add one more check: prefer collection paths with visible failure. A custom script that exits silently and leaves yesterday's textfile metric behind is worse than a collector that exports its own success and age. A cache should expose refresh result and age. A database collector should expose whether its query succeeded. A log pipeline should expose drops. The observer has to be observable.

The chosen path therefore reflects more than convenience. It is part of the fault conditionl: which component can lie, which credential can expire, which namespace the query sees, and what remains observable when another layer breaks.

## How I reason about a threshold for this topic

I make a point not to begin with a round number. I begin with the consequence I am trying to avoid and how much reaction time exists. Capacity thresholds such as disk or connection utilization should leave enough margin to investigate before exhaustion. Pressure thresholds should remain high long enough to distinguish real contention from transient scheduling noise. Certificate thresholds are measured in days because the repair process is administrative, not millisecond-sensitive. External availability failures can justify much faster response.

For **Seven Days of Logs Was an Engineering Choice, Not a Default**, the next threshold review should use the historical distribution plus the component's configured limit and the time needed to act. If that distribution is not captured in the current acceptance artifact, the honest value is **[CURRENT MEASUREMENT NEEDED]**. I make a point not to derive a the production stack page from an attractive number in a blog post.

I add one more check: test both sides of the boundary. A warning threshold should actually enter pending/firing state when a fixture crosses it, and it should resolve when the signal recovers. A critical threshold should not be inhibited by the warning in a way that loses the more serious state. If the signal is a counter, the window should contain enough events to be meaningful. If it is a gauge, the `for` duration and freshness semantics matter more than counter reset behavior.

Thresholds are therefore versioned policy. When topology, workload, resource limits or collector semantics change, I expect the threshold to be reviewed alongside the code.

## The mechanism underneath the graph

Loki indexes labels rather than full log text. Every unique label set creates a stream, which is why source IPs, request IDs and container IDs are dangerous as labels when they change without bound. Alloy discovery produces targets, applies relabeling and maintains read state such as journald cursors. Docker recreation changes object identities, so discovery reconciliation has to remove stale targets. The write path must also expose dropped entries or bytes; otherwise successful collector liveness can coexist with incomplete telemetry evidence.

That mechanism matters for `Seven Days of Logs Was an Engineering Choice, Not a Default` because two visually similar graphs can have very different semantics. A cumulative counter should normally be turned into a rate or increase over a time window. A gauge can be read directly but still needs freshness. A ratio is meaningless if its denominator is missing, zero or describes a different capacity boundary. A status value needs an explicit state model. A log-derived count depends on the reliability of ingestion and parsing. A synthetic probe depends on where the probe originates and which route it exercises.

I try to preserve units all the way from collection to the panel and detection rule. Seconds should not silently become milliseconds. Bytes should not be compared with decimal “GB” labels without deciding which convention is in use. Percentages should identify their denominator. Ages should be derived from timestamps in a timezone-independent way. These details look small in configuration review and become large during incidents, when the operator is making decisions from the graph under time pressure.

The other subtlety is reset behavior. Counters restart with processes. Container identities change on recreation. database cumulative statistics can reset after engine restart. A monitoring view that uses raw cumulative values can therefore interpret restart as recovery or huge negative activity. Query functions and labels need to match the lifecycle of the component being measured.

## Implementation: make the observation cheap and reproducible

The runtime mechanism is deliberately smaller than the explanation. I am trying to preserve the collection path to be boring: deterministic configuration in Git, bounded work on the host, a clear scrape or evaluation cadence, and a result that can be checked after deployment. Repository telemetry evidence associated with this topic is `b65d5d4`.

A representative query or configuration fragment is:

```
Loki retention = 168h
# Monitor ingestion rate, dropped entries/bytes and Loki disk use before extending retention.
```

The fragment is not meant to be copied blindly into another system. Labels, device names, mount points, job names and custom metric families are deployment-specific. The important point is the shape of the control. Ratios need denominators. Counters need rates or increases over windows. Slow-changing inventory should not be polled at CPU-metric cadence. Authentication-aware probes need status semantics. Freshness-sensitive collectors need age checks. Expensive queries should be recorded or sampled at a cadence that matches the decision they support.

I add one more check: keep configuration ownership separate from runtime telemetry evidence. Prometheus rules, scrape configuration, monitoring views and collector code live in the reviewed source tree. Runtime acceptance data records what the production stack actually observed. Secret values stay out of both metrics and public documentation. This lets me reproduce the monitoring design without turning the monitoring repository into a credential store.

## Query semantics: small expression mistakes become large operational mistakes

The runtime mechanism fragment earlier is intentionally small, but even small PromQL or LogQL expressions carry assumptions. Counter queries need a window long enough to contain useful events but short enough to react. Ratios need both numerator and denominator to describe the same population. Aggregation labels decide whether a single bad instance disappears inside a fleet average. `sum`, `avg`, `max` and `count` answer different questions; choosing one because it makes the panel look cleaner is not query engineering.

For `Seven Days of Logs Was an Engineering Choice, Not a Default`, I review whether the query behaves during restart, missing series, zero traffic and partial fleet failure. A rate over an idle counter may legitimately be zero. A ratio with no denominator needs protection. `absent()` or target-state logic may be more appropriate than treating missing data as zero. Freshness checks may be required for textfile or cache-backed metrics. A histogram, if present, needs bucket semantics and enough observations before a quantile is meaningful.

I add one more check: avoid encoding the entire diagnosis into one unreadable PromQL expression. Recording rules can name intermediate concepts, make monitoring views cheaper and give detection rules a reviewed semantic layer. The cost is extra stored series and another rule dependency, so I use them where the expression is repeatedly valuable, not merely because the query language permits it.

The same principle applies to logs: a regex that happens to match today's message format is not a durable security signal unless the source and parser are tested. Queries are the production stack code when detection rules and incident decisions depend on them.

## Walk the failure from symptom back to cause

A defensible way to review this monitor is to imagine a failure and force myself to predict what each layer would show. I make a point not to claim the following sequence happened unless it is part of the recorded telemetry evidence; it is a design exercise for the control.

Start with the user-visible symptom related to **Seven Days of Logs Was an Engineering Choice, Not a Default**. The top-level probe or service metric changes first or eventually. I then ask whether the host is still reachable, whether the target is still being scraped, and whether `Prometheus 30-day retention plus 15 GB size cap and Loki seven-day retention` is fresh. If the target is down, an old threshold value is no longer the primary telemetry evidence; target failure becomes the first branch. If the target is up, I compare the signal with its nearest independent corroborator.

From there I trace downward. A host-pressure signal leads to per-container attribution and kernel logs. A container symptom leads to host resource state and application health. A database symptom leads from reachability to connection, wait, lock and engine state. A public probe failure is compared with the internal probe, DNS/TLS phases and edge logs. A VoIP symptom is separated into signaling, worker and media telemetry evidence. A backup symptom is followed through job, artifact, checksum and restore state.

What I want from it is not to prove that every incident follows one tree. It is to make sure each metric has a place in an investigation. If a signal cannot tell me which branch to take next, I question whether it belongs in the always-on monitoring budget.

## How I debug this signal when it looks wrong

I use a layered debugging order because the fastest way to waste time is to treat the first abnormal graph as the root cause. For **Seven Days of Logs Was an Engineering Choice, Not a Default**, I start by proving that the sample is current. I check target or collector health, the timestamp/freshness path, and whether a recent deployment changed labels or collection cadence. If the value can be generated from a custom collector, I compare the exported value with the underlying operating-system, Docker, database or application state.

Next I look for a neighboring signal that should move if my hypothesis is correct. Memory pressure should have some relationship to MemAvailable, swap activity, OOM telemetry evidence or workload latency. Storage latency should have some relationship to I/O pressure or application waits. Container I/O should reconcile with host disk activity. A database saturation hypothesis should be visible in connection, wait or lock state. A public availability failure should be compared with an internal probe so I can separate application failure from DNS, TLS, tunnel or edge failure.

Only after that do I broaden into logs. Logs are best when the failure domain is already smaller: kernel OOM records, Docker daemon warnings, authentication failures, Alloy/Loki pipeline errors, database messages or VoIP-specific events. This keeps me from searching an unbounded log corpus for an event I have not yet defined.

The last step is to check the monitoring system itself. A quiet monitoring view can be caused by a missing target. A stable line can be a stale sample. A zero-detection rule page can coexist with rule-evaluation failures. I am trying to preserve telemetry evidence that the observer is alive before I trust the observation.

## The hserver case that shaped this part of the design

The Alloy stale-container problem is the logging case study. Docker recreation changes container IDs, and the collector repeatedly attempted to inspect objects that no longer existed. That noise came from the observability system, not the application. Fixing discovery/reconciliation reduced stale-object noise and reinforced a design rule: dynamic discovery needs deletion semantics, persisted read position and drop monitoring if logs are going to be trusted as incident telemetry evidence.

I use that case as a guardrail for `Seven Days of Logs Was an Engineering Choice, Not a Default` because it prevents the discussion from becoming a generic monitoring tutorial. The interesting question is not whether another platform supports the same metric. It is what decision the signal enabled on this constrained the production stack host, what cost it imposed, and what telemetry evidence proved that the change improved rather than merely rearranged the system.

It additionally keeps causality honest. A before/after measurement is telemetry evidence for this configuration at that time. It is not a universal benchmark for cAdvisor, Prometheus, Docker, OpenBao or any database engine. When the article makes a recommendation, the recommendation is about the engineering method—measure, isolate cost, preserve the useful signal, verify the new fault conditions—not about assuming another machine will reproduce the same number.

## What would make this monitor lie?

I ask this question explicitly because most monitoring failures are not fabricated numbers; they are numbers interpreted outside their validity. `Prometheus 30-day retention plus 15 GB size cap and Loki seven-day retention` can become misleading if its collector is stale, labels change, the underlying source resets, the query aggregates away the failing member, the scrape path observes a different network namespace, or the monitored component changes semantics after an upgrade.

Caching creates another class of lies. The Docker storage inventory is deliberately cached because continuous filesystem inspection was too expensive. A cache-backed metric is only trustworthy when cache age and refresh success are visible. Textfile metrics have the same issue if the producer stops updating them. Database-derived metrics can lie by omission if the collector account loses access to a system view. Log-derived metrics can go quiet because Alloy or Loki is dropping data rather than because the event stopped happening.

Authentication and synthetic probes can lie through overly permissive expectations. Following redirects blindly may turn an application failure into a successful login-page response. Accepting every status code may hide a broken route. Requiring only 200 may create the opposite error and call a healthy access-control response an outage. The probe has to encode the intended contract.

My response to these risks is not distrust of monitoring. It is meta-monitoring, freshness, independent telemetry evidence and explicit UNKNOWN states when the observation path cannot make a strong claim.

## The monitoring tax for this signal

On this machine, collection cost is part of the design review. The present host has roughly 7.1 GiB of usable RAM, and the observability stack has occupied a meaningful fraction of that budget in different acceptance snapshots. The low-RAM artifact recorded the low-RAM acceptance artifact recorded a 726.2 MiB observability-memory sample; another aggregate runtime field recorded 841,814,016 bytes, so I treat both as snapshot telemetry evidence rather than a universal footprint. Those snapshots cover different accounting views, so I make a point not to collapse them into one magic “monitoring uses X MiB” claim. I use them to prove that observability is large enough to manage deliberately.

The cAdvisor case is the clearest example: cAdvisor measured at 428.2 MiB before the low-RAM work and 27.87 MiB in one post-change sample, with an observed steady range around 20–28 MiB. That improvement came from removing work whose cost exceeded its operational value, not from disabling container observability. The same reasoning applies to `Seven Days of Logs Was an Engineering Choice, Not a Default`. I ask how often the state can meaningfully change, how quickly I need to react, how many series or log streams the observation creates, whether a cheaper collector can answer the same question, and whether the query belongs at scrape time, recording-rule time or investigation time.

There is also a human monitoring tax. Every detection rule that cannot lead to an action consumes attention. Every monitoring view panel that lacks a clear question makes incidents slower. Every high-cardinality label creates future storage and query work. The resource budget therefore includes RAM, CPU, disk, network, series count, log streams and operator cognition.

On a larger host I might tolerate a more expensive collector to gain richer diagnostics. On this small the production stack machine the default is the opposite: collect the smallest reliable signal that preserves the failure telemetry evidence I need, then keep deeper inspection available on demand.

## Sampling, cardinality and storage economics

Even when `Seven Days of Logs Was an Engineering Choice, Not a Default` is not primarily a Prometheus article, the signal eventually has storage economics. A gauge sampled every 15 seconds creates four times as many samples as the same gauge sampled every minute. A label that takes ten values multiplies one series into ten. A per-user, per-request, per-IP or per-container-ID label can turn a small metric family into a cardinality problem. Logs have the same issue at the stream-label layer.

For that reason I separate high-frequency operational signals from slow inventory. CPU, pressure and service availability can change quickly enough to justify short cadences. Certificate expiry, image inventory, volume size or SMART state usually cannot. The accepted profile already uses slower collection for Docker inventory and background caching for expensive storage data. The exact cadence is less important than the reasoning: sample at the speed of the decision, not at the speed of the default configuration.

Retention has the same trade-off. Prometheus retention set to about 30 days with a 15 GB size cap; Loki retention set to 168 hours. Extending either retention window consumes capacity and may change fault conditions on a small disk. If I need year-scale history later, I would rather design remote long-term storage than silently turn the local TSDB or log store into the largest workload on the machine.

Cardinality review is therefore part of feature review. A new monitoring view panel that requires an unbounded label is not “just visualization”; it changes ingestion and memory cost. The monitoring stack has to remain affordable during the incident it is meant to diagnose, when the production stack may already be under resource pressure.

## Turning the observation into an detection rule without creating noise

Not every article in this series ends with a page. Some of the best signals are diagnostic. When I do detection rule, I separate **prediction**, **saturation**, and **symptom**. Prediction covers conditions such as disk capacity or certificate expiry where action before failure is possible. Saturation covers sustained pressure or exhausted pools. Symptoms cover conditions such as a failed public probe, no healthy SIP worker, or unsuccessful restore verification where the service contract is already affected.

The rule duration has to fit the failure. A single scrape miss or short deployment restart should not create an incident. A total public outage should not sit pending for an arbitrary long `for:` window simply because another resource rule uses ten minutes. Warning and critical labels are response contracts: warning means investigate or schedule action before the margin disappears; critical means the operating state is already outside the tolerated envelope or approaching it fast enough to require immediate attention.

I add one more check: ask what other detection rule will fire at the same time. If host loss makes every public service fail, paging separately for Grafana, OTA, authentication, gateway and VoIP adds noise without information. Grouping and inhibition should preserve useful symptoms while making the likely root event obvious. Resolution is part of the lifecycle too. The latest accepted notification telemetry evidence recorded external notification counters in the acceptance artifact: 13 success, 0 failure, 6 resolved; that is a snapshot of delivery behavior, not an SLA claim.

For `Seven Days of Logs Was an Engineering Choice, Not a Default`, the detection rule is successful only if its annotation tells me what was observed, over what window, which monitoring view or runbook to open next, and what secondary signal can confirm the hypothesis.

## Acceptance: prove the monitor after changing it

I make a point not to treat a configuration commit as proof that monitoring works. After meaningful observability changes I compare the desired state in Git with runtime acceptance. The present artifact records 52/52 accepted Prometheus targets UP, 106 detection rule/recording rules loaded, 0 firing and 0 pending detection rules, 27,578 active Prometheus series, against a 27,414-series acceptance baseline, 10/10 public probes UP, 9/9 database probes UP and 35 monitored configuration files with zero drift in the latest runtime sample. Those numbers are useful because they make blind spots and accidental cardinality growth measurable after deployment.

The validation depends on the feature. A scrape change should prove the target is UP and the expected series exists. A relabel change should prove the required monitoring view and detection rule queries still return data. A log-pipeline change should prove cursor continuity and check drop counters. A public probe should be exercised against both healthy and intentionally invalid behavior. A backup control should be followed by checksum and restore telemetry evidence. A notification change should send a synthetic detection rule and verify both firing and resolved delivery.

Where safe, I prefer failure injection to passive confidence. The external dead-man watcher was tested by forcing a synthetic outage: the hosted workflow failed, an incident issue was created, recovery later passed and the issue closed. That sequence proved more than reading the workflow YAML. The same idea scales down to small controls: temporarily make a test target fail, expire a synthetic sample, or use a fixture that triggers the rule without damaging the production stack.

## Tests that make the monitoring logic trustworthy

I separate tests into collection, semantics, rule and end-to-end behavior. Collection tests answer whether the metric or log event appears with the expected labels and units. Semantic tests compare it with the underlying source: `/proc`, Docker, SQL, a service API, a certificate, an actual file timestamp or another authoritative state. Rule tests feed boundary conditions into PromQL or detection rule fixtures so warning, critical, pending and resolved transitions are predictable.

End-to-end testing is stronger. A synthetic failure should make the expected detection rule fire through the real routing path, and recovery should produce the expected resolution. The external watcher already demonstrated this model by creating and then closing an incident around a forced outage. For backup monitoring, an end-to-end test is a restore verification rather than a successful archive command. For authentication-aware probing, it is seeing the expected redirect or authorization status instead of weakening the route to return 200.

For `Seven Days of Logs Was an Engineering Choice, Not a Default`, I would also test missing data. Many rules are exercised only with high or low values and never with a vanished series. The correct behavior may be a target-down detection rule, an UNKNOWN state, or a dedicated freshness detection rule. Missing telemetry evidence should not silently inherit the last green value.

## Telemetry can leak data if I treat it as harmless

Metrics and logs are the production stack data. Labels can reveal hostnames, internal services, user identities or network details. Logs can contain source addresses, request paths and authentication context. A convenient custom collector can accidentally print a credential. A monitoring view can expose an administrative topology to anyone who can reach it.

My rule is to collect state, not secrets. OpenBao monitoring exposes initialized/sealed state, health and certificate information, not secret values or tokens. Configuration drift uses hashes of approved files rather than exporting `.env` contents. Authentication monitoring keeps high-cardinality identities and IPs in bounded log content rather than promoting them to Prometheus labels. Secret files remain outside Git and are not copied into article source.

The same principle affects probe design. The external dead-man watcher intentionally needs no hserver credential. A health check should not require broad the production stack authority merely to answer whether a service is alive. Where authenticated deep checks are necessary, the identity should have the minimum query capability and its lifecycle should be monitored separately.

For `Seven Days of Logs Was an Engineering Choice, Not a Default`, I review telemetry exposure together with collection cost. Observability is not exempt from least privilege simply because the output is “only monitoring.”

## What the current accepted system says

The 2026-09-15 acceptance snapshot gives me a concrete reference point while writing this series. It records 52/52 accepted Prometheus targets UP, 106 detection rule/recording rules loaded, 0 firing and 0 pending detection rules, and 15 provisioned monitoring views. Prometheus reported 27,578 active Prometheus series, against a 27,414-series acceptance baseline. Public probing reported 10/10 public probes UP; database probing reported 9/9 database probes UP. The accepted configuration manifest reported 35 monitored configuration files with zero drift in the latest runtime sample.

For storage and retention, Prometheus retention set to about 30 days with a 15 GB size cap; Loki retention set to 168 hours. For hardware telemetry evidence, SMART status healthy in the acceptance artifact, with a 49 C device-temperature sample. For recovery, encrypted DR verification PASS, required payload PASS, internal checksum PASS, off-host pull PASS, and restore verification PASS. For OpenBao, main OpenBao initialized and unsealed with Transit auto-unseal; same-host seal node initialized and unsealed with no host-published ports. These values are intentionally described with a date because they are not permanent properties of the architecture. They are telemetry evidence that the system reached a known state after a particular round of changes.

This distinction is important for `Seven Days of Logs Was an Engineering Choice, Not a Default`. Monitoring documentation tends to age badly when it turns an observation into a law. I would rather write “27,578 active series in this acceptance snapshot” than imply that 27,578 is a target, a limit or a recommendation. The same applies to cAdvisor memory, disk temperature, monitoring view count and detection rule-rule count. This the production stack design should survive changing numbers because the interpretation rules remain explicit.

## What I would change at larger scale

The small-server version optimizes for bounded cost and direct inspectability. At larger scale I would preserve the semantic model but move some responsibilities. Metrics storage could move off the application host. Long-term retention could use a system designed for remote or object-backed storage. Loki could live on a dedicated node. Exporter and collector work could be distributed closer to the workloads while query and detection rule evaluation stay centralized. High-availability Alertmanager and independent monitoring storage would reduce shared failure domains.

I would not, however, replace `Prometheus 30-day retention plus 15 GB size cap and Loki seven-day retention` with a generic “enterprise monitoring” product and call the problem solved. The key question remains what the observation proves. If the signal is about Linux pressure, the kernel semantics remain. If it is about database locks, the engine semantics remain. If it is about SIP versus RTP, the protocol boundaries remain. If it is about dead-man monitoring, the observer still has to live outside the failure domain.

Scale primarily changes collection topology, retention, redundancy and automation. It does not remove the need to define failure semantics. In fact, larger systems punish ambiguous metrics more severely because a noisy or high-cardinality mistake multiplies across more hosts and more operators.

## What I keep from this decision

What survived from this work is not a particular threshold. It is the interpretation contract behind **Seven Days of Logs Was an Engineering Choice, Not a Default** and the telemetry evidence required before I trust it. The control is useful because I know its acquisition cost, expected cadence, fault conditions, corroborating signals and response path. That is the standard I now use before adding another metric or detection rule to hserver.

The server is still an old Mac mini. That constraint has not stopped the monitoring system from becoming serious. It has forced every layer to be explicit about what it is worth. For me that is the more interesting engineering result: the production stack-grade observability is less about how many products are installed and more about whether the telemetry evidence is sufficient, current, independent where necessary, and cheap enough that the observer does not become the outage.
