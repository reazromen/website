---
title: I Deliberately Broke the Probe to Test the Monitoring System
url: /posts/prod-monitoring-i-deliberately-broke-the-probe-to-test-the-monitoring-system.html
date: '2024-02-17'
read_time: 35
excerpt: A production-engineering deep dive into i deliberately broke the probe to
  test the monitoring system, grounded in the 2014 Mac mini hserver observability
  stack and its accepted runtime evidence.
topic: observability-monitoring
tags:
- blackbox-exporter
- synthetic-monitoring
- edge
- dead-man
draft: false
featured: false
language: en
eyebrow: 'Production Monitoring: Network, Edge & Synthetic Monitoring · deep-dive'
outputs:
- url: /posts/prod-monitoring-i-deliberately-broke-the-probe-to-test-the-monitoring-system.html
  template: cms/templates/posts/posts--prod-monitoring-i-deliberately-broke-the-probe-to-test-the-monitoring-system.tpl
  source: cms/templates/posts/posts--prod-monitoring-i-deliberately-broke-the-probe-to-test-the-monitoring-system.json
---

On a large monitoring cluster it is easy to collect first and decide what matters later. On this 2014 Mac mini I had to reverse that order. **I Deliberately Broke the Probe to Test the Monitoring System** came out of that constraint.

The host is 2014 Apple Mac mini running Linux, with roughly 7.1 GiB usable RAM from an 8 GB-class machine. Applications, databases, networking, authentication, OTA, OpenBao, VoIP and the observability stack share the same limited CPU, memory and storage. That makes monitoring part of the workload rather than something outside it. The central failure I am trying to avoid is not merely “a metric went high.” Operationally I want enough measured proof to tell whether a user-facing service is degrading, which dependency owns the problem, whether the signal is current, and whether the monitoring path itself is still trustworthy.

For this specific problem the primary observation point is `external GitHub-hosted synthetic watcher, five-minute schedule, incident issue lifecycle and forced outage test`. The short the live host note that preceded this article captured the core finding: Direct service health closes the silent-period gap and provides measured proof that the receiver is available even when no incidents are firing. This long-form version goes further: what that signal really proves, which nearby signals can falsify my first hypothesis, how I implement and warning condition on it, what it costs on this host, and how I would redesign the same control at larger scale.

The numbers in this article are not generic benchmarks. When I mention 27,578 active Prometheus series, against a 27,414-series acceptance baseline, cAdvisor measured at 428.2 MiB before the low-RAM work and 27.87 MiB in one post-change sample, with an observed steady range around 20–28 MiB, or any other concrete value, I mean the 2026-09-15 acceptance snapshot unless I explicitly say otherwise. If a current value is not present in the accepted measured proof, I leave `[CURRENT MEASUREMENT NEEDED]` rather than inventing a number.

## The engineering question specific to this article

The short version of the problem is not “how do I graph I Deliberately Broke the Probe to Test the Monitoring System?” It is: **Delivery counters only change when an warning condition is sent, so a quiet system could leave a dead notification service unnoticed for hours.** That failure can be confused with neighboring conditions, which is why the primary observation is `external GitHub-hosted synthetic watcher, five-minute schedule, incident issue lifecycle and forced outage test` rather than a generic process-up flag.

The latest accepted the live host conclusion is specific: Direct service health closes the silent-period gap and provides measured proof that the receiver is available even when no incidents are firing. I turn that conclusion into an operational practice—synthetic monitoring of the paging path—and into a preventive control: Scrape or probe the notification service continuously and still retain real delivery counters because health does not prove message acceptance end to end. Those three layers are intentionally separate. The finding explains what the measured proof taught me. The practice describes how I diagnose it. The prevention rule describes how I keep the same ambiguity from returning after the next deployment.

There is also a data-model question. The observation has to retain the dimension that matters without encoding unbounded identity. If the question is per node, the node label matters. If it is fleet capacity, an aggregate may be more useful. If it is an event such as a deadlock or OOM kill, a counter over a time window carries different meaning from a current-state gauge. If it is a cached inventory value, age and refresh success are part of the value's contract.

Finally I decide how close this signal is to user impact. Some topics in this series are direct symptoms; others are explanatory measured proof. `I Deliberately Broke the Probe to Test the Monitoring System` belongs at the point where it can reduce investigation time without claiming more certainty than the underlying source provides. That classification determines whether it becomes a page, a warning, a visualization drill-down or simply retained forensic context.

