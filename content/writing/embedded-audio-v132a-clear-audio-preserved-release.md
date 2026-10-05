---
title: 'V132A: Turning Clear Audio into a Preserved Release Asset'
url: /posts/embedded-audio-v132a-clear-audio-preserved-release.html
date: '2020-06-01'
read_time: 12
excerpt: A working phone is not a release unless the exact artifact and source context
  can survive the next experiment.
topic: embedded-audio-voice
tags:
- esp32-s3
- embedded-audio
- loup
- acoustics
- release-engineering
draft: false
featured: false
language: en
eyebrow: 'Embedded Audio Debugging: Acoustics, Release & Production · deep-dive'
outputs:
- url: /posts/embedded-audio-v132a-clear-audio-preserved-release.html
  template: cms/templates/posts/posts--embedded-audio-v132a-clear-audio-preserved-release.tpl
  source: cms/templates/posts/posts--embedded-audio-v132a-clear-audio-preserved-release.json
---

# V132A: Turning Clear Audio into a Preserved Release Asset

One of the easiest ways to lose days in embedded voice work is to collapse several layers into one symptom. In this case, a working phone is not a release unless the exact artifact and source context can survive the next experiment.

The test platform was the LOUP ESP32-S3 voice device with ES8311 playback, ES7210 capture, SIP/RTP media and a small speakerphone enclosure. The network codec was G.711 A-law/PCMA at nominal 8 kHz with 20 ms / 160-byte RTP payloads, while the physical audio path ran at 16 kHz in the recovered playback design. That mismatch between network time, device time and acoustic time is exactly why a vague word like “crackle” is not a diagnosis.

The evidence that matters for this article is specific: The V132A handoff preserved a phone-read ESP32-S3 app image, app-only flash offset 0x20000, exact binary identity, source overlay/archive and private Git release tag; it was known to make clear two-way calls. I keep those observations tied to the build and test where they were recorded. They are not universal ESP32 performance claims.

The engineering result was also specific: V132A became an immutable rollback/reference while new source work continued elsewhere. This article is about how I got from the symptom to that bounded conclusion, what the data did not prove, and what I would monitor before touching the same path again.

## How I framed this case

The debugging value here came from using two independent views of the same event. One view described the user-visible failure—A working phone is not a release unless the exact artifact and source context can survive the next experiment. The other described the machine state—The V132A handoff preserved a phone-read ESP32-S3 app image, app-only flash offset 0x20000, exact binary identity, source overlay/archive and private Git release tag; it was known to make clear two-way calls. Because Release engineering for embedded audio must preserve executable behavior, build provenance and rollback separately from feature development., agreement between those views was meaningful and disagreement was informative. I specifically resisted Rebuilding over the only known-good binary or merging power-button work into the audio baseline before regression testing.. If the second observation did not support the first hypothesis, I moved the fault boundary instead of adding another patch. The result was V132A became an immutable rollback/reference while new source work continued elsewhere. and the general engineering rule became The best audio result is fragile until it becomes a reproducible, hash-identified release asset.

## Product audio ends at the ear, not at I2S

Once the digital path is stable, the mechanical product becomes the next experiment. Speaker driver, enclosure volume, vents, sealing, amplifier behavior, microphone placement and user volume all alter what reaches the room and what returns to the microphone. AEC is part of that physical loop even though its code is digital.

Release engineering belongs here too. The acoustic result is only useful if I can identify and restore the firmware that produced it. The V132A handoff treated the working binary as an immutable rollback reference while source cleanup and unrelated power work continued elsewhere. That is how a good call becomes an engineering baseline rather than a memory.

## Case notebook

| Question | Recorded answer |
| --- | --- |
| Symptom | A working phone is not a release unless the exact artifact and source context can survive the next experiment. |
| Evidence | The V132A handoff preserved a phone-read ESP32-S3 app image, app-only flash offset 0x20000, exact binary identity, source overlay/archive and private Git release tag; it was known to make clear two-way calls. |
| Mechanism | Release engineering for embedded audio must preserve executable behavior, build provenance and rollback separately from feature development. |
| Rejected explanation | Rebuilding over the only known-good binary or merging power-button work into the audio baseline before regression testing. |
| Retained result | V132A became an immutable rollback/reference while new source work continued elsewhere. |
| Rule carried forward | The best audio result is fragile until it becomes a reproducible, hash-identified release asset. |

