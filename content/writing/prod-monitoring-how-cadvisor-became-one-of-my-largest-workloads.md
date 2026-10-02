---
title: How cAdvisor Became One of My Largest Workloads
url: /posts/prod-monitoring-how-cadvisor-became-one-of-my-largest-workloads.html
date: '2026-09-15'
read_time: 36
excerpt: A production-engineering deep dive into how cadvisor became one of my largest
  workloads, grounded in the 2014 Mac mini hserver observability stack and its accepted
  runtime evidence.
topic: observability-monitoring
tags:
- docker
- cadvisor
- containers
- capacity
draft: false
featured: false
language: en
eyebrow: 'Production Monitoring: Docker & Containers · deep-dive'
outputs:
- url: /posts/prod-monitoring-how-cadvisor-became-one-of-my-largest-workloads.html
  template: cms/templates/posts/posts--prod-monitoring-how-cadvisor-became-one-of-my-largest-workloads.tpl
  source: cms/templates/posts/posts--prod-monitoring-how-cadvisor-became-one-of-my-largest-workloads.json
---

I did not add this signal because I am looking fored another graph. I added it because `How cAdvisor Became One of My Largest Workloads` describes a operational failure that the rest of the stack could not explain cleanly.

The host is 2014 Apple Mac mini running Linux, with roughly 7.1 GiB usable RAM from an 8 GB-class machine. Applications, databases, networking, authentication, OTA, OpenBao, VoIP and the observability stack share the same limited CPU, memory and storage. That makes monitoring part of the workload rather than something outside it. The central failure I am trying to avoid is not merely “a metric went high.” I am looking for enough telemetry evidence to tell whether a user-facing service is degrading, which dependency owns the problem, whether the signal is current, and whether the monitoring path itself is still trustworthy.

For this specific problem the primary observation point is `process memory for Prometheus, Grafana, Loki, Alloy, cAdvisor and exporters`. The short the running stack note that preceded this article captured the core finding: Monitoring overhead is part of the running stack capacity and should be measured like any other service rather than treated as free infrastructure. This long-form version goes further: what that signal really proves, which nearby signals can falsify my first hypothesis, how I implement and rule outcome on it, what it costs on this host, and how I would redesign the same control at larger scale.

The numbers in this article are not generic benchmarks. When I mention 27,578 active Prometheus series, against a 27,414-series acceptance baseline, cAdvisor measured at 428.2 MiB before the low-RAM work and 27.87 MiB in one post-change sample, with an observed steady range around 20–28 MiB, or any other concrete value, I mean the 2026-09-15 acceptance snapshot unless I explicitly say otherwise. If a current value is not present in the accepted telemetry evidence, I leave `[CURRENT MEASUREMENT NEEDED]` rather than inventing a number.

## The engineering question specific to this article

The short version of the problem is not “how do I graph How cAdvisor Became One of My Largest Workloads?” It is: **Observability was becoming one of the larger workloads on a small the running stack server, which is dangerous when monitoring competes with the services it protects.** That failure can be confused with neighboring conditions, which is why the primary observation is `process memory for Prometheus, Grafana, Loki, Alloy, cAdvisor and exporters` rather than a generic process-up flag.

The current reviewed the running stack conclusion is specific: Monitoring overhead is part of the running stack capacity and should be measured like any other service rather than treated as free infrastructure. I turn that conclusion into an operational practice—observability resource budgeting—and into a preventive control: Track the stack's aggregate memory, optimize expensive collector processs first, and keep enough headroom that an incident does not cause the monitor itself to amplify pressure. Those three layers are intentionally separate. The finding explains what the telemetry evidence taught me. The practice describes how I diagnose it. The prevention rule describes how I keep the same ambiguity from returning after the next deployment.

There is also a data-model question. The observation has to retain the dimension that matters without encoding unbounded identity. If the question is per node, the node label matters. If it is fleet capacity, an aggregate may be more useful. If it is an event such as a deadlock or OOM kill, a counter over a time window carries different meaning from a current-state gauge. If it is a cached inventory value, age and refresh success are part of the value's contract.

Finally I decide how close this signal is to user impact. Some topics in this series are direct symptoms; others are explanatory telemetry evidence. `How cAdvisor Became One of My Largest Workloads` belongs at the point where it can reduce investigation time without claiming more certainty than the underlying source provides. That classification determines whether it becomes a page, a warning, a visualization drill-down or simply retained forensic context.

## Competing hypotheses before I touch the running stack

