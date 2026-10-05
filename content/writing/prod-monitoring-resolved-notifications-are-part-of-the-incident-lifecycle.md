---
title: Resolved Notifications Are Part of the Incident Lifecycle
url: /posts/prod-monitoring-resolved-notifications-are-part-of-the-incident-lifecycle.html
date: '2020-02-22'
read_time: 33
excerpt: A production-engineering deep dive into resolved notifications are part of
  the incident lifecycle, grounded in the 2014 Mac mini hserver observability stack
  and its accepted runtime evidence.
topic: observability-monitoring
tags:
- alertmanager
- alerting
- slo
- error-budget
draft: false
featured: false
language: en
eyebrow: 'Production Monitoring: Alert Engineering & SLOs · advanced'
outputs:
- url: /posts/prod-monitoring-resolved-notifications-are-part-of-the-incident-lifecycle.html
  template: cms/templates/posts/posts--prod-monitoring-resolved-notifications-are-part-of-the-incident-lifecycle.tpl
  source: cms/templates/posts/posts--prod-monitoring-resolved-notifications-are-part-of-the-incident-lifecycle.json
---

I did not add this signal because I expected another graph. I added it because `Resolved Notifications Are Part of the Incident Lifecycle` describes a degradation mode that the rest of the stack could not explain cleanly.

The host is 2014 Apple Mac mini running Linux, with roughly 7.1 GiB usable RAM from an 8 GB-class machine. Applications, databases, networking, authentication, OTA, OpenBao, VoIP and the observability stack share the same limited CPU, memory and storage. That makes monitoring part of the workload rather than something outside it. The central failure I am trying to avoid is not merely “a metric went high.” I expect enough evidence to tell whether a user-facing service is degrading, which dependency owns the problem, whether the signal is current, and whether the monitoring path itself is still trustworthy.

For this specific problem the primary observation point is `increase(hserver_postgres_deadlocks_total[15m])`. The short the production stack note that preceded this article captured the core finding: Deadlock counters preserve evidence of a concurrency failure that application success-rate graphs may quickly forget. This long-form version goes further: what that signal really proves, which nearby signals can falsify my first hypothesis, how I implement and alerting condition on it, what it costs on this host, and how I would redesign the same control at larger scale.

The numbers in this article are not generic benchmarks. When I mention 27,578 active Prometheus series, against a 27,414-series acceptance baseline, cAdvisor measured at 428.2 MiB before the low-RAM work and 27.87 MiB in one post-change sample, with an observed steady range around 20–28 MiB, or any other concrete value, I mean the 2026-09-15 acceptance snapshot unless I explicitly say otherwise. If a current value is not present in the accepted evidence, I leave `[CURRENT MEASUREMENT NEEDED]` rather than inventing a number.

## The engineering question specific to this article

The short version of the problem is not “how do I graph Resolved Notifications Are Part of the Incident Lifecycle?” It is: **A PostgreSQL deadlock can resolve automatically by aborting one transaction, leaving the service apparently healthy after the incident.** That failure can be confused with neighboring conditions, which is why the primary observation is `increase(hserver_postgres_deadlocks_total[15m])` rather than a generic process-up flag.

The the production stack the production stack conclusion is specific: Deadlock counters preserve evidence of a concurrency failure that application success-rate graphs may quickly forget. I turn that conclusion into an operational practice—event-counter monitoring—and into a preventive control: Alert on any new deadlock, capture application context, and fix lock ordering or transaction scope instead of treating retries as the permanent solution. Those three layers are intentionally separate. The finding explains what the evidence taught me. The practice describes how I diagnose it. The prevention rule describes how I keep the same ambiguity from returning after the next deployment.

There is also a data-model question. The observation has to retain the dimension that matters without encoding unbounded identity. If the question is per node, the node label matters. If it is fleet capacity, an aggregate may be more useful. If it is an event such as a deadlock or OOM kill, a counter over a time window carries different meaning from a current-state gauge. If it is a cached inventory value, age and refresh success are part of the value's contract.

Finally I decide how close this signal is to user impact. Some topics in this series are direct symptoms; others are explanatory evidence. `Resolved Notifications Are Part of the Incident Lifecycle` belongs at the point where it can reduce investigation time without claiming more certainty than the underlying source provides. That classification determines whether it becomes a page, a warning, a panel set drill-down or simply retained forensic context.

