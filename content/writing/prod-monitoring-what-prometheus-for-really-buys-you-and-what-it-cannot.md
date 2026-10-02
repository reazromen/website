---
title: What Prometheus `for:` Really Buys You—and What It Cannot
url: /posts/prod-monitoring-what-prometheus-for-really-buys-you-and-what-it-cannot.html
date: '2026-09-15'
read_time: 35
excerpt: A production-engineering deep dive into what prometheus `for:` really buys
  you—and what it cannot, grounded in the 2014 Mac mini hserver observability stack
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
eyebrow: 'Production Monitoring: Alert Engineering & SLOs · deep-dive'
outputs:
- url: /posts/prod-monitoring-what-prometheus-for-really-buys-you-and-what-it-cannot.html
  template: cms/templates/posts/posts--prod-monitoring-what-prometheus-for-really-buys-you-and-what-it-cannot.tpl
  source: cms/templates/posts/posts--prod-monitoring-what-prometheus-for-really-buys-you-and-what-it-cannot.json
---

The useful question behind **What Prometheus `for:` Really Buys You—and What It Cannot** was not whether I could collect another metric. It was whether the metric would reduce uncertainty during a the accepted runtime failure on a very small machine.

The host is 2014 Apple Mac mini running Linux, with roughly 7.1 GiB usable RAM from an 8 GB-class machine. Applications, databases, networking, authentication, OTA, OpenBao, VoIP and the observability stack share the same limited CPU, memory and storage. That makes monitoring part of the workload rather than something outside it. The central failure I am trying to avoid is not merely “a metric went high.” The system should give me enough measured proof to tell whether a user-facing service is degrading, which dependency owns the problem, whether the signal is current, and whether the monitoring path itself is still trustworthy.

For this specific problem the primary observation point is `HserverExternalNotificationDeliveryFailed from incident signal-sink failure counters`. The short the accepted runtime note that preceded this article captured the core finding: The notification path is a the accepted runtime dependency and must be monitored from inside the observability system rather than assumed to work forever. This long-form version goes further: what that signal really proves, which nearby signals can falsify my first hypothesis, how I implement and incident signal on it, what it costs on this host, and how I would redesign the same control at larger scale.

The numbers in this article are not generic benchmarks. When I mention 27,578 active Prometheus series, against a 27,414-series acceptance baseline, cAdvisor measured at 428.2 MiB before the low-RAM work and 27.87 MiB in one post-change sample, with an observed steady range around 20–28 MiB, or any other concrete value, I mean the 2026-09-15 acceptance snapshot unless I explicitly say otherwise. If a current value is not present in the accepted measured proof, I leave `[CURRENT MEASUREMENT NEEDED]` rather than inventing a number.

## The engineering question specific to this article

The short version of the problem is not “how do I graph What Prometheus `for:` Really Buys You—and What It Cannot?” It is: **An operational-monitoring system that detects failures but cannot notify anyone is partially failed even if every Prometheus target remains green.** That failure can be confused with neighboring conditions, which is why the primary observation is `HserverExternalNotificationDeliveryFailed from incident signal-sink failure counters` rather than a generic process-up flag.

The current reviewed the accepted runtime conclusion is specific: The notification path is a the accepted runtime dependency and must be monitored from inside the observability system rather than assumed to work forever. I turn that conclusion into an operational practice—meta-monitoring of paging infrastructure—and into a preventive control: Page or surface notification failures through an alternate visible channel and regularly test delivery with controlled synthetic incident signals. Those three layers are intentionally separate. The finding explains what the measured proof taught me. The practice describes how I diagnose it. The prevention rule describes how I keep the same ambiguity from returning after the next deployment.

There is also a data-model question. The observation has to retain the dimension that matters without encoding unbounded identity. If the question is per node, the node label matters. If it is fleet capacity, an aggregate may be more useful. If it is an event such as a deadlock or OOM kill, a counter over a time window carries different meaning from a current-state gauge. If it is a cached inventory value, age and refresh success are part of the value's contract.

Finally I decide how close this signal is to user impact. Some topics in this series are direct symptoms; others are explanatory measured proof. `What Prometheus`for:`Really Buys You—and What It Cannot` belongs at the point where it can reduce investigation time without claiming more certainty than the underlying source provides. That classification determines whether it becomes a page, a warning, a Grafana view drill-down or simply retained forensic context.

## Competing hypotheses before I touch the accepted runtime