I try to write down multiple explanations before making a change. For **How cAdvisor Became One of My Largest Workloads**, the candidate set I would test includes: **the container restarted and erased current-state telemetry evidence**; **the collector process itself is adding too much runtime overhead**; **the container process exists but readiness is broken**; **a cgroup limit, not host capacity, caused the failure**; and **a noisy neighbor is consuming shared I/O or network resources**. The point is not that all five are equally likely. It is to stop the first plausible graph from becoming the conclusion.

The primary observation `process memory for Prometheus, Grafana, Loki, Alloy, cAdvisor and exporters` should eliminate some of those hypotheses, not all of them. I choose the next query or log source by information gain: which check can separate the most remaining explanations at the lowest operational cost? A fresh internal probe versus a failed public probe immediately moves suspicion toward the edge. High memory utilization with low pressure and stable swap activity moves me away from a memory-emergency diagnosis. A stale FreeSWITCH heartbeat with a running container moves the problem from process liveness into worker readiness.

This habit is especially useful on a single host because many symptoms are correlated. Storage pressure can slow databases, logs and containers simultaneously. Host memory pressure can make the monitoring stack itself late. A router or Internet failure can make every public service look broken while the applications are healthy. Explicit competing hypotheses keep correlation from being mistaken for independent failures.

## The observation contract I expect this signal to keep

For `process memory for Prometheus, Grafana, Loki, Alloy, cAdvisor and exporters` I am looking for a written contract even if it is only a few lines in a runbook. The contract says who produces the data, what unit it uses, which labels are bounded and meaningful, how often it should update, what reset behavior exists, and what missing data means. Without those details an old metric can survive long after its interpretation has changed.

The contract also names the strongest claim the signal supports. Monitoring overhead is part of the running stack capacity and should be measured like any other service rather than treated as free infrastructure. That sentence is intentionally narrower than “the service is healthy.” It leaves room for independent telemetry evidence and tells future maintainers not to reuse the metric for a stronger conclusion without re-validating it.

Freshness belongs in the contract whenever the producer is not scraped directly. Cache-backed Docker inventory, textfile metrics, heartbeat state and backup timestamps can all remain syntactically valid after the producer stops. I therefore prefer either an explicit age metric or a timestamp from which age can be derived. For direct Prometheus targets, `up` is part of the collection contract but still not the service-health contract.

Finally, the contract includes data sensitivity. Labels and log content must not turn operational telemetry into a secret-disclosure channel. If the observation cannot be collected safely with bounded identity and least privilege, I redesign the collector process rather than assuming the monitoring network is trusted.

## Start with the failure, not the exporter

The operational failurel for this article is: **Observability was becoming one of the larger workloads on a small the running stack server, which is dangerous when monitoring competes with the services it protects.** That wording matters because it describes the operational ambiguity I need to remove. A raw metric has no value until I know what claim I am trying to make from it.

The obvious monitoring mistake is to collapse several layers into one binary state. A process can exist while the application is unusable. A collector process can return a number that is already stale. A public service can correctly return a redirect or authorization error and still be healthy. A database can accept a TCP connection while lock contention makes useful queries stall. A host can report high memory utilization while reclaimable page cache means applications are not under pressure. The same general problem appears repeatedly: one layer's “up” is only telemetry evidence about that layer.

I therefore map each failure to at least three questions. First, what is the earliest useful signal that something is changing? Second, what is the strongest user-visible symptom I can observe independently? Third, what telemetry evidence tells me the monitoring path is alive enough to trust the first two answers? For `How cAdvisor Became One of My Largest Workloads`, `process memory for Prometheus, Grafana, Loki, Alloy, cAdvisor and exporters` belongs in that chain, but it is never allowed to stand alone if the failure can be confirmed from another layer.

This is also how I decide whether an rule outcome belongs on a metric. A signal may be excellent for diagnosis and terrible for paging. Context switches, container block-I/O bytes or database size trends can be valuable telemetry evidence without being reasons to interrupt an operator immediately. Conversely, a public probe failure or no-healthy-worker condition may deserve much more direct attention because it is already close to user impact.

## Where this sits in the hserver observability architecture

Container observability sits between host state and application state. The Docker daemon can say a container is running while the application is unable to serve traffic. A health check can pass while the public dependency chain is broken. cgroup memory can look high because of reclaimable cache, while a smaller working set may better represent active pressure. Restart counts preserve telemetry evidence of crashes that disappeared from a current-state view. OOM events distinguish a memory failure from a merely busy service. Network errors and block-I/O attribution help identify a noisy neighbor that host-wide counters cannot name.