## Competing hypotheses before I touch the production stack

I try to write down multiple explanations before making a change. For **Resolved Notifications Are Part of the Incident Lifecycle**, the candidate set I would test includes: **one root failure fans out into many pages**; **notification delivery fails after the rule fires**; **the SLO burns slowly enough to evade a short-window rule**; **the threshold is noisy but the service is healthy**; and **a real symptom is delayed by an inappropriate `for` duration**. The point is not that all five are equally likely. It is to stop the first plausible graph from becoming the conclusion.

The primary observation `increase(hserver_postgres_deadlocks_total[15m])` should eliminate some of those hypotheses, not all of them. I choose the next query or log source by information gain: which check can separate the most remaining explanations at the lowest operational cost? A fresh internal probe versus a failed public probe immediately moves suspicion toward the edge. High memory utilization with low pressure and stable swap activity moves me away from a memory-emergency diagnosis. A stale FreeSWITCH heartbeat with a running container moves the problem from process liveness into worker readiness.

This habit is especially useful on a single host because many symptoms are correlated. Storage pressure can slow databases, logs and containers simultaneously. Host memory pressure can make the monitoring stack itself late. A router or Internet failure can make every public service look broken while the applications are healthy. Explicit competing hypotheses keep correlation from being mistaken for independent failures.

## The observation contract I expect this signal to keep

For `increase(hserver_postgres_deadlocks_total[15m])` I expect a written contract even if it is only a few lines in a runbook. The contract says who produces the data, what unit it uses, which labels are bounded and meaningful, how often it should update, what reset behavior exists, and what missing data means. Without those details an old metric can survive long after its interpretation has changed.

The contract also names the strongest claim the signal supports. Deadlock counters preserve evidence of a concurrency failure that application success-rate graphs may quickly forget. That sentence is intentionally narrower than “the service is healthy.” It leaves room for independent evidence and tells future maintainers not to reuse the metric for a stronger conclusion without re-validating it.

Freshness belongs in the contract whenever the producer is not scraped directly. Cache-backed Docker inventory, textfile metrics, heartbeat state and backup timestamps can all remain syntactically valid after the producer stops. I therefore prefer either an explicit age metric or a timestamp from which age can be derived. For direct Prometheus targets, `up` is part of the collection contract but still not the service-health contract.

Finally, the contract includes data sensitivity. Labels and log content must not turn operational telemetry into a secret-disclosure channel. If the observation cannot be collected safely with bounded identity and least privilege, I redesign the data-collection path rather than assuming the monitoring network is trusted.

## Start with the failure, not the exporter

The degradation model for this article is: **A PostgreSQL deadlock can resolve automatically by aborting one transaction, leaving the service apparently healthy after the incident.** That wording matters because it describes the operational ambiguity I need to remove. A raw metric has no value until I know what claim I am trying to make from it.

The obvious monitoring mistake is to collapse several layers into one binary state. A process can exist while the application is unusable. A data-collection path can return a number that is already stale. A public service can correctly return a redirect or authorization error and still be healthy. A database can accept a TCP connection while lock contention makes useful queries stall. A host can report high memory utilization while reclaimable page cache means applications are not under pressure. The same general problem appears repeatedly: one layer's “up” is only evidence about that layer.

I therefore map each failure to at least three questions. First, what is the earliest useful signal that something is changing? Second, what is the strongest user-visible symptom I can observe independently? Third, what evidence tells me the monitoring path is alive enough to trust the first two answers? For `Resolved Notifications Are Part of the Incident Lifecycle`, `increase(hserver_postgres_deadlocks_total[15m])` belongs in that chain, but it is never allowed to stand alone if the failure can be confirmed from another layer.

This is also how I decide whether an alerting condition belongs on a metric. A signal may be excellent for diagnosis and terrible for paging. Context switches, container block-I/O bytes or database size trends can be valuable evidence without being reasons to interrupt an operator immediately. Conversely, a public probe failure or no-healthy-worker condition may deserve much more direct attention because it is already close to user impact.

## Where this sits in the hserver observability architecture

