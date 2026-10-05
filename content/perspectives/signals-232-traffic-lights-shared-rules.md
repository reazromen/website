---
title: "Traffic Lights and the Shared Rules Behind a Signal"
date: '2024-07-11'
draft: false
language: en
url: /posts/signals-232-traffic-lights-shared-rules.html
topic: signals-and-signaling
tags:
- signals-and-signaling
featured: false
read_time: 15
excerpt: "A button press, a detector call, a controller decision, and a green indication are different events. Following them through a constructed intersection reveals why signalling depends on shared rules and observable state."
series: signals-around-us
series_index: 232
eyebrow: "Signals Around Us · 232 of 300"
---

Someone presses a crossing button and watches the vehicle lights remain unchanged. “The button does nothing” is a reasonable suspicion, but it is not yet a diagnosis. Perhaps the request was not detected. Perhaps it was detected and is waiting for a permitted service opportunity. Perhaps the crossing is already scheduled and another press changes nothing visible. One outward observation can fit several internal states. The interesting question is what evidence would distinguish them.

A traffic signal is a particularly clear example of communication embedded in a control system. Light reaches the eye, but its meaning depends on a shared convention, the movement it addresses, and the surrounding state. Behind the display, detectors and timers influence decisions under constraints. Beyond the display, people interpret and act. The complete system includes all of those relationships. Measuring only whether a lamp illuminates leaves most of the communication problem unexamined.

For concrete documentation, I use the United States Federal Highway Administration's current MUTCD and its technical traffic-signal timing manual.[1][2][3] They provide a documented example of signal meanings and control concepts; the discussion does not substitute those documents for another jurisdiction's rules. The intersection, demands, and numerical queues below are constructed. No real junction was inspected, and the examples are explanatory models rather than a timing plan for installation.

## A color becomes a message through a convention

A wavelength distribution does not inherently contain the instruction “stop.” A traffic-control system assigns meanings to displayed indications and their context. Position, shape, direction, timing, and the road movement addressed can all help determine that meaning. A photograph of one illuminated lamp may omit information a road user has at the scene. The physical signal and the interpreted instruction are therefore connected by a convention, not by optics alone.

The MUTCD's detailed treatment of traffic-control signals makes that dependence visible.[1] A circular indication and a directional arrow are not interchangeable descriptions of permission. Nor should an indication be read as proof that an intersection is physically empty. The device communicates a defined instruction or permission within an operating context. The actual positions of people and vehicles remain part of the situation. A command about movement and evidence that movement can occur are different kinds of information.

For an engineering analogy, a protocol field only makes sense when sender and receiver share its definition. A byte value can be received perfectly and interpreted incorrectly if the convention differs. Traffic signals expose the same general issue in an everyday setting. Reliable transmission of the physical indication matters, but agreement about its meaning matters too. A bright, electrically functioning display does not by itself establish that every intended user can perceive and interpret it as designed.

## A request is different from an immediate command

Consider a constructed crossing where a button generates a request for pedestrian service. Detecting the press records demand; it does not necessarily authorize an immediate change in every displayed indication. Other movements may already be receiving service, and the controller has to follow the applicable sequence and constraints. The FHWA timing manual describes pedestrian intervals and actuated timing concepts that make this separation explicit.[3] The request and its eventual service are distinct events.

That distinction explains why repeated presses may provide no visible acceleration in some arrangements. If a request is already stored, another identical request may not change the relevant state. Whether that is how a particular installation works requires its configuration and observations. I would avoid both universal claims: that repeated presses always help, or that every button is merely decorative. The defensible question is what state the input changes in the system being investigated.

A useful record would identify the input event, whether a request was registered, when the relevant service became eligible, and when the indication actually changed. Those timestamps separate a detection problem from a scheduling delay or a display problem. Looking only at the time between a person's gesture and a visible light change merges several mechanisms into one number. That number can describe the experience, but it cannot independently identify which mechanism produced it.

## Follow the control loop beyond the controller

Vehicle detection is another input pathway. The timing manual discusses detector operation, including presence and pulse modes, and how detection supports phase calls and termination decisions.[2] A detector's observation is not the same as the road scene itself. It is a measurement with a defined zone, timing behavior, and possible errors. A controller can make a perfectly consistent decision from an inaccurate input. That is why investigating the software alone may miss the cause of an apparently irrational signal sequence.