The cAdvisor incident made this layer concrete. In one pre-optimization observation, cAdvisor itself used about 428.2 MiB. After disabling expensive filesystem disk scanning, retaining useful disk-I/O metrics, tuning housekeeping, shortening internal storage duration and reducing unnecessary series, one post-change sample was 27.87 MiB and the observed steady range was about 20–28 MiB. Those numbers are host-specific acceptance telemetry evidence, not universal cAdvisor benchmarks. The architectural lesson is universal: the system measuring resource use is itself a resource consumer. Exporters need budgets, and a metric that costs hundreds of megabytes must justify the operational decision it enables.

For this article, the component boundary matters as much as the metric. The current reviewed accepted observability stack includes Prometheus, Grafana, Loki, Alloy, Alertmanager, Blackbox Exporter, Node Exporter, cAdvisor, SMART collection, Docker inventory and deep host/database collector processs, plus application-native and external synthetic signals. The latest acceptance artifact records 52/52 accepted Prometheus targets UP, 106 rule outcome/recording rules loaded, 15 provisioned visualizations and 10/10 public probes UP.

I deliberately do not interpret those counts as a maturity score. More targets and more rules can make a system worse if they add noise or cost without reducing uncertainty. The useful part is that the inventory is explicit and accepted. When I add a control for `How cAdvisor Became One of My Largest Workloads`, I can ask which existing layer already sees part of the problem, whether a new metric is necessary, and how the new observation will be validated after deployment.

## The decision this monitor should let me make

If this telemetry cannot change a decision, it should not automatically consume always-on budget. For **How cAdvisor Became One of My Largest Workloads**, the decisions fall into four categories. I may need to intervene immediately because a service contract is already broken. I may need to schedule capacity work because margin is shrinking. I may need to isolate a dependency during incident diagnosis. Or I may decide that the condition is normal and explicitly avoid action.

That last outcome is important. Monitoring is partly a system for proving when *not* to react. Page cache, historical swap, a 302 authentication redirect, a controlled restart, or a busy response from a SIP endpoint can look abnormal without representing infrastructure failure. The metric model should carry enough context to distinguish those cases.

A second part of the design is want the monitor to make rollback decisions safer. If a deployment changes `process memory for Prometheus, Grafana, Loki, Alloy, cAdvisor and exporters`, I should be able to compare the new state with the accepted baseline and decide whether the change is intended. That is why provenance `218300b` stays attached to the topic. A the running stack metric without a known configuration history is harder to use as change telemetry evidence.

At scale this decision-centric approach becomes even more important. Hundreds of hosts can produce unlimited telemetry; operator time remains finite. The series therefore treats observability as a decision system rather than a storage system.

## Why this particular collection path won

There are usually several ways to obtain the state behind **How cAdvisor Became One of My Largest Workloads**: scrape an existing exporter, query an application API, run a SQL statement, parse logs, inspect the Docker API, read a Linux kernel interface, or publish a small custom metric through the textfile path. I choose among them by authority, cost, security and failure independence.

The closest source is not always the best source. A Docker container metric can tell me process resource use but not whether PostgreSQL sessions are waiting. A log parser can count authentication failures but is a weaker source for current service readiness than a direct state query. A raw TCP probe is cheap but deliberately shallow. A deep query may be authoritative but require credentials or create load. The concrete mechanism behind `process memory for Prometheus, Grafana, Loki, Alloy, cAdvisor and exporters` is valuable because it sits at the layer that owns the state I need to interpret.

A second part of the design is prefer collection paths with visible failure. A custom script that exits silently and leaves yesterday's textfile metric behind is worse than a collector process that exports its own success and age. A cache should expose refresh result and age. A database collector process should expose whether its query succeeded. A log pipeline should expose drops. The observer has to be observable.

The chosen path therefore reflects more than convenience. It is part of the operational failurel: which component can lie, which credential can expire, which namespace the query sees, and what remains observable when another layer breaks.

## How I reason about a threshold for this topic

I deliberately do not begin with a round number. I begin with the consequence I am trying to avoid and how much reaction time exists. Capacity thresholds such as disk or connection utilization should leave enough margin to investigate before exhaustion. Pressure thresholds should remain high long enough to distinguish real contention from transient scheduling noise. Certificate thresholds are measured in days because the repair process is administrative, not millisecond-sensitive. External availability failures can justify much faster response.

For **How cAdvisor Became One of My Largest Workloads**, the next threshold review should use the historical distribution plus the component's configured limit and the time needed to act. If that distribution is not captured in the latest accepted runtime artifact, the honest value is **[CURRENT MEASUREMENT NEEDED]**. I deliberately do not derive a the running stack page from an attractive number in a blog post.