Alert engineering begins after collection. A threshold crossing is not automatically an incident, and an incident does not need twenty independent pages. I distinguish predictive resource alerting conditions from user-facing symptom alerting conditions. Disk capacity, certificate expiry and memory pressure can warn before an outage. Public availability failure or “no healthy voice worker” is already a service symptom. The `for` duration filters short-lived transitions but cannot be copied blindly: waiting ten minutes for a total public outage is very different from requiring sustained high load before paging.

Alertmanager grouping and inhibition encode relationships between failures so one root event does not become a notification storm. Warning and critical are response contracts rather than colors. Notification delivery is itself monitored because rule correctness is meaningless if no message reaches an operator. SLO-style rules add another time dimension: error-budget burn rate distinguishes a fast outage consuming reliability budget immediately from a slower degradation. I adapt the SRE model to the traffic and scale of this server rather than importing hyperscale thresholds without evidence.

For this article, the component boundary matters as much as the metric. The the production stack accepted observability stack includes Prometheus, Grafana, Loki, Alloy, Alertmanager, Blackbox Exporter, Node Exporter, cAdvisor, SMART collection, Docker inventory and deep host/database data-collection paths, plus application-native and external synthetic signals. The latest acceptance artifact records 52/52 accepted Prometheus targets UP, 106 alerting condition/recording rules loaded, 15 provisioned panel sets and 10/10 public probes UP.

I avoid interpret those counts as a maturity score. More targets and more rules can make a system worse if they add noise or cost without reducing uncertainty. The useful part is that the inventory is explicit and accepted. When I add a control for `Resolved Notifications Are Part of the Incident Lifecycle`, I can ask which existing layer already sees part of the problem, whether a new metric is necessary, and how the new observation will be validated after deployment.

## The decision this monitor should let me make

If this telemetry cannot change a decision, it should not automatically consume always-on budget. For **Resolved Notifications Are Part of the Incident Lifecycle**, the decisions fall into four categories. I may need to intervene immediately because a service contract is already broken. I may need to schedule capacity work because margin is shrinking. I may need to isolate a dependency during incident diagnosis. Or I may decide that the condition is normal and explicitly avoid action.

That last outcome is important. Monitoring is partly a system for proving when *not* to react. Page cache, historical swap, a 302 authentication redirect, a controlled restart, or a busy response from a SIP endpoint can look abnormal without representing infrastructure failure. The metric model should carry enough context to distinguish those cases.

I keep another rule: want the monitor to make rollback decisions safer. If a deployment changes `increase(hserver_postgres_deadlocks_total[15m])`, I should be able to compare the new state with the accepted baseline and decide whether the change is intended. That is why provenance `b65d5d4` stays attached to the topic. A the production stack metric without a known configuration history is harder to use as change evidence.

At scale this decision-centric approach becomes even more important. Hundreds of hosts can produce unlimited telemetry; operator time remains finite. The series therefore treats observability as a decision system rather than a storage system.

## Why this particular collection path won

There are usually several ways to obtain the state behind **Resolved Notifications Are Part of the Incident Lifecycle**: scrape an existing exporter, query an application API, run a SQL statement, parse logs, inspect the Docker API, read a Linux kernel interface, or publish a small custom metric through the textfile path. I choose among them by authority, cost, security and failure independence.

The closest source is not always the best source. A Docker container metric can tell me process resource use but not whether PostgreSQL sessions are waiting. A log parser can count authentication failures but is a weaker source for current service readiness than a direct state query. A raw TCP probe is cheap but deliberately shallow. A deep query may be authoritative but require credentials or create load. The implementation on hserver behind `increase(hserver_postgres_deadlocks_total[15m])` is valuable because it sits at the layer that owns the state I need to interpret.

I keep another rule: prefer collection paths with visible failure. A custom script that exits silently and leaves yesterday's textfile metric behind is worse than a data-collection path that exports its own success and age. A cache should expose refresh result and age. A database data-collection path should expose whether its query succeeded. A log pipeline should expose drops. The observer has to be observable.

The chosen path therefore reflects more than convenience. It is part of the degradation model: which component can lie, which credential can expire, which namespace the query sees, and what remains observable when another layer breaks.

## How I reason about a threshold for this topic

I avoid begin with a round number. I begin with the consequence I am trying to avoid and how much reaction time exists. Capacity thresholds such as disk or connection utilization should leave enough margin to investigate before exhaustion. Pressure thresholds should remain high long enough to distinguish real contention from transient scheduling noise. Certificate thresholds are measured in days because the repair process is administrative, not millisecond-sensitive. External availability failures can justify much faster response.

For **Resolved Notifications Are Part of the Incident Lifecycle**, the next threshold review should use the historical distribution plus the component's configured limit and the time needed to act. If that distribution is not captured in the the production stack acceptance artifact artifact, the honest value is **[CURRENT MEASUREMENT NEEDED]**. I avoid derive a the production stack page from an attractive number in a blog post.

I keep another rule: test both sides of the boundary. A warning threshold should actually enter pending/firing state when a fixture crosses it, and it should resolve when the signal recovers. A critical threshold should not be inhibited by the warning in a way that loses the more serious state. If the signal is a counter, the window should contain enough events to be meaningful. If it is a gauge, the `for` duration and freshness semantics matter more than counter reset behavior.

Thresholds are therefore versioned policy. When topology, workload, resource limits or data-collection path semantics change, I expect the threshold to be reviewed alongside the code.

## The mechanism underneath the graph

Prometheus alerting condition rules move through inactive, pending and firing states. A `for` duration controls the pending-to-firing transition; it does not make an expression more correct. Alertmanager then groups, routes, inhibits and repeats notifications. Those are separate state machines. SLO burn-rate rules add another layer by comparing observed error ratio with the error budget implied by the objective. Multi-window designs use a short window for timely detection and a long window for confidence that the burn is sustained.

That mechanism matters for `Resolved Notifications Are Part of the Incident Lifecycle` because two visually similar graphs can have very different semantics. A cumulative counter should normally be turned into a rate or increase over a time window. A gauge can be read directly but still needs freshness. A ratio is meaningless if its denominator is missing, zero or describes a different capacity boundary. A status value needs an explicit state model. A log-derived count depends on the reliability of ingestion and parsing. A synthetic probe depends on where the probe originates and which route it exercises.

I try to preserve units all the way from collection to the panel and alerting condition. Seconds should not silently become milliseconds. Bytes should not be compared with decimal “GB” labels without deciding which convention is in use. Percentages should identify their denominator. Ages should be derived from timestamps in a timezone-independent way. These details look small in configuration review and become large during incidents, when the operator is making decisions from the graph under time pressure.

The other subtlety is reset behavior. Counters restart with processes. Container identities change on recreation. database cumulative statistics can reset after engine restart. A panel set that uses raw cumulative values can therefore interpret restart as recovery or huge negative activity. Query functions and labels need to match the lifecycle of the component being measured.

## Implementation: make the observation cheap and reproducible

The implementation on hserver is deliberately smaller than the explanation. I expect the collection path to be boring: deterministic configuration in Git, bounded work on the host, a clear scrape or evaluation cadence, and a result that can be checked after deployment. Repository evidence associated with this topic is `b65d5d4`.

A representative query or configuration fragment is:

```
send_resolved: true
# Acceptance snapshot: notification success=13, failure=0, resolved=6.
```

The fragment is not meant to be copied blindly into another system. Labels, device names, mount points, job names and custom metric families are deployment-specific. The important point is the shape of the control. Ratios need denominators. Counters need rates or increases over windows. Slow-changing inventory should not be polled at CPU-metric cadence. Authentication-aware probes need status semantics. Freshness-sensitive data-collection paths need age checks. Expensive queries should be recorded or sampled at a cadence that matches the decision they support.

I keep another rule: keep configuration ownership separate from runtime evidence. Prometheus rules, scrape configuration, panel sets and data-collection path code live in the reviewed source tree. Runtime acceptance data records what the production stack actually observed. Secret values stay out of both metrics and public documentation. This lets me reproduce the monitoring design without turning the monitoring repository into a credential store.

## Query semantics: small expression mistakes become large operational mistakes