I try to write down multiple explanations before making a change. For **What Prometheus `for:` Really Buys You—and What It Cannot**, the candidate set I would test includes: **the SLO burns slowly enough to evade a short-window rule**; **the threshold is noisy but the service is healthy**; **a real symptom is delayed by an inappropriate `for` duration**; **one root failure fans out into many pages**; and **notification delivery fails after the rule fires**. The point is not that all five are equally likely. It is to stop the first plausible graph from becoming the conclusion.

The primary observation `HserverExternalNotificationDeliveryFailed from incident signal-sink failure counters` should eliminate some of those hypotheses, not all of them. I choose the next query or log source by information gain: which check can separate the most remaining explanations at the lowest operational cost? A fresh internal probe versus a failed public probe immediately moves suspicion toward the edge. High memory utilization with low pressure and stable swap activity moves me away from a memory-emergency diagnosis. A stale FreeSWITCH heartbeat with a running container moves the problem from process liveness into worker readiness.

This habit is especially useful on a single host because many symptoms are correlated. Storage pressure can slow databases, logs and containers simultaneously. Host memory pressure can make the monitoring stack itself late. A router or Internet failure can make every public service look broken while the applications are healthy. Explicit competing hypotheses keep correlation from being mistaken for independent failures.

## The observation contract I expect this signal to keep

For `HserverExternalNotificationDeliveryFailed from incident signal-sink failure counters` The system should give me a written contract even if it is only a few lines in a runbook. The contract says who produces the data, what unit it uses, which labels are bounded and meaningful, how often it should update, what reset behavior exists, and what missing data means. Without those details an old metric can survive long after its interpretation has changed.

The contract also names the strongest claim the signal supports. The notification path is a the accepted runtime dependency and must be monitored from inside the observability system rather than assumed to work forever. That sentence is intentionally narrower than “the service is healthy.” It leaves room for independent measured proof and tells future maintainers not to reuse the metric for a stronger conclusion without re-validating it.

Freshness belongs in the contract whenever the producer is not scraped directly. Cache-backed Docker inventory, textfile metrics, heartbeat state and backup timestamps can all remain syntactically valid after the producer stops. I therefore prefer either an explicit age metric or a timestamp from which age can be derived. For direct Prometheus targets, `up` is part of the collection contract but still not the service-health contract.

Finally, the contract includes data sensitivity. Labels and log content must not turn operational telemetry into a secret-disclosure channel. If the observation cannot be collected safely with bounded identity and least privilege, I redesign the measurement path rather than assuming the monitoring network is trusted.

## Start with the failure, not the exporter

The incident shapel for this article is: **An operational-monitoring system that detects failures but cannot notify anyone is partially failed even if every Prometheus target remains green.** That wording matters because it describes the operational ambiguity I need to remove. A raw metric has no value until I know what claim I am trying to make from it.

The obvious monitoring mistake is to collapse several layers into one binary state. A process can exist while the application is unusable. A measurement path can return a number that is already stale. A public service can correctly return a redirect or authorization error and still be healthy. A database can accept a TCP connection while lock contention makes useful queries stall. A host can report high memory utilization while reclaimable page cache means applications are not under pressure. The same general problem appears repeatedly: one layer's “up” is only measured proof about that layer.

I therefore map each failure to at least three questions. First, what is the earliest useful signal that something is changing? Second, what is the strongest user-visible symptom I can observe independently? Third, what measured proof tells me the monitoring path is alive enough to trust the first two answers? For `What Prometheus`for:`Really Buys You—and What It Cannot`, `HserverExternalNotificationDeliveryFailed from incident signal-sink failure counters` belongs in that chain, but it is never allowed to stand alone if the failure can be confirmed from another layer.

This is also how I decide whether an incident signal belongs on a metric. A signal may be excellent for diagnosis and terrible for paging. Context switches, container block-I/O bytes or database size trends can be valuable measured proof without being reasons to interrupt an operator immediately. Conversely, a public probe failure or no-healthy-worker condition may deserve much more direct attention because it is already close to user impact.

## Where this sits in the hserver observability architecture

Alert engineering begins after collection. A threshold crossing is not automatically an incident, and an incident does not need twenty independent pages. I distinguish predictive resource incident signals from user-facing symptom incident signals. Disk capacity, certificate expiry and memory pressure can warn before an outage. Public availability failure or “no healthy voice worker” is already a service symptom. The `for` duration filters short-lived transitions but cannot be copied blindly: waiting ten minutes for a total public outage is very different from requiring sustained high load before paging.

