---
title: A Healthy FreeSWITCH Process Can Still Mean Broken Calls
url: /posts/prod-monitoring-a-healthy-freeswitch-process-can-still-mean-broken-calls.html
date: '2026-09-15'
read_time: 32
excerpt: A production-engineering deep dive into a healthy freeswitch process can
  still mean broken calls, grounded in the 2014 Mac mini hserver observability stack
  and its accepted runtime evidence.
topic: observability-monitoring
tags:
- voip
- opensips
- drachtio
- rtpengine
draft: false
featured: false
language: en
eyebrow: 'Production Monitoring: VoIP Observability · advanced'
outputs:
- url: /posts/prod-monitoring-a-healthy-freeswitch-process-can-still-mean-broken-calls.html
  template: cms/templates/posts/posts--prod-monitoring-a-healthy-freeswitch-process-can-still-mean-broken-calls.tpl
  source: cms/templates/posts/posts--prod-monitoring-a-healthy-freeswitch-process-can-still-mean-broken-calls.json
---

The useful question behind **A Healthy FreeSWITCH Process Can Still Mean Broken Calls** was not whether I could collect another metric. It was whether the metric would reduce uncertainty during a the live host failure on a very small machine.

The host is 2014 Apple Mac mini running Linux, with roughly 7.1 GiB usable RAM from an 8 GB-class machine. Applications, databases, networking, authentication, OTA, OpenBao, VoIP and the observability stack share the same limited CPU, memory and storage. That makes monitoring part of the workload rather than something outside it. The central failure I am trying to avoid is not merely “a metric went high.” I want enough corroborating data to tell whether a user-facing service is degrading, which dependency owns the problem, whether the signal is current, and whether the monitoring path itself is still trustworthy.

For this specific problem the primary observation point is `FreeSWITCH sessions by node`. The short the live host note that preceded this article captured the core finding: Per-node distribution reveals skew, draining problems and backend selection bias that aggregate call totals cannot show. This long-form version goes further: what that signal really proves, which nearby signals can falsify my first hypothesis, how I implement and detection rule on it, what it costs on this host, and how I would redesign the same control at larger scale.

The numbers in this article are not generic benchmarks. When I mention 27,578 active Prometheus series, against a 27,414-series acceptance baseline, cAdvisor measured at 428.2 MiB before the low-RAM work and 27.87 MiB in one post-change sample, with an observed steady range around 20–28 MiB, or any other concrete value, I mean the 2026-09-15 acceptance snapshot unless I explicitly say otherwise. If a current value is not present in the accepted corroborating data, I leave `[CURRENT MEASUREMENT NEEDED]` rather than inventing a number.

## The engineering question specific to this article

The short version of the problem is not “how do I graph A Healthy FreeSWITCH Process Can Still Mean Broken Calls?” It is: **A healthy total session count can hide a load-balancing problem if one FreeSWITCH node carries nearly all calls while another remains idle.** That failure can be confused with neighboring conditions, which is why the primary observation is `FreeSWITCH sessions by node` rather than a generic process-up flag.

The deployed the live host conclusion is specific: Per-node distribution reveals skew, draining problems and backend selection bias that aggregate call totals cannot show. I turn that conclusion into an operational practice—load-distribution monitoring—and into a preventive control: Graph sessions and idle CPU per worker and compare them during steady traffic before changing balancing weights. Those three layers are intentionally separate. The finding explains what the corroborating data taught me. The practice describes how I diagnose it. The prevention rule describes how I keep the same ambiguity from returning after the next deployment.

There is also a data-model question. The observation has to retain the dimension that matters without encoding unbounded identity. If the question is per node, the node label matters. If it is fleet capacity, an aggregate may be more useful. If it is an event such as a deadlock or OOM kill, a counter over a time window carries different meaning from a current-state gauge. If it is a cached inventory value, age and refresh success are part of the value's contract.

Finally I decide how close this signal is to user impact. Some topics in this series are direct symptoms; others are explanatory corroborating data. `A Healthy FreeSWITCH Process Can Still Mean Broken Calls` belongs at the point where it can reduce investigation time without claiming more certainty than the underlying source provides. That classification determines whether it becomes a page, a warning, a drill-down view drill-down or simply retained forensic context.