A second part of the design is test both sides of the boundary. A warning threshold should actually enter pending/firing state when a fixture crosses it, and it should resolve when the signal recovers. A critical threshold should not be inhibited by the warning in a way that loses the more serious state. If the signal is a counter, the window should contain enough events to be meaningful. If it is a gauge, the `for` duration and freshness semantics matter more than counter reset behavior.

Thresholds are therefore versioned policy. When topology, workload, resource limits or collector process semantics change, I expect the threshold to be reviewed alongside the code.

## The mechanism underneath the graph

Container metrics add cgroup and runtime semantics. cAdvisor reads cgroup counters and Docker/runtime metadata, while the inventory exporter handles the running stack-specific state that cAdvisor does not know, such as expected containers, restart policy, security-sensitive mounts and cached Docker storage inventory. Working set, RSS, cache and limits answer different memory questions. Block-I/O counters attribute volume but not necessarily user-visible latency. Healthcheck state is application-defined and therefore stronger than process existence but weaker than an external user path.

That mechanism matters for `How cAdvisor Became One of My Largest Workloads` because two visually similar graphs can have very different semantics. A cumulative counter should normally be turned into a rate or increase over a time window. A gauge can be read directly but still needs freshness. A ratio is meaningless if its denominator is missing, zero or describes a different capacity boundary. A status value needs an explicit state model. A log-derived count depends on the reliability of ingestion and parsing. A synthetic probe depends on where the probe originates and which route it exercises.

I try to preserve units all the way from collection to the panel and rule outcome. Seconds should not silently become milliseconds. Bytes should not be compared with decimal “GB” labels without deciding which convention is in use. Percentages should identify their denominator. Ages should be derived from timestamps in a timezone-independent way. These details look small in configuration review and become large during incidents, when the operator is making decisions from the graph under time pressure.

The other subtlety is reset behavior. Counters restart with processes. Container identities change on recreation. database cumulative statistics can reset after engine restart. A visualization that uses raw cumulative values can therefore interpret restart as recovery or huge negative activity. Query functions and labels need to match the lifecycle of the component being measured.

## Implementation: make the observation cheap and reproducible

The concrete mechanism is deliberately smaller than the explanation. I am looking for the collection path to be boring: deterministic configuration in Git, bounded work on the host, a clear scrape or evaluation cadence, and a result that can be checked after deployment. Repository telemetry evidence associated with this topic is `218300b`.

A representative query or configuration fragment is:

```
# Accepted low-RAM profile
cAdvisor filesystem disk scanner: disabled
container disk-I/O metrics: retained
housekeeping interval: 30s
max housekeeping: 60s
storage duration: 1m
```

The fragment is not meant to be copied blindly into another system. Labels, device names, mount points, job names and custom metric families are deployment-specific. The important point is the shape of the control. Ratios need denominators. Counters need rates or increases over windows. Slow-changing inventory should not be polled at CPU-metric cadence. Authentication-aware probes need status semantics. Freshness-sensitive collector processs need age checks. Expensive queries should be recorded or sampled at a cadence that matches the decision they support.

A second part of the design is keep configuration ownership separate from runtime telemetry evidence. Prometheus rules, scrape configuration, visualizations and collector process code live in the reviewed source tree. Runtime acceptance data records what the running stack actually observed. Secret values stay out of both metrics and public documentation. This lets me reproduce the monitoring design without turning the monitoring repository into a credential store.

## Walk the failure from symptom back to cause

An operationally useful way to review this monitor is to imagine a failure and force myself to predict what each layer would show. I deliberately do not claim the following sequence happened unless it is part of the recorded telemetry evidence; it is a design exercise for the control.

Start with the user-visible symptom related to **How cAdvisor Became One of My Largest Workloads**. The top-level probe or service metric changes first or eventually. I then ask whether the host is still reachable, whether the target is still being scraped, and whether `process memory for Prometheus, Grafana, Loki, Alloy, cAdvisor and exporters` is fresh. If the target is down, an old threshold value is no longer the primary telemetry evidence; target failure becomes the first branch. If the target is up, I compare the signal with its nearest independent corroborator.

From there I trace downward. A host-pressure signal leads to per-container attribution and kernel logs. A container symptom leads to host resource state and application health. A database symptom leads from reachability to connection, wait, lock and engine state. A public probe failure is compared with the internal probe, DNS/TLS phases and edge logs. A VoIP symptom is separated into signaling, worker and media telemetry evidence. A backup symptom is followed through job, artifact, checksum and restore state.