Alertmanager grouping and inhibition encode relationships between failures so one root event does not become a notification storm. Warning and critical are response contracts rather than colors. Notification delivery is itself monitored because rule correctness is meaningless if no message reaches an operator. SLO-style rules add another time dimension: error-budget burn rate distinguishes a fast outage consuming reliability budget immediately from a slower degradation. I adapt the SRE model to the traffic and scale of this server rather than importing hyperscale thresholds without measured proof.

For this article, the component boundary matters as much as the metric. The current reviewed accepted observability stack includes Prometheus, Grafana, Loki, Alloy, Alertmanager, Blackbox Exporter, Node Exporter, cAdvisor, SMART collection, Docker inventory and deep host/database measurement paths, plus application-native and external synthetic signals. The latest acceptance artifact records 52/52 accepted Prometheus targets UP, 106 incident signal/recording rules loaded, 15 provisioned Grafana views and 10/10 public probes UP.

I do not interpret those counts as a maturity score. More targets and more rules can make a system worse if they add noise or cost without reducing uncertainty. The useful part is that the inventory is explicit and accepted. When I add a control for `What Prometheus`for:`Really Buys You—and What It Cannot`, I can ask which existing layer already sees part of the problem, whether a new metric is necessary, and how the new observation will be validated after deployment.

## The decision this monitor should let me make

If this telemetry cannot change a decision, it should not automatically consume always-on budget. For **What Prometheus `for:` Really Buys You—and What It Cannot**, the decisions fall into four categories. I may need to intervene immediately because a service contract is already broken. I may need to schedule capacity work because margin is shrinking. I may need to isolate a dependency during incident diagnosis. Or I may decide that the condition is normal and explicitly avoid action.

That last outcome is important. Monitoring is partly a system for proving when *not* to react. Page cache, historical swap, a 302 authentication redirect, a controlled restart, or a busy response from a SIP endpoint can look abnormal without representing infrastructure failure. The metric model should carry enough context to distinguish those cases.

I add one more check: want the monitor to make rollback decisions safer. If a deployment changes `HserverExternalNotificationDeliveryFailed from incident signal-sink failure counters`, I should be able to compare the new state with the accepted baseline and decide whether the change is intended. That is why provenance `49ec1dd` stays attached to the topic. A the accepted runtime metric without a known configuration history is harder to use as change measured proof.

At scale this decision-centric approach becomes even more important. Hundreds of hosts can produce unlimited telemetry; operator time remains finite. The series therefore treats observability as a decision system rather than a storage system.

## Why this particular collection path won

There are usually several ways to obtain the state behind **What Prometheus `for:` Really Buys You—and What It Cannot**: scrape an existing exporter, query an application API, run a SQL statement, parse logs, inspect the Docker API, read a Linux kernel interface, or publish a small custom metric through the textfile path. I choose among them by authority, cost, security and failure independence.

The closest source is not always the best source. A Docker container metric can tell me process resource use but not whether PostgreSQL sessions are waiting. A log parser can count authentication failures but is a weaker source for current service readiness than a direct state query. A raw TCP probe is cheap but deliberately shallow. A deep query may be authoritative but require credentials or create load. The implementation on hserver behind `HserverExternalNotificationDeliveryFailed from incident signal-sink failure counters` is valuable because it sits at the layer that owns the state I need to interpret.

I add one more check: prefer collection paths with visible failure. A custom script that exits silently and leaves yesterday's textfile metric behind is worse than a measurement path that exports its own success and age. A cache should expose refresh result and age. A database measurement path should expose whether its query succeeded. A log pipeline should expose drops. The observer has to be observable.

The chosen path therefore reflects more than convenience. It is part of the incident shapel: which component can lie, which credential can expire, which namespace the query sees, and what remains observable when another layer breaks.

## How I reason about a threshold for this topic

I do not begin with a round number. I begin with the consequence I am trying to avoid and how much reaction time exists. Capacity thresholds such as disk or connection utilization should leave enough margin to investigate before exhaustion. Pressure thresholds should remain high long enough to distinguish real contention from transient scheduling noise. Certificate thresholds are measured in days because the repair process is administrative, not millisecond-sensitive. External availability failures can justify much faster response.