## Competing hypotheses before I touch the live host

I try to write down multiple explanations before making a change. For **A Healthy FreeSWITCH Process Can Still Mean Broken Calls**, the candidate set I would test includes: **registration/signaling is healthy while media is broken**; **a worker process is alive but its heartbeat is stale**; **OpenSIPS signaling quality degrades while the port remains reachable**; **RTPengine closes sessions for a specific failure reason**; and **one node is unhealthy while fleet totals still look acceptable**. The point is not that all five are equally likely. It is to stop the first plausible graph from becoming the conclusion.

The primary observation `FreeSWITCH sessions by node` should eliminate some of those hypotheses, not all of them. I choose the next query or log source by information gain: which check can separate the most remaining explanations at the lowest operational cost? A fresh internal probe versus a failed public probe immediately moves suspicion toward the edge. High memory utilization with low pressure and stable swap activity moves me away from a memory-emergency diagnosis. A stale FreeSWITCH heartbeat with a running container moves the problem from process liveness into worker readiness.

This habit is especially useful on a single host because many symptoms are correlated. Storage pressure can slow databases, logs and containers simultaneously. Host memory pressure can make the monitoring stack itself late. A router or Internet failure can make every public service look broken while the applications are healthy. Explicit competing hypotheses keep correlation from being mistaken for independent failures.

## The observation contract I expect this signal to keep

For `FreeSWITCH sessions by node` I want a written contract even if it is only a few lines in a runbook. The contract says who produces the data, what unit it uses, which labels are bounded and meaningful, how often it should update, what reset behavior exists, and what missing data means. Without those details an old metric can survive long after its interpretation has changed.

The contract also names the strongest claim the signal supports. Per-node distribution reveals skew, draining problems and backend selection bias that aggregate call totals cannot show. That sentence is intentionally narrower than “the service is healthy.” It leaves room for independent corroborating data and tells future maintainers not to reuse the metric for a stronger conclusion without re-validating it.

Freshness belongs in the contract whenever the producer is not scraped directly. Cache-backed Docker inventory, textfile metrics, heartbeat state and backup timestamps can all remain syntactically valid after the producer stops. I therefore prefer either an explicit age metric or a timestamp from which age can be derived. For direct Prometheus targets, `up` is part of the collection contract but still not the service-health contract.

Finally, the contract includes data sensitivity. Labels and log content must not turn operational telemetry into a secret-disclosure channel. If the observation cannot be collected safely with bounded identity and least privilege, I redesign the observation path rather than assuming the monitoring network is trusted.

## Start with the failure, not the exporter

The fault conditionl for this article is: **A healthy total session count can hide a load-balancing problem if one FreeSWITCH node carries nearly all calls while another remains idle.** That wording matters because it describes the operational ambiguity I need to remove. A raw metric has no value until I know what claim I am trying to make from it.

The obvious monitoring mistake is to collapse several layers into one binary state. A process can exist while the application is unusable. A observation path can return a number that is already stale. A public service can correctly return a redirect or authorization error and still be healthy. A database can accept a TCP connection while lock contention makes useful queries stall. A host can report high memory utilization while reclaimable page cache means applications are not under pressure. The same general problem appears repeatedly: one layer's “up” is only corroborating data about that layer.

I therefore map each failure to at least three questions. First, what is the earliest useful signal that something is changing? Second, what is the strongest user-visible symptom I can observe independently? Third, what corroborating data tells me the monitoring path is alive enough to trust the first two answers? For `A Healthy FreeSWITCH Process Can Still Mean Broken Calls`, `FreeSWITCH sessions by node` belongs in that chain, but it is never allowed to stand alone if the failure can be confirmed from another layer.

This is also how I decide whether an detection rule belongs on a metric. A signal may be excellent for diagnosis and terrible for paging. Context switches, container block-I/O bytes or database size trends can be valuable corroborating data without being reasons to interrupt an operator immediately. Conversely, a public probe failure or no-healthy-worker condition may deserve much more direct attention because it is already close to user impact.