## Competing hypotheses before I touch the live host

I try to write down multiple explanations before making a change. For **I Deliberately Broke the Probe to Test the Monitoring System**, the candidate set I would test includes: **DNS or TLS fails before the request reaches the app**; **authentication returns an expected non-200 status**; **the external observer itself is unavailable**; **the local monitor dies with the host and produces no local warning condition**; and **the application is healthy internally but the public path is broken**. The point is not that all five are equally likely. It is to stop the first plausible graph from becoming the conclusion.

The primary observation `external GitHub-hosted synthetic watcher, five-minute schedule, incident issue lifecycle and forced outage test` should eliminate some of those hypotheses, not all of them. I choose the next query or log source by information gain: which check can separate the most remaining explanations at the lowest operational cost? A fresh internal probe versus a failed public probe immediately moves suspicion toward the edge. High memory utilization with low pressure and stable swap activity moves me away from a memory-emergency diagnosis. A stale FreeSWITCH heartbeat with a running container moves the problem from process liveness into worker readiness.

This habit is especially useful on a single host because many symptoms are correlated. Storage pressure can slow databases, logs and containers simultaneously. Host memory pressure can make the monitoring stack itself late. A router or Internet failure can make every public service look broken while the applications are healthy. Explicit competing hypotheses keep correlation from being mistaken for independent failures.

## The observation contract I expect this signal to keep

For `external GitHub-hosted synthetic watcher, five-minute schedule, incident issue lifecycle and forced outage test` Operationally I want a written contract even if it is only a few lines in a runbook. The contract says who produces the data, what unit it uses, which labels are bounded and meaningful, how often it should update, what reset behavior exists, and what missing data means. Without those details an old metric can survive long after its interpretation has changed.

The contract also names the strongest claim the signal supports. Direct service health closes the silent-period gap and provides measured proof that the receiver is available even when no incidents are firing. That sentence is intentionally narrower than “the service is healthy.” It leaves room for independent measured proof and tells future maintainers not to reuse the metric for a stronger conclusion without re-validating it.

Freshness belongs in the contract whenever the producer is not scraped directly. Cache-backed Docker inventory, textfile metrics, heartbeat state and backup timestamps can all remain syntactically valid after the producer stops. I therefore prefer either an explicit age metric or a timestamp from which age can be derived. For direct Prometheus targets, `up` is part of the collection contract but still not the service-health contract.

Finally, the contract includes data sensitivity. Labels and log content must not turn operational telemetry into a secret-disclosure channel. If the observation cannot be collected safely with bounded identity and least privilege, I redesign the telemetry collector rather than assuming the monitoring network is trusted.

## Start with the failure, not the exporter

The incident shapel for this article is: **Delivery counters only change when an warning condition is sent, so a quiet system could leave a dead notification service unnoticed for hours.** That wording matters because it describes the operational ambiguity I need to remove. A raw metric has no value until I know what claim I am trying to make from it.

The obvious monitoring mistake is to collapse several layers into one binary state. A process can exist while the application is unusable. A telemetry collector can return a number that is already stale. A public service can correctly return a redirect or authorization error and still be healthy. A database can accept a TCP connection while lock contention makes useful queries stall. A host can report high memory utilization while reclaimable page cache means applications are not under pressure. The same general problem appears repeatedly: one layer's “up” is only measured proof about that layer.

I therefore map each failure to at least three questions. First, what is the earliest useful signal that something is changing? Second, what is the strongest user-visible symptom I can observe independently? Third, what measured proof tells me the monitoring path is alive enough to trust the first two answers? For `I Deliberately Broke the Probe to Test the Monitoring System`, `external GitHub-hosted synthetic watcher, five-minute schedule, incident issue lifecycle and forced outage test` belongs in that chain, but it is never allowed to stand alone if the failure can be confirmed from another layer.

This is also how I decide whether an warning condition belongs on a metric. A signal may be excellent for diagnosis and terrible for paging. Context switches, container block-I/O bytes or database size trends can be valuable measured proof without being reasons to interrupt an operator immediately. Conversely, a public probe failure or no-healthy-worker condition may deserve much more direct attention because it is already close to user impact.