For **What Prometheus `for:` Really Buys You—and What It Cannot**, the next threshold review should use the historical distribution plus the component's configured limit and the time needed to act. If that distribution is not captured in the the accepted runtime acceptance artifact artifact, the honest value is **[CURRENT MEASUREMENT NEEDED]**. I do not derive a the accepted runtime page from an attractive number in a blog post.

I add one more check: test both sides of the boundary. A warning threshold should actually enter pending/firing state when a fixture crosses it, and it should resolve when the signal recovers. A critical threshold should not be inhibited by the warning in a way that loses the more serious state. If the signal is a counter, the window should contain enough events to be meaningful. If it is a gauge, the `for` duration and freshness semantics matter more than counter reset behavior.

Thresholds are therefore versioned policy. When topology, workload, resource limits or measurement path semantics change, I expect the threshold to be reviewed alongside the code.

## The mechanism underneath the graph

Prometheus incident signal rules move through inactive, pending and firing states. A `for` duration controls the pending-to-firing transition; it does not make an expression more correct. Alertmanager then groups, routes, inhibits and repeats notifications. Those are separate state machines. SLO burn-rate rules add another layer by comparing observed error ratio with the error budget implied by the objective. Multi-window designs use a short window for timely detection and a long window for confidence that the burn is sustained.

That mechanism matters for `What Prometheus`for:`Really Buys You—and What It Cannot` because two visually similar graphs can have very different semantics. A cumulative counter should normally be turned into a rate or increase over a time window. A gauge can be read directly but still needs freshness. A ratio is meaningless if its denominator is missing, zero or describes a different capacity boundary. A status value needs an explicit state model. A log-derived count depends on the reliability of ingestion and parsing. A synthetic probe depends on where the probe originates and which route it exercises.

I try to preserve units all the way from collection to the panel and incident signal. Seconds should not silently become milliseconds. Bytes should not be compared with decimal “GB” labels without deciding which convention is in use. Percentages should identify their denominator. Ages should be derived from timestamps in a timezone-independent way. These details look small in configuration review and become large during incidents, when the operator is making decisions from the graph under time pressure.

The other subtlety is reset behavior. Counters restart with processes. Container identities change on recreation. database cumulative statistics can reset after engine restart. A Grafana view that uses raw cumulative values can therefore interpret restart as recovery or huge negative activity. Query functions and labels need to match the lifecycle of the component being measured.

## Implementation: make the observation cheap and reproducible

The implementation on hserver is deliberately smaller than the explanation. The system should give me the collection path to be boring: deterministic configuration in Git, bounded work on the host, a clear scrape or evaluation cadence, and a result that can be checked after deployment. Repository measured proof associated with this topic is `49ec1dd`.

A representative query or configuration fragment is:

```
- incident signal: ExampleSustainedCondition
  expr: <condition>
  for: 10m
  labels:
    severity: warning
```

The fragment is not meant to be copied blindly into another system. Labels, device names, mount points, job names and custom metric families are deployment-specific. The important point is the shape of the control. Ratios need denominators. Counters need rates or increases over windows. Slow-changing inventory should not be polled at CPU-metric cadence. Authentication-aware probes need status semantics. Freshness-sensitive measurement paths need age checks. Expensive queries should be recorded or sampled at a cadence that matches the decision they support.

I add one more check: keep configuration ownership separate from runtime measured proof. Prometheus rules, scrape configuration, Grafana views and measurement path code live in the reviewed source tree. Runtime acceptance data records what the accepted runtime actually observed. Secret values stay out of both metrics and public documentation. This lets me reproduce the monitoring design without turning the monitoring repository into a credential store.

## Query semantics: small expression mistakes become large operational mistakes

The implementation on hserver fragment earlier is intentionally small, but even small PromQL or LogQL expressions carry assumptions. Counter queries need a window long enough to contain useful events but short enough to react. Ratios need both numerator and denominator to describe the same population. Aggregation labels decide whether a single bad instance disappears inside a fleet average. `sum`, `avg`, `max` and `count` answer different questions; choosing one because it makes the panel look cleaner is not query engineering.

For `What Prometheus`for:`Really Buys You—and What It Cannot`, I review whether the query behaves during restart, missing series, zero traffic and partial fleet failure. A rate over an idle counter may legitimately be zero. A ratio with no denominator needs protection. `absent()` or target-state logic may be more appropriate than treating missing data as zero. Freshness checks may be required for textfile or cache-backed metrics. A histogram, if present, needs bucket semantics and enough observations before a quantile is meaningful.