What I want from it is not to prove that every incident follows one tree. It is to make sure each metric has a place in an investigation. If a signal cannot tell me which branch to take next, I question whether it belongs in the always-on monitoring budget.

## How I debug this signal when it looks wrong

I rely on a layered debugging order because the fastest way to waste time is to treat the first abnormal graph as the root cause. For **How cAdvisor Became One of My Largest Workloads**, I start by proving that the sample is current. I check target or collector process health, the timestamp/freshness path, and whether a recent deployment changed labels or collection cadence. If the value can be generated from a custom collector process, I compare the exported value with the underlying operating-system, Docker, database or application state.

Next I look for a neighboring signal that should move if my hypothesis is correct. Memory pressure should have some relationship to MemAvailable, swap activity, OOM telemetry evidence or workload latency. Storage latency should have some relationship to I/O pressure or application waits. Container I/O should reconcile with host disk activity. A database saturation hypothesis should be visible in connection, wait or lock state. A public availability failure should be compared with an internal probe so I can separate application failure from DNS, TLS, tunnel or edge failure.

Only after that do I broaden into logs. Logs are best when the failure domain is already smaller: kernel OOM records, Docker daemon warnings, authentication failures, Alloy/Loki pipeline errors, database messages or VoIP-specific events. This keeps me from searching an unbounded log corpus for an event I have not yet defined.

The last step is to check the monitoring system itself. A quiet visualization can be caused by a missing target. A stable line can be a stale sample. A zero-rule outcome page can coexist with rule-evaluation failures. I am looking for telemetry evidence that the observer is alive before I trust the observation.

## The hserver case that shaped this part of the design

The cAdvisor low-RAM work is the container case study. A roughly 428.2 MiB observation was large enough to compete with the running stack workloads. The fix was not to remove cAdvisor but to remove expensive filesystem disk scanning, keep the disk-I/O signals that mattered, tune housekeeping, shorten internal storage duration and trim unneeded series. A later sample was 27.87 MiB with an observed 20–28 MiB steady range. This is a concrete example of monitoring the monitor and budgeting visibility.

I rely on that case as a guardrail for `How cAdvisor Became One of My Largest Workloads` because it prevents the discussion from becoming a generic monitoring tutorial. The interesting question is not whether another platform supports the same metric. It is what decision the signal enabled on this constrained the running stack host, what cost it imposed, and what telemetry evidence proved that the change improved rather than merely rearranged the system.

The design also keeps causality honest. A before/after measurement is telemetry evidence for this configuration at that time. It is not a universal benchmark for cAdvisor, Prometheus, Docker, OpenBao or any database engine. When the article makes a recommendation, the recommendation is about the engineering method—measure, isolate cost, preserve the useful signal, verify the new operational failures—not about assuming another machine will reproduce the same number.

## What would make this monitor lie?

I ask this question explicitly because most monitoring failures are not fabricated numbers; they are numbers interpreted outside their validity. `process memory for Prometheus, Grafana, Loki, Alloy, cAdvisor and exporters` can become misleading if its collector process is stale, labels change, the underlying source resets, the query aggregates away the failing member, the scrape path observes a different network namespace, or the monitored component changes semantics after an upgrade.

Caching creates another class of lies. The Docker storage inventory is deliberately cached because continuous filesystem inspection was too expensive. A cache-backed metric is only trustworthy when cache age and refresh success are visible. Textfile metrics have the same issue if the producer stops updating them. Database-derived metrics can lie by omission if the collector process account loses access to a system view. Log-derived metrics can go quiet because Alloy or Loki is dropping data rather than because the event stopped happening.

Authentication and synthetic probes can lie through overly permissive expectations. Following redirects blindly may turn an application failure into a successful login-page response. Accepting every status code may hide a broken route. Requiring only 200 may create the opposite error and call a healthy access-control response an outage. The probe has to encode the intended contract.

My response to these risks is not distrust of monitoring. It is meta-monitoring, freshness, independent telemetry evidence and explicit UNKNOWN states when the observation path cannot make a strong claim.

## The monitoring tax for this signal

On this machine, collection cost is part of the design review. The current reviewed host has roughly 7.1 GiB of usable RAM, and the observability stack has occupied a meaningful fraction of that budget in different acceptance snapshots. The low-RAM artifact recorded the low-RAM acceptance artifact recorded a 726.2 MiB observability-memory sample; another aggregate runtime field recorded 841,814,016 bytes, so I classify both as snapshot telemetry evidence rather than a universal footprint. Those snapshots cover different accounting views, so I deliberately do not collapse them into one magic “monitoring uses X MiB” claim. I rely on them to prove that observability is large enough to manage deliberately.