The implementation on hserver fragment earlier is intentionally small, but even small PromQL or LogQL expressions carry assumptions. Counter queries need a window long enough to contain useful events but short enough to react. Ratios need both numerator and denominator to describe the same population. Aggregation labels decide whether a single bad instance disappears inside a fleet average. `sum`, `avg`, `max` and `count` answer different questions; choosing one because it makes the panel look cleaner is not query engineering.

For `Resolved Notifications Are Part of the Incident Lifecycle`, I review whether the query behaves during restart, missing series, zero traffic and partial fleet failure. A rate over an idle counter may legitimately be zero. A ratio with no denominator needs protection. `absent()` or target-state logic may be more appropriate than treating missing data as zero. Freshness checks may be required for textfile or cache-backed metrics. A histogram, if present, needs bucket semantics and enough observations before a quantile is meaningful.

I keep another rule: avoid encoding the entire diagnosis into one unreadable PromQL expression. Recording rules can name intermediate concepts, make panel sets cheaper and give alerting conditions a reviewed semantic layer. The cost is extra stored series and another rule dependency, so I keep them where the expression is repeatedly valuable, not merely because the query language permits it.

The same principle applies to logs: a regex that happens to match today's message format is not a durable security signal unless the source and parser are tested. Queries are the production stack code when alerting conditions and incident decisions depend on them.

## Walk the failure from symptom back to cause

A useful way to review this monitor is to imagine a failure and force myself to predict what each layer would show. I avoid claim the following sequence happened unless it is part of the recorded evidence; it is a design exercise for the control.

Start with the user-visible symptom related to **Resolved Notifications Are Part of the Incident Lifecycle**. The top-level probe or service metric changes first or eventually. I then ask whether the host is still reachable, whether the target is still being scraped, and whether `increase(hserver_postgres_deadlocks_total[15m])` is fresh. If the target is down, an old threshold value is no longer the primary evidence; target failure becomes the first branch. If the target is up, I compare the signal with its nearest independent corroborator.

From there I trace downward. A host-pressure signal leads to per-container attribution and kernel logs. A container symptom leads to host resource state and application health. A database symptom leads from reachability to connection, wait, lock and engine state. A public probe failure is compared with the internal probe, DNS/TLS phases and edge logs. A VoIP symptom is separated into signaling, worker and media evidence. A backup symptom is followed through job, artifact, checksum and restore state.

The operational aim is not to prove that every incident follows one tree. It is to make sure each metric has a place in an investigation. If a signal cannot tell me which branch to take next, I question whether it belongs in the always-on monitoring budget.

## The false-positive and false-negative traps

Every monitoring decision has at least two ways to be wrong. A false positive declares a failure when the system is operating within its intended semantics. A false negative keeps the panel set green while the service contract is broken. `Resolved Notifications Are Part of the Incident Lifecycle` is useful only if I can describe both.

A common false positive is reading a state without duration or context. Non-zero swap can be historical. High CPU can be productive work. A protected HTTP endpoint can return 302, 401 or 403 because authentication is functioning. A brief container restart can be a deployment. A temporarily high database connection count can be harmless if capacity and latency remain healthy. These cases need windows, denominators or state semantics before they become incidents.

The false negative is usually more dangerous. A target can scrape successfully while its downstream dependency is broken. A stale custom metric can remain below threshold after its data-collection path died. A database socket can accept connections while waits or locks stop useful work. A FreeSWITCH process can run while the worker heartbeat is stale. A backup archive can exist while restore verification has not succeeded. Those failures are why the architecture uses independent layers instead of treating one green signal as global truth.

When I review a rule or panel, I explicitly ask: what normal condition could make this look bad, and what bad condition could make this look normal? That question often produces a better second metric than adding another threshold to the first one.

## What would make this monitor lie?

I ask this question explicitly because most monitoring failures are not fabricated numbers; they are numbers interpreted outside their validity. `increase(hserver_postgres_deadlocks_total[15m])` can become misleading if its data-collection path is stale, labels change, the underlying source resets, the query aggregates away the failing member, the scrape path observes a different network namespace, or the monitored component changes semantics after an upgrade.