I add one more check: avoid encoding the entire diagnosis into one unreadable PromQL expression. Recording rules can name intermediate concepts, make Grafana views cheaper and give incident signals a reviewed semantic layer. The cost is extra stored series and another rule dependency, so My default is to use them where the expression is repeatedly valuable, not merely because the query language permits it.

The same principle applies to logs: a regex that happens to match today's message format is not a durable security signal unless the source and parser are tested. Queries are the accepted runtime code when incident signals and incident decisions depend on them.

## Walk the failure from symptom back to cause

A helpful way to review this monitor is to imagine a failure and force myself to predict what each layer would show. I do not claim the following sequence happened unless it is part of the recorded measured proof; it is a design exercise for the control.

Start with the user-visible symptom related to **What Prometheus `for:` Really Buys You—and What It Cannot**. The top-level probe or service metric changes first or eventually. I then ask whether the host is still reachable, whether the target is still being scraped, and whether `HserverExternalNotificationDeliveryFailed from incident signal-sink failure counters` is fresh. If the target is down, an old threshold value is no longer the primary measured proof; target failure becomes the first branch. If the target is up, I compare the signal with its nearest independent corroborator.

From there I trace downward. A host-pressure signal leads to per-container attribution and kernel logs. A container symptom leads to host resource state and application health. A database symptom leads from reachability to connection, wait, lock and engine state. A public probe failure is compared with the internal probe, DNS/TLS phases and edge logs. A VoIP symptom is separated into signaling, worker and media measured proof. A backup symptom is followed through job, artifact, checksum and restore state.

The objective is not to prove that every incident follows one tree. It is to make sure each metric has a place in an investigation. If a signal cannot tell me which branch to take next, I question whether it belongs in the always-on monitoring budget.

## The false-positive and false-negative traps

Every monitoring decision has at least two ways to be wrong. A false positive declares a failure when the system is operating within its intended semantics. A false negative keeps the Grafana view green while the service contract is broken. `What Prometheus`for:`Really Buys You—and What It Cannot` is useful only if I can describe both.

A common false positive is reading a state without duration or context. Non-zero swap can be historical. High CPU can be productive work. A protected HTTP endpoint can return 302, 401 or 403 because authentication is functioning. A brief container restart can be a deployment. A temporarily high database connection count can be harmless if capacity and latency remain healthy. These cases need windows, denominators or state semantics before they become incidents.

The false negative is usually more dangerous. A target can scrape successfully while its downstream dependency is broken. A stale custom metric can remain below threshold after its measurement path died. A database socket can accept connections while waits or locks stop useful work. A FreeSWITCH process can run while the worker heartbeat is stale. A backup archive can exist while restore verification has not succeeded. Those failures are why the architecture uses independent layers instead of treating one green signal as global truth.

When I review a rule or panel, I explicitly ask: what normal condition could make this look bad, and what bad condition could make this look normal? That question often produces a better second metric than adding another threshold to the first one.

## What would make this monitor lie?

I ask this question explicitly because most monitoring failures are not fabricated numbers; they are numbers interpreted outside their validity. `HserverExternalNotificationDeliveryFailed from incident signal-sink failure counters` can become misleading if its measurement path is stale, labels change, the underlying source resets, the query aggregates away the failing member, the scrape path observes a different network namespace, or the monitored component changes semantics after an upgrade.

Caching creates another class of lies. The Docker storage inventory is deliberately cached because continuous filesystem inspection was too expensive. A cache-backed metric is only trustworthy when cache age and refresh success are visible. Textfile metrics have the same issue if the producer stops updating them. Database-derived metrics can lie by omission if the measurement path account loses access to a system view. Log-derived metrics can go quiet because Alloy or Loki is dropping data rather than because the event stopped happening.

Authentication and synthetic probes can lie through overly permissive expectations. Following redirects blindly may turn an application failure into a successful login-page response. Accepting every status code may hide a broken route. Requiring only 200 may create the opposite error and call a healthy access-control response an outage. The probe has to encode the intended contract.

My response to these risks is not distrust of monitoring. It is meta-monitoring, freshness, independent measured proof and explicit UNKNOWN states when the observation path cannot make a strong claim.

## The hserver case that shaped this part of the design

Notification delivery became part of the incident signal model rather than an assumption. The accepted snapshot records 13 successful external notification events, zero failures and six resolved events. Those are snapshot counters, not an SLA, but they demonstrate that firing and recovery both travel through the delivery path. A quiet Alertmanager is trustworthy only when rule evaluation, targets and notification endpoints are also healthy.