This matrix is what I would hand to another engineer before giving them the source tree. It makes the next test start from evidence instead of folklore.

A useful follow-up is to ask what would falsify the retained result. For this case, a repeat run on the same controlled topology should reproduce the relevant observation. If **The V132A handoff preserved a phone-read ESP32-S3 app image, app-only flash offset 0x20000, exact binary identity, source overlay/archive and private Git release tag; it was known to make clear two-way calls.** disappears while the symptom remains, then the old explanation no longer covers the new incident. If the observation returns without the symptom, then it may be contextual rather than causal. That is why I keep mechanism-level counters beside the listening test.

### Instrumentation sketch

```
release evidence bundle:
  board revision
  firmware artifact hash
  source commit/archive identity
  app-only flash offset
  call topology
  timing summary
  full-duplex / mute / volume result
  acoustic observation
  rollback artifact

"sounds good" is one field, not the bundle
```

The snippet is not presented as drop-in production code. It documents the measurement model. I want the instrumentation to be cheaper than the deadline it observes, explicit about units, and easy to disable or summarize after the call. The most dangerous diagnostic is one that silently changes scheduler behavior while appearing to measure it.

For **V132A: Turning Clear Audio into a Preserved Release Asset**, the next retest would therefore preserve the same topology and change only the variable tied to **Release engineering for embedded audio must preserve executable behavior, build provenance and rollback separately from feature development.**. I would collect the same observation again, compare it with the known-good control, and only then decide whether a new firmware branch deserves to replace the baseline.

## How I interpret the numbers

The measurements in this series are deliberately tied to their recorded tests. They describe one board, one firmware revision, one network path and one observation window unless the evidence says otherwise. I do not turn 0.457 ms into a product-wide latency claim, or 175.6 seconds into proof of indefinite stability, or a 20–28 ms network variation into a codec property.

I use distributions and boundaries wherever possible. A maximum speaker write tells me a deadline was missed, while incidence tells me how common the miss was. Packet p50/p95/p99 and maximum gaps reveal whether a path is usually healthy with isolated excursions or continuously unstable. Drift is a slope, not a single latency. AEC-off stability is a control result, not a shipping configuration. A binary hash proves identity, not quality.

For **V132A: Turning Clear Audio into a Preserved Release Asset**, the important interpretation is: Release engineering for embedded audio must preserve executable behavior, build provenance and rollback separately from feature development. The number is useful only because it narrows the fault domain.

When exact current data is not available, I would rather repeat the test than invent a value. The same applies to acoustic latency: without synchronized physical capture, the correct statement is that the network/device measurements bound parts of the delay, not that they measure mouth-to-ear time.

## Change one layer, freeze the others

The practical experiment design was to freeze as much of the call path as possible and change the narrowest variable that could test the hypothesis. That meant preserving the SIP identity and call flow, keeping the codec and I2S configuration stable unless they were the subject of the test, using app-only flashes where appropriate, retaining a rollback binary, and capturing the same small set of counters after each call.

For this topic the controlled variable was the mechanism described above, not the entire audio stack. The surrounding rule was: **The best audio result is fragile until it becomes a reproducible, hash-identified release asset.** A change that improves one symptom but also changes AEC, queue depth, volume, sample conversion and logging at once produces a better demo perhaps, but a worse experiment.

I also learned to keep the diagnostic path quiet during the actual call. Counters can increment in RAM. Histograms can accumulate. A summary can print after BYE. That pattern is much safer than serializing kilobytes of task state while a 20 ms media deadline is active. The quiet-V115 work made this principle measurable rather than theoretical.

The acceptance test should therefore include both the perceptual outcome and the mechanism-specific evidence. A call that sounds better but increases slow I2S writes is not automatically a win. A PCAP that looks cleaner while echo becomes objectionable is not a win either. The experiment passes only when the intended layer improves without violating the known-good invariants around it.

## What this result proves—and what it does not