## Where this sits in the hserver observability architecture

Synthetic monitoring exists because a healthy process is not the same as a usable service. Internal probes test the service from inside the infrastructure; public probes exercise more of the dependency chain—DNS, routing, TLS, reverse proxy or tunnel, authentication boundary and application. The expected HTTP result is route-specific. A protected service returning 302 to an authentication portal, or 401/403 to an unauthenticated machine probe, may be behaving exactly correctly. Hard-coding “200 equals up” confuses policy with availability.

The largest blind spot is shared failure domain. Prometheus, Alertmanager and local notifications can all be correct and still vanish together when the Mac mini loses power, Docker or the router disappears, or the host becomes unreachable. The independent watcher uses GitHub-hosted runners approximately every five minutes and holds no hserver credential. It probes public measured proof, opens or updates an external incident issue when failure persists, and records recovery when probes return. A forced synthetic outage exercised the failure path and automatic closure. That test mattered because a dead-man mechanism that has never experienced an artificial death is still partly hypothetical.

For this article, the component boundary matters as much as the metric. The latest accepted accepted observability stack includes Prometheus, Grafana, Loki, Alloy, Alertmanager, Blackbox Exporter, Node Exporter, cAdvisor, SMART collection, Docker inventory and deep host/database telemetry collectors, plus application-native and external synthetic signals. The latest acceptance artifact records 52/52 accepted Prometheus targets UP, 106 warning condition/recording rules loaded, 15 provisioned visualizations and 10/10 public probes UP.

I try not to interpret those counts as a maturity score. More targets and more rules can make a system worse if they add noise or cost without reducing uncertainty. The useful part is that the inventory is explicit and accepted. When I add a control for `I Deliberately Broke the Probe to Test the Monitoring System`, I can ask which existing layer already sees part of the problem, whether a new metric is necessary, and how the new observation will be validated after deployment.

## The decision this monitor should let me make

If this telemetry cannot change a decision, it should not automatically consume always-on budget. For **I Deliberately Broke the Probe to Test the Monitoring System**, the decisions fall into four categories. I may need to intervene immediately because a service contract is already broken. I may need to schedule capacity work because margin is shrinking. I may need to isolate a dependency during incident diagnosis. Or I may decide that the condition is normal and explicitly avoid action.

That last outcome is important. Monitoring is partly a system for proving when *not* to react. Page cache, historical swap, a 302 authentication redirect, a controlled restart, or a busy response from a SIP endpoint can look abnormal without representing infrastructure failure. The metric model should carry enough context to distinguish those cases.

A second part of the design is want the monitor to make rollback decisions safer. If a deployment changes `external GitHub-hosted synthetic watcher, five-minute schedule, incident issue lifecycle and forced outage test`, I should be able to compare the new state with the accepted baseline and decide whether the change is intended. That is why provenance `hserver-external-watch + MONITORING-COVERAGE.md` stays attached to the topic. A the live host metric without a known configuration history is harder to use as change measured proof.

At scale this decision-centric approach becomes even more important. Hundreds of hosts can produce unlimited telemetry; operator time remains finite. The series therefore treats observability as a decision system rather than a storage system.

## Why this particular collection path won

There are usually several ways to obtain the state behind **I Deliberately Broke the Probe to Test the Monitoring System**: scrape an existing exporter, query an application API, run a SQL statement, parse logs, inspect the Docker API, read a Linux kernel interface, or publish a small custom metric through the textfile path. I choose among them by authority, cost, security and failure independence.

The closest source is not always the best source. A Docker container metric can tell me process resource use but not whether PostgreSQL sessions are waiting. A log parser can count authentication failures but is a weaker source for current service readiness than a direct state query. A raw TCP probe is cheap but deliberately shallow. A deep query may be authoritative but require credentials or create load. The deployed implementation behind `external GitHub-hosted synthetic watcher, five-minute schedule, incident issue lifecycle and forced outage test` is valuable because it sits at the layer that owns the state I need to interpret.

A second part of the design is prefer collection paths with visible failure. A custom script that exits silently and leaves yesterday's textfile metric behind is worse than a telemetry collector that exports its own success and age. A cache should expose refresh result and age. A database telemetry collector should expose whether its query succeeded. A log pipeline should expose drops. The observer has to be observable.