![Conceptual traffic-signal control loop linking detection, request state, controller constraints, displayed indications, and observed road-user movement.](/static/signals/signals-232-control-loop.png)

*Figure 1. Conceptual relationships, not a deployable controller design. A request, a selected service, an observed indication, and an actual movement are separate states. Feedback about the road scene can affect later decisions, while the governing rules constrain which decisions are permitted.*

The controller's output is also not the end of the causal chain. A commanded display must be produced by the equipment, perceived by the road user, interpreted, and acted upon. A log saying that an output was requested is evidence about a command, not automatically evidence about the physical lamp or a person's response. An investigation should identify which boundary each observation covers. Otherwise a healthy controller log can be mistaken for proof that the entire system behaved as intended.

This is familiar in distributed software: sending a message, acknowledging receipt, completing work, and observing the intended real-world result are different milestones. The analogy helps organize the evidence without treating road users as software processes. People have perception, reaction, and accessibility needs that the model must respect. The control loop is useful precisely because it includes the physical and human consequences beyond the internal state machine.

## Conflicting movements create a scheduling problem

Imagine two abstract movements that cannot be served together in our simplified intersection. Giving one more service time reduces the time available to the other unless the overall schedule changes. Requests can therefore be valid and still wait. The controller is not simply maximizing the response speed to the most recent input. It must coordinate demands under constraints and a chosen operating policy. A complaint about delay should be investigated with those competing demands visible.

Real intersections can include compatible simultaneous movements, turning movements, pedestrian service, and different control arrangements. The timing manual discusses phasing and the relationship between design choices and operation.[2] A two-movement drawing is useful for explaining competition for time, but it cannot stand in for that full geometry. I would establish which movements actually conflict and which can operate together before interpreting a sequence or proposing why one approach receives a particular share.

The selected objective matters as well. Minimizing average vehicle delay, serving pedestrians, avoiding excessive queues, accommodating transit, and handling unusual demand can lead to different tradeoffs. An apparently inefficient moment may reflect a constraint or priority not visible from one approach. That does not make every delay justified. It means the evaluation needs an explicit objective and evidence about the whole intersection, rather than assuming that the observer's waiting time is the only performance measure.

## A simple queue makes the tradeoff measurable

Build a deliberately restricted model with a sixty-second cycle. Suppose a movement can discharge vehicles at a rate equivalent to 1,800 vehicles per hour while it receives effective service, and enough vehicles are waiting to use that opportunity. That rate is one vehicle every two seconds. If the movement receives twenty-four seconds of effective service per cycle, it can serve twelve vehicles per cycle, equivalent to an average of 720 per hour under these assumptions.

Increase effective service to thirty-six seconds and the model serves eighteen vehicles per cycle, equivalent to 1,080 per hour. The word “effective” is important: these are assumed productive service intervals, not a claim that every displayed green second produces identical discharge. The calculation omits many real effects and is not a prescription for green times. It isolates one relationship between allocated service and possible departures so that we can inspect its consequences for a queue.

Now assume fifteen vehicles arrive before each cycle's service opportunity, corresponding to 900 per hour in this deterministic example. With capacity for twelve departures, the queue grows by three vehicles each cycle while demand remains unchanged. With capacity for eighteen, a pre-existing queue can shrink by three per cycle until there is insufficient backlog to use all eighteen slots. The comparison shows why a modest change in service can move a simplified system from persistent accumulation to eventual clearance.

## A queue can grow while the signal appears busy

Start the model with twenty waiting vehicles. After ten cycles at twelve departures against fifteen arrivals per cycle, fifty remain. The signal has served vehicles repeatedly, so an observer sees movement and functioning equipment. Nevertheless, the queue grows because arrivals exceed service. “The light turns green” and “the movement has enough capacity for this demand” are different claims. A system can be active throughout an observation and still fall further behind.

![Deterministic queue calculations for fifteen arrivals per cycle and service capacities of twelve or eighteen vehicles, starting with twenty waiting vehicles.](/static/signals/signals-232-queue.png)

