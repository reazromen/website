---
title: When a Model Becomes the World
url: /posts/signals-of-reality-005-model-becomes-world.html
date: '2026-09-01'
read_time: 7
excerpt: A model becomes dangerous not when it simplifies reality, but when decisions begin treating its categories as reality's own boundaries.
topic: philosophy-science
tags:
- models
- interpretation
- measurement
draft: false
featured: false
language: en
eyebrow: 'Signals of Reality · Reality Is Not What You See'
editorial_batch: signals-of-reality-200
---

A weather map can be wrong without anyone confusing it with the sky. A more interesting failure begins when the map stops feeling like a representation at all. The colors become the weather; the risk score becomes the patient; the dashboard becomes the service; the ranking becomes the quality of the thing being ranked.

Models are indispensable precisely because the world contains too much detail. A model selects variables, relationships and scales that make a question tractable. The difficulty is that successful models acquire authority. Once a number enters a workflow, people reorganize around it. The model no longer merely describes the territory. It starts changing the route through it.

Consider a deliberately simple operational example. A support team defines "healthy" as an API returning HTTP 200 within 500 milliseconds. That is a useful test. It is reproducible, cheap and easy to graph. After several months, management begins using the percentage of successful probes as the service's main reliability measure. Engineers optimize the endpoint. The health check remains fast even when a downstream workflow is failing.

Nothing mystical happened. The measurement stayed accurate at the narrow task it was designed to perform. What changed was the claim attached to it.

This is one reason models need a stated purpose. A heart-rate monitor, a climate model and a fraud classifier are not incomplete in the same way. Each is built to preserve some relationships and ignore others. The Stanford Encyclopedia of Philosophy's survey of scientific models emphasizes that models can represent through idealization, abstraction and other devices without being literal copies of their targets. The useful question is therefore not whether a model contains simplifications. It must. The useful question is whether those simplifications remain appropriate for the inference being made.

## The category starts acting back

Some models are passive enough that their categories do not affect the thing classified. The orbit of Mars does not change because an astronomer chooses a different plotting style. Human systems are different. A score can become a target, a gate or an incentive.

Imagine a warehouse that evaluates teams by the number of packages closed per hour. At first, the metric may correlate with useful throughput. Once bonuses depend on it, workers have a reason to favor easy packages, delay complicated cases, or redefine when a package counts as "closed." The metric did not reveal a hidden moral defect. It altered the environment in which behavior occurs.

This family of problems is often discussed through Goodhart's law: when a measure becomes a target, it can cease to be a good measure. The slogan is memorable, but the mechanism matters more. The causal pathway usually involves incentives, selection and adaptation. A metric is not corrupted by magic. People and systems respond to what is rewarded.

A related danger appears in automated classification. In a widely discussed 2019 study in Science, Ziad Obermeyer and colleagues examined a commercial health-management algorithm that used health-care spending as a proxy for health need. Because spending and need were not equivalent across racial groups in the data, the proxy produced systematic disparities in who was identified for extra care. The lesson is not that algorithms are uniquely incapable of representing people. It is that a proxy can be statistically convenient while failing to preserve the property the decision actually concerns.

That distinction generalizes far beyond machine learning:

measured variable → model output → institutional decision

At each arrow, a new claim is being made.

A temperature reading may support a statement about one sensor at one location. A model may combine many readings into an estimate of regional conditions. A policy may then use that estimate to trigger an action. The final decision is not simply "the data speaking." It includes choices about thresholds, costs and acceptable uncertainty.

## Reality does not inherit the schema

Engineers know this problem in databases. A schema may contain an active=true flag because a product needs a binary state. Real users, however, can be suspended, partially provisioned, awaiting verification, active in one subsystem and stale in another. If every component eventually treats active as the complete ontology of an account, the convenience of the original schema becomes a source of bugs.

The same mistake appears in scientific language when a useful operational definition is mistaken for a complete definition of the phenomenon. Intelligence is not identical to one test score. Economic welfare is not identical to GDP. A biological species concept that works well for many sexually reproducing organisms does not automatically settle every case in microbiology or paleontology.

None of this means categories are arbitrary. Some classifications survive repeated tests because they capture stable structure. The periodic table is not merely a cultural arrangement of boxes. Its success is tied to physical regularities that support prediction and explanation. The caution is narrower: the boxes are still part of a representational system, and the system has a scope.

This is where lazy relativism gets the problem backwards. If models are constructed, it does not follow that any model is as good as any other. Models can be compared by prediction, explanatory power, calibration, robustness, simplicity, domain of validity and many other criteria. A bridge model that predicts loads correctly is better for that task than a horoscope. A clinical test with validated sensitivity and specificity is not epistemically equivalent to a guess.

The fact that we use maps does not erase the territory. It gives us a reason to test our maps against it.

## The recovery move

When a model feels too much like the world, one question is unusually effective:

**What observation could force us to redraw this model?**

If the answer is "nothing," the object may no longer be functioning as an empirical model. It has become a vocabulary protected from revision.

For a production dashboard, the challenge might be an end-to-end synthetic transaction. For a medical risk model, it may be outcomes measured independently of the proxy used for prediction. For an astronomical model, it can be a new observation whose distribution differs from what the model predicts.

A second question is equally useful: **Who or what falls outside the categories?** Every schema has edge cases. Seeing them does not automatically destroy the schema; sometimes it clarifies its range.

Models let finite minds and finite machines work with a world that contains more detail than either can hold. Their power comes from leaving things out while preserving enough structure to reason.

The danger begins when the omitted structure becomes invisible.

At that point we are no longer saying, "according to this model." We are saying, "this is what the world is."

And reality has never signed that contract.

### Sources

- Stanford Encyclopedia of Philosophy, [Models in Science](https://plato.stanford.edu/entries/models-science/).
- Ziad Obermeyer et al., [Dissecting racial bias in an algorithm used to manage the health of populations](https://www.science.org/doi/10.1126/science.aax2342), Science (2019).
- NIST, [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework).