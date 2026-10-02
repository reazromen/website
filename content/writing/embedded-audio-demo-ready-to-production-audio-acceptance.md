---
title: From Demo-Ready Audio to Production Acceptance
url: /posts/embedded-audio-demo-ready-to-production-audio-acceptance.html
date: '2026-09-15'
read_time: 12
excerpt: One strong call can prove a candidate is promising but not that it is ready
  for manufacturing or field release.
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
- url: /posts/embedded-audio-demo-ready-to-production-audio-acceptance.html
  template: cms/templates/posts/posts--embedded-audio-demo-ready-to-production-audio-acceptance.tpl
  source: cms/templates/posts/posts--embedded-audio-demo-ready-to-production-audio-acceptance.json
---

# From Demo-Ready Audio to Production Acceptance

The useful breakthrough was not another codec setting. It was recognizing that one strong call can prove a candidate is promising but not that it is ready for manufacturing or field release.

The test platform was the LOUP ESP32-S3 voice device with ES8311 playback, ES7210 capture, SIP/RTP media and a small speakerphone enclosure. The network codec was G.711 A-law/PCMA at nominal 8 kHz with 20 ms / 160-byte RTP payloads, while the physical audio path ran at 16 kHz in the recovered playback design. That mismatch between network time, device time and acoustic time is exactly why a vague word like “crackle” is not a diagnosis.

The evidence that matters for this article is specific: The recovery record kept explicit remaining gates: repeated calls, muted-microphone behavior, full-duplex/echo at controlled volumes, cell-to-device calling, local-PBX latency and preservation of the rollback image. I keep those observations tied to the build and test where they were recorded. They are not universal ESP32 performance claims.

The engineering result was also specific: The candidate remained labeled as a production candidate until the defined gates were completed. This article is about how I got from the symptom to that bounded conclusion, what the data did not prove, and what I would monitor before touching the same path again.

## How I framed this case

The most important design decision here was preserving reversibility. The problem was One strong call can prove a candidate is promising but not that it is ready for manufacturing or field release. I kept a known-good control, changed one layer, and required The recovery record kept explicit remaining gates: repeated calls, muted-microphone behavior, full-duplex/echo at controlled volumes, cell-to-device calling, local-PBX latency and preservation of the rollback image. to justify keeping the change. The mechanism was Production acceptance combines quality, stability, repeatability, hardware controls, network variation and recoverability. I explicitly avoided Calling a binary final because one investor-demo call sounded good.. This let me return to the previous baseline when the experiment regressed audio instead of rationalizing the regression as progress. The retained result was The candidate remained labeled as a production candidate until the defined gates were completed. The lesson I would carry to another product is Engineering maturity is the gap between “it worked” and “we know what must stay true for it to keep working.”

## Product audio ends at the ear, not at I2S

Once the digital path is stable, the mechanical product becomes the next experiment. Speaker driver, enclosure volume, vents, sealing, amplifier behavior, microphone placement and user volume all alter what reaches the room and what returns to the microphone. AEC is part of that physical loop even though its code is digital.

Release engineering belongs here too. The acoustic result is only useful if I can identify and restore the firmware that produced it. The V132A handoff treated the working binary as an immutable rollback reference while source cleanup and unrelated power work continued elsewhere. That is how a good call becomes an engineering baseline rather than a memory.

## Case notebook

| Question | Recorded answer |
| --- | --- |
| Symptom | One strong call can prove a candidate is promising but not that it is ready for manufacturing or field release. |
| Evidence | The recovery record kept explicit remaining gates: repeated calls, muted-microphone behavior, full-duplex/echo at controlled volumes, cell-to-device calling, local-PBX latency and preservation of the rollback image. |
| Mechanism | Production acceptance combines quality, stability, repeatability, hardware controls, network variation and recoverability. |
| Rejected explanation | Calling a binary final because one investor-demo call sounded good. |
| Retained result | The candidate remained labeled as a production candidate until the defined gates were completed. |
| Rule carried forward | Engineering maturity is the gap between “it worked” and “we know what must stay true for it to keep working.” |

