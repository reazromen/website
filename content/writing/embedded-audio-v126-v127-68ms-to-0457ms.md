---
title: 'V126 to V127: What 68.201 ms to 0.457 ms Actually Proved'
url: /posts/embedded-audio-v126-v127-68ms-to-0457ms.html
date: '2026-04-19'
read_time: 12
excerpt: A large first callback-to-speaker delay suggested work was accumulating between
  RTP reception and physical output.
topic: embedded-audio-voice
tags:
- esp32-s3
- embedded-audio
- loup
- i2s
- realtime
draft: false
featured: false
language: en
eyebrow: 'Embedded Audio Debugging: Real-Time Playback & Timing · deep-dive'
outputs:
- url: /posts/embedded-audio-v126-v127-68ms-to-0457ms.html
  template: cms/templates/posts/posts--embedded-audio-v126-v127-68ms-to-0457ms.tpl
  source: cms/templates/posts/posts--embedded-audio-v126-v127-68ms-to-0457ms.json
---

# V126 to V127: What 68.201 ms to 0.457 ms Actually Proved

The useful breakthrough was not another codec setting. It was recognizing that a large first callback-to-speaker delay suggested work was accumulating between RTP reception and physical output.

The test platform was the LOUP ESP32-S3 voice device with ES8311 playback, ES7210 capture, SIP/RTP media and a small speakerphone enclosure. The network codec was G.711 A-law/PCMA at nominal 8 kHz with 20 ms / 160-byte RTP payloads, while the physical audio path ran at 16 kHz in the recovered playback design. That mismatch between network time, device time and acoustic time is exactly why a vague word like “crackle” is not a diagnosis.

The evidence that matters for this article is specific: In the recorded V127 validation, first callback-to-speaker-write start measured 0.457 ms versus 68.201 ms in V126, and that tested call reported no audio cutouts. I keep those observations tied to the build and test where they were recorded. They are not universal ESP32 performance claims.

The engineering result was also specific: The measurement became evidence that the local hot path was no longer carrying the same startup delay. This article is about how I got from the symptom to that bounded conclusion, what the data did not prove, and what I would monitor before touching the same path again.

## How I framed this case

This case is a useful example of negative evidence. The system contained a suspicious condition, but suspicion is not causality. The observed problem was A large first callback-to-speaker delay suggested work was accumulating between RTP reception and physical output. The candidate explanation was Advertising sub-millisecond latency as a universal product benchmark.. I looked for the consequence that explanation should create and compared it with In the recorded V127 validation, first callback-to-speaker-write start measured 0.457 ms versus 68.201 ms in V126, and that tested call reported no audio cutouts.. The deeper mechanism—A point latency measurement proves a specific path changed materially, but it does not prove end-to-end conversational latency or universal stability.—showed why the relationship was weaker than it first appeared. The final result was The measurement became evidence that the local hot path was no longer carrying the same startup delay. The important outcome was not just a fix; it was permission to stop spending time on a theory that the data no longer supported.

## Deadline math I use for playout

With nominal 20 ms telephony frames, I treat one frame as a useful unit of budget, not a guarantee of arrival. A receive callback can be early, late or bursty; the speaker still needs continuous samples. I therefore distinguish arrival-gap statistics from local callback-to-I2S time and from I2S write duration. They answer three separate questions: what the network delivered, how quickly firmware reacted, and whether the output boundary blocked.

For long calls I add drift. If the local playout clock differs from the media production rate, the queue can slowly walk even when every individual write is fast. That is why a short “no cutout” test and a long stability test are complementary rather than redundant.

## Case notebook

| Question | Recorded answer |
| --- | --- |
| Symptom | A large first callback-to-speaker delay suggested work was accumulating between RTP reception and physical output. |
| Evidence | In the recorded V127 validation, first callback-to-speaker-write start measured 0.457 ms versus 68.201 ms in V126, and that tested call reported no audio cutouts. |
| Mechanism | A point latency measurement proves a specific path changed materially, but it does not prove end-to-end conversational latency or universal stability. |
| Rejected explanation | Advertising sub-millisecond latency as a universal product benchmark. |
| Retained result | The measurement became evidence that the local hot path was no longer carrying the same startup delay. |
| Rule carried forward | Tie performance numbers to exact builds and test paths; never convert one good sample into a timeless requirement. |