## Where this sits in the hserver observability architecture

VoIP monitoring cannot be reduced to an HTTP health endpoint because voice has several independent planes. Registration can be broken while established media continues. SIP signaling can return successful responses while RTP is one-way or silent. A Drachtio process can be connected while its FreeSWITCH pool has no healthy worker. OpenSIPS can answer OPTIONS while transactions are failing. RTPengine can run while media sessions close for failure reasons that matter to callers.

The monitoring model therefore follows the call path. Drachtio connectivity, configured-versus-healthy FreeSWITCH counts, heartbeat age, no-healthy-worker events and proxy failures cover the programmable SIP edge. OpenSIPS transaction classes, 5xx changes, dialogs and registered users cover signaling state. RTPengine close reasons and session behavior cover the media relay. Per-worker session counts prevent fleet totals from hiding one bad node. The drill-down view should let an operator move from user symptom to signaling, worker and media corroborating data without pretending that one green web panel proves a call can complete.

For this article, the component boundary matters as much as the metric. The deployed accepted observability stack includes Prometheus, Grafana, Loki, Alloy, Alertmanager, Blackbox Exporter, Node Exporter, cAdvisor, SMART collection, Docker inventory and deep host/database observation paths, plus application-native and external synthetic signals. The latest acceptance artifact records 52/52 accepted Prometheus targets UP, 106 detection rule/recording rules loaded, 15 provisioned drill-down views and 10/10 public probes UP.

I intentionally avoid interpret those counts as a maturity score. More targets and more rules can make a system worse if they add noise or cost without reducing uncertainty. The useful part is that the inventory is explicit and accepted. When I add a control for `A Healthy FreeSWITCH Process Can Still Mean Broken Calls`, I can ask which existing layer already sees part of the problem, whether a new metric is necessary, and how the new observation will be validated after deployment.

## The decision this monitor should let me make

If this telemetry cannot change a decision, it should not automatically consume always-on budget. For **A Healthy FreeSWITCH Process Can Still Mean Broken Calls**, the decisions fall into four categories. I may need to intervene immediately because a service contract is already broken. I may need to schedule capacity work because margin is shrinking. I may need to isolate a dependency during incident diagnosis. Or I may decide that the condition is normal and explicitly avoid action.

That last outcome is important. Monitoring is partly a system for proving when *not* to react. Page cache, historical swap, a 302 authentication redirect, a controlled restart, or a busy response from a SIP endpoint can look abnormal without representing infrastructure failure. The metric model should carry enough context to distinguish those cases.

I also make sure to want the monitor to make rollback decisions safer. If a deployment changes `FreeSWITCH sessions by node`, I should be able to compare the new state with the accepted baseline and decide whether the change is intended. That is why provenance `b65d5d4` stays attached to the topic. A the live host metric without a known configuration history is harder to use as change corroborating data.

At scale this decision-centric approach becomes even more important. Hundreds of hosts can produce unlimited telemetry; operator time remains finite. The series therefore treats observability as a decision system rather than a storage system.

## Why this particular collection path won

There are usually several ways to obtain the state behind **A Healthy FreeSWITCH Process Can Still Mean Broken Calls**: scrape an existing exporter, query an application API, run a SQL statement, parse logs, inspect the Docker API, read a Linux kernel interface, or publish a small custom metric through the textfile path. I choose among them by authority, cost, security and failure independence.

The closest source is not always the best source. A Docker container metric can tell me process resource use but not whether PostgreSQL sessions are waiting. A log parser can count authentication failures but is a weaker source for current service readiness than a direct state query. A raw TCP probe is cheap but deliberately shallow. A deep query may be authoritative but require credentials or create load. The actual configuration behind `FreeSWITCH sessions by node` is valuable because it sits at the layer that owns the state I need to interpret.

I also make sure to prefer collection paths with visible failure. A custom script that exits silently and leaves yesterday's textfile metric behind is worse than a observation path that exports its own success and age. A cache should expose refresh result and age. A database observation path should expose whether its query succeeded. A log pipeline should expose drops. The observer has to be observable.