The result I am willing to claim is narrow: **V132A became an immutable rollback/reference while new source work continued elsewhere.** It is supported by the recorded observation: **The V132A handoff preserved a phone-read ESP32-S3 app image, app-only flash offset 0x20000, exact binary identity, source overlay/archive and private Git release tag; it was known to make clear two-way calls.**

It does not prove that every LOUP board, every network path or every future firmware build behaves the same way. It does not turn a server-side packet capture into an acoustic measurement. It does not turn a stable AEC-off test into permission to remove AEC from a speakerphone. It does not make a hash a quality metric. Those distinctions sound obvious in hindsight and are easy to lose when a demo deadline rewards a simple story.

The useful causal statement is the one consistent with the mechanism: Release engineering for embedded audio must preserve executable behavior, build provenance and rollback separately from feature development. If another experiment changes that mechanism, I expect the evidence to change too. If the evidence stays the same, I should question the theory before rewriting more code.

I also keep the rejected explanation visible: Rebuilding over the only known-good binary or merging power-button work into the audio baseline before regression testing. That is part of the result. Knowing which layer did *not* create the step change prevents future debugging from starting at the same dead end.

## Reproducing the experiment without changing the experiment

If I had to hand this case to another engineer, I would ask them to preserve the same evidence boundary before attempting a fix:

- preserve the rollback binary before unrelated feature work
- repeat calls at controlled speaker levels
- separate digital timing evidence from acoustic observations
- record hardware/enclosure revision with every audio result
- require rollback, mute, full-duplex and call-origin gates before final sign-off

The point is not ceremony. Embedded audio is sensitive to hidden changes. A different softphone setting, a different PBX region, a new enclosure revision, a verbose log level or a queue added “for safety” can all change the result while leaving the test name unchanged.

For **V132A: Turning Clear Audio into a Preserved Release Asset**, the pass condition should be written in terms of the mechanism and evidence, not just “sounds good.” The subjective call still matters—it is the product—but the engineering result has to survive comparison.

## The production rule that survived the incident

The best audio result is fragile until it becomes a reproducible, hash-identified release asset.

I translate that sentence into an operational rule. The metric or artifact that revealed the failure must remain available in future debug builds, but it must not create the same realtime cost. The known-good binary must remain recoverable. A new audio experiment must identify exactly which layer changed. A release candidate must be tested against the same user-visible behaviors that made the earlier baseline valuable.

This keeps debugging cumulative. Instead of starting every audio complaint with “maybe packet loss” or “maybe AEC,” the next investigation begins with a fault tree and a set of already-proven boundaries. The value of the V115/V127/V132A history is not the version numbers themselves; it is the accumulated map of which measurements are trustworthy and which changes have already regressed the product.

## What I would do differently on the next product

I would design the measurement points earlier. The RTP callback, playout clock, queue, I2S boundary, exact AEC reference, capture slots and acoustic test points would all have named interfaces and low-cost counters from the beginning. That would reduce the amount of forensic reconstruction needed after subjective complaints arrive.

I would also separate debug verbosity from realtime instrumentation by architecture, not convention. Realtime code would update fixed counters or ring-buffer events; a lower-priority task would export summaries. If a UART or network logger can block the media task, the design has already allowed the observer into the deadline path.

For multi-device validation I would automate the call matrix and preserve a compact evidence bundle per run: firmware identity, hardware revision, test endpoint, RTP summary, device timing summary and subjective/acoustic result. The point is not to collect everything. It is to make two runs comparable.

Most importantly, I would preserve the same failure-model discipline. Release engineering for embedded audio must preserve executable behavior, build provenance and rollback separately from feature development. That principle remains true whether the next product uses ESP32-S3, a Linux SoC, a different codec or a cloud media service.

## The result I keep from this incident

V132A became an immutable rollback/reference while new source work continued elsewhere.

The deeper value is the method. I started with a perceptual symptom, located the earliest layer that could create it, chose evidence that could see that layer, changed one variable, and checked the known-good invariants afterward. The process is slower than random tuning for the first build and dramatically faster by the tenth.

The short version of the lesson is: **The best audio result is fragile until it becomes a reproducible, hash-identified release asset.**

That is the standard I now use for embedded audio work. A fix is not convincing because the call sounds better once. It is convincing when the mechanism, measurement, artifact identity and regression behavior all agree about why it got better.