*Figure 2. A toy queue follows Qnext = max(0, Q + 15 − service). After ten cycles, the lower-service case has 50 vehicles waiting and the higher-service case has cleared. Arrivals are assumed to occur before each service opportunity; the figure is not a traffic simulation or a measured junction.*

The higher-service model reaches zero after seven cycles, with unused service opportunities once the queue clears. That unused time might look wasteful if viewed without the preceding backlog and competing demands. In a responsive real system, service can depend on detected demand and configured rules. Our fixed calculation simply shows why both the arrival process and the prior queue matter. A photograph or one cycle cannot establish the longer-term balance between incoming demand and completed service.

Average demand also conceals timing. Fifteen evenly spaced arrivals and a batch of fifteen arriving immediately after service ends can create different waiting experiences even if the per-cycle count matches. Our recurrence chooses one timing convention explicitly. A more detailed model would need arrival times, departures, and the actual service intervals. Precision in the average does not compensate for omitting the temporal structure relevant to the question being asked.

## Detection errors can imitate a scheduling fault

Suppose a constructed detector misses a waiting user. The controller may receive no request from that input, even though someone is physically present. From the user's viewpoint, the system appears to ignore them. From the controller's internal log, it may appear to be following its rules. The discrepancy is between the road scene and the measurement entering the controller. A diagnosis needs evidence on both sides of that boundary.

The reverse problem is possible in a measurement system too: a request can be reported when the intended demand is absent. A controller responding to such inputs may allocate apparently unnecessary service. These are hypotheses to test, not accusations about a particular detector technology or installation. I would compare independently observed presence with recorded detector events over a defined interval, then examine the conditions associated with mismatches. One anecdote cannot establish the frequency or cause of either error.

For a simple bookkeeping example, suppose one hundred genuine events occur, ninety are detected, and five additional detections have no matching genuine event under a stated matching rule. The total of ninety-five detections does not mean the detector missed only five events. There were ten misses and five unmatched detections. Aggregate totals hide that distinction. The same issue appears in many signal systems: a nearly correct count can coexist with errors in which events were actually recognized.

## Time alignment can change the apparent explanation

Imagine comparing a video with a controller log whose clock is several seconds ahead. An output change may appear to precede its request, or a request may seem to wait longer than it did. The analysis could invent a scheduling fault from a clock mismatch. Before building a causal narrative from several records, establish their time references and uncertainty. Timestamps are measurements too, and their relationship needs evidence rather than assumption.

A useful approach is to identify events visible in more than one record and estimate the alignment, preserving uncertainty where the match is ambiguous. If the offset changes during the observation, a single correction may not be enough. The goal is not to force every event into a tidy sequence. It is to determine which temporal relationships the records can actually support. An unexplained gap in one log should remain a gap until another observation justifies filling it.

The observation interval must also cover the claim. A short clip can show one user's wait, but it may omit the request registration or the preceding service. A longer record can reveal whether the event repeats under similar demand. I would distinguish a documented individual delay from a claim about typical operation. Both may matter, but they require different evidence and should not be made interchangeable merely because the same short video illustrates them.

## Pedestrian service has its own temporal meaning

Pedestrian indications communicate more than one undifferentiated state. The timing manual distinguishes an interval for beginning a crossing from an interval for completing a crossing already begun, followed by other states in the sequence.[3] The details are defined in the applicable current rules. This is another example of meaning depending on context: the same person sees a changing indication while already in a different physical position from someone still waiting to enter.

A countdown, where provided, also refers to a defined interval; it should not be casually interpreted as a universal countdown to any event an observer happens to expect. To evaluate the display, establish what interval it represents and compare it with the intended behavior. A timer can be numerically accurate and still be misunderstood if its purpose is unclear to the user. Good signaling requires a relationship between the displayed quantity and the decision it is meant to support.

Perception and accessibility belong in this investigation, not as an afterthought to electrical operation. A system must address its intended users under the relevant conditions. The official signal standards include provisions for pedestrian and accessible indications.[1] A working lamp is therefore only one component of a broader communication requirement. An engineering account should ask who can detect the signal, distinguish the relevant states, and know which movement or crossing the indication addresses.

## Logs need independent observations of the outcome

Suppose a maintenance record reports that every scheduled output was commanded correctly. That supports a claim about the command sequence. To establish what road users actually saw, an investigator may need output monitoring or an appropriate observation of the display. To establish the resulting movement, another observation is needed again. Each layer supplies evidence about a different part of the chain. Treating them as identical can leave a failure undetected between two apparently healthy subsystems.