The chosen path therefore reflects more than convenience. It is part of the incident shapel: which component can lie, which credential can expire, which namespace the query sees, and what remains observable when another layer breaks.

## How I reason about a threshold for this topic

I try not to begin with a round number. I begin with the consequence I am trying to avoid and how much reaction time exists. Capacity thresholds such as disk or connection utilization should leave enough margin to investigate before exhaustion. Pressure thresholds should remain high long enough to distinguish real contention from transient scheduling noise. Certificate thresholds are measured in days because the repair process is administrative, not millisecond-sensitive. External availability failures can justify much faster response.

For **I Deliberately Broke the Probe to Test the Monitoring System**, the next threshold review should use the historical distribution plus the component's configured limit and the time needed to act. If that distribution is not captured in the dated acceptance measured proof artifact, the honest value is **[CURRENT MEASUREMENT NEEDED]**. I try not to derive a the live host page from an attractive number in a blog post.

A second part of the design is test both sides of the boundary. A warning threshold should actually enter pending/firing state when a fixture crosses it, and it should resolve when the signal recovers. A critical threshold should not be inhibited by the warning in a way that loses the more serious state. If the signal is a counter, the window should contain enough events to be meaningful. If it is a gauge, the `for` duration and freshness semantics matter more than counter reset behavior.

Thresholds are therefore versioned policy. When topology, workload, resource limits or telemetry collector semantics change, I expect the threshold to be reviewed alongside the code.

## Draw the data path before trusting the panel

For this part of the system I keep a simple failure-domain drawing in mind:

```
external client -> DNS -> Internet path -> TLS -> tunnel/proxy -> auth boundary -> app
GitHub runner ------------------------------------------------------^
```

The diagram matters because every arrow can fail independently. Collection can succeed while storage or rule evaluation fails. An internal probe can succeed while the public path fails. A public probe running on hserver still shares the host failure domain even if it reaches a public URL. A database exporter can be healthy while its engine query permission is broken. A log telemetry collector can be alive while the write path drops entries.

For `I Deliberately Broke the Probe to Test the Monitoring System`, I identify the authoritative source on the left, every transformation before the visualization or warning condition, and which component owns persistence. Then I decide where failure should become visible. If a transformation silently converts “unknown” into zero, the diagram has an observability gap. If both the service and its observer depend on the same process or credential, the diagram has a shared failure domain.

This exercise is cheap and often catches problems before PromQL is written. The design also explains why I retained both internal and public probes, why the external watcher lives on hosted runners, and why backup measured proof has multiple stages rather than one success bit.

## The mechanism underneath the graph

Blackbox-style monitoring turns the network path into a measurement. HTTP probing can expose DNS, connect, TLS and processing phases; TCP probing proves reachability at a lower layer; DNS and ICMP answer still different questions. The expected response must include security semantics. External dead-man monitoring is stronger for host-loss detection because the probe scheduler, network origin and incident state live outside hserver. It deliberately avoids credentials from the system it is supposed to declare dead.

That mechanism matters for `I Deliberately Broke the Probe to Test the Monitoring System` because two visually similar graphs can have very different semantics. A cumulative counter should normally be turned into a rate or increase over a time window. A gauge can be read directly but still needs freshness. A ratio is meaningless if its denominator is missing, zero or describes a different capacity boundary. A status value needs an explicit state model. A log-derived count depends on the reliability of ingestion and parsing. A synthetic probe depends on where the probe originates and which route it exercises.

I try to preserve units all the way from collection to the panel and warning condition. Seconds should not silently become milliseconds. Bytes should not be compared with decimal “GB” labels without deciding which convention is in use. Percentages should identify their denominator. Ages should be derived from timestamps in a timezone-independent way. These details look small in configuration review and become large during incidents, when the operator is making decisions from the graph under time pressure.

The other subtlety is reset behavior. Counters restart with processes. Container identities change on recreation. database cumulative statistics can reset after engine restart. A visualization that uses raw cumulative values can therefore interpret restart as recovery or huge negative activity. Query functions and labels need to match the lifecycle of the component being measured.

## Implementation: make the observation cheap and reproducible

The deployed implementation is deliberately smaller than the explanation. Operationally I want the collection path to be boring: deterministic configuration in Git, bounded work on the host, a clear scrape or evaluation cadence, and a result that can be checked after deployment. Repository measured proof associated with this topic is `hserver-external-watch + MONITORING-COVERAGE.md`.

