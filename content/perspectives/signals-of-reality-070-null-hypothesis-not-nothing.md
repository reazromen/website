---
title: "The Null Hypothesis Is Not “Nothing Happened”"
url: /posts/signals-of-reality-070-null-hypothesis-not-nothing.html
date: '2026-06-02'
read_time: 7
excerpt: A null hypothesis is a statistical model used as a reference for a test. Failing to reject it does not prove that no effect, mechanism, or difference exists.
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

A statistical test returns a large p-value.

Someone writes:

> Nothing happened.

That conclusion may be much stronger than the test.

The null hypothesis is not the metaphysical proposition that the universe contains no effect. It is a specified statistical model used as a reference.

What the test tells us depends on that model, the test statistic, the design, the sample size, and the assumptions.

## A null is a model

A simple experiment may define a null hypothesis such as:

the mean difference between two conditions is zero.

Another study may define a null model of equal event rates.

Another may test whether observed data are compatible with a particular distribution.

These are mathematical statements.

They are not identical to "the phenomenon does not exist."

An effect can be real but smaller than the experiment can resolve.

The chosen statistic can be insensitive to the way the effect appears.

Assumptions can be violated.

A null result therefore has to be interpreted with the design.

## Failure to reject is not acceptance

Classical hypothesis testing is asymmetric.

A small p-value can indicate that the observed data would be surprising under the null model, subject to assumptions.

A large p-value usually means the data did not provide strong evidence against that model.

It does not automatically prove the null.

This distinction is central to responsible statistical interpretation. The American Statistical Association has repeatedly emphasized that p-values do not measure the probability that a hypothesis is true and should not be treated as a substitute for scientific reasoning. See the ASA's [task-force statement on statistical significance](https://magazine.amstat.org/blog/2021/08/01/task-force-statement-p-value/).

## Power matters

Imagine trying to detect a one-millimeter change with a ruler marked only in centimeters.

The experiment may repeatedly fail to find a difference.

That does not show the change is zero.

It shows the method lacks resolving power for that scale.

Statistical power formalizes a related idea: given a particular effect size and design, how likely is the test to detect it?

Small samples, high variability, or insensitive measurements can produce inconclusive results even when an effect exists.

A null result without a power or precision discussion is hard to interpret.

## Equivalence needs a different question

Sometimes we genuinely want evidence that two conditions are sufficiently similar.

That requires defining what difference would be practically important.

Equivalence tests and confidence-interval approaches can address this more directly than simply failing to reject a zero-difference null.

"Not detectably different" and "similar within an agreed margin" are different claims.

The second is often what engineering actually needs.

## Statistical and physical nulls can diverge

Suppose a sensor comparison shows no statistically detectable mean offset.

One instrument may still have a frequency-dependent bias.

The mean can be zero while errors vary systematically across the range.

A test answers the question encoded in its statistic.

If the statistic is incomplete, the null can be passed while the system remains wrong in another dimension.

This is why residual plots, calibration curves, and domain knowledge matter alongside formal tests.

## A null result can still be valuable

When a well-powered experiment fails to detect a predicted effect, a theory can lose support.

When an intervention expected to produce a large change produces a tightly estimated near-zero difference, the result can eliminate practical options.

Negative evidence is real evidence when the experiment had a fair chance to observe the predicted consequence.

The important question is not whether the p-value crossed one threshold.

It is what range of effects remains compatible with the data.

## Replace the slogan with a quantitative statement

Instead of:

> Nothing happened.

write:

> Under this measurement and model, we did not detect the predicted difference; the estimated effect and its uncertainty rule out changes larger than this range but remain compatible with smaller effects.

That statement is longer.

It is also much more informative.

The null hypothesis is a reference model.

Statistics tell us how observations relate to that model.

Reality is allowed to be subtler than reject or fail to reject.