The chosen path therefore reflects more than convenience. It is part of the fault conditionl: which component can lie, which credential can expire, which namespace the query sees, and what remains observable when another layer breaks.

## How I reason about a threshold for this topic

I intentionally avoid begin with a round number. I begin with the consequence I am trying to avoid and how much reaction time exists. Capacity thresholds such as disk or connection utilization should leave enough margin to investigate before exhaustion. Pressure thresholds should remain high long enough to distinguish real contention from transient scheduling noise. Certificate thresholds are measured in days because the repair process is administrative, not millisecond-sensitive. External availability failures can justify much faster response.

For **A Healthy FreeSWITCH Process Can Still Mean Broken Calls**, the next threshold review should use the historical distribution plus the component's configured limit and the time needed to act. If that distribution is not captured in the current acceptance artifact, the honest value is **[CURRENT MEASUREMENT NEEDED]**. I intentionally avoid derive a the live host page from an attractive number in a blog post.

I also make sure to test both sides of the boundary. A warning threshold should actually enter pending/firing state when a fixture crosses it, and it should resolve when the signal recovers. A critical threshold should not be inhibited by the warning in a way that loses the more serious state. If the signal is a counter, the window should contain enough events to be meaningful. If it is a gauge, the `for` duration and freshness semantics matter more than counter reset behavior.

Thresholds are therefore versioned policy. When topology, workload, resource limits or observation path semantics change, I expect the threshold to be reviewed alongside the code.

## Draw the data path before trusting the panel

For this part of the system I keep a simple failure-domain drawing in mind:

```
endpoint -> SIP edge (OpenSIPS/Drachtio) -> FreeSWITCH worker -> RTPengine/media -> peer
              \-> SQL/DNS dependencies      \-> heartbeat/session state
```

The diagram matters because every arrow can fail independently. Collection can succeed while storage or rule evaluation fails. An internal probe can succeed while the public path fails. A public probe running on hserver still shares the host failure domain even if it reaches a public URL. A database exporter can be healthy while its engine query permission is broken. A log observation path can be alive while the write path drops entries.

For `A Healthy FreeSWITCH Process Can Still Mean Broken Calls`, I identify the authoritative source on the left, every transformation before the drill-down view or detection rule, and which component owns persistence. Then I decide where failure should become visible. If a transformation silently converts “unknown” into zero, the diagram has an observability gap. If both the service and its observer depend on the same process or credential, the diagram has a shared failure domain.

This exercise is cheap and often catches problems before PromQL is written. It additionally explains why I retained both internal and public probes, why the external watcher lives on hosted runners, and why backup corroborating data has multiple stages rather than one success bit.

## The mechanism underneath the graph

A VoIP call crosses independent state machines. SIP registration establishes reachability, SIP transactions establish signaling exchanges, dialogs retain routing state, FreeSWITCH workers own B2BUA call legs, and RTPengine handles media state. Drachtio health and worker heartbeat state affect new-call routing; OpenSIPS transaction classes expose proxy behavior; RTPengine close reasons expose media outcomes. A single HTTP health endpoint cannot collapse those planes without losing the reason a call failed.

That mechanism matters for `A Healthy FreeSWITCH Process Can Still Mean Broken Calls` because two visually similar graphs can have very different semantics. A cumulative counter should normally be turned into a rate or increase over a time window. A gauge can be read directly but still needs freshness. A ratio is meaningless if its denominator is missing, zero or describes a different capacity boundary. A status value needs an explicit state model. A log-derived count depends on the reliability of ingestion and parsing. A synthetic probe depends on where the probe originates and which route it exercises.

I try to preserve units all the way from collection to the panel and detection rule. Seconds should not silently become milliseconds. Bytes should not be compared with decimal “GB” labels without deciding which convention is in use. Percentages should identify their denominator. Ages should be derived from timestamps in a timezone-independent way. These details look small in configuration review and become large during incidents, when the operator is making decisions from the graph under time pressure.