A representative query or configuration fragment is:

```
# External watcher, independent of hserver
on:
  schedule:
    - cron: '*/5 * * * *'
# Probe public service measured proof only; do not require an hserver credential.
# On failure: open/update incident issue. On recovery: record recovery and close.
```

The fragment is not meant to be copied blindly into another system. Labels, device names, mount points, job names and custom metric families are deployment-specific. The important point is the shape of the control. Ratios need denominators. Counters need rates or increases over windows. Slow-changing inventory should not be polled at CPU-metric cadence. Authentication-aware probes need status semantics. Freshness-sensitive telemetry collectors need age checks. Expensive queries should be recorded or sampled at a cadence that matches the decision they support.

A second part of the design is keep configuration ownership separate from runtime measured proof. Prometheus rules, scrape configuration, visualizations and telemetry collector code live in the reviewed source tree. Runtime acceptance data records what the live host actually observed. Secret values stay out of both metrics and public documentation. This lets me reproduce the monitoring design without turning the monitoring repository into a credential store.

## Walk the failure from symptom back to cause

A stronger way to review this monitor is to imagine a failure and force myself to predict what each layer would show. I try not to claim the following sequence happened unless it is part of the recorded measured proof; it is a design exercise for the control.

Start with the user-visible symptom related to **I Deliberately Broke the Probe to Test the Monitoring System**. The top-level probe or service metric changes first or eventually. I then ask whether the host is still reachable, whether the target is still being scraped, and whether `external GitHub-hosted synthetic watcher, five-minute schedule, incident issue lifecycle and forced outage test` is fresh. If the target is down, an old threshold value is no longer the primary measured proof; target failure becomes the first branch. If the target is up, I compare the signal with its nearest independent corroborator.

From there I trace downward. A host-pressure signal leads to per-container attribution and kernel logs. A container symptom leads to host resource state and application health. A database symptom leads from reachability to connection, wait, lock and engine state. A public probe failure is compared with the internal probe, DNS/TLS phases and edge logs. A VoIP symptom is separated into signaling, worker and media measured proof. A backup symptom is followed through job, artifact, checksum and restore state.

What I want from it is not to prove that every incident follows one tree. It is to make sure each metric has a place in an investigation. If a signal cannot tell me which branch to take next, I question whether it belongs in the always-on monitoring budget.

## How I debug this signal when it looks wrong

I work with a layered debugging order because the fastest way to waste time is to treat the first abnormal graph as the root cause. For **I Deliberately Broke the Probe to Test the Monitoring System**, I start by proving that the sample is current. I check target or telemetry collector health, the timestamp/freshness path, and whether a recent deployment changed labels or collection cadence. If the value can be generated from a custom telemetry collector, I compare the exported value with the underlying operating-system, Docker, database or application state.

Next I look for a neighboring signal that should move if my hypothesis is correct. Memory pressure should have some relationship to MemAvailable, swap activity, OOM measured proof or workload latency. Storage latency should have some relationship to I/O pressure or application waits. Container I/O should reconcile with host disk activity. A database saturation hypothesis should be visible in connection, wait or lock state. A public availability failure should be compared with an internal probe so I can separate application failure from DNS, TLS, tunnel or edge failure.

Only after that do I broaden into logs. Logs are best when the failure domain is already smaller: kernel OOM records, Docker daemon warnings, authentication failures, Alloy/Loki pipeline errors, database messages or VoIP-specific events. This keeps me from searching an unbounded log corpus for an event I have not yet defined.

The last step is to check the monitoring system itself. A quiet visualization can be caused by a missing target. A stable line can be a stale sample. A zero-warning condition page can coexist with rule-evaluation failures. Operationally I want measured proof that the observer is alive before I trust the observation.

## The false-positive and false-negative traps

Every monitoring decision has at least two ways to be wrong. A false positive declares a failure when the system is operating within its intended semantics. A false negative keeps the visualization green while the service contract is broken. `I Deliberately Broke the Probe to Test the Monitoring System` is useful only if I can describe both.

A common false positive is reading a state without duration or context. Non-zero swap can be historical. High CPU can be productive work. A protected HTTP endpoint can return 302, 401 or 403 because authentication is functioning. A brief container restart can be a deployment. A temporarily high database connection count can be harmless if capacity and latency remain healthy. These cases need windows, denominators or state semantics before they become incidents.