The same discipline applies to a successful repair. If a changed configuration appears to reduce waiting, compare comparable demand and observation periods before attributing the improvement to the change. A quiet period after maintenance is not a controlled demonstration that a previously busy intersection has improved. Record the intervention, relevant input conditions, and outcome measures. If several changes occurred together, the report should preserve that fact rather than assigning all benefit to the most visible one.

For a public explanation, I would describe what was observed, what the records establish, and which hypotheses remain. “A request was registered at this time and served later under this sequence” is stronger than “the button is fake.” It is also more useful when a genuine fault exists, because it identifies the boundary that needs further examination. Clear limits on the evidence do not weaken an investigation; they prevent an attractive story from replacing it.

## The same waiting time can conceal different failures

Consider three invented records in which a person presses a button at timestamp ten and sees the intended indication at timestamp fifty. The experienced delay is forty seconds in every case. In the first record, the request is registered immediately and service is selected at fifty. That establishes a wait between registration and service, but it does not by itself establish an error. To assess the wait, we still need the governing sequence, competing demands, and conditions that determine when service can occur.

In the second record, the request is registered at ten and the controller commands the intended output at twenty, while an independent observation still places the visible change at fifty. The discrepancy now lies between the recorded command and observed display, assuming their clocks and event definitions are aligned. That evidence directs attention to a different boundary. Rewriting the scheduler would be a poorly supported first explanation if the output command had already been issued as intended.

In the third record, no request is registered until timestamp forty, despite an independently observed press at ten. Service follows at fifty. The long initial gap raises questions about detection, input processing, or the correspondence between the observed button and the logged request. It does not tell us which of those explanations is correct. The useful next evidence concerns that input path, rather than treating the entire forty-second wait as one undifferentiated controller delay.

These timestamps are arbitrary examples, not acceptable waiting-time limits or proposed signal settings. Their purpose is to show why an investigation needs intermediate observations. A single end-to-end duration measures the user's experience, which matters, but cannot locate the cause. The strongest account retains both: the total delay experienced by the person and the sequence of independently supported events that explains how that delay accumulated. That makes the finding useful to both the user and the people responsible for the system.

## The shared rule is part of the signal path

Traffic lights show why signaling cannot be reduced to energy moving from a source to a receiver. The light carries an indication whose meaning is supplied by a shared rule. Detectors report an imperfect view of demand. A controller selects service under constraints. Road users perceive and act, changing the scene that later observations describe. Each relationship can fail differently, and each requires a different kind of evidence to investigate.

The question about the crossing button now has a more useful form. Did the input register? Was its request retained? When was service permitted and selected? Did the equipment display the intended indication, and could the user understand it? Those questions do not assume that the system worked or that it failed. They turn one frustrating outward experience into a sequence of testable relationships, without pretending that the observer already knows the internal cause.

That method applies well beyond roads. An acknowledgement, an alarm, a call-state message, or a dashboard light also needs a defined meaning and a trustworthy relationship to the process it represents. A signal is useful when the receiver can connect it to the right decision. The traffic light makes that dependence visible every day: the physical indication matters, the shared rule matters, and the evidence about what actually happened matters just as much.

## References and method

1. Federal Highway Administration, [MUTCD, 11th Edition with Revision 1, December 2025](https://mutcd.fhwa.dot.gov/kno_11th_Editionr1.htm); current official edition checked for this article, including Part 4 on traffic-control signals.
2. Federal Highway Administration, [Traffic Signal Timing Manual, Chapter 4](https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter4.htm); control types, phasing, and detection concepts.
3. Federal Highway Administration, [Traffic Signal Timing Manual, Chapter 5](https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter5.htm); basic timing and actuated-operation concepts. This older technical manual is used for concepts, not as the current source of mandatory timing values.

All intersections, detector counts, and queues are constructed. No numerical timing value here is an installation recommendation, and no real crossing button is alleged to be defective. The queue illustration omits geometry, turning movements, pedestrian constraints, stochastic arrivals, and spillback. Sources checked on 3 October 2026.

[Explore the complete Signals Around Us series](/signals.html).