The other subtlety is reset behavior. Counters restart with processes. Container identities change on recreation. database cumulative statistics can reset after engine restart. A drill-down view that uses raw cumulative values can therefore interpret restart as recovery or huge negative activity. Query functions and labels need to match the lifecycle of the component being measured.

## Implementation: make the observation cheap and reproducible

The actual configuration is deliberately smaller than the explanation. I want the collection path to be boring: deterministic configuration in Git, bounded work on the host, a clear scrape or evaluation cadence, and a result that can be checked after deployment. Repository corroborating data associated with this topic is `b65d5d4`.

A representative query or configuration fragment is:

```
voip_freeswitch_nodes_healthy
voip_freeswitch_heartbeat_age_seconds
```

The fragment is not meant to be copied blindly into another system. Labels, device names, mount points, job names and custom metric families are deployment-specific. The important point is the shape of the control. Ratios need denominators. Counters need rates or increases over windows. Slow-changing inventory should not be polled at CPU-metric cadence. Authentication-aware probes need status semantics. Freshness-sensitive observation paths need age checks. Expensive queries should be recorded or sampled at a cadence that matches the decision they support.

I also make sure to keep configuration ownership separate from runtime corroborating data. Prometheus rules, scrape configuration, drill-down views and observation path code live in the reviewed source tree. Runtime acceptance data records what the live host actually observed. Secret values stay out of both metrics and public documentation. This lets me reproduce the monitoring design without turning the monitoring repository into a credential store.

## Walk the failure from symptom back to cause

A concrete way to review this monitor is to imagine a failure and force myself to predict what each layer would show. I intentionally avoid claim the following sequence happened unless it is part of the recorded corroborating data; it is a design exercise for the control.

Start with the user-visible symptom related to **A Healthy FreeSWITCH Process Can Still Mean Broken Calls**. The top-level probe or service metric changes first or eventually. I then ask whether the host is still reachable, whether the target is still being scraped, and whether `FreeSWITCH sessions by node` is fresh. If the target is down, an old threshold value is no longer the primary corroborating data; target failure becomes the first branch. If the target is up, I compare the signal with its nearest independent corroborator.

From there I trace downward. A host-pressure signal leads to per-container attribution and kernel logs. A container symptom leads to host resource state and application health. A database symptom leads from reachability to connection, wait, lock and engine state. A public probe failure is compared with the internal probe, DNS/TLS phases and edge logs. A VoIP symptom is separated into signaling, worker and media corroborating data. A backup symptom is followed through job, artifact, checksum and restore state.

The objective is not to prove that every incident follows one tree. It is to make sure each metric has a place in an investigation. If a signal cannot tell me which branch to take next, I question whether it belongs in the always-on monitoring budget.

## How I debug this signal when it looks wrong

I prefer a layered debugging order because the fastest way to waste time is to treat the first abnormal graph as the root cause. For **A Healthy FreeSWITCH Process Can Still Mean Broken Calls**, I start by proving that the sample is current. I check target or observation path health, the timestamp/freshness path, and whether a recent deployment changed labels or collection cadence. If the value can be generated from a custom observation path, I compare the exported value with the underlying operating-system, Docker, database or application state.

Next I look for a neighboring signal that should move if my hypothesis is correct. Memory pressure should have some relationship to MemAvailable, swap activity, OOM corroborating data or workload latency. Storage latency should have some relationship to I/O pressure or application waits. Container I/O should reconcile with host disk activity. A database saturation hypothesis should be visible in connection, wait or lock state. A public availability failure should be compared with an internal probe so I can separate application failure from DNS, TLS, tunnel or edge failure.

Only after that do I broaden into logs. Logs are best when the failure domain is already smaller: kernel OOM records, Docker daemon warnings, authentication failures, Alloy/Loki pipeline errors, database messages or VoIP-specific events. This keeps me from searching an unbounded log corpus for an event I have not yet defined.

The last step is to check the monitoring system itself. A quiet drill-down view can be caused by a missing target. A stable line can be a stale sample. A zero-detection rule page can coexist with rule-evaluation failures. I want corroborating data that the observer is alive before I trust the observation.

## The false-positive and false-negative traps