The false negative is usually more dangerous. A target can scrape successfully while its downstream dependency is broken. A stale custom metric can remain below threshold after its telemetry collector died. A database socket can accept connections while waits or locks stop useful work. A FreeSWITCH process can run while the worker heartbeat is stale. A backup archive can exist while restore verification has not succeeded. Those failures are why the architecture uses independent layers instead of treating one green signal as global truth.

When I review a rule or panel, I explicitly ask: what normal condition could make this look bad, and what bad condition could make this look normal? That question often produces a better second metric than adding another threshold to the first one.

## What would make this monitor lie?

I ask this question explicitly because most monitoring failures are not fabricated numbers; they are numbers interpreted outside their validity. `external GitHub-hosted synthetic watcher, five-minute schedule, incident issue lifecycle and forced outage test` can become misleading if its telemetry collector is stale, labels change, the underlying source resets, the query aggregates away the failing member, the scrape path observes a different network namespace, or the monitored component changes semantics after an upgrade.

Caching creates another class of lies. The Docker storage inventory is deliberately cached because continuous filesystem inspection was too expensive. A cache-backed metric is only trustworthy when cache age and refresh success are visible. Textfile metrics have the same issue if the producer stops updating them. Database-derived metrics can lie by omission if the telemetry collector account loses access to a system view. Log-derived metrics can go quiet because Alloy or Loki is dropping data rather than because the event stopped happening.

Authentication and synthetic probes can lie through overly permissive expectations. Following redirects blindly may turn an application failure into a successful login-page response. Accepting every status code may hide a broken route. Requiring only 200 may create the opposite error and call a healthy access-control response an outage. The probe has to encode the intended contract.

My response to these risks is not distrust of monitoring. It is meta-monitoring, freshness, independent measured proof and explicit UNKNOWN states when the observation path cannot make a strong claim.

## The hserver case that shaped this part of the design

The independent watcher was tested as a system rather than a YAML file. A forced synthetic outage made the external workflow fail, incident state was created outside hserver, and recovery closed the incident. That proves scheduler, network origin, probe logic and incident lifecycle together. The design also proves why no hserver credential should be required for the dead-man path: the detector must survive loss of the credential-serving infrastructure it monitors.

I work with that case as a guardrail for `I Deliberately Broke the Probe to Test the Monitoring System` because it prevents the discussion from becoming a generic monitoring tutorial. The interesting question is not whether another platform supports the same metric. It is what decision the signal enabled on this constrained the live host host, what cost it imposed, and what measured proof proved that the change improved rather than merely rearranged the system.

The design also keeps causality honest. A before/after measurement is measured proof for this configuration at that time. It is not a universal benchmark for cAdvisor, Prometheus, Docker, OpenBao or any database engine. When the article makes a recommendation, the recommendation is about the engineering method—measure, isolate cost, preserve the useful signal, verify the new incident shapes—not about assuming another machine will reproduce the same number.

## Turning the observation into an warning condition without creating noise

Not every article in this series ends with a page. Some of the best signals are diagnostic. When I do warning condition, I separate **prediction**, **saturation**, and **symptom**. Prediction covers conditions such as disk capacity or certificate expiry where action before failure is possible. Saturation covers sustained pressure or exhausted pools. Symptoms cover conditions such as a failed public probe, no healthy SIP worker, or unsuccessful restore verification where the service contract is already affected.

The rule duration has to fit the failure. A single scrape miss or short deployment restart should not create an incident. A total public outage should not sit pending for an arbitrary long `for:` window simply because another resource rule uses ten minutes. Warning and critical labels are response contracts: warning means investigate or schedule action before the margin disappears; critical means the operating state is already outside the tolerated envelope or approaching it fast enough to require immediate attention.

A second part of the design is ask what other warning condition will fire at the same time. If host loss makes every public service fail, paging separately for Grafana, OTA, authentication, gateway and VoIP adds noise without information. Grouping and inhibition should preserve useful symptoms while making the likely root event obvious. Resolution is part of the lifecycle too. The latest accepted notification measured proof recorded external notification counters in the acceptance artifact: 13 success, 0 failure, 6 resolved; that is a snapshot of delivery behavior, not an SLA claim.