My default is to use that case as a guardrail for `What Prometheus`for:`Really Buys You—and What It Cannot` because it prevents the discussion from becoming a generic monitoring tutorial. The interesting question is not whether another platform supports the same metric. It is what decision the signal enabled on this constrained the accepted runtime host, what cost it imposed, and what measured proof proved that the change improved rather than merely rearranged the system.

This further keeps causality honest. A before/after measurement is measured proof for this configuration at that time. It is not a universal benchmark for cAdvisor, Prometheus, Docker, OpenBao or any database engine. When the article makes a recommendation, the recommendation is about the engineering method—measure, isolate cost, preserve the useful signal, verify the new incident shapes—not about assuming another machine will reproduce the same number.

## Turning the observation into an incident signal without creating noise

Not every article in this series ends with a page. Some of the best signals are diagnostic. When I do incident signal, I separate **prediction**, **saturation**, and **symptom**. Prediction covers conditions such as disk capacity or certificate expiry where action before failure is possible. Saturation covers sustained pressure or exhausted pools. Symptoms cover conditions such as a failed public probe, no healthy SIP worker, or unsuccessful restore verification where the service contract is already affected.

The rule duration has to fit the failure. A single scrape miss or short deployment restart should not create an incident. A total public outage should not sit pending for an arbitrary long `for:` window simply because another resource rule uses ten minutes. Warning and critical labels are response contracts: warning means investigate or schedule action before the margin disappears; critical means the operating state is already outside the tolerated envelope or approaching it fast enough to require immediate attention.

I add one more check: ask what other incident signal will fire at the same time. If host loss makes every public service fail, paging separately for Grafana, OTA, authentication, gateway and VoIP adds noise without information. Grouping and inhibition should preserve useful symptoms while making the likely root event obvious. Resolution is part of the lifecycle too. The latest accepted notification measured proof recorded external notification counters in the acceptance artifact: 13 success, 0 failure, 6 resolved; that is a snapshot of delivery behavior, not an SLA claim.

For `What Prometheus`for:`Really Buys You—and What It Cannot`, the incident signal is successful only if its annotation tells me what was observed, over what window, which Grafana view or runbook to open next, and what secondary signal can confirm the hypothesis.

## Acceptance: prove the monitor after changing it

I do not treat a configuration commit as proof that monitoring works. After meaningful observability changes I compare the desired state in Git with runtime acceptance. The current reviewed artifact records 52/52 accepted Prometheus targets UP, 106 incident signal/recording rules loaded, 0 firing and 0 pending incident signals, 27,578 active Prometheus series, against a 27,414-series acceptance baseline, 10/10 public probes UP, 9/9 database probes UP and 35 monitored configuration files with zero drift in the latest runtime sample. Those numbers are useful because they make blind spots and accidental cardinality growth measurable after deployment.

The validation depends on the feature. A scrape change should prove the target is UP and the expected series exists. A relabel change should prove the required Grafana view and incident signal queries still return data. A log-pipeline change should prove cursor continuity and check drop counters. A public probe should be exercised against both healthy and intentionally invalid behavior. A backup control should be followed by checksum and restore measured proof. A notification change should send a synthetic incident signal and verify both firing and resolved delivery.

Where safe, I prefer failure injection to passive confidence. The external dead-man watcher was tested by forcing a synthetic outage: the hosted workflow failed, an incident issue was created, recovery later passed and the issue closed. That sequence proved more than reading the workflow YAML. The same idea scales down to small controls: temporarily make a test target fail, expire a synthetic sample, or use a fixture that triggers the rule without damaging the accepted runtime.

## Tests that make the monitoring logic trustworthy

I separate tests into collection, semantics, rule and end-to-end behavior. Collection tests answer whether the metric or log event appears with the expected labels and units. Semantic tests compare it with the underlying source: `/proc`, Docker, SQL, a service API, a certificate, an actual file timestamp or another authoritative state. Rule tests feed boundary conditions into PromQL or incident signal fixtures so warning, critical, pending and resolved transitions are predictable.

End-to-end testing is stronger. A synthetic failure should make the expected incident signal fire through the real routing path, and recovery should produce the expected resolution. The external watcher already demonstrated this model by creating and then closing an incident around a forced outage. For backup monitoring, an end-to-end test is a restore verification rather than a successful archive command. For authentication-aware probing, it is seeing the expected redirect or authorization status instead of weakening the route to return 200.

