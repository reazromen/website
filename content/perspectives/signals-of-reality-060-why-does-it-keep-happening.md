---
title: "Why Does It Keep Happening?"
url: /posts/signals-of-reality-060-why-does-it-keep-happening.html
date: '2026-07-25'
read_time: 7
excerpt: Recurrence is often the first clue that an event belongs to a process rather than a one-off accident. The useful question is what variable resets, cycles, or persists between occurrences.
topic: signals-and-signaling
tags:
- repetition
- evidence
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Signal / Noise'
editorial_batch: signals-of-reality-200
---

The first time a service fails at 02:17, it looks like an incident.

The fourth time it fails at almost the same minute, it starts to look like a clock.

That change in perspective is one of the most useful moves in debugging and science. Recurrence turns an event into a candidate process. The interesting question is no longer only *what happened?* It becomes *what state, schedule, dependency, or environmental condition is being recreated each time?*

Repetition is evidence of structure, but it is not yet an explanation.

## Start with the interval

When something keeps happening, measure the spacing before inventing a story.

Is the recurrence every five minutes, every day, every deployment, every temperature transition, every thousand requests, or every time one particular device reconnects?

Different intervals suggest different mechanisms.

A five-minute rhythm points toward schedulers, polling loops, lease expiry, or periodic jobs. A daily rhythm might track sunlight, traffic, backup windows, or human activity. A failure after a fixed number of operations can point toward counters, buffers, resource exhaustion, or accumulated state.

The interval is a signal about the mechanism.

A calendar is sometimes more useful than a stack trace.

## Ask what resets

Recurring failures are often produced by something that returns the system to a similar initial condition.

A cache expires.

A token is refreshed.

A process restarts.

A battery crosses a voltage threshold.

A scheduled workload begins.

A rotating component reaches the same orientation.

A human shift changes.

The event repeats because the causal ingredients are rebuilt.

This is why "it fixed itself" is often a dangerous description. If the symptom disappears when state resets, the underlying mechanism may remain untouched and wait for the same conditions to accumulate again.

Recovery can hide recurrence.

## Correlation with a clock is not enough

Suppose a sensor spike appears at noon every day.

Sunlight is an obvious hypothesis.

But several other variables also change near noon: building temperature, human occupancy, network load, scheduled processes, power use, and perhaps the sensor's own thermal state.

A timestamp narrows the search. It does not identify the cause.

The next step is intervention.

Shade the sensor.

Move it.

Change the schedule.

Compare a nearby reference instrument.

Shift one suspected process by an hour.

A mechanism becomes credible when changing the candidate cause changes the recurrence in a predicted way.

## Recurrence can emerge from thresholds

Not every repeating event is driven by an external clock.

Consider a system that slowly accumulates a resource until a threshold is crossed. A queue grows. Memory fragments. Pressure builds. A capacitor charges. A reservoir fills. When the threshold is reached, the system releases or resets, then the cycle begins again.

The recurrence period may vary because the accumulation rate varies.

This kind of system can look irregular if we examine only event timestamps. Plotting the hidden state reveals the cycle.

The right variable is not always time since midnight.

Sometimes it is time since the last reset.

## Keep one timeline for all layers

A recurring systems failure often spans several clocks and components.

Application logs show an error at 02:17:05.

A database checkpoint begins at 02:16:58.

Disk latency rises at 02:17:01.

A queue crosses its threshold at 02:17:03.

The user reports failure at 02:17:06.

None of those records is the event by itself.

The timeline lets us see ordering.

Accurate clocks and common identifiers matter because causal stories become fragile when timestamps drift. A beautifully repeated pattern can be an artifact if one source is consistently offset.

## Repetition strengthens some claims and weakens others

If a problem occurs after every specific configuration change, explanations unrelated to that change become less plausible.

If the problem happens with and without the configuration, the same explanation weakens.

Repeated observations therefore help by creating comparisons.

But repetition alone never proves causation. A recurring event may share a common cause with another recurring event without being caused by it.

Day follows night every day. Night does not cause clocks to strike midnight.

## The best recurring bug gives you an experiment

A one-off failure is difficult because the evidence may vanish.

A recurring failure is annoying, but scientifically generous.

It gives you another trial.

Before the next occurrence, change one variable. Add one measurement. Preserve one missing log. Move one sensor. Shift one schedule. Capture the raw packet trace. Record the environment.

Then wait.

The recurrence becomes a natural experiment.

"Why does it keep happening?" is therefore more than frustration.

It is a recognition that the system has memory or periodicity.

Once we identify what survives between events, what resets, and what returns, the repetition stops being a mystery and starts becoming a mechanism.