Every monitoring decision has at least two ways to be wrong. A false positive declares a failure when the system is operating within its intended semantics. A false negative keeps the drill-down view green while the service contract is broken. `A Healthy FreeSWITCH Process Can Still Mean Broken Calls` is useful only if I can describe both.

A common false positive is reading a state without duration or context. Non-zero swap can be historical. High CPU can be productive work. A protected HTTP endpoint can return 302, 401 or 403 because authentication is functioning. A brief container restart can be a deployment. A temporarily high database connection count can be harmless if capacity and latency remain healthy. These cases need windows, denominators or state semantics before they become incidents.

The false negative is usually more dangerous. A target can scrape successfully while its downstream dependency is broken. A stale custom metric can remain below threshold after its observation path died. A database socket can accept connections while waits or locks stop useful work. A FreeSWITCH process can run while the worker heartbeat is stale. A backup archive can exist while restore verification has not succeeded. Those failures are why the architecture uses independent layers instead of treating one green signal as global truth.

When I review a rule or panel, I explicitly ask: what normal condition could make this look bad, and what bad condition could make this look normal? That question often produces a better second metric than adding another threshold to the first one.

## What would make this monitor lie?

I ask this question explicitly because most monitoring failures are not fabricated numbers; they are numbers interpreted outside their validity. `FreeSWITCH sessions by node` can become misleading if its observation path is stale, labels change, the underlying source resets, the query aggregates away the failing member, the scrape path observes a different network namespace, or the monitored component changes semantics after an upgrade.

Caching creates another class of lies. The Docker storage inventory is deliberately cached because continuous filesystem inspection was too expensive. A cache-backed metric is only trustworthy when cache age and refresh success are visible. Textfile metrics have the same issue if the producer stops updating them. Database-derived metrics can lie by omission if the observation path account loses access to a system view. Log-derived metrics can go quiet because Alloy or Loki is dropping data rather than because the event stopped happening.

Authentication and synthetic probes can lie through overly permissive expectations. Following redirects blindly may turn an application failure into a successful login-page response. Accepting every status code may hide a broken route. Requiring only 200 may create the opposite error and call a healthy access-control response an outage. The probe has to encode the intended contract.

My response to these risks is not distrust of monitoring. It is meta-monitoring, freshness, independent corroborating data and explicit UNKNOWN states when the observation path cannot make a strong claim.

## The hserver case that shaped this part of the design

The voice stack makes cross-layer observability unavoidable. Drachtio can be connected while a worker heartbeat is stale. OpenSIPS can be reachable while 5xx transaction behavior degrades. FreeSWITCH can be healthy as a process while there is no acceptable worker for new calls. RTPengine can have a different failure story again. The deep VoIP drill-down view is therefore organized around call-path corroborating data rather than around container names.

I prefer that case as a guardrail for `A Healthy FreeSWITCH Process Can Still Mean Broken Calls` because it prevents the discussion from becoming a generic monitoring tutorial. The interesting question is not whether another platform supports the same metric. It is what decision the signal enabled on this constrained the live host host, what cost it imposed, and what corroborating data proved that the change improved rather than merely rearranged the system.

It additionally keeps causality honest. A before/after measurement is corroborating data for this configuration at that time. It is not a universal benchmark for cAdvisor, Prometheus, Docker, OpenBao or any database engine. When the article makes a recommendation, the recommendation is about the engineering method—measure, isolate cost, preserve the useful signal, verify the new fault conditions—not about assuming another machine will reproduce the same number.

## Cross-layer dependencies I intentionally avoid want this monitor to hide

The signal in this article belongs to one layer, but incidents cross layers. A memory-pressure detection rule can be caused by a container leak, a database cache change, observability cardinality growth or an unrelated batch job. A public HTTP failure can be application, reverse proxy, authentication, DNS, TLS, tunnel, router or Internet path. A database latency symptom can be locks, storage, memory reclaim or connection saturation. A VoIP symptom can cross registration, SIP transaction, worker health, DNS/SQL dependency and RTP media.

