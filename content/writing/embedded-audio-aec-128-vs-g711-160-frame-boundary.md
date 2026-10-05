---
title: 128-Sample AEC Blocks vs 160-Sample G.711 Frames
url: /posts/embedded-audio-aec-128-vs-g711-160-frame-boundary.html
date: '2025-03-28'
read_time: 12
excerpt: The AEC library consumed a block size that did not divide evenly into the
  telephony frame size.
topic: embedded-audio-voice
tags:
- esp32-s3
- embedded-audio
- loup
- aec
- codec
draft: false
featured: false
language: en
eyebrow: 'Embedded Audio Debugging: Capture, Codec & AEC · deep-dive'
outputs:
- url: /posts/embedded-audio-aec-128-vs-g711-160-frame-boundary.html
  template: cms/templates/posts/posts--embedded-audio-aec-128-vs-g711-160-frame-boundary.tpl
  source: cms/templates/posts/posts--embedded-audio-aec-128-vs-g711-160-frame-boundary.json
---

# 128-Sample AEC Blocks vs 160-Sample G.711 Frames

This part of the LOUP audio investigation began with a deceptively simple symptom: the AEC library consumed a block size that did not divide evenly into the telephony frame size.

The test platform was the LOUP ESP32-S3 voice device with ES8311 playback, ES7210 capture, SIP/RTP media and a small speakerphone enclosure. The network codec was G.711 A-law/PCMA at nominal 8 kHz with 20 ms / 160-byte RTP payloads, while the physical audio path ran at 16 kHz in the recovered playback design. That mismatch between network time, device time and acoustic time is exactly why a vague word like “crackle” is not a diagnosis.

The evidence that matters for this article is specific: The ADF AEC consumed 128-sample chunks while G.711 frames carried 160 samples; V113 preserved tails across reads rather than dropping or duplicating the remainder. I keep those observations tied to the build and test where they were recorded. They are not universal ESP32 performance claims.

The engineering result was also specific: Tail preservation allowed the DSP block size and RTP framing to coexist without corrupting continuity. This article is about how I got from the symptom to that bounded conclusion, what the data did not prove, and what I would monitor before touching the same path again.

## How I framed this case

The debugging value here came from using two independent views of the same event. One view described the user-visible failure—The AEC library consumed a block size that did not divide evenly into the telephony frame size. The other described the machine state—The ADF AEC consumed 128-sample chunks while G.711 frames carried 160 samples; V113 preserved tails across reads rather than dropping or duplicating the remainder. Because Mismatched processing granularities require explicit carry-over state; otherwise every boundary can introduce loss, duplication or timing drift., agreement between those views was meaningful and disagreement was informative. I specifically resisted Forcing every subsystem to operate on the network packet size.. If the second observation did not support the first hypothesis, I moved the fault boundary instead of adding another patch. The result was Tail preservation allowed the DSP block size and RTP framing to coexist without corrupting continuity. and the general engineering rule became Frame-boundary code is part of the signal path and deserves the same review as the DSP algorithm.

## Signal identity before DSP tuning

My first capture/AEC question is now “what exact sample is this?” I want sample rate, channel/slot, bit width, scaling, physical source and timestamp relationship. A DSP block receiving perfectly formatted samples from the wrong microphone is still wrong. An AEC receiving a far-end signal that differs from physical playback is still wrong. A resampler that drops tails can be wrong only at frame boundaries and therefore sound intermittent.

Once those identities are proven, algorithm tuning becomes meaningful. Before that, tuning can hide routing defects and make the next hardware revision harder to reason about.

## Case notebook

| Question | Recorded answer |
| --- | --- |
| Symptom | The AEC library consumed a block size that did not divide evenly into the telephony frame size. |
| Evidence | The ADF AEC consumed 128-sample chunks while G.711 frames carried 160 samples; V113 preserved tails across reads rather than dropping or duplicating the remainder. |
| Mechanism | Mismatched processing granularities require explicit carry-over state; otherwise every boundary can introduce loss, duplication or timing drift. |
| Rejected explanation | Forcing every subsystem to operate on the network packet size. |
| Retained result | Tail preservation allowed the DSP block size and RTP framing to coexist without corrupting continuity. |
| Rule carried forward | Frame-boundary code is part of the signal path and deserves the same review as the DSP algorithm. |