For `What Prometheus`for:`Really Buys You—and What It Cannot`, I would also test missing data. Many rules are exercised only with high or low values and never with a vanished series. The correct behavior may be a target-down incident signal, an UNKNOWN state, or a dedicated freshness incident signal. Missing measured proof should not silently inherit the last green value.

## The investigation sequence The system should give me at 2 a.m.

The runbook for this signal is intentionally ordered. First confirm time and freshness. I do not troubleshoot an old sample as though it were current. Second confirm the measurement path or target path. Third compare the value with the nearest independent signal. Fourth look at the dependency layer below it. Fifth use logs or a direct engine query for detail. Only then change the accepted runtime.

For `What Prometheus`for:`Really Buys You—and What It Cannot`, the first direct question is whether `HserverExternalNotificationDeliveryFailed from incident signal-sink failure counters` is updating on schedule. If it is, I compare it with the signal that would be expected to move under the same failure hypothesis. If the two disagree, that disagreement is measured proof: either the original hypothesis is wrong, the metrics have different semantics, or one observation path is broken.

I add one more check: preserve before/after measured proof around changes. If I tune a scrape interval, relabel metrics, disable an expensive measurement path feature or change an incident signal window, I capture the relevant series count, memory state, target state and rule health. That makes rollback rational. Without a before state, optimization can quietly delete the only metric that explained a future incident.

The final runbook step is acceptance, not “container restarted successfully.” The system should give me the query to return the expected data, the Grafana view to render, the rule to evaluate, the synthetic path to behave correctly, and the monitoring stack to remain inside its resource budget.

## Questions My default is to use in design review

Before merging a monitoring change around this topic, The system should give me concise answers to a set of questions. What failure does the signal detect? What is the authoritative source? How stale can it become before interpretation is unsafe? What is the collection cost? Does it add an unbounded label? Can it expose a secret? What normal condition looks similar to failure? What independent signal confirms the problem? What happens if the measurement path itself dies? Does the incident signal have an operator action? How will I prove the change in the accepted runtime without causing a real outage?

Those questions are deliberately tool-agnostic. They work whether the implementation is Prometheus, Loki, a shell measurement path, SQL, Blackbox Exporter or a GitHub-hosted workflow. They also make deletion possible. If a metric no longer supports a Grafana view, incident signal, capacity decision or incident workflow, I can remove it instead of preserving telemetry indefinitely because “we might need it.”

The final review question is whether the control still makes sense on a 7.1 GiB host. A signal that would be cheap in a large observability cluster can be expensive here. `What Prometheus`for:`Really Buys You—and What It Cannot` has to justify not only correctness but its share of the limited the accepted runtime budget.

## Operational limits and thresholds are configuration, not physics

Thresholds in this system are chosen from capacity, consequence and response time. Disk warning/critical bands, certificate windows, incident signal `for:` durations, heartbeat age, memory budgets and SLO burn-rate factors all express policy. I document them as current the accepted runtime choices, not constants of Linux or Prometheus.

That distinction matters during growth. If workload changes, a threshold that once provided useful warning may become permanently noisy. If a measurement path is optimized, an observability-memory budget may be tightened. If a service moves off-host, its failure domain changes and an old incident signal relationship may no longer apply. If public traffic increases, SLO windows may have enough events to use a different statistical model.

For `What Prometheus`for:`Really Buys You—and What It Cannot`, I would review the threshold whenever the component version, workload, resource limit or topology materially changes. I would also inspect the historical distribution before tightening it. A threshold selected only from a desired round number is less defensible than one derived from observed normal behavior plus an explicit safety margin.

Where the the accepted runtime acceptance artifact measured proof does not contain the distribution needed to justify a new threshold, the article leaves **[CURRENT MEASUREMENT NEEDED]**. That is not an incomplete monitoring practice; it is a refusal to pretend policy has empirical support that has not yet been collected.

## What the current accepted system says

The 2026-09-15 acceptance snapshot gives me a concrete reference point while writing this series. It records 52/52 accepted Prometheus targets UP, 106 incident signal/recording rules loaded, 0 firing and 0 pending incident signals, and 15 provisioned Grafana views. Prometheus reported 27,578 active Prometheus series, against a 27,414-series acceptance baseline. Public probing reported 10/10 public probes UP; database probing reported 9/9 database probes UP. The accepted configuration manifest reported 35 monitored configuration files with zero drift in the latest runtime sample.

