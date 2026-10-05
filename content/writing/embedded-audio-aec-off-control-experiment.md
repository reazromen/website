---
title: An AEC-Off Run Is a Control Experiment, Not a Product Setting
url: /posts/embedded-audio-aec-off-control-experiment.html
date: '2020-03-21'
read_time: 12
excerpt: AEC was implicated in several symptoms, but disabling it permanently would
  remove a required speakerphone function.
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
- url: /posts/embedded-audio-aec-off-control-experiment.html
  template: cms/templates/posts/posts--embedded-audio-aec-off-control-experiment.tpl
  source: cms/templates/posts/posts--embedded-audio-aec-off-control-experiment.json
---

# An AEC-Off Run Is a Control Experiment, Not a Product Setting

I stopped treating this as an audio-quality problem when aEC was implicated in several symptoms, but disabling it permanently would remove a required speakerphone function.

The test platform was the LOUP ESP32-S3 voice device with ES8311 playback, ES7210 capture, SIP/RTP media and a small speakerphone enclosure. The network codec was G.711 A-law/PCMA at nominal 8 kHz with 20 ms / 160-byte RTP payloads, while the physical audio path ran at 16 kHz in the recovered playback design. That mismatch between network time, device time and acoustic time is exactly why a vague word like “crackle” is not a diagnosis.

The evidence that matters for this article is specific: A recorded AEC-off diagnostic call ran 175.6 seconds stably and helped isolate timing/stall behavior from echo-canceller processing. I keep those observations tied to the build and test where they were recorded. They are not universal ESP32 performance claims.

The engineering result was also specific: AEC-off evidence narrowed the fault domain while the final clear path restored the needed reference/AEC behavior. This article is about how I got from the symptom to that bounded conclusion, what the data did not prove, and what I would monitor before touching the same path again.

## How I framed this case

The most important design decision here was preserving reversibility. The problem was AEC was implicated in several symptoms, but disabling it permanently would remove a required speakerphone function. I kept a known-good control, changed one layer, and required A recorded AEC-off diagnostic call ran 175.6 seconds stably and helped isolate timing/stall behavior from echo-canceller processing. to justify keeping the change. The mechanism was A control experiment removes one subsystem to test causality; it does not automatically define the final architecture. I explicitly avoided Interpreting “works with AEC off” as evidence that production should ship without AEC.. This let me return to the previous baseline when the experiment regressed audio instead of rationalizing the regression as progress. The retained result was AEC-off evidence narrowed the fault domain while the final clear path restored the needed reference/AEC behavior. The lesson I would carry to another product is Use feature-disable tests to isolate causes, then reintroduce required functionality under measurement.

## Signal identity before DSP tuning

My first capture/AEC question is now “what exact sample is this?” I want sample rate, channel/slot, bit width, scaling, physical source and timestamp relationship. A DSP block receiving perfectly formatted samples from the wrong microphone is still wrong. An AEC receiving a far-end signal that differs from physical playback is still wrong. A resampler that drops tails can be wrong only at frame boundaries and therefore sound intermittent.

Once those identities are proven, algorithm tuning becomes meaningful. Before that, tuning can hide routing defects and make the next hardware revision harder to reason about.

## Case notebook

| Question | Recorded answer |
| --- | --- |
| Symptom | AEC was implicated in several symptoms, but disabling it permanently would remove a required speakerphone function. |
| Evidence | A recorded AEC-off diagnostic call ran 175.6 seconds stably and helped isolate timing/stall behavior from echo-canceller processing. |
| Mechanism | A control experiment removes one subsystem to test causality; it does not automatically define the final architecture. |
| Rejected explanation | Interpreting “works with AEC off” as evidence that production should ship without AEC. |
| Retained result | AEC-off evidence narrowed the fault domain while the final clear path restored the needed reference/AEC behavior. |
| Rule carried forward | Use feature-disable tests to isolate causes, then reintroduce required functionality under measurement. |

The rule carried forward is the part I want to survive the specific firmware version. Version numbers change; the debugging invariant should not.

A useful follow-up is to ask what would falsify the retained result. For this case, a repeat run on the same controlled topology should reproduce the relevant observation. If **A recorded AEC-off diagnostic call ran 175.6 seconds stably and helped isolate timing/stall behavior from echo-canceller processing.** disappears while the symptom remains, then the old explanation no longer covers the new incident. If the observation returns without the symptom, then it may be contextual rather than causal. That is why I keep mechanism-level counters beside the listening test.

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

For **An AEC-Off Run Is a Control Experiment, Not a Product Setting**, the next retest would therefore preserve the same topology and change only the variable tied to **A control experiment removes one subsystem to test causality; it does not automatically define the final architecture.**. I would collect the same observation again, compare it with the known-good control, and only then decide whether a new firmware branch deserves to replace the baseline.

## The tempting explanation I did not accept

The attractive wrong turn was: **Interpreting “works with AEC off” as evidence that production should ship without AEC.**

Embedded audio is full of these traps because many failure modes sound alike. Packet bursts, resampler artifacts, AEC suppression, output starvation, clipping and acoustic echo can all be described as “robotic” by a listener. A large queue can hide packet jitter while making conversation sluggish. Turning AEC off can remove one processing cost while making the product unusable as a speakerphone. A warning in the log can look causal simply because it is the only visible abnormality.

The rule I now use is that a theory must predict another observable fact. If I believe packet loss is causing a missing word, I should find the corresponding sequence gap or payload absence before the device. If I believe I2S is stalling, speaker-write timing should show it. If I believe the PBX is batching media, its receive/forward timestamps should expose the batch before the ESP32 sees it. If I believe echo is acoustic, changing volume or geometry should change the failure even when packet timing remains stable.

