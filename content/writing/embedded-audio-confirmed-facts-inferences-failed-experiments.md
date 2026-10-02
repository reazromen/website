---
title: How I Separate Confirmed Facts, Inferences and Failed Experiments
url: /posts/embedded-audio-confirmed-facts-inferences-failed-experiments.html
date: '2026-09-15'
read_time: 12
excerpt: Fast-moving firmware work made it easy for an attractive theory to become
  remembered as fact.
topic: embedded-audio-voice
tags:
- esp32-s3
- embedded-audio
- loup
- debugging
- evidence
draft: false
featured: false
language: en
eyebrow: 'Embedded Audio Debugging: Evidence & Failure Models · deep-dive'
outputs:
- url: /posts/embedded-audio-confirmed-facts-inferences-failed-experiments.html
  template: cms/templates/posts/posts--embedded-audio-confirmed-facts-inferences-failed-experiments.tpl
  source: cms/templates/posts/posts--embedded-audio-confirmed-facts-inferences-failed-experiments.json
---

# How I Separate Confirmed Facts, Inferences and Failed Experiments

The useful breakthrough was not another codec setting. It was recognizing that fast-moving firmware work made it easy for an attractive theory to become remembered as fact.

The test platform was the LOUP ESP32-S3 voice device with ES8311 playback, ES7210 capture, SIP/RTP media and a small speakerphone enclosure. The network codec was G.711 A-law/PCMA at nominal 8 kHz with 20 ms / 160-byte RTP payloads, while the physical audio path ran at 16 kHz in the recovered playback design. That mismatch between network time, device time and acoustic time is exactly why a vague word like “crackle” is not a diagnosis.

The evidence that matters for this article is specific: The recovery record explicitly separated confirmed conditions, reasonable inferences, inconclusive experiments and remaining validation gates across logs, source, binaries and PCAPs. I keep those observations tied to the build and test where they were recorded. They are not universal ESP32 performance claims.

The engineering result was also specific: The handoff became reproducible enough for another engineer to review without inheriting undocumented beliefs. This article is about how I got from the symptom to that bounded conclusion, what the data did not prove, and what I would monitor before touching the same path again.

## How I framed this case

The most important design decision here was preserving reversibility. The problem was Fast-moving firmware work made it easy for an attractive theory to become remembered as fact. I kept a known-good control, changed one layer, and required The recovery record explicitly separated confirmed conditions, reasonable inferences, inconclusive experiments and remaining validation gates across logs, source, binaries and PCAPs. to justify keeping the change. The mechanism was A technical conclusion should carry proof status and the evidence that could falsify it. I explicitly avoided Writing a postmortem as a clean story that hides uncertainty and discarded hypotheses.. This let me return to the previous baseline when the experiment regressed audio instead of rationalizing the regression as progress. The retained result was The handoff became reproducible enough for another engineer to review without inheriting undocumented beliefs. The lesson I would carry to another product is Good incident documentation records what was disproved as carefully as what was fixed.

## Evidence engineering for firmware audio

I now keep three identities together for important audio tests: the executable artifact, the source state and the observation bundle. A filename is not identity. A Git branch is not necessarily the binary running on the board. A PCAP without the matching call log can still be useful, but it is weaker evidence for cross-layer timing. The recovery work became much easier after every important experiment could answer “which exact behavior did we run?” before answering “did it sound better?”

This is also why I preserve failed hypotheses. If a warning, queue theory or codec suspicion was tested and did not explain the step change, that negative result belongs beside the final fix. Otherwise the same theory returns in a later chat, branch or handoff and consumes the same debugging time again.

## Case notebook

| Question | Recorded answer |
| --- | --- |
| Symptom | Fast-moving firmware work made it easy for an attractive theory to become remembered as fact. |
| Evidence | The recovery record explicitly separated confirmed conditions, reasonable inferences, inconclusive experiments and remaining validation gates across logs, source, binaries and PCAPs. |
| Mechanism | A technical conclusion should carry proof status and the evidence that could falsify it. |
| Rejected explanation | Writing a postmortem as a clean story that hides uncertainty and discarded hypotheses. |
| Retained result | The handoff became reproducible enough for another engineer to review without inheriting undocumented beliefs. |
| Rule carried forward | Good incident documentation records what was disproved as carefully as what was fixed. |