For `I Deliberately Broke the Probe to Test the Monitoring System`, the warning condition is successful only if its annotation tells me what was observed, over what window, which visualization or runbook to open next, and what secondary signal can confirm the hypothesis.

## Acceptance: prove the monitor after changing it

I try not to treat a configuration commit as proof that monitoring works. After meaningful observability changes I compare the desired state in Git with runtime acceptance. The latest accepted artifact records 52/52 accepted Prometheus targets UP, 106 warning condition/recording rules loaded, 0 firing and 0 pending warning conditions, 27,578 active Prometheus series, against a 27,414-series acceptance baseline, 10/10 public probes UP, 9/9 database probes UP and 35 monitored configuration files with zero drift in the latest runtime sample. Those numbers are useful because they make blind spots and accidental cardinality growth measurable after deployment.

The validation depends on the feature. A scrape change should prove the target is UP and the expected series exists. A relabel change should prove the required visualization and warning condition queries still return data. A log-pipeline change should prove cursor continuity and check drop counters. A public probe should be exercised against both healthy and intentionally invalid behavior. A backup control should be followed by checksum and restore measured proof. A notification change should send a synthetic warning condition and verify both firing and resolved delivery.

Where safe, I prefer failure injection to passive confidence. The external dead-man watcher was tested by forcing a synthetic outage: the hosted workflow failed, an incident issue was created, recovery later passed and the issue closed. That sequence proved more than reading the workflow YAML. The same idea scales down to small controls: temporarily make a test target fail, expire a synthetic sample, or use a fixture that triggers the rule without damaging the live host.

## Tests that make the monitoring logic trustworthy

I separate tests into collection, semantics, rule and end-to-end behavior. Collection tests answer whether the metric or log event appears with the expected labels and units. Semantic tests compare it with the underlying source: `/proc`, Docker, SQL, a service API, a certificate, an actual file timestamp or another authoritative state. Rule tests feed boundary conditions into PromQL or warning condition fixtures so warning, critical, pending and resolved transitions are predictable.

End-to-end testing is stronger. A synthetic failure should make the expected warning condition fire through the real routing path, and recovery should produce the expected resolution. The external watcher already demonstrated this model by creating and then closing an incident around a forced outage. For backup monitoring, an end-to-end test is a restore verification rather than a successful archive command. For authentication-aware probing, it is seeing the expected redirect or authorization status instead of weakening the route to return 200.

For `I Deliberately Broke the Probe to Test the Monitoring System`, I would also test missing data. Many rules are exercised only with high or low values and never with a vanished series. The correct behavior may be a target-down warning condition, an UNKNOWN state, or a dedicated freshness warning condition. Missing measured proof should not silently inherit the last green value.

## Telemetry can leak data if I model it as harmless

Metrics and logs are the live host data. Labels can reveal hostnames, internal services, user identities or network details. Logs can contain source addresses, request paths and authentication context. A convenient custom telemetry collector can accidentally print a credential. A visualization can expose an administrative topology to anyone who can reach it.

My rule is to collect state, not secrets. OpenBao monitoring exposes initialized/sealed state, health and certificate information, not secret values or tokens. Configuration drift uses hashes of approved files rather than exporting `.env` contents. Authentication monitoring keeps high-cardinality identities and IPs in bounded log content rather than promoting them to Prometheus labels. Secret files remain outside Git and are not copied into article source.

The same principle affects probe design. The external dead-man watcher intentionally needs no hserver credential. A health check should not require broad the live host authority merely to answer whether a service is alive. Where authenticated deep checks are necessary, the identity should have the minimum query capability and its lifecycle should be monitored separately.

For `I Deliberately Broke the Probe to Test the Monitoring System`, I review telemetry exposure together with collection cost. Observability is not exempt from least privilege simply because the output is “only monitoring.”

## What I would change at larger scale

The small-server version optimizes for bounded cost and direct inspectability. At fleet scale I would preserve the semantic model but move some responsibilities. Metrics storage could move off the application host. Long-term retention could use a system designed for remote or object-backed storage. Loki could live on a dedicated node. Exporter and telemetry collector work could be distributed closer to the workloads while query and warning condition evaluation stay centralized. High-availability Alertmanager and independent monitoring storage would reduce shared failure domains.