This is slower than guessing for the first ten minutes and much faster than carrying a wrong theory through ten firmware versions.

## Tools were chosen by the question, not by habit

The useful toolset for this layer was codec register/source inspection, raw-slot probes, sample dumps, AEC reference checks, mute controls and controlled AEC on/off tests. I did not expect one tool to explain the whole call.

When the question was packet loss, I looked at RTP sequence and timestamps. When the question was device scheduling, I looked at monotonic callback and I2S timing. When the question was build identity, I used hashes and preserved artifacts. When the question was echo or timbre, packet capture stopped at the digital boundary and the next test had to include the physical speaker/microphone path.

That separation matters because every tool has a blind spot. UART logs can perturb timing. PCAP cannot hear the room. Far-end listening cannot prove which queue grew. Docker/Asterisk logs cannot prove the ESP32 played a sample. A codec detection scan cannot prove the channel mapping matches the DSP assumptions. The tool is evidence only for the layer it can actually observe.

This is also why I prefer small, named counters over giant debug dumps in realtime code. A counter such as “writes over 20 ms,” “max callback gap,” “queue underrun,” or “first callback to I2S start” has a defined semantic. It can be compared across builds without parsing thousands of lines whose own output may change the result.

## What this result proves—and what it does not

The result I am willing to claim is narrow: **AEC-off evidence narrowed the fault domain while the final clear path restored the needed reference/AEC behavior.** It is supported by the recorded observation: **A recorded AEC-off diagnostic call ran 175.6 seconds stably and helped isolate timing/stall behavior from echo-canceller processing.**

It does not prove that every LOUP board, every network path or every future firmware build behaves the same way. It does not turn a server-side packet capture into an acoustic measurement. It does not turn a stable AEC-off test into permission to remove AEC from a speakerphone. It does not make a hash a quality metric. Those distinctions sound obvious in hindsight and are easy to lose when a demo deadline rewards a simple story.

The useful causal statement is the one consistent with the mechanism: A control experiment removes one subsystem to test causality; it does not automatically define the final architecture. If another experiment changes that mechanism, I expect the evidence to change too. If the evidence stays the same, I should question the theory before rewriting more code.

I also keep the rejected explanation visible: Interpreting “works with AEC off” as evidence that production should ship without AEC. That is part of the result. Knowing which layer did *not* create the step change prevents future debugging from starting at the same dead end.

## Reproducing the experiment without changing the experiment

If I had to hand this case to another engineer, I would ask them to preserve the same evidence boundary before attempting a fix:

- record codec/sample format and physical channel mapping
- verify the exact PCM used as AEC reference
- test capture with AEC both enabled and disabled as controlled experiments
- preserve partial DSP blocks/tails across frame boundaries
- repeat mute and full-duplex tests after any mapping change

The point is not ceremony. Embedded audio is sensitive to hidden changes. A different softphone setting, a different PBX region, a new enclosure revision, a verbose log level or a queue added “for safety” can all change the result while leaving the test name unchanged.

For **An AEC-Off Run Is a Control Experiment, Not a Product Setting**, the pass condition should be written in terms of the mechanism and evidence, not just “sounds good.” The subjective call still matters—it is the product—but the engineering result has to survive comparison.

## The production rule that survived the incident

Use feature-disable tests to isolate causes, then reintroduce required functionality under measurement.

I translate that sentence into an operational rule. The metric or artifact that revealed the failure must remain available in future debug builds, but it must not create the same realtime cost. The known-good binary must remain recoverable. A new audio experiment must identify exactly which layer changed. A release candidate must be tested against the same user-visible behaviors that made the earlier baseline valuable.

This keeps debugging cumulative. Instead of starting every audio complaint with “maybe packet loss” or “maybe AEC,” the next investigation begins with a fault tree and a set of already-proven boundaries. The value of the V115/V127/V132A history is not the version numbers themselves; it is the accumulated map of which measurements are trustworthy and which changes have already regressed the product.

## What I would do differently on the next product

I would design the measurement points earlier. The RTP callback, playout clock, queue, I2S boundary, exact AEC reference, capture slots and acoustic test points would all have named interfaces and low-cost counters from the beginning. That would reduce the amount of forensic reconstruction needed after subjective complaints arrive.

I would also separate debug verbosity from realtime instrumentation by architecture, not convention. Realtime code would update fixed counters or ring-buffer events; a lower-priority task would export summaries. If a UART or network logger can block the media task, the design has already allowed the observer into the deadline path.

For multi-device validation I would automate the call matrix and preserve a compact evidence bundle per run: firmware identity, hardware revision, test endpoint, RTP summary, device timing summary and subjective/acoustic result. The point is not to collect everything. It is to make two runs comparable.

Most importantly, I would preserve the same failure-model discipline. A control experiment removes one subsystem to test causality; it does not automatically define the final architecture. That principle remains true whether the next product uses ESP32-S3, a Linux SoC, a different codec or a cloud media service.

## The result I keep from this incident

AEC-off evidence narrowed the fault domain while the final clear path restored the needed reference/AEC behavior.

The deeper value is the method. I started with a perceptual symptom, located the earliest layer that could create it, chose evidence that could see that layer, changed one variable, and checked the known-good invariants afterward. The process is slower than random tuning for the first build and dramatically faster by the tenth.

The short version of the lesson is: **Use feature-disable tests to isolate causes, then reintroduce required functionality under measurement.**

That is the standard I now use for embedded audio work. A fix is not convincing because the call sounds better once. It is convincing when the mechanism, measurement, artifact identity and regression behavior all agree about why it got better.