The rule carried forward is the part I want to survive the specific firmware version. Version numbers change; the debugging invariant should not.

A useful follow-up is to ask what would falsify the retained result. For this case, a repeat run on the same controlled topology should reproduce the relevant observation. If **The recovery record explicitly separated confirmed conditions, reasonable inferences, inconclusive experiments and remaining validation gates across logs, source, binaries and PCAPs.** disappears while the symptom remains, then the old explanation no longer covers the new incident. If the observation returns without the symptom, then it may be contextual rather than causal. That is why I keep mechanism-level counters beside the listening test.

### Instrumentation sketch

```
artifact_id = sha256(app_binary)
source_id   = git_commit + source_archive_hash
observation = {pcap_hash, log_hash, test_topology, monotonic_window}

accept_conclusion only if:
  artifact identity is known
  observation point can see the claimed mechanism
  competing hypothesis predicts different evidence
```

The snippet is not presented as drop-in production code. It documents the measurement model. I want the instrumentation to be cheaper than the deadline it observes, explicit about units, and easy to disable or summarize after the call. The most dangerous diagnostic is one that silently changes scheduler behavior while appearing to measure it.

For **How I Separate Confirmed Facts, Inferences and Failed Experiments**, the next retest would therefore preserve the same topology and change only the variable tied to **A technical conclusion should carry proof status and the evidence that could falsify it.**. I would collect the same observation again, compare it with the known-good control, and only then decide whether a new firmware branch deserves to replace the baseline.

## Change one layer, freeze the others

The practical experiment design was to freeze as much of the call path as possible and change the narrowest variable that could test the hypothesis. That meant preserving the SIP identity and call flow, keeping the codec and I2S configuration stable unless they were the subject of the test, using app-only flashes where appropriate, retaining a rollback binary, and capturing the same small set of counters after each call.

For this topic the controlled variable was the mechanism described above, not the entire audio stack. The surrounding rule was: **Good incident documentation records what was disproved as carefully as what was fixed.** A change that improves one symptom but also changes AEC, queue depth, volume, sample conversion and logging at once produces a better demo perhaps, but a worse experiment.

I also learned to keep the diagnostic path quiet during the actual call. Counters can increment in RAM. Histograms can accumulate. A summary can print after BYE. That pattern is much safer than serializing kilobytes of task state while a 20 ms media deadline is active. The quiet-V115 work made this principle measurable rather than theoretical.

The acceptance test should therefore include both the perceptual outcome and the mechanism-specific evidence. A call that sounds better but increases slow I2S writes is not automatically a win. A PCAP that looks cleaner while echo becomes objectionable is not a win either. The experiment passes only when the intended layer improves without violating the known-good invariants around it.

## How I interpret the numbers

The measurements in this series are deliberately tied to their recorded tests. They describe one board, one firmware revision, one network path and one observation window unless the evidence says otherwise. I do not turn 0.457 ms into a product-wide latency claim, or 175.6 seconds into proof of indefinite stability, or a 20–28 ms network variation into a codec property.

I use distributions and boundaries wherever possible. A maximum speaker write tells me a deadline was missed, while incidence tells me how common the miss was. Packet p50/p95/p99 and maximum gaps reveal whether a path is usually healthy with isolated excursions or continuously unstable. Drift is a slope, not a single latency. AEC-off stability is a control result, not a shipping configuration. A binary hash proves identity, not quality.

For **How I Separate Confirmed Facts, Inferences and Failed Experiments**, the important interpretation is: A technical conclusion should carry proof status and the evidence that could falsify it. The number is useful only because it narrows the fault domain.

When exact current data is not available, I would rather repeat the test than invent a value. The same applies to acoustic latency: without synchronized physical capture, the correct statement is that the network/device measurements bound parts of the delay, not that they measure mouth-to-ear time.

## What this result proves—and what it does not