The rule carried forward is the part I want to survive the specific firmware version. Version numbers change; the debugging invariant should not.

A useful follow-up is to ask what would falsify the retained result. For this case, a repeat run on the same controlled topology should reproduce the relevant observation. If **The recovery record kept explicit remaining gates: repeated calls, muted-microphone behavior, full-duplex/echo at controlled volumes, cell-to-device calling, local-PBX latency and preservation of the rollback image.** disappears while the symptom remains, then the old explanation no longer covers the new incident. If the observation returns without the symptom, then it may be contextual rather than causal. That is why I keep mechanism-level counters beside the listening test.

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

For **From Demo-Ready Audio to Production Acceptance**, the next retest would therefore preserve the same topology and change only the variable tied to **Production acceptance combines quality, stability, repeatability, hardware controls, network variation and recoverability.**. I would collect the same observation again, compare it with the known-good control, and only then decide whether a new firmware branch deserves to replace the baseline.

## The evidence I trusted

The strongest evidence was: **The recovery record kept explicit remaining gates: repeated calls, muted-microphone behavior, full-duplex/echo at controlled volumes, cell-to-device calling, local-PBX latency and preservation of the rollback image.**

I try to rank evidence by how close it is to the mechanism. A subjective report is important because it defines the product failure, but it is not enough to choose a patch. A log line is stronger only if the logging path does not perturb the timing being measured. A packet capture is strong for transport questions but weak for acoustics. A binary hash is excellent for identity and useless for explaining timbre. A synchronized measurement is valuable only if the clocks and capture points are understood.

For this investigation I used the evidence as a boundary. It allowed me to say what changed and, just as importantly, what did not change. That distinction prevented the later write-up from turning a plausible story into a fabricated root cause.

The mechanism underneath the observation is straightforward: Production acceptance combines quality, stability, repeatability, hardware controls, network variation and recoverability. This is the part I would teach to another firmware engineer before giving them any patch, because without the mechanism the numbers are easy to misread.

## Change one layer, freeze the others

The practical experiment design was to freeze as much of the call path as possible and change the narrowest variable that could test the hypothesis. That meant preserving the SIP identity and call flow, keeping the codec and I2S configuration stable unless they were the subject of the test, using app-only flashes where appropriate, retaining a rollback binary, and capturing the same small set of counters after each call.

For this topic the controlled variable was the mechanism described above, not the entire audio stack. The surrounding rule was: **Engineering maturity is the gap between “it worked” and “we know what must stay true for it to keep working.”** A change that improves one symptom but also changes AEC, queue depth, volume, sample conversion and logging at once produces a better demo perhaps, but a worse experiment.

I also learned to keep the diagnostic path quiet during the actual call. Counters can increment in RAM. Histograms can accumulate. A summary can print after BYE. That pattern is much safer than serializing kilobytes of task state while a 20 ms media deadline is active. The quiet-V115 work made this principle measurable rather than theoretical.

The acceptance test should therefore include both the perceptual outcome and the mechanism-specific evidence. A call that sounds better but increases slow I2S writes is not automatically a win. A PCAP that looks cleaner while echo becomes objectionable is not a win either. The experiment passes only when the intended layer improves without violating the known-good invariants around it.

## What this result proves—and what it does not

The result I am willing to claim is narrow: **The candidate remained labeled as a production candidate until the defined gates were completed.** It is supported by the recorded observation: **The recovery record kept explicit remaining gates: repeated calls, muted-microphone behavior, full-duplex/echo at controlled volumes, cell-to-device calling, local-PBX latency and preservation of the rollback image.**