I would not, however, replace `external GitHub-hosted synthetic watcher, five-minute schedule, incident issue lifecycle and forced outage test` with a generic “enterprise monitoring” product and call the problem solved. The key question remains what the observation proves. If the signal is about Linux pressure, the kernel semantics remain. If it is about database locks, the engine semantics remain. If it is about SIP versus RTP, the protocol boundaries remain. If it is about dead-man monitoring, the observer still has to live outside the failure domain.

Scale primarily changes collection topology, retention, redundancy and automation. It does not remove the need to define failure semantics. In fact, larger systems punish ambiguous metrics more severely because a noisy or high-cardinality mistake multiplies across more hosts and more operators.

## What the current accepted system says

The 2026-09-15 acceptance snapshot gives me a concrete reference point while writing this series. It records 52/52 accepted Prometheus targets UP, 106 warning condition/recording rules loaded, 0 firing and 0 pending warning conditions, and 15 provisioned visualizations. Prometheus reported 27,578 active Prometheus series, against a 27,414-series acceptance baseline. Public probing reported 10/10 public probes UP; database probing reported 9/9 database probes UP. The accepted configuration manifest reported 35 monitored configuration files with zero drift in the latest runtime sample.

For storage and retention, Prometheus retention set to about 30 days with a 15 GB size cap; Loki retention set to 168 hours. For hardware measured proof, SMART status healthy in the acceptance artifact, with a 49 C device-temperature sample. For recovery, encrypted DR verification PASS, required payload PASS, internal checksum PASS, off-host pull PASS, and restore verification PASS. For OpenBao, main OpenBao initialized and unsealed with Transit auto-unseal; same-host seal node initialized and unsealed with no host-published ports. These values are intentionally described with a date because they are not permanent properties of the architecture. They are measured proof that the system reached a known state after a particular round of changes.

This distinction is important for `I Deliberately Broke the Probe to Test the Monitoring System`. Monitoring documentation tends to age badly when it turns an observation into a law. I would rather write “27,578 active series in this acceptance snapshot” than imply that 27,578 is a target, a limit or a recommendation. The same applies to cAdvisor memory, disk temperature, visualization count and warning condition-rule count. This the live host design should survive changing numbers because the interpretation rules remain explicit.

## Deep-dive notes: separating mechanism from policy

A recurring source of monitoring bugs is mixing mechanism with policy. The mechanism answers how the observation is produced: kernel counter, cgroup metric, SQL query, log parser, HTTP probe, application counter or external workflow. Policy answers what the organization does when that observation changes. `external GitHub-hosted synthetic watcher, five-minute schedule, incident issue lifecycle and forced outage test` is mechanism. The threshold, window, severity, grouping and escalation path are policy.

Keeping those separate makes the system easier to evolve. I can improve collection without changing the paging contract, or change a warning threshold after capacity review without rewriting the telemetry collector. The design also makes testing clearer. Collector tests validate units, labels, freshness and failure behavior. Rule tests validate expressions and state transitions. End-to-end tests validate that an actual synthetic condition reaches the operator and resolves correctly.

The same separation applies to desired state and measured proof. Git defines reviewed configuration, but Git cannot prove the running system loaded it. Runtime acceptance proves what the live host observed, but runtime state is not a reproducible configuration source. The latest accepted manifest model bridges the two by hashing approved monitored configuration and measuring drift without exporting secret values.

For this topic, I would treat a future scale-out as another policy change rather than an excuse to discard the semantic model. A managed metrics backend, Kubernetes, multiple nodes or cloud load balancers change topology. They do not change what memory pressure means, what a deadlock means, what a stale heartbeat means, or why a probe outside the failure domain is stronger measured proof of host death than a local visualization.

## What I keep from this decision

I keep **I Deliberately Broke the Probe to Test the Monitoring System** in this series because it shows the difference between collecting telemetry and engineering measured proof. The control is useful because I know its acquisition cost, expected cadence, incident shapes, corroborating signals and response path. That is the standard I now use before adding another metric or warning condition to hserver.

The server is still an old Mac mini. That constraint has not stopped the monitoring system from becoming serious. It has forced every layer to be explicit about what it is worth. For me that is the more interesting engineering result: the live host-grade observability is less about how many products are installed and more about whether the measured proof is sufficient, current, independent where necessary, and cheap enough that the observer does not become the outage.