The result I am willing to claim is narrow: **The handoff became reproducible enough for another engineer to review without inheriting undocumented beliefs.** It is supported by the recorded observation: **The recovery record explicitly separated confirmed conditions, reasonable inferences, inconclusive experiments and remaining validation gates across logs, source, binaries and PCAPs.**

It does not prove that every LOUP board, every network path or every future firmware build behaves the same way. It does not turn a server-side packet capture into an acoustic measurement. It does not turn a stable AEC-off test into permission to remove AEC from a speakerphone. It does not make a hash a quality metric. Those distinctions sound obvious in hindsight and are easy to lose when a demo deadline rewards a simple story.

The useful causal statement is the one consistent with the mechanism: A technical conclusion should carry proof status and the evidence that could falsify it. If another experiment changes that mechanism, I expect the evidence to change too. If the evidence stays the same, I should question the theory before rewriting more code.

I also keep the rejected explanation visible: Writing a postmortem as a clean story that hides uncertainty and discarded hypotheses. That is part of the result. Knowing which layer did *not* create the step change prevents future debugging from starting at the same dead end.

## Reproducing the experiment without changing the experiment

If I had to hand this case to another engineer, I would ask them to preserve the same evidence boundary before attempting a fix:

- freeze the known-good binary and source identity
- capture the exact test topology
- use monotonic timing where wall clocks are unreliable
- hash PCAP/log artifacts before analysis
- record disproved hypotheses beside accepted conclusions

The point is not ceremony. Embedded audio is sensitive to hidden changes. A different softphone setting, a different PBX region, a new enclosure revision, a verbose log level or a queue added “for safety” can all change the result while leaving the test name unchanged.

For **How I Separate Confirmed Facts, Inferences and Failed Experiments**, the pass condition should be written in terms of the mechanism and evidence, not just “sounds good.” The subjective call still matters—it is the product—but the engineering result has to survive comparison.

## The production rule that survived the incident

Good incident documentation records what was disproved as carefully as what was fixed.

I translate that sentence into an operational rule. The metric or artifact that revealed the failure must remain available in future debug builds, but it must not create the same realtime cost. The known-good binary must remain recoverable. A new audio experiment must identify exactly which layer changed. A release candidate must be tested against the same user-visible behaviors that made the earlier baseline valuable.

This keeps debugging cumulative. Instead of starting every audio complaint with “maybe packet loss” or “maybe AEC,” the next investigation begins with a fault tree and a set of already-proven boundaries. The value of the V115/V127/V132A history is not the version numbers themselves; it is the accumulated map of which measurements are trustworthy and which changes have already regressed the product.

## What I would do differently on the next product

I would design the measurement points earlier. The RTP callback, playout clock, queue, I2S boundary, exact AEC reference, capture slots and acoustic test points would all have named interfaces and low-cost counters from the beginning. That would reduce the amount of forensic reconstruction needed after subjective complaints arrive.

I would also separate debug verbosity from realtime instrumentation by architecture, not convention. Realtime code would update fixed counters or ring-buffer events; a lower-priority task would export summaries. If a UART or network logger can block the media task, the design has already allowed the observer into the deadline path.

For multi-device validation I would automate the call matrix and preserve a compact evidence bundle per run: firmware identity, hardware revision, test endpoint, RTP summary, device timing summary and subjective/acoustic result. The point is not to collect everything. It is to make two runs comparable.

Most importantly, I would preserve the same failure-model discipline. A technical conclusion should carry proof status and the evidence that could falsify it. That principle remains true whether the next product uses ESP32-S3, a Linux SoC, a different codec or a cloud media service.

## The result I keep from this incident

The handoff became reproducible enough for another engineer to review without inheriting undocumented beliefs.

The deeper value is the method. I started with a perceptual symptom, located the earliest layer that could create it, chose evidence that could see that layer, changed one variable, and checked the known-good invariants afterward. The process is slower than random tuning for the first build and dramatically faster by the tenth.

The short version of the lesson is: **Good incident documentation records what was disproved as carefully as what was fixed.**

That is the standard I now use for embedded audio work. A fix is not convincing because the call sounds better once. It is convincing when the mechanism, measurement, artifact identity and regression behavior all agree about why it got better.
