---
title: Accuracy Is Not Completeness
url: /posts/signals-of-reality-013-accuracy-not-completeness.html
date: '2026-05-13'
read_time: 6
excerpt: A statement can be exactly correct and still leave out the fact that changes the decision.
topic: philosophy-science
tags:
- measurement
- interpretation
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Reality Is Not What You See'
editorial_batch: signals-of-reality-200
---

At 09:42 a monitoring system reports: **CPU utilization: 18 percent**.

Assume the number is correct. The counters were read properly, the interval is known, the calculation is sound.

At the same moment, customers cannot complete checkout because a dependency is timing out.

The CPU reading is not false. It is simply not the answer to the question everyone suddenly cares about.

That difference—between **accuracy** and **completeness**—is easy to state and surprisingly easy to forget.

A representation can be accurate about every fact it contains while omitting other relevant facts. A street map may place every road correctly and omit elevation. A blood test can accurately measure one biomarker without diagnosing the cause of a symptom. A photograph can faithfully record what fell inside its frame while excluding what stood half a metre to the left.

There is no contradiction. Accuracy asks whether the represented claims match their targets. Completeness asks what relevant parts of the target are represented at all.

## The missing dimension

Imagine two routes from a village to a hospital. A map says route A is 18 kilometres and route B is 22. Surveying confirms both numbers.

If distance is the only variable, A looks preferable.

Now add elevation and road condition. Route A crosses a flooded section and a steep damaged bridge. Route B is longer but passable.

Nothing happened to the original distances. They remained accurate. The decision changed because the first representation did not contain enough dimensions for the task.

This is a recurring pattern in data work. We collect what is cheap to collect, then gradually forget the difference between "available" and "important."

A dashboard may have hundreds of correct measurements and still be incomplete for a new incident. The missing signal could be queue age, DNS resolution time, audio quality, device firmware version or something nobody instrumented because the failure had not previously occurred.

Observability is not the fantasy of measuring everything. Measuring everything would create its own storage, cost and interpretation problems. The practical goal is to retain enough evidence—and enough flexibility—to answer important questions as they arise.

## Completeness is relative to a question

There is no useful representation that is complete in an absolute sense.

A photograph of a leaf does not contain its genome. A genome sequence does not contain the temperature in which the leaf grew. A temperature log does not tell you which insect bit it yesterday.

Demanding total completeness would make every representation fail.

So completeness has to be indexed to purpose.

A topographic map can be sufficiently complete for planning a hike while being useless for locating underground water pipes. A clinical trial can answer a narrowly defined question about an intervention under specified conditions while leaving unanswered how the intervention performs in a population the trial did not study.

This is why good scientific papers spend so much space specifying populations, methods and limitations. Those details define the region over which the evidence can travel.

The same discipline helps outside science. When someone says, "The data show X," a useful follow-up is: **which data, collected from what, and what relevant variable could be absent?**

That question does not invalidate the evidence. It locates it.

## Precision can camouflage omission

Incomplete representations become especially persuasive when the included measurements are very precise.

Suppose a device reports indoor air temperature as 29.37 °C. The two decimal places can feel authoritative. Yet if the sensor is mounted beside a warm power supply, the measurement may be precise about the sensor's local environment and poor as a representation of the room.

Precision concerns repeatability or numerical resolution; accuracy concerns closeness to the relevant target; completeness concerns whether the representation contains the dimensions required for the inference. These concepts interact, but they are not synonyms.

A table can therefore be precise but inaccurate, accurate but incomplete, or complete enough for one task and inadequate for another.

The labels are useful only after the target and purpose are specified.

## The frame is part of the evidence

Journalism and photography make the issue visible.

A photograph may be authentic—no pixels fabricated—and still give a misleading account if the crop removes crucial context. The remedy is not to declare photographs untrustworthy. It is to treat framing as part of how evidence is produced.

Scientific visualization faces the same responsibility. A graph can use accurate points and still hide structure through an inappropriate axis range, aggregation window or omitted subgroup. Sometimes the choice is innocent and necessary. Every graph must choose a scale. The ethical and technical question is whether the choice materially changes what a reasonable reader would infer.

A useful practice is to ask what disappears during each transformation:

**world → measurement → dataset → summary → chart → decision**

At each step information is discarded.

Some loss is intentional compression. Some is accidental. Some is the result of limits in instruments or sampling. The chain becomes trustworthy when those losses are understood well enough that the final claim does not require information that vanished upstream.

## The counterweight: more is not automatically better

Once omission is recognized, the instinct can swing too far: collect every possible variable.

That does not guarantee understanding.

Adding irrelevant variables can increase noise, complicate models, raise privacy costs and make causal reasoning harder. In machine learning, more features can improve a model in one setting and make it overfit in another. In operations, more dashboards can bury a failure under thousands of panels.

The opposite of incompleteness is not maximal collection. It is **sufficiency for the question, with known limits**.

That is why the 18 percent CPU reading from the opening still matters. It helps eliminate one class of hypotheses. It tells us something about the system. The mistake would be turning that true observation into the much larger sentence: "The system is healthy."

An accurate representation earns the right to support the claims it actually measures.

It does not inherit every claim we wish it could answer.

### Sources

- Stanford Encyclopedia of Philosophy, [Measurement in Science](https://plato.stanford.edu/entries/measurement-science/).
- NIST, [Uncertainty of Measurement](https://www.nist.gov/pml/nist-technical-note-1297).
- OpenTelemetry, [Observability Primer](https://opentelemetry.io/docs/concepts/observability-primer/).