Keeping the rejected explanation in the same record is important. Audio teams otherwise rediscover the same plausible theory every few weeks.

A useful follow-up is to ask what would falsify the retained result. For this case, a repeat run on the same controlled topology should reproduce the relevant observation. If **In the recorded V127 validation, first callback-to-speaker-write start measured 0.457 ms versus 68.201 ms in V126, and that tested call reported no audio cutouts.** disappears while the symptom remains, then the old explanation no longer covers the new incident. If the observation returns without the symptom, then it may be contextual rather than causal. That is why I keep mechanism-level counters beside the listening test.

### Instrumentation sketch

```
// hot path: counters only, no per-frame printf
now = esp_timer_get_time();
callback_gap_us = now - last_callback_us;
last_callback_us = now;

start = esp_timer_get_time();
write_pcm_to_i2s(frame);
write_us = esp_timer_get_time() - start;
if (write_us > 20000) slow_write_count++;
if (write_us > max_write_us) max_write_us = write_us;
```

The snippet is not presented as drop-in production code. It documents the measurement model. I want the instrumentation to be cheaper than the deadline it observes, explicit about units, and easy to disable or summarize after the call. The most dangerous diagnostic is one that silently changes scheduler behavior while appearing to measure it.

For **V126 to V127: What 68.201 ms to 0.457 ms Actually Proved**, the next retest would therefore preserve the same topology and change only the variable tied to **A point latency measurement proves a specific path changed materially, but it does not prove end-to-end conversational latency or universal stability.**. I would collect the same observation again, compare it with the known-good control, and only then decide whether a new firmware branch deserves to replace the baseline.

## The evidence I trusted

The strongest evidence was: **In the recorded V127 validation, first callback-to-speaker-write start measured 0.457 ms versus 68.201 ms in V126, and that tested call reported no audio cutouts.**

I try to rank evidence by how close it is to the mechanism. A subjective report is important because it defines the product failure, but it is not enough to choose a patch. A log line is stronger only if the logging path does not perturb the timing being measured. A packet capture is strong for transport questions but weak for acoustics. A binary hash is excellent for identity and useless for explaining timbre. A synchronized measurement is valuable only if the clocks and capture points are understood.

For this investigation I used the evidence as a boundary. It allowed me to say what changed and, just as importantly, what did not change. That distinction prevented the later write-up from turning a plausible story into a fabricated root cause.

The mechanism underneath the observation is straightforward: A point latency measurement proves a specific path changed materially, but it does not prove end-to-end conversational latency or universal stability. This is the part I would teach to another firmware engineer before giving them any patch, because without the mechanism the numbers are easy to misread.

## Change one layer, freeze the others

The practical experiment design was to freeze as much of the call path as possible and change the narrowest variable that could test the hypothesis. That meant preserving the SIP identity and call flow, keeping the codec and I2S configuration stable unless they were the subject of the test, using app-only flashes where appropriate, retaining a rollback binary, and capturing the same small set of counters after each call.

For this topic the controlled variable was the mechanism described above, not the entire audio stack. The surrounding rule was: **Tie performance numbers to exact builds and test paths; never convert one good sample into a timeless requirement.** A change that improves one symptom but also changes AEC, queue depth, volume, sample conversion and logging at once produces a better demo perhaps, but a worse experiment.

I also learned to keep the diagnostic path quiet during the actual call. Counters can increment in RAM. Histograms can accumulate. A summary can print after BYE. That pattern is much safer than serializing kilobytes of task state while a 20 ms media deadline is active. The quiet-V115 work made this principle measurable rather than theoretical.

The acceptance test should therefore include both the perceptual outcome and the mechanism-specific evidence. A call that sounds better but increases slow I2S writes is not automatically a win. A PCAP that looks cleaner while echo becomes objectionable is not a win either. The experiment passes only when the intended layer improves without violating the known-good invariants around it.

## What this result proves—and what it does not