This matrix is what I would hand to another engineer before giving them the source tree. It makes the next test start from evidence instead of folklore.

A useful follow-up is to ask what would falsify the retained result. For this case, a repeat run on the same controlled topology should reproduce the relevant observation. If **The ADF AEC consumed 128-sample chunks while G.711 frames carried 160 samples; V113 preserved tails across reads rather than dropping or duplicating the remainder.** disappears while the symptom remains, then the old explanation no longer covers the new incident. If the observation returns without the symptom, then it may be contextual rather than causal. That is why I keep mechanism-level counters beside the listening test.

### Instrumentation sketch

```
raw slot 0 -> verify physical source before naming it
raw slot 1 -> selected MIC1 in the recorded path
raw slot 2 -> verify / unused in historical mapping
raw slot 3 -> historical MIC2

AEC reference := exact PCM chosen for physical playback
AEC input blocks := 128 samples
network voice frame := 160 samples @ 8 kHz
carry remainder; never silently drop the tail
```

The snippet is not presented as drop-in production code. It documents the measurement model. I want the instrumentation to be cheaper than the deadline it observes, explicit about units, and easy to disable or summarize after the call. The most dangerous diagnostic is one that silently changes scheduler behavior while appearing to measure it.

For **128-Sample AEC Blocks vs 160-Sample G.711 Frames**, the next retest would therefore preserve the same topology and change only the variable tied to **Mismatched processing granularities require explicit carry-over state; otherwise every boundary can introduce loss, duplication or timing drift.**. I would collect the same observation again, compare it with the known-good control, and only then decide whether a new firmware branch deserves to replace the baseline.

## The evidence I trusted

The strongest evidence was: **The ADF AEC consumed 128-sample chunks while G.711 frames carried 160 samples; V113 preserved tails across reads rather than dropping or duplicating the remainder.**

I try to rank evidence by how close it is to the mechanism. A subjective report is important because it defines the product failure, but it is not enough to choose a patch. A log line is stronger only if the logging path does not perturb the timing being measured. A packet capture is strong for transport questions but weak for acoustics. A binary hash is excellent for identity and useless for explaining timbre. A synchronized measurement is valuable only if the clocks and capture points are understood.

For this investigation I used the evidence as a boundary. It allowed me to say what changed and, just as importantly, what did not change. That distinction prevented the later write-up from turning a plausible story into a fabricated root cause.

The mechanism underneath the observation is straightforward: Mismatched processing granularities require explicit carry-over state; otherwise every boundary can introduce loss, duplication or timing drift. This is the part I would teach to another firmware engineer before giving them any patch, because without the mechanism the numbers are easy to misread.

## Tools were chosen by the question, not by habit

The useful toolset for this layer was codec register/source inspection, raw-slot probes, sample dumps, AEC reference checks, mute controls and controlled AEC on/off tests. I did not expect one tool to explain the whole call.

When the question was packet loss, I looked at RTP sequence and timestamps. When the question was device scheduling, I looked at monotonic callback and I2S timing. When the question was build identity, I used hashes and preserved artifacts. When the question was echo or timbre, packet capture stopped at the digital boundary and the next test had to include the physical speaker/microphone path.

That separation matters because every tool has a blind spot. UART logs can perturb timing. PCAP cannot hear the room. Far-end listening cannot prove which queue grew. Docker/Asterisk logs cannot prove the ESP32 played a sample. A codec detection scan cannot prove the channel mapping matches the DSP assumptions. The tool is evidence only for the layer it can actually observe.

This is also why I prefer small, named counters over giant debug dumps in realtime code. A counter such as “writes over 20 ms,” “max callback gap,” “queue underrun,” or “first callback to I2S start” has a defined semantic. It can be compared across builds without parsing thousands of lines whose own output may change the result.

## What this result proves—and what it does not

The result I am willing to claim is narrow: **Tail preservation allowed the DSP block size and RTP framing to coexist without corrupting continuity.** It is supported by the recorded observation: **The ADF AEC consumed 128-sample chunks while G.711 frames carried 160 samples; V113 preserved tails across reads rather than dropping or duplicating the remainder.**

