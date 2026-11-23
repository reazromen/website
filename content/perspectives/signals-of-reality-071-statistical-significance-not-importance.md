---
title: Statistical Significance Is Not Importance
url: /posts/signals-of-reality-071-statistical-significance-not-importance.html
date: '2026-08-12'
read_time: 7
excerpt: Statistical significance does not tell us whether an effect is large, useful, consequential, or causally understood.
topic: philosophy-science
tags:
- uncertainty
- evidence
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · How Do We Know?'
editorial_batch: signals-of-reality-200
---

A dataset contains ten million observations. Two groups differ by 0.02%. A conventional statistical test reports strong evidence against a simple no-difference model.

Should anyone care?

Maybe. The test has not answered that question.

Statistical significance and practical importance live at different layers.

## Large samples detect small differences

As sample size grows, estimates can become more precise. That is usually good. It also means very small departures from a reference model can become statistically detectable.

A tiny effect can be estimated with high confidence when the dataset is large enough.

The test result does not tell us the size of the effect. That requires an effect estimate and its uncertainty.

This is one reason the American Statistical Association has argued against reducing conclusions to whether one significance threshold is crossed.

## Effect size answers another question

Suppose a software optimization reduces median latency from 100.00 milliseconds to 99.98 milliseconds. With enough requests, that difference may be estimated very precisely.

If users cannot perceive it, cost does not change, tail latency remains the same, and no capacity benefit appears, the improvement may be operationally irrelevant.

Now imagine a change that substantially reduces rare multi-second stalls while barely moving the median.

That effect may matter enormously even if the average change looks small.

Importance depends on the decision.

## A threshold can manufacture drama

Two results that sit just on opposite sides of a conventional cutoff are usually not members of different scientific universes.

A small change in sample, model, or preprocessing can move a result across the line without meaningfully changing the evidence.

Confidence intervals and effect estimates often tell a richer story. They show which magnitudes remain compatible with the observations.

## Precision is not mechanism

Even a large and precisely estimated difference does not identify why the difference exists.

Confounding, measurement bias, selection, and reverse causation remain possible in observational data.

A statistical test cannot convert association into causation.

The mechanism needs design and evidence of its own.

This is another recurring theme: a statistic can be correct for the question it computes and still be used to support a larger claim it never tested.

## Importance can be defined before analysis

Good experiments often define a practically meaningful effect in advance.

How much latency reduction would justify deployment?

How much measurement drift would break a requirement?

How large a change would alter a scientific model?

This creates a scale for interpreting results.

An analysis can then distinguish among a large meaningful effect, a small but precisely measured effect, an inconclusive estimate, and evidence that meaningful effects are unlikely.

Those categories are more useful than significant versus not significant.

## Statistical significance still has a role

The problem is not that hypothesis tests are useless.

They are useful tools when the question and assumptions fit.

A test can help quantify how compatible data are with a reference model. It can be one component of an analysis.

The error comes from turning one output into a universal quality score.

A conventional significance result does not certify experimental design, replication, truth, or importance.

## Ask the question the decision actually needs

When someone says a result is significant, ask how large it is, how uncertain the estimate is, what would count as important in the domain, what alternative explanations remain, whether the effect reproduces, and whether a decision would change because of it.

The answers can transform an impressive statistical result into a trivial one.

They can also reveal that a modest-looking number has major consequences.

Statistical significance is a property of an analysis.

Importance belongs to the world in which the result will be used.