That is why I avoid drill-down views grouped only by exporter. Exporters reflect collection technology; incidents follow dependencies. `A Healthy FreeSWITCH Process Can Still Mean Broken Calls` should link naturally to the next corroborating data domain. The host view links to containers and storage. Database panels link to host I/O and container limits. Public probes link to internal probes and edge logs. Alert-delivery panels link back to rule health. Backup panels link to disk headroom, job logs and restore verification.

This cross-layer model also changes detection rule grouping. If one host failure makes ten applications disappear, the application probes are still useful symptoms, but the operator should not receive ten unrelated pages. Conversely, if the host is healthy and only one public route fails, collapsing everything into “host healthy” would hide the actual service outage. Correlation is therefore contextual, not a reason to suppress independent corroborating data.

## Turning the observation into an detection rule without creating noise

Not every article in this series ends with a page. Some of the best signals are diagnostic. When I do detection rule, I separate **prediction**, **saturation**, and **symptom**. Prediction covers conditions such as disk capacity or certificate expiry where action before failure is possible. Saturation covers sustained pressure or exhausted pools. Symptoms cover conditions such as a failed public probe, no healthy SIP worker, or unsuccessful restore verification where the service contract is already affected.

The rule duration has to fit the failure. A single scrape miss or short deployment restart should not create an incident. A total public outage should not sit pending for an arbitrary long `for:` window simply because another resource rule uses ten minutes. Warning and critical labels are response contracts: warning means investigate or schedule action before the margin disappears; critical means the operating state is already outside the tolerated envelope or approaching it fast enough to require immediate attention.

I also make sure to ask what other detection rule will fire at the same time. If host loss makes every public service fail, paging separately for Grafana, OTA, authentication, gateway and VoIP adds noise without information. Grouping and inhibition should preserve useful symptoms while making the likely root event obvious. Resolution is part of the lifecycle too. The latest accepted notification corroborating data recorded external notification counters in the acceptance artifact: 13 success, 0 failure, 6 resolved; that is a snapshot of delivery behavior, not an SLA claim.

For `A Healthy FreeSWITCH Process Can Still Mean Broken Calls`, the detection rule is successful only if its annotation tells me what was observed, over what window, which drill-down view or runbook to open next, and what secondary signal can confirm the hypothesis.

## Acceptance: prove the monitor after changing it

I intentionally avoid treat a configuration commit as proof that monitoring works. After meaningful observability changes I compare the desired state in Git with runtime acceptance. The deployed artifact records 52/52 accepted Prometheus targets UP, 106 detection rule/recording rules loaded, 0 firing and 0 pending detection rules, 27,578 active Prometheus series, against a 27,414-series acceptance baseline, 10/10 public probes UP, 9/9 database probes UP and 35 monitored configuration files with zero drift in the latest runtime sample. Those numbers are useful because they make blind spots and accidental cardinality growth measurable after deployment.

The validation depends on the feature. A scrape change should prove the target is UP and the expected series exists. A relabel change should prove the required drill-down view and detection rule queries still return data. A log-pipeline change should prove cursor continuity and check drop counters. A public probe should be exercised against both healthy and intentionally invalid behavior. A backup control should be followed by checksum and restore corroborating data. A notification change should send a synthetic detection rule and verify both firing and resolved delivery.

Where safe, I prefer failure injection to passive confidence. The external dead-man watcher was tested by forcing a synthetic outage: the hosted workflow failed, an incident issue was created, recovery later passed and the issue closed. That sequence proved more than reading the workflow YAML. The same idea scales down to small controls: temporarily make a test target fail, expire a synthetic sample, or use a fixture that triggers the rule without damaging the live host.

## The investigation sequence I want at 2 a.m.

The runbook for this signal is intentionally ordered. First confirm time and freshness. I intentionally avoid troubleshoot an old sample as though it were current. Second confirm the observation path or target path. Third compare the value with the nearest independent signal. Fourth look at the dependency layer below it. Fifth use logs or a direct engine query for detail. Only then change the live host.

For `A Healthy FreeSWITCH Process Can Still Mean Broken Calls`, the first direct question is whether `FreeSWITCH sessions by node` is updating on schedule. If it is, I compare it with the signal that would be expected to move under the same failure hypothesis. If the two disagree, that disagreement is corroborating data: either the original hypothesis is wrong, the metrics have different semantics, or one observation path is broken.

I also make sure to preserve before/after corroborating data around changes. If I tune a scrape interval, relabel metrics, disable an expensive observation path feature or change an detection rule window, I capture the relevant series count, memory state, target state and rule health. That makes rollback rational. Without a before state, optimization can quietly delete the only metric that explained a future incident.

My final runbook step is acceptance, not “container restarted successfully.” I want the query to return the expected data, the drill-down view to render, the rule to evaluate, the synthetic path to behave correctly, and the monitoring stack to remain inside its resource budget.

## What I would change at larger scale

The small-server version optimizes for bounded cost and direct inspectability. With dedicated monitoring nodes I would preserve the semantic model but move some responsibilities. Metrics storage could move off the application host. Long-term retention could use a system designed for remote or object-backed storage. Loki could live on a dedicated node. Exporter and observation path work could be distributed closer to the workloads while query and detection rule evaluation stay centralized. High-availability Alertmanager and independent monitoring storage would reduce shared failure domains.

I would not, however, replace `FreeSWITCH sessions by node` with a generic “enterprise monitoring” product and call the problem solved. The key question remains what the observation proves. If the signal is about Linux pressure, the kernel semantics remain. If it is about database locks, the engine semantics remain. If it is about SIP versus RTP, the protocol boundaries remain. If it is about dead-man monitoring, the observer still has to live outside the failure domain.

Scale primarily changes collection topology, retention, redundancy and automation. It does not remove the need to define failure semantics. In fact, larger systems punish ambiguous metrics more severely because a noisy or high-cardinality mistake multiplies across more hosts and more operators.

## What the current accepted system says

The 2026-09-15 acceptance snapshot gives me a concrete reference point while writing this series. It records 52/52 accepted Prometheus targets UP, 106 detection rule/recording rules loaded, 0 firing and 0 pending detection rules, and 15 provisioned drill-down views. Prometheus reported 27,578 active Prometheus series, against a 27,414-series acceptance baseline. Public probing reported 10/10 public probes UP; database probing reported 9/9 database probes UP. The accepted configuration manifest reported 35 monitored configuration files with zero drift in the latest runtime sample.

For storage and retention, Prometheus retention set to about 30 days with a 15 GB size cap; Loki retention set to 168 hours. For hardware corroborating data, SMART status healthy in the acceptance artifact, with a 49 C device-temperature sample. For recovery, encrypted DR verification PASS, required payload PASS, internal checksum PASS, off-host pull PASS, and restore verification PASS. For OpenBao, main OpenBao initialized and unsealed with Transit auto-unseal; same-host seal node initialized and unsealed with no host-published ports. These values are intentionally described with a date because they are not permanent properties of the architecture. They are corroborating data that the system reached a known state after a particular round of changes.

This distinction is important for `A Healthy FreeSWITCH Process Can Still Mean Broken Calls`. Monitoring documentation tends to age badly when it turns an observation into a law. I would rather write “27,578 active series in this acceptance snapshot” than imply that 27,578 is a target, a limit or a recommendation. The same applies to cAdvisor memory, disk temperature, drill-down view count and detection rule-rule count. The system design should survive changing numbers because the interpretation rules remain explicit.

## What I keep from this decision

The practical lesson from **A Healthy FreeSWITCH Process Can Still Mean Broken Calls** is that a useful monitor is a tested claim about a fault condition, not a decorative line on a drill-down view. The control is useful because I know its acquisition cost, expected cadence, fault conditions, corroborating signals and response path. That is the standard I now use before adding another metric or detection rule to hserver.

The server is still an old Mac mini. That constraint has not stopped the monitoring system from becoming serious. It has forced every layer to be explicit about what it is worth. For me that is the more interesting engineering result: the live host-grade observability is less about how many products are installed and more about whether the corroborating data is sufficient, current, independent where necessary, and cheap enough that the observer does not become the outage.