Caching creates another class of lies. The Docker storage inventory is deliberately cached because continuous filesystem inspection was too expensive. A cache-backed metric is only trustworthy when cache age and refresh success are visible. Textfile metrics have the same issue if the producer stops updating them. Database-derived metrics can lie by omission if the data-collection path account loses access to a system view. Log-derived metrics can go quiet because Alloy or Loki is dropping data rather than because the event stopped happening.

Authentication and synthetic probes can lie through overly permissive expectations. Following redirects blindly may turn an application failure into a successful login-page response. Accepting every status code may hide a broken route. Requiring only 200 may create the opposite error and call a healthy access-control response an outage. The probe has to encode the intended contract.

My response to these risks is not distrust of monitoring. It is meta-monitoring, freshness, independent evidence and explicit UNKNOWN states when the observation path cannot make a strong claim.

## The hserver case that shaped this part of the design

Notification delivery became part of the alerting condition model rather than an assumption. The accepted snapshot records 13 successful external notification events, zero failures and six resolved events. Those are snapshot counters, not an SLA, but they demonstrate that firing and recovery both travel through the delivery path. A quiet Alertmanager is trustworthy only when rule evaluation, targets and notification endpoints are also healthy.

I keep that case as a guardrail for `Resolved Notifications Are Part of the Incident Lifecycle` because it prevents the discussion from becoming a generic monitoring tutorial. The interesting question is not whether another platform supports the same metric. It is what decision the signal enabled on this constrained the production stack host, what cost it imposed, and what evidence proved that the change improved rather than merely rearranged the system.

Another consequence is that keeps causality honest. A before/after measurement is evidence for this configuration at that time. It is not a universal benchmark for cAdvisor, Prometheus, Docker, OpenBao or any database engine. When the article makes a recommendation, the recommendation is about the engineering method—measure, isolate cost, preserve the useful signal, verify the new degradation modes—not about assuming another machine will reproduce the same number.

## Turning the observation into an alerting condition without creating noise

Not every article in this series ends with a page. Some of the best signals are diagnostic. When I do alerting condition, I separate **prediction**, **saturation**, and **symptom**. Prediction covers conditions such as disk capacity or certificate expiry where action before failure is possible. Saturation covers sustained pressure or exhausted pools. Symptoms cover conditions such as a failed public probe, no healthy SIP worker, or unsuccessful restore verification where the service contract is already affected.

The rule duration has to fit the failure. A single scrape miss or short deployment restart should not create an incident. A total public outage should not sit pending for an arbitrary long `for:` window simply because another resource rule uses ten minutes. Warning and critical labels are response contracts: warning means investigate or schedule action before the margin disappears; critical means the operating state is already outside the tolerated envelope or approaching it fast enough to require immediate attention.

I keep another rule: ask what other alerting condition will fire at the same time. If host loss makes every public service fail, paging separately for Grafana, OTA, authentication, gateway and VoIP adds noise without information. Grouping and inhibition should preserve useful symptoms while making the likely root event obvious. Resolution is part of the lifecycle too. The latest accepted notification evidence recorded external notification counters in the acceptance artifact: 13 success, 0 failure, 6 resolved; that is a snapshot of delivery behavior, not an SLA claim.

For `Resolved Notifications Are Part of the Incident Lifecycle`, the alerting condition is successful only if its annotation tells me what was observed, over what window, which panel set or runbook to open next, and what secondary signal can confirm the hypothesis.

## Acceptance: prove the monitor after changing it

I avoid treat a configuration commit as proof that monitoring works. After meaningful observability changes I compare the desired state in Git with runtime acceptance. The the production stack artifact records 52/52 accepted Prometheus targets UP, 106 alerting condition/recording rules loaded, 0 firing and 0 pending alerting conditions, 27,578 active Prometheus series, against a 27,414-series acceptance baseline, 10/10 public probes UP, 9/9 database probes UP and 35 monitored configuration files with zero drift in the latest runtime sample. Those numbers are useful because they make blind spots and accidental cardinality growth measurable after deployment.

The validation depends on the feature. A scrape change should prove the target is UP and the expected series exists. A relabel change should prove the required panel set and alerting condition queries still return data. A log-pipeline change should prove cursor continuity and check drop counters. A public probe should be exercised against both healthy and intentionally invalid behavior. A backup control should be followed by checksum and restore evidence. A notification change should send a synthetic alerting condition and verify both firing and resolved delivery.

