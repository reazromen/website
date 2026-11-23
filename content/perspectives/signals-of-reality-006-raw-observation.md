---
title: Is There Such a Thing as Raw Observation?
url: /posts/signals-of-reality-006-raw-observation.html
date: '2026-10-07'
read_time: 6
excerpt: A detector records what happened to the detector. Turning that record into evidence about the world requires work we should make visible.
topic: philosophy-science
tags:
- measurement
- interpretation
draft: false
featured: false
language: en
eyebrow: 'Signals of Reality · Reality Is Not What You See'
editorial_batch: signals-of-reality-200
---

A bright pixel is an event in a file. Whether it is also evidence of a star is a further question.

Imagine opening an astronomical exposure before its calibration. Most of the frame is dark. A handful of points stand out. One might be light from a distant object; another might be a detector defect. Both arrive on the screen with the same immediate authority: a number has been recorded, and the display has made it visible.

The tempting instruction is to leave the image alone. Do not interfere. Let the observation speak.

But leaving it alone does not remove the instrument from the picture. It leaves the instrument's contribution mixed into the picture. A refusal to process data can preserve an error just as faithfully as it preserves a signal.

## Before the picture becomes evidence

Hubble's Space Telescope Imaging Spectrograph offers a concrete example. Its documentation describes corrections for electronic bias, dark current and variations in detector response. Bias supplies an electronic offset; dark current contributes charge even without the intended illumination; flat-field calibration addresses differences in sensitivity. These corrections themselves have uncertainties and limitations. Calibration is a measured procedure, not a cosmetic promise of perfection. [STScI's account of calibration error sources](https://hst-docs.stsci.edu/stisdhb/chapter-4-stis-error-sources/4-1-error-sources-associated-with-pipeline-calibration-steps) makes those limitations unusually explicit.

Consider a simplified detector with two pixels receiving equal illumination. Suppose one produces a larger output because it is more sensitive. The uncorrected record accurately preserves two different outputs. It does not accurately represent a difference in the illumination. To answer the astronomical question, the difference introduced by the detector has to be estimated.

The crucial distinction is between fidelity to a recording and fidelity to the thing being investigated. They can come apart.

This is not permission to adjust a result until it looks plausible. In the hypothetical two-pixel case, the correction needs independent support: calibration exposures, tests of stability, an account of conditions under which the response changes. If the only reason for reducing one value is that the scientist dislikes it, the procedure has lost its evidential footing.

Processing becomes trustworthy through constraints. We need to know what operation was performed, why it was justified, and what observations could reveal that it was wrong.

## Three meanings of raw

In an archive, *raw* can name a useful processing stage. It may mean data retained before specified calibration steps or before an investigator's later selections. Such a file lets another team revisit decisions. Rawness here is relative: before this transformation, after those operations in the instrument and acquisition system.

A stronger meaning is psychological: experience before deliberate judgment. A flash can startle someone before they identify its source. It would be excessive to describe every such experience as a consciously reasoned conclusion. Yet the absence of deliberate reasoning does not establish the absence of sensory organization. Nor does it turn the later sentence “there was lightning” into a report without assumptions.

The strongest meaning is philosophical: an observation entirely free of concepts, background commitments and selection, able to settle a dispute without relying on anything beyond itself. That is much harder to defend. Even deciding what counts as the observation already gives it a role in an inquiry.

Philosophers call several different dependencies *theory-ladenness*. An instrument may depend on physical theory; a report may use theoretical vocabulary; a research question may determine what is recorded. These are different claims, and none automatically proves that belief changes everything a person literally sees. The distinctions matter in the debate surveyed by the [Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/science-theory-observation/).

A practical example separates them. Two people can agree that an instrument displayed a particular number while disagreeing about what caused it. They share a report at one level and contest an inference at another. Calling the whole episode “interpretation” conceals the location of the disagreement.

That concealment is costly. If the dispute concerns a calibration coefficient, inspecting the scientist's choice of descriptive words will not resolve it. If the dispute concerns whether the detector was pointed at the right object, a more sophisticated statistical model will not repair the missing identification.

## The danger is dependence without a check

Suppose, in an illustrative investigation, a team looks for a faint pulse predicted by its model. It smooths the record, removes troublesome stretches, and searches only a narrow time window. Each operation might have a good reason. Together, however, they might make almost any record resemble the expected pulse.

The right objection is specific. Which operations were selected after seeing the answer? How often would the same procedure find a pulse in records known to contain none? Does the result survive reasonable alternative settings? Can an independent instrument detect the event?

These questions do more work than demanding an impossible absence of assumptions. They distinguish assumptions that expose a claim to failure from assumptions that protect it from failure.

Independence also needs care. Two analyses are not independent merely because two people ran them. If they inherit the same incorrect timestamp or reference file, agreement can reproduce the same mistake. A useful cross-check changes a relevant route by which error could enter.

This is why an account of the measurement chain is part of the evidence. It tells a critic where to push.

There remains a good reason to preserve early records even when they are not philosophically pure. Later processing can discard information. An average cannot generally be unfolded into its original samples; a thresholded image cannot recover everything below the threshold. Keeping the earlier record preserves possibilities for correction. It does not preserve a view from outside all mediation.

The analogy with keeping an original manuscript is helpful only up to a point. A detector file is not a witness with intentions, and calibration is not literary interpretation. The shared feature is narrower: retaining an earlier version allows later transformations to be examined rather than merely trusted.

The bright pixel is still there at the end of this inquiry. What has changed is the question asked of it. “Was this recorded?” can be answered from the file. “Did light from that object produce it?” requires a connection between the file and the world, supported by tests.

Observation earns authority through that connection. Its value does not depend on having escaped every instrument, concept or choice. It depends on allowing us to discover when those instruments, concepts and choices have led us astray.

## Sources

- [STScI: Error Sources Associated with Pipeline Calibration Steps](https://hst-docs.stsci.edu/stisdhb/chapter-4-stis-error-sources/4-1-error-sources-associated-with-pipeline-calibration-steps), for the specific detector corrections and their limitations.
- [Stanford Encyclopedia of Philosophy: Theory and Observation in Science](https://plato.stanford.edu/entries/science-theory-observation/), for the philosophical distinctions behind theory-ladenness and empirical constraint.