It does not prove that every LOUP board, every network path or every future firmware build behaves the same way. It does not turn a server-side packet capture into an acoustic measurement. It does not turn a stable AEC-off test into permission to remove AEC from a speakerphone. It does not make a hash a quality metric. Those distinctions sound obvious in hindsight and are easy to lose when a demo deadline rewards a simple story.

The useful causal statement is the one consistent with the mechanism: Mismatched processing granularities require explicit carry-over state; otherwise every boundary can introduce loss, duplication or timing drift. If another experiment changes that mechanism, I expect the evidence to change too. If the evidence stays the same, I should question the theory before rewriting more code.

I also keep the rejected explanation visible: Forcing every subsystem to operate on the network packet size. That is part of the result. Knowing which layer did *not* create the step change prevents future debugging from starting at the same dead end.

## Reproducing the experiment without changing the experiment

If I had to hand this case to another engineer, I would ask them to preserve the same evidence boundary before attempting a fix:

- record codec/sample format and physical channel mapping
- verify the exact PCM used as AEC reference
- test capture with AEC both enabled and disabled as controlled experiments
- preserve partial DSP blocks/tails across frame boundaries
- repeat mute and full-duplex tests after any mapping change

The point is not ceremony. Embedded audio is sensitive to hidden changes. A different softphone setting, a different PBX region, a new enclosure revision, a verbose log level or a queue added “for safety” can all change the result while leaving the test name unchanged.

For **128-Sample AEC Blocks vs 160-Sample G.711 Frames**, the pass condition should be written in terms of the mechanism and evidence, not just “sounds good.” The subjective call still matters—it is the product—but the engineering result has to survive comparison.

## The production rule that survived the incident

Frame-boundary code is part of the signal path and deserves the same review as the DSP algorithm.

I translate that sentence into an operational rule. The metric or artifact that revealed the failure must remain available in future debug builds, but it must not create the same realtime cost. The known-good binary must remain recoverable. A new audio experiment must identify exactly which layer changed. A release candidate must be tested against the same user-visible behaviors that made the earlier baseline valuable.

This keeps debugging cumulative. Instead of starting every audio complaint with “maybe packet loss” or “maybe AEC,” the next investigation begins with a fault tree and a set of already-proven boundaries. The value of the V115/V127/V132A history is not the version numbers themselves; it is the accumulated map of which measurements are trustworthy and which changes have already regressed the product.

## What I would do differently on the next product

I would design the measurement points earlier. The RTP callback, playout clock, queue, I2S boundary, exact AEC reference, capture slots and acoustic test points would all have named interfaces and low-cost counters from the beginning. That would reduce the amount of forensic reconstruction needed after subjective complaints arrive.

I would also separate debug verbosity from realtime instrumentation by architecture, not convention. Realtime code would update fixed counters or ring-buffer events; a lower-priority task would export summaries. If a UART or network logger can block the media task, the design has already allowed the observer into the deadline path.

For multi-device validation I would automate the call matrix and preserve a compact evidence bundle per run: firmware identity, hardware revision, test endpoint, RTP summary, device timing summary and subjective/acoustic result. The point is not to collect everything. It is to make two runs comparable.

Most importantly, I would preserve the same failure-model discipline. Mismatched processing granularities require explicit carry-over state; otherwise every boundary can introduce loss, duplication or timing drift. That principle remains true whether the next product uses ESP32-S3, a Linux SoC, a different codec or a cloud media service.

## The result I keep from this incident

Tail preservation allowed the DSP block size and RTP framing to coexist without corrupting continuity.

The deeper value is the method. I started with a perceptual symptom, located the earliest layer that could create it, chose evidence that could see that layer, changed one variable, and checked the known-good invariants afterward. The process is slower than random tuning for the first build and dramatically faster by the tenth.

The short version of the lesson is: **Frame-boundary code is part of the signal path and deserves the same review as the DSP algorithm.**

That is the standard I now use for embedded audio work. A fix is not convincing because the call sounds better once. It is convincing when the mechanism, measurement, artifact identity and regression behavior all agree about why it got better.