Where safe, I prefer failure injection to passive confidence. The external dead-man watcher was tested by forcing a synthetic outage: the hosted workflow failed, an incident issue was created, recovery later passed and the issue closed. That sequence proved more than reading the workflow YAML. The same idea scales down to small controls: temporarily make a test target fail, expire a synthetic sample, or use a fixture that triggers the rule without damaging the production stack.

## Tests that make the monitoring logic trustworthy

I separate tests into collection, semantics, rule and end-to-end behavior. Collection tests answer whether the metric or log event appears with the expected labels and units. Semantic tests compare it with the underlying source: `/proc`, Docker, SQL, a service API, a certificate, an actual file timestamp or another authoritative state. Rule tests feed boundary conditions into PromQL or alerting condition fixtures so warning, critical, pending and resolved transitions are predictable.

End-to-end testing is stronger. A synthetic failure should make the expected alerting condition fire through the real routing path, and recovery should produce the expected resolution. The external watcher already demonstrated this model by creating and then closing an incident around a forced outage. For backup monitoring, an end-to-end test is a restore verification rather than a successful archive command. For authentication-aware probing, it is seeing the expected redirect or authorization status instead of weakening the route to return 200.

For `Resolved Notifications Are Part of the Incident Lifecycle`, I would also test missing data. Many rules are exercised only with high or low values and never with a vanished series. The correct behavior may be a target-down alerting condition, an UNKNOWN state, or a dedicated freshness alerting condition. Missing evidence should not silently inherit the last green value.

## The investigation sequence I expect at 2 a.m.

The runbook for this signal is intentionally ordered. First confirm time and freshness. I avoid troubleshoot an old sample as though it were current. Second confirm the data-collection path or target path. Third compare the value with the nearest independent signal. Fourth look at the dependency layer below it. Fifth use logs or a direct engine query for detail. Only then change the production stack.

For `Resolved Notifications Are Part of the Incident Lifecycle`, the first direct question is whether `increase(hserver_postgres_deadlocks_total[15m])` is updating on schedule. If it is, I compare it with the signal that would be expected to move under the same failure hypothesis. If the two disagree, that disagreement is evidence: either the original hypothesis is wrong, the metrics have different semantics, or one observation path is broken.

I keep another rule: preserve before/after evidence around changes. If I tune a scrape interval, relabel metrics, disable an expensive data-collection path feature or change an alerting condition window, I capture the relevant series count, memory state, target state and rule health. That makes rollback rational. Without a before state, optimization can quietly delete the only metric that explained a future incident.

The concluding runbook step is acceptance, not “container restarted successfully.” I expect the query to return the expected data, the panel set to render, the rule to evaluate, the synthetic path to behave correctly, and the monitoring stack to remain inside its resource budget.

## Questions I keep in design review

Before merging a monitoring change around this topic, I expect concise answers to a set of questions. What failure does the signal detect? What is the authoritative source? How stale can it become before interpretation is unsafe? What is the collection cost? Does it add an unbounded label? Can it expose a secret? What normal condition looks similar to failure? What independent signal confirms the problem? What happens if the data-collection path itself dies? Does the alerting condition have an operator action? How will I prove the change in the production stack without causing a real outage?

Those questions are deliberately tool-agnostic. They work whether the implementation is Prometheus, Loki, a shell data-collection path, SQL, Blackbox Exporter or a GitHub-hosted workflow. They also make deletion possible. If a metric no longer supports a panel set, alerting condition, capacity decision or incident workflow, I can remove it instead of preserving telemetry indefinitely because “we might need it.”

The concluding review question is whether the control still makes sense on a 7.1 GiB host. A signal that would be cheap in a large observability cluster can be expensive here. `Resolved Notifications Are Part of the Incident Lifecycle` has to justify not only correctness but its share of the limited the production stack budget.

## Operational limits and thresholds are configuration, not physics

Thresholds in this system are chosen from capacity, consequence and response time. Disk warning/critical bands, certificate windows, alerting condition `for:` durations, heartbeat age, memory budgets and SLO burn-rate factors all express policy. I document them as current the production stack choices, not constants of Linux or Prometheus.