The cAdvisor case is the clearest example: cAdvisor measured at 428.2 MiB before the low-RAM work and 27.87 MiB in one post-change sample, with an observed steady range around 20–28 MiB. That improvement came from removing work whose cost exceeded its operational value, not from disabling container observability. The same reasoning applies to `How cAdvisor Became One of My Largest Workloads`. I ask how often the state can meaningfully change, how quickly I need to react, how many series or log streams the observation creates, whether a cheaper collector process can answer the same question, and whether the query belongs at scrape time, recording-rule time or investigation time.

There is also a human monitoring tax. Every rule outcome that cannot lead to an action consumes attention. Every visualization panel that lacks a clear question makes incidents slower. Every high-cardinality label creates future storage and query work. The resource budget therefore includes RAM, CPU, disk, network, series count, log streams and operator cognition.

On a larger host I might tolerate a more expensive collector process to gain richer diagnostics. In this deployment the default is the opposite: collect the smallest reliable signal that preserves the failure telemetry evidence I need, then keep deeper inspection available on demand.

## Capacity math I rely on instead of intuition

The simplest capacity calculation is sample multiplication. If a job exports `S` series every `I` seconds, the rough sample count over a day is `S * 86400 / I` before considering churn, compression and block behavior. Halving the scrape interval doubles sample density. Adding a label with ten stable values can multiply a metric family by roughly ten. Turning an unbounded identifier into a label can be far worse because the population grows with traffic rather than with infrastructure.

I deliberately do not use that arithmetic as a precise Prometheus storage estimator; WAL encoding, chunks, label indexes and compression make byte cost more complex. I rely on it to compare design choices before deploying them. The latest accepted runtime point of 27,578 active series gives me a local baseline. If a small visualization feature adds thousands of active series, that is visible as an architectural cost even before disk use becomes alarming.

Memory budgeting uses the same idea. With roughly 7.1 GiB usable RAM, a 400 MiB monitoring regression is not “only a few hundred megabytes.” It competes with the running stack. The cAdvisor before/after telemetry evidence showed why percentage-of-host thinking is useful. I track the observability aggregate, large individual processes and host MemAvailable/pressure together rather than assigning one static memory number to the entire stack forever.

For `How cAdvisor Became One of My Largest Workloads`, any new collector process, label or cadence change should therefore answer two questions: how much additional telemetry evidence does it buy, and what the running stack resource is being spent to buy it?

## Sampling, cardinality and storage economics

Even when `How cAdvisor Became One of My Largest Workloads` is not primarily a Prometheus article, the signal eventually has storage economics. A gauge sampled every 15 seconds creates four times as many samples as the same gauge sampled every minute. A label that takes ten values multiplies one series into ten. A per-user, per-request, per-IP or per-container-ID label can turn a small metric family into a cardinality problem. Logs have the same issue at the stream-label layer.

That design pressure is why I separate high-frequency operational signals from slow inventory. CPU, pressure and service availability can change quickly enough to justify short cadences. Certificate expiry, image inventory, volume size or SMART state usually cannot. The accepted profile already uses slower collection for Docker inventory and background caching for expensive storage data. The exact cadence is less important than the reasoning: sample at the speed of the decision, not at the speed of the default configuration.

Retention has the same trade-off. Prometheus retention set to about 30 days with a 15 GB size cap; Loki retention set to 168 hours. Extending either retention window consumes capacity and may change operational failures on a small disk. If I need year-scale history later, I would rather design remote long-term storage than silently turn the local TSDB or log store into the largest workload on the machine.

Cardinality review is therefore part of feature review. A new visualization panel that requires an unbounded label is not “just visualization”; it changes ingestion and memory cost. The monitoring stack has to remain affordable during the incident it is meant to diagnose, when the running stack may already be under resource pressure.

## Operational limits and thresholds are configuration, not physics

Thresholds in this system are chosen from capacity, consequence and response time. Disk warning/critical bands, certificate windows, rule outcome `for:` durations, heartbeat age, memory budgets and SLO burn-rate factors all express policy. I document them as current the running stack choices, not constants of Linux or Prometheus.

That distinction matters during growth. If workload changes, a threshold that once provided useful warning may become permanently noisy. If a collector process is optimized, an observability-memory budget may be tightened. If a service moves off-host, its failure domain changes and an old rule outcome relationship may no longer apply. If public traffic increases, SLO windows may have enough events to use a different statistical model.

