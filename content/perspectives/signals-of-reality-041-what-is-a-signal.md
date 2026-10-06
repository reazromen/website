---
title: What Is a Signal?
url: /posts/signals-of-reality-041-what-is-a-signal.html
date: '2026-07-31'
read_time: 6
excerpt: A signal is not a special kind of substance. It is a physical variation treated as carrying information for a receiver, model, or measurement task.
topic: signals-and-signaling
tags:
- signals-and-signaling
- information
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Signal / Noise'
editorial_batch: signals-of-reality-200
---

A voltage changes on a wire. A pressure wave crosses a room. A pulse of light arrives at a detector. A hormone concentration rises in blood. A sequence of packets appears on a network interface.

All of these can be signals.

The word sounds as if it names a particular physical ingredient, like copper or oxygen. It does not. A signal is better understood as a role played by physical variation inside a system of observation or communication.

The same voltage can be a signal in one circuit and irrelevant fluctuation in another. The same radio emission can be a target for an astronomer and interference for a communications engineer. The same packet timing can be metadata to one analyst and meaningless background to another.

So what makes something a signal?

## Variation plus a relation

At minimum, a signal has to vary in a way that can be related to something else.

A microphone voltage varies with air pressure at its diaphragm. A thermometer output varies with a property of the sensing element that is related, after calibration and thermal assumptions, to temperature. A digital message varies across symbols selected from an alphabet.

The relation does not have to be perfect. Real sensors have noise, distortion, saturation, delay, and uncertainty. A signal can still be useful if its variations preserve enough structure for a task.

This is why calibration matters. Without a model relating output to input, a number may be only a number. Once that relation is characterized, the same number becomes evidence about a quantity.

## A signal does not require human meaning

Claude Shannon's 1948 paper, [A Mathematical Theory of Communication](https://onlinelibrary.wiley.com/doi/10.1002/j.1538-7305.1948.tb01338.x), made a decisive separation between the engineering problem of transmitting selected messages and the semantic question of what those messages mean.

That separation is easy to underestimate.

A communication channel can be analyzed in terms of possible symbols, probabilities, rates, errors, and noise without knowing whether the message is poetry, telemetry, speech, or random test data. The receiver may reconstruct a sequence perfectly while understanding nothing about its human significance.

This does not make meaning unimportant. It means meaning is not required for every useful theory of signals.

## The receiver helps define the signal

Imagine a room containing Wi-Fi, visible light, sound, and infrared radiation. A human ear responds to only part of the acoustic variation. A Wi-Fi receiver is designed for a radio band. A camera responds to light according to its sensor and filters.

The room is not divided into signal and non-signal by nature in advance.

A receiver creates selectivity.

That selectivity can be physical, as with a band-pass filter, or conceptual, as when an analyst decides that only events associated with one user session are relevant. In both cases, the signal is partly defined by a question.

This does not make it arbitrary. A receiver cannot extract information that leaves no usable physical trace. Selectivity chooses among available structure; it does not invent structure without constraint.

## Signals can be continuous or discrete

Some signals are modeled as continuous functions of time: microphone voltage, pressure, temperature, field strength. Others are treated as sequences of symbols: bits, packets, nucleotide bases, event records.

The distinction often belongs to the model as much as to the underlying physics.

A digital bit is implemented by continuous physical states. A sampled audio file is a sequence of numbers produced from a continuously varying pressure field through a measurement process. A spike train in neuroscience can be represented as discrete events even though membrane voltage evolves continuously.

This is why saying reality is digital or analog based on one representation is usually too fast. We choose a representation suitable for a scale and task.

## A signal is evidence, not the thing itself

Suppose a river gauge reports rising water level. The time series is a signal about the river. It is not the river.

The distinction becomes important when the gauge malfunctions, when debris affects the sensor, or when the relationship between local level and downstream flooding changes. The signal can remain numerically precise while ceasing to represent the quantity we care about.

The same problem appears everywhere: heart-rate monitors, radar, SIP signaling, satellite imagery, financial data, and environmental sensors.

A signal always comes with a chain:

physical process → interaction → detector or channel → representation → interpretation.

Each arrow can fail differently.

## Why this definition matters

People often say "the signal is clear" when they mean the evidence strongly supports one interpretation. That may be correct, but it compresses several questions.

Is the physical variation reliably detected? Is it distinguished from background variation? Does the mapping from signal to cause hold under these conditions? Could another process produce the same pattern? Is the receiver calibrated? Is the interpretation supported by independent evidence?

These questions do not weaken the idea of a signal. They make it operational.

A signal is not reality speaking in a language already prepared for us.

It is a pattern in a physical or symbolic channel that a system can use to distinguish among possibilities.

Once that distinction exists, communication, measurement, control, perception, and inference can begin.