The result I am willing to claim is narrow: **The measurement became evidence that the local hot path was no longer carrying the same startup delay.** It is supported by the recorded observation: **In the recorded V127 validation, first callback-to-speaker-write start measured 0.457 ms versus 68.201 ms in V126, and that tested call reported no audio cutouts.**

It does not prove that every LOUP board, every network path or every future firmware build behaves the same way. It does not turn a server-side packet capture into an acoustic measurement. It does not turn a stable AEC-off test into permission to remove AEC from a speakerphone. It does not make a hash a quality metric. Those distinctions sound obvious in hindsight and are easy to lose when a demo deadline rewards a simple story.

The useful causal statement is the one consistent with the mechanism: A point latency measurement proves a specific path changed materially, but it does not prove end-to-end conversational latency or universal stability. If another experiment changes that mechanism, I expect the evidence to change too. If the evidence stays the same, I should question the theory before rewriting more code.

I also keep the rejected explanation visible: Advertising sub-millisecond latency as a universal product benchmark. That is part of the result. Knowing which layer did *not* create the step change prevents future debugging from starting at the same dead end.

## Reproducing the experiment without changing the experiment

If I had to hand this case to another engineer, I would ask them to preserve the same evidence boundary before attempting a fix:

- quiet the call hot path before measuring it
- record callback gaps and speaker-write duration in RAM
- capture queue/underrun state without per-frame printing
- run a short quality call and a longer drift call
- compare against the same known-good playout path

The point is not ceremony. Embedded audio is sensitive to hidden changes. A different softphone setting, a different PBX region, a new enclosure revision, a verbose log level or a queue added “for safety” can all change the result while leaving the test name unchanged.

For **V126 to V127: What 68.201 ms to 0.457 ms Actually Proved**, the pass condition should be written in terms of the mechanism and evidence, not just “sounds good.” The subjective call still matters—it is the product—but the engineering result has to survive comparison.

## The production rule that survived the incident

Tie performance numbers to exact builds and test paths; never convert one good sample into a timeless requirement.

I translate that sentence into an operational rule. The metric or artifact that revealed the failure must remain available in future debug builds, but it must not create the same realtime cost. The known-good binary must remain recoverable. A new audio experiment must identify exactly which layer changed. A release candidate must be tested against the same user-visible behaviors that made the earlier baseline valuable.

This keeps debugging cumulative. Instead of starting every audio complaint with “maybe packet loss” or “maybe AEC,” the next investigation begins with a fault tree and a set of already-proven boundaries. The value of the V115/V127/V132A history is not the version numbers themselves; it is the accumulated map of which measurements are trustworthy and which changes have already regressed the product.

## What I would do differently on the next product

I would design the measurement points earlier. The RTP callback, playout clock, queue, I2S boundary, exact AEC reference, capture slots and acoustic test points would all have named interfaces and low-cost counters from the beginning. That would reduce the amount of forensic reconstruction needed after subjective complaints arrive.

I would also separate debug verbosity from realtime instrumentation by architecture, not convention. Realtime code would update fixed counters or ring-buffer events; a lower-priority task would export summaries. If a UART or network logger can block the media task, the design has already allowed the observer into the deadline path.

For multi-device validation I would automate the call matrix and preserve a compact evidence bundle per run: firmware identity, hardware revision, test endpoint, RTP summary, device timing summary and subjective/acoustic result. The point is not to collect everything. It is to make two runs comparable.

Most importantly, I would preserve the same failure-model discipline. A point latency measurement proves a specific path changed materially, but it does not prove end-to-end conversational latency or universal stability. That principle remains true whether the next product uses ESP32-S3, a Linux SoC, a different codec or a cloud media service.

## The result I keep from this incident

The measurement became evidence that the local hot path was no longer carrying the same startup delay.

The deeper value is the method. I started with a perceptual symptom, located the earliest layer that could create it, chose evidence that could see that layer, changed one variable, and checked the known-good invariants afterward. The process is slower than random tuning for the first build and dramatically faster by the tenth.

The short version of the lesson is: **Tie performance numbers to exact builds and test paths; never convert one good sample into a timeless requirement.**

That is the standard I now use for embedded audio work. A fix is not convincing because the call sounds better once. It is convincing when the mechanism, measurement, artifact identity and regression behavior all agree about why it got better.