For `How cAdvisor Became One of My Largest Workloads`, I would review the threshold whenever the component version, workload, resource limit or topology materially changes. I would also inspect the historical distribution before tightening it. A threshold selected only from a desired round number is less defensible than one derived from observed normal behavior plus an explicit safety margin.

Where the latest accepted runtime telemetry evidence does not contain the distribution needed to justify a new threshold, the article leaves **[CURRENT MEASUREMENT NEEDED]**. That is not an incomplete monitoring practice; it is a refusal to pretend policy has empirical support that has not yet been collected.

## Acceptance: prove the monitor after changing it

I deliberately do not treat a configuration commit as proof that monitoring works. After meaningful observability changes I compare the desired state in Git with runtime acceptance. The current reviewed artifact records 52/52 accepted Prometheus targets UP, 106 rule outcome/recording rules loaded, 0 firing and 0 pending rule outcomes, 27,578 active Prometheus series, against a 27,414-series acceptance baseline, 10/10 public probes UP, 9/9 database probes UP and 35 monitored configuration files with zero drift in the latest runtime sample. Those numbers are useful because they make blind spots and accidental cardinality growth measurable after deployment.

The validation depends on the feature. A scrape change should prove the target is UP and the expected series exists. A relabel change should prove the required visualization and rule outcome queries still return data. A log-pipeline change should prove cursor continuity and check drop counters. A public probe should be exercised against both healthy and intentionally invalid behavior. A backup control should be followed by checksum and restore telemetry evidence. A notification change should send a synthetic rule outcome and verify both firing and resolved delivery.

Where safe, I prefer failure injection to passive confidence. The external dead-man watcher was tested by forcing a synthetic outage: the hosted workflow failed, an incident issue was created, recovery later passed and the issue closed. That sequence proved more than reading the workflow YAML. The same idea scales down to small controls: temporarily make a test target fail, expire a synthetic sample, or use a fixture that triggers the rule without damaging the running stack.

## Change management and rollback for monitoring itself

Monitoring changes can cause outages indirectly. A bad Prometheus rule can increase evaluation load. A label change can break every visualization and rule outcome that joins on the old label. A log relabel rule can drop security telemetry evidence. A Blackbox change can generate false incidents. A database probe can even change engine counters, as the removed raw MySQL TCP probe demonstrated by incrementing `Aborted_connects`.

I therefore treat observability changes like the running stack software. Before a risky change I preserve the relevant configuration and acceptance state. I validate syntax and rule files before deployment. After deployment I verify target count, rule count/evaluation health, expected query results, visualization rendering, series/cardinality movement and the resource budget. If those checks fail, rollback should restore the previous known configuration rather than “fix forward” while the monitoring system is partially blind.

The current reviewed source-of-truth model helps here: reviewed configuration lives in Git; runtime acceptance and config hashes tell me what was actually deployed. `218300b` is associated with this article for the same reason. Provenance is not decoration. When an rule outcome behaves differently weeks later, I am looking for to know which configuration decision created that behavior.

## Measurements I would capture before changing this again

If I revisit this control, I am looking for a before/after dataset rather than a subjective impression. At minimum I would record the primary signal, its update age, target health, the relevant host/container resource cost, Prometheus active-series count and the query or collection duration if available. For a logging change I would also record ingestion/drop counters and Loki storage growth. For a probe change I would preserve phase timing and expected status behavior. For a database change I would capture the engine state that justifies the query cadence.

Some current values are already accepted: 27,578 active Prometheus series, against a 27,414-series acceptance baseline; cAdvisor measured at 428.2 MiB before the low-RAM work and 27.87 MiB in one post-change sample, with an observed steady range around 20–28 MiB; 52/52 accepted Prometheus targets UP; and 106 rule outcome/recording rules loaded. Where this article needs a value that the acceptance artifact does not contain—such as an exact current query latency, per-component RAM split, database size, call volume or request rate—the correct value is **[CURRENT MEASUREMENT NEEDED]**. I would rather leave that marker than create false precision in a personal engineering record.

A second part of the design is keep measurement windows long enough to catch steady-state behavior. A container immediately after restart can look very different after caches warm. A five-minute resource sample can miss daily batch work. Retention and series changes may need hours to become obvious. The acceptance window should match the phenomenon being evaluated, not the time I am willing to stare at the terminal.

## What the current accepted system says