It does not prove that every LOUP board, every network path or every future firmware build behaves the same way. It does not turn a server-side packet capture into an acoustic measurement. It does not turn a stable AEC-off test into permission to remove AEC from a speakerphone. It does not make a hash a quality metric. Those distinctions sound obvious in hindsight and are easy to lose when a demo deadline rewards a simple story.

The useful causal statement is the one consistent with the mechanism: Production acceptance combines quality, stability, repeatability, hardware controls, network variation and recoverability. If another experiment changes that mechanism, I expect the evidence to change too. If the evidence stays the same, I should question the theory before rewriting more code.

I also keep the rejected explanation visible: Calling a binary final because one investor-demo call sounded good. That is part of the result. Knowing which layer did *not* create the step change prevents future debugging from starting at the same dead end.

## Reproducing the experiment without changing the experiment

If I had to hand this case to another engineer, I would ask them to preserve the same evidence boundary before attempting a fix:

- preserve the rollback binary before unrelated feature work
- repeat calls at controlled speaker levels
- separate digital timing evidence from acoustic observations
- record hardware/enclosure revision with every audio result
- require rollback, mute, full-duplex and call-origin gates before final sign-off

The point is not ceremony. Embedded audio is sensitive to hidden changes. A different softphone setting, a different PBX region, a new enclosure revision, a verbose log level or a queue added “for safety” can all change the result while leaving the test name unchanged.

For **From Demo-Ready Audio to Production Acceptance**, the pass condition should be written in terms of the mechanism and evidence, not just “sounds good.” The subjective call still matters—it is the product—but the engineering result has to survive comparison.

## The production rule that survived the incident

Engineering maturity is the gap between “it worked” and “we know what must stay true for it to keep working.”

I translate that sentence into an operational rule. The metric or artifact that revealed the failure must remain available in future debug builds, but it must not create the same realtime cost. The known-good binary must remain recoverable. A new audio experiment must identify exactly which layer changed. A release candidate must be tested against the same user-visible behaviors that made the earlier baseline valuable.

This keeps debugging cumulative. Instead of starting every audio complaint with “maybe packet loss” or “maybe AEC,” the next investigation begins with a fault tree and a set of already-proven boundaries. The value of the V115/V127/V132A history is not the version numbers themselves; it is the accumulated map of which measurements are trustworthy and which changes have already regressed the product.

## What I would do differently on the next product

I would design the measurement points earlier. The RTP callback, playout clock, queue, I2S boundary, exact AEC reference, capture slots and acoustic test points would all have named interfaces and low-cost counters from the beginning. That would reduce the amount of forensic reconstruction needed after subjective complaints arrive.

I would also separate debug verbosity from realtime instrumentation by architecture, not convention. Realtime code would update fixed counters or ring-buffer events; a lower-priority task would export summaries. If a UART or network logger can block the media task, the design has already allowed the observer into the deadline path.

For multi-device validation I would automate the call matrix and preserve a compact evidence bundle per run: firmware identity, hardware revision, test endpoint, RTP summary, device timing summary and subjective/acoustic result. The point is not to collect everything. It is to make two runs comparable.

Most importantly, I would preserve the same failure-model discipline. Production acceptance combines quality, stability, repeatability, hardware controls, network variation and recoverability. That principle remains true whether the next product uses ESP32-S3, a Linux SoC, a different codec or a cloud media service.

## The result I keep from this incident

The candidate remained labeled as a production candidate until the defined gates were completed.

The deeper value is the method. I started with a perceptual symptom, located the earliest layer that could create it, chose evidence that could see that layer, changed one variable, and checked the known-good invariants afterward. The process is slower than random tuning for the first build and dramatically faster by the tenth.

The short version of the lesson is: **Engineering maturity is the gap between “it worked” and “we know what must stay true for it to keep working.”**

That is the standard I now use for embedded audio work. A fix is not convincing because the call sounds better once. It is convincing when the mechanism, measurement, artifact identity and regression behavior all agree about why it got better.