That distinction matters during growth. If workload changes, a threshold that once provided useful warning may become permanently noisy. If a data-collection path is optimized, an observability-memory budget may be tightened. If a service moves off-host, its failure domain changes and an old alerting condition relationship may no longer apply. If public traffic increases, SLO windows may have enough events to use a different statistical model.

For `Resolved Notifications Are Part of the Incident Lifecycle`, I would review the threshold whenever the component version, workload, resource limit or topology materially changes. I would also inspect the historical distribution before tightening it. A threshold selected only from a desired round number is less defensible than one derived from observed normal behavior plus an explicit safety margin.

Where the the production stack acceptance artifact evidence does not contain the distribution needed to justify a new threshold, the article leaves **[CURRENT MEASUREMENT NEEDED]**. That is not an incomplete monitoring practice; it is a refusal to pretend policy has empirical support that has not yet been collected.

## What the current accepted system says

The 2026-09-15 acceptance snapshot gives me a concrete reference point while writing this series. It records 52/52 accepted Prometheus targets UP, 106 alerting condition/recording rules loaded, 0 firing and 0 pending alerting conditions, and 15 provisioned panel sets. Prometheus reported 27,578 active Prometheus series, against a 27,414-series acceptance baseline. Public probing reported 10/10 public probes UP; database probing reported 9/9 database probes UP. The accepted configuration manifest reported 35 monitored configuration files with zero drift in the latest runtime sample.

For storage and retention, Prometheus retention set to about 30 days with a 15 GB size cap; Loki retention set to 168 hours. For hardware evidence, SMART status healthy in the acceptance artifact, with a 49 C device-temperature sample. For recovery, encrypted DR verification PASS, required payload PASS, internal checksum PASS, off-host pull PASS, and restore verification PASS. For OpenBao, main OpenBao initialized and unsealed with Transit auto-unseal; same-host seal node initialized and unsealed with no host-published ports. These values are intentionally described with a date because they are not permanent properties of the architecture. They are evidence that the system reached a known state after a particular round of changes.

This distinction is important for `Resolved Notifications Are Part of the Incident Lifecycle`. Monitoring documentation tends to age badly when it turns an observation into a law. I would rather write “27,578 active series in this acceptance snapshot” than imply that 27,578 is a target, a limit or a recommendation. The same applies to cAdvisor memory, disk temperature, panel set count and alerting condition-rule count. The architecture should survive changing numbers because the interpretation rules remain explicit.

## What I would change at larger scale

The small-server version optimizes for bounded cost and direct inspectability. In a multi-host design I would preserve the semantic model but move some responsibilities. Metrics storage could move off the application host. Long-term retention could use a system designed for remote or object-backed storage. Loki could live on a dedicated node. Exporter and data-collection path work could be distributed closer to the workloads while query and alerting condition evaluation stay centralized. High-availability Alertmanager and independent monitoring storage would reduce shared failure domains.

I would not, however, replace `increase(hserver_postgres_deadlocks_total[15m])` with a generic “enterprise monitoring” product and call the problem solved. The key question remains what the observation proves. If the signal is about Linux pressure, the kernel semantics remain. If it is about database locks, the engine semantics remain. If it is about SIP versus RTP, the protocol boundaries remain. If it is about dead-man monitoring, the observer still has to live outside the failure domain.

Scale primarily changes collection topology, retention, redundancy and automation. It does not remove the need to define failure semantics. In fact, larger systems punish ambiguous metrics more severely because a noisy or high-cardinality mistake multiplies across more hosts and more operators.

## What I keep from this decision

The practical lesson from **Resolved Notifications Are Part of the Incident Lifecycle** is that a useful monitor is a tested claim about a degradation mode, not a decorative line on a panel set. The control is useful because I know its acquisition cost, expected cadence, degradation modes, corroborating signals and response path. That is the standard I now use before adding another metric or alerting condition to hserver.

The server is still an old Mac mini. That constraint has not stopped the monitoring system from becoming serious. It has forced every layer to be explicit about what it is worth. For me that is the more interesting engineering result: the production stack-grade observability is less about how many products are installed and more about whether the evidence is sufficient, current, independent where necessary, and cheap enough that the observer does not become the outage.