The 2026-09-15 acceptance snapshot gives me a concrete reference point while writing this series. It records 52/52 accepted Prometheus targets UP, 106 rule outcome/recording rules loaded, 0 firing and 0 pending rule outcomes, and 15 provisioned visualizations. Prometheus reported 27,578 active Prometheus series, against a 27,414-series acceptance baseline. Public probing reported 10/10 public probes UP; database probing reported 9/9 database probes UP. The accepted configuration manifest reported 35 monitored configuration files with zero drift in the latest runtime sample.

For storage and retention, Prometheus retention set to about 30 days with a 15 GB size cap; Loki retention set to 168 hours. For hardware telemetry evidence, SMART status healthy in the acceptance artifact, with a 49 C device-temperature sample. For recovery, encrypted DR verification PASS, required payload PASS, internal checksum PASS, off-host pull PASS, and restore verification PASS. For OpenBao, main OpenBao initialized and unsealed with Transit auto-unseal; same-host seal node initialized and unsealed with no host-published ports. These values are intentionally described with a date because they are not permanent properties of the architecture. They are telemetry evidence that the system reached a known state after a particular round of changes.

This distinction is important for `How cAdvisor Became One of My Largest Workloads`. Monitoring documentation tends to age badly when it turns an observation into a law. I would rather write “27,578 active series in this acceptance snapshot” than imply that 27,578 is a target, a limit or a recommendation. The same applies to cAdvisor memory, disk temperature, visualization count and rule outcome-rule count. The observability design should survive changing numbers because the interpretation rules remain explicit.

## What I would change at larger scale

The small-server version optimizes for bounded cost and direct inspectability. With dedicated monitoring nodes I would preserve the semantic model but move some responsibilities. Metrics storage could move off the application host. Long-term retention could use a system designed for remote or object-backed storage. Loki could live on a dedicated node. Exporter and collector process work could be distributed closer to the workloads while query and rule outcome evaluation stay centralized. High-availability Alertmanager and independent monitoring storage would reduce shared failure domains.

I would not, however, replace `process memory for Prometheus, Grafana, Loki, Alloy, cAdvisor and exporters` with a generic “enterprise monitoring” product and call the problem solved. The key question remains what the observation proves. If the signal is about Linux pressure, the kernel semantics remain. If it is about database locks, the engine semantics remain. If it is about SIP versus RTP, the protocol boundaries remain. If it is about dead-man monitoring, the observer still has to live outside the failure domain.

Scale primarily changes collection topology, retention, redundancy and automation. It does not remove the need to define failure semantics. In fact, larger systems punish ambiguous metrics more severely because a noisy or high-cardinality mistake multiplies across more hosts and more operators.

## Deep-dive notes: separating mechanism from policy

A recurring source of monitoring bugs is mixing mechanism with policy. The mechanism answers how the observation is produced: kernel counter, cgroup metric, SQL query, log parser, HTTP probe, application counter or external workflow. Policy answers what the organization does when that observation changes. `process memory for Prometheus, Grafana, Loki, Alloy, cAdvisor and exporters` is mechanism. The threshold, window, severity, grouping and escalation path are policy.

Keeping those separate makes the system easier to evolve. I can improve collection without changing the paging contract, or change a warning threshold after capacity review without rewriting the collector process. The design also makes testing clearer. Collector tests validate units, labels, freshness and failure behavior. Rule tests validate expressions and state transitions. End-to-end tests validate that an actual synthetic condition reaches the operator and resolves correctly.

The same separation applies to desired state and telemetry evidence. Git defines reviewed configuration, but Git cannot prove the running system loaded it. Runtime acceptance proves what the running stack observed, but runtime state is not a reproducible configuration source. The current reviewed manifest model bridges the two by hashing approved monitored configuration and measuring drift without exporting secret values.

For this topic, I would treat a future scale-out as another policy change rather than an excuse to discard the semantic model. A managed metrics backend, Kubernetes, multiple nodes or cloud load balancers change topology. They do not change what memory pressure means, what a deadlock means, what a stale heartbeat means, or why a probe outside the failure domain is stronger telemetry evidence of host death than a local visualization.

## What I keep from this decision

What survived from this work is not a particular threshold. It is the interpretation contract behind **How cAdvisor Became One of My Largest Workloads** and the telemetry evidence required before I trust it. The control is useful because I know its acquisition cost, expected cadence, operational failures, corroborating signals and response path. That is the standard I now use before adding another metric or rule outcome to hserver.

The server is still an old Mac mini. That constraint has not stopped the monitoring system from becoming serious. It has forced every layer to be explicit about what it is worth. For me that is the more interesting engineering result: the running stack-grade observability is less about how many products are installed and more about whether the telemetry evidence is sufficient, current, independent where necessary, and cheap enough that the observer does not become the outage.