For storage and retention, Prometheus retention set to about 30 days with a 15 GB size cap; Loki retention set to 168 hours. For hardware measured proof, SMART status healthy in the acceptance artifact, with a 49 C device-temperature sample. For recovery, encrypted DR verification PASS, required payload PASS, internal checksum PASS, off-host pull PASS, and restore verification PASS. For OpenBao, main OpenBao initialized and unsealed with Transit auto-unseal; same-host seal node initialized and unsealed with no host-published ports. These values are intentionally described with a date because they are not permanent properties of the architecture. They are measured proof that the system reached a known state after a particular round of changes.

This distinction is important for `What Prometheus`for:`Really Buys You—and What It Cannot`. Monitoring documentation tends to age badly when it turns an observation into a law. I would rather write “27,578 active series in this acceptance snapshot” than imply that 27,578 is a target, a limit or a recommendation. The same applies to cAdvisor memory, disk temperature, Grafana view count and incident signal-rule count. The system design should survive changing numbers because the interpretation rules remain explicit.

## What I would change at larger scale

The small-server version optimizes for bounded cost and direct inspectability. In a multi-host design I would preserve the semantic model but move some responsibilities. Metrics storage could move off the application host. Long-term retention could use a system designed for remote or object-backed storage. Loki could live on a dedicated node. Exporter and measurement path work could be distributed closer to the workloads while query and incident signal evaluation stay centralized. High-availability Alertmanager and independent monitoring storage would reduce shared failure domains.

I would not, however, replace `HserverExternalNotificationDeliveryFailed from incident signal-sink failure counters` with a generic “enterprise monitoring” product and call the problem solved. The key question remains what the observation proves. If the signal is about Linux pressure, the kernel semantics remain. If it is about database locks, the engine semantics remain. If it is about SIP versus RTP, the protocol boundaries remain. If it is about dead-man monitoring, the observer still has to live outside the failure domain.

Scale primarily changes collection topology, retention, redundancy and automation. It does not remove the need to define failure semantics. In fact, larger systems punish ambiguous metrics more severely because a noisy or high-cardinality mistake multiplies across more hosts and more operators.

## Deep-dive notes: separating mechanism from policy

A recurring source of monitoring bugs is mixing mechanism with policy. The mechanism answers how the observation is produced: kernel counter, cgroup metric, SQL query, log parser, HTTP probe, application counter or external workflow. Policy answers what the organization does when that observation changes. `HserverExternalNotificationDeliveryFailed from incident signal-sink failure counters` is mechanism. The threshold, window, severity, grouping and escalation path are policy.

Keeping those separate makes the system easier to evolve. I can improve collection without changing the paging contract, or change a warning threshold after capacity review without rewriting the measurement path. This further makes testing clearer. Collector tests validate units, labels, freshness and failure behavior. Rule tests validate expressions and state transitions. End-to-end tests validate that an actual synthetic condition reaches the operator and resolves correctly.

The same separation applies to desired state and measured proof. Git defines reviewed configuration, but Git cannot prove the running system loaded it. Runtime acceptance proves what the accepted runtime observed, but runtime state is not a reproducible configuration source. The current reviewed manifest model bridges the two by hashing approved monitored configuration and measuring drift without exporting secret values.

For this topic, I would treat a future scale-out as another policy change rather than an excuse to discard the semantic model. A managed metrics backend, Kubernetes, multiple nodes or cloud load balancers change topology. They do not change what memory pressure means, what a deadlock means, what a stale heartbeat means, or why a probe outside the failure domain is stronger measured proof of host death than a local Grafana view.

## What I keep from this decision

What survived from this work is not a particular threshold. It is the interpretation contract behind **What Prometheus `for:` Really Buys You—and What It Cannot** and the measured proof required before I trust it. The control is useful because I know its acquisition cost, expected cadence, incident shapes, corroborating signals and response path. That is the standard I now use before adding another metric or incident signal to hserver.

The server is still an old Mac mini. That constraint has not stopped the monitoring system from becoming serious. It has forced every layer to be explicit about what it is worth. For me that is the more interesting engineering result: the accepted runtime-grade observability is less about how many products are installed and more about whether the measured proof is sufficient, current, independent where necessary, and cheap enough that the observer does not become the outage.
