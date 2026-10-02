---
title: The Measurement Stack That Made Subjective Audio Debuggable
url: /posts/embedded-audio-measurement-stack-for-subjective-audio.html
date: '2026-09-15'
read_time: 12
excerpt: Words like robotic, delayed and crackly were useful user reports but poor
  root-cause evidence.
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
- url: /posts/embedded-audio-measurement-stack-for-subjective-audio.html
  template: cms/templates/posts/posts--embedded-audio-measurement-stack-for-subjective-audio.tpl
  source: cms/templates/posts/posts--embedded-audio-measurement-stack-for-subjective-audio.json
---

# The Measurement Stack That Made Subjective Audio Debuggable

This part of the LOUP audio investigation began with a deceptively simple symptom: words like robotic, delayed and crackly were useful user reports but poor root-cause evidence.

The test platform was the LOUP ESP32-S3 voice device with ES8311 playback, ES7210 capture, SIP/RTP media and a small speakerphone enclosure. The network codec was G.711 A-law/PCMA at nominal 8 kHz with 20 ms / 160-byte RTP payloads, while the physical audio path ran at 16 kHz in the recovered playback design. That mismatch between network time, device time and acoustic time is exactly why a vague word like “crackle” is not a diagnosis.

The evidence that matters for this article is specific: The working evidence stack combined synchronized UART logs, firmware counters, I2S write timing, RTP PCAPs, hashes, far-end listening and controlled call repetition. I keep those observations tied to the build and test where they were recorded. They are not universal ESP32 performance claims.

The engineering result was also specific: The team could correlate what was heard with what the network and firmware actually did. This article is about how I got from the symptom to that bounded conclusion, what the data did not prove, and what I would monitor before touching the same path again.

## How I framed this case

This case is a useful example of negative evidence. The system contained a suspicious condition, but suspicion is not causality. The observed problem was Words like robotic, delayed and crackly were useful user reports but poor root-cause evidence. The candidate explanation was Adding more verbose logs to compensate for uncertainty.. I looked for the consequence that explanation should create and compared it with The working evidence stack combined synchronized UART logs, firmware counters, I2S write timing, RTP PCAPs, hashes, far-end listening and controlled call repetition.. The deeper mechanism—Different tools observe different state: firmware timing sees local stalls, PCAP sees transport, listening sees perceptual quality, hashes preserve experimental identity.—showed why the relationship was weaker than it first appeared. The final result was The team could correlate what was heard with what the network and firmware actually did. The important outcome was not just a fix; it was permission to stop spending time on a theory that the data no longer supported.

## Evidence engineering for firmware audio

I now keep three identities together for important audio tests: the executable artifact, the source state and the observation bundle. A filename is not identity. A Git branch is not necessarily the binary running on the board. A PCAP without the matching call log can still be useful, but it is weaker evidence for cross-layer timing. The recovery work became much easier after every important experiment could answer “which exact behavior did we run?” before answering “did it sound better?”

This is also why I preserve failed hypotheses. If a warning, queue theory or codec suspicion was tested and did not explain the step change, that negative result belongs beside the final fix. Otherwise the same theory returns in a later chat, branch or handoff and consumes the same debugging time again.

## Case notebook

| Question | Recorded answer |
| --- | --- |
| Symptom | Words like robotic, delayed and crackly were useful user reports but poor root-cause evidence. |
| Evidence | The working evidence stack combined synchronized UART logs, firmware counters, I2S write timing, RTP PCAPs, hashes, far-end listening and controlled call repetition. |
| Mechanism | Different tools observe different state: firmware timing sees local stalls, PCAP sees transport, listening sees perceptual quality, hashes preserve experimental identity. |
| Rejected explanation | Adding more verbose logs to compensate for uncertainty. |
| Retained result | The team could correlate what was heard with what the network and firmware actually did. |
| Rule carried forward | Subjective quality becomes engineerable when each perceptual complaint has at least one independent instrumentation path. |

Keeping the rejected explanation in the same record is important. Audio teams otherwise rediscover the same plausible theory every few weeks.

A useful follow-up is to ask what would falsify the retained result. For this case, a repeat run on the same controlled topology should reproduce the relevant observation. If **The working evidence stack combined synchronized UART logs, firmware counters, I2S write timing, RTP PCAPs, hashes, far-end listening and controlled call repetition.** disappears while the symptom remains, then the old explanation no longer covers the new incident. If the observation returns without the symptom, then it may be contextual rather than causal. That is why I keep mechanism-level counters beside the listening test.

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

For **The Measurement Stack That Made Subjective Audio Debuggable**, the next retest would therefore preserve the same topology and change only the variable tied to **Different tools observe different state: firmware timing sees local stalls, PCAP sees transport, listening sees perceptual quality, hashes preserve experimental identity.**. I would collect the same observation again, compare it with the known-good control, and only then decide whether a new firmware branch deserves to replace the baseline.

## Tools were chosen by the question, not by habit

The useful toolset for this layer was SHA-256 identity, isolated source trees, esp-idf-monitor, PCAP parsing, synchronized notes and explicit proof-status tables. I did not expect one tool to explain the whole call.

When the question was packet loss, I looked at RTP sequence and timestamps. When the question was device scheduling, I looked at monotonic callback and I2S timing. When the question was build identity, I used hashes and preserved artifacts. When the question was echo or timbre, packet capture stopped at the digital boundary and the next test had to include the physical speaker/microphone path.

That separation matters because every tool has a blind spot. UART logs can perturb timing. PCAP cannot hear the room. Far-end listening cannot prove which queue grew. Docker/Asterisk logs cannot prove the ESP32 played a sample. A codec detection scan cannot prove the channel mapping matches the DSP assumptions. The tool is evidence only for the layer it can actually observe.

This is also why I prefer small, named counters over giant debug dumps in realtime code. A counter such as “writes over 20 ms,” “max callback gap,” “queue underrun,” or “first callback to I2S start” has a defined semantic. It can be compared across builds without parsing thousands of lines whose own output may change the result.

## The evidence I trusted

The strongest evidence was: **The working evidence stack combined synchronized UART logs, firmware counters, I2S write timing, RTP PCAPs, hashes, far-end listening and controlled call repetition.**

I try to rank evidence by how close it is to the mechanism. A subjective report is important because it defines the product failure, but it is not enough to choose a patch. A log line is stronger only if the logging path does not perturb the timing being measured. A packet capture is strong for transport questions but weak for acoustics. A binary hash is excellent for identity and useless for explaining timbre. A synchronized measurement is valuable only if the clocks and capture points are understood.

For this investigation I used the evidence as a boundary. It allowed me to say what changed and, just as importantly, what did not change. That distinction prevented the later write-up from turning a plausible story into a fabricated root cause.

The mechanism underneath the observation is straightforward: Different tools observe different state: firmware timing sees local stalls, PCAP sees transport, listening sees perceptual quality, hashes preserve experimental identity. This is the part I would teach to another firmware engineer before giving them any patch, because without the mechanism the numbers are easy to misread.

## What this result proves—and what it does not

The result I am willing to claim is narrow: **The team could correlate what was heard with what the network and firmware actually did.** It is supported by the recorded observation: **The working evidence stack combined synchronized UART logs, firmware counters, I2S write timing, RTP PCAPs, hashes, far-end listening and controlled call repetition.**

It does not prove that every LOUP board, every network path or every future firmware build behaves the same way. It does not turn a server-side packet capture into an acoustic measurement. It does not turn a stable AEC-off test into permission to remove AEC from a speakerphone. It does not make a hash a quality metric. Those distinctions sound obvious in hindsight and are easy to lose when a demo deadline rewards a simple story.

The useful causal statement is the one consistent with the mechanism: Different tools observe different state: firmware timing sees local stalls, PCAP sees transport, listening sees perceptual quality, hashes preserve experimental identity. If another experiment changes that mechanism, I expect the evidence to change too. If the evidence stays the same, I should question the theory before rewriting more code.

I also keep the rejected explanation visible: Adding more verbose logs to compensate for uncertainty. That is part of the result. Knowing which layer did *not* create the step change prevents future debugging from starting at the same dead end.

## Reproducing the experiment without changing the experiment

If I had to hand this case to another engineer, I would ask them to preserve the same evidence boundary before attempting a fix:

- freeze the known-good binary and source identity
- capture the exact test topology
- use monotonic timing where wall clocks are unreliable
- hash PCAP/log artifacts before analysis
- record disproved hypotheses beside accepted conclusions

The point is not ceremony. Embedded audio is sensitive to hidden changes. A different softphone setting, a different PBX region, a new enclosure revision, a verbose log level or a queue added “for safety” can all change the result while leaving the test name unchanged.

For **The Measurement Stack That Made Subjective Audio Debuggable**, the pass condition should be written in terms of the mechanism and evidence, not just “sounds good.” The subjective call still matters—it is the product—but the engineering result has to survive comparison.

## The production rule that survived the incident

Subjective quality becomes engineerable when each perceptual complaint has at least one independent instrumentation path.

I translate that sentence into an operational rule. The metric or artifact that revealed the failure must remain available in future debug builds, but it must not create the same realtime cost. The known-good binary must remain recoverable. A new audio experiment must identify exactly which layer changed. A release candidate must be tested against the same user-visible behaviors that made the earlier baseline valuable.

This keeps debugging cumulative. Instead of starting every audio complaint with “maybe packet loss” or “maybe AEC,” the next investigation begins with a fault tree and a set of already-proven boundaries. The value of the V115/V127/V132A history is not the version numbers themselves; it is the accumulated map of which measurements are trustworthy and which changes have already regressed the product.

## What I would do differently on the next product

I would design the measurement points earlier. The RTP callback, playout clock, queue, I2S boundary, exact AEC reference, capture slots and acoustic test points would all have named interfaces and low-cost counters from the beginning. That would reduce the amount of forensic reconstruction needed after subjective complaints arrive.

I would also separate debug verbosity from realtime instrumentation by architecture, not convention. Realtime code would update fixed counters or ring-buffer events; a lower-priority task would export summaries. If a UART or network logger can block the media task, the design has already allowed the observer into the deadline path.

For multi-device validation I would automate the call matrix and preserve a compact evidence bundle per run: firmware identity, hardware revision, test endpoint, RTP summary, device timing summary and subjective/acoustic result. The point is not to collect everything. It is to make two runs comparable.

Most importantly, I would preserve the same failure-model discipline. Different tools observe different state: firmware timing sees local stalls, PCAP sees transport, listening sees perceptual quality, hashes preserve experimental identity. That principle remains true whether the next product uses ESP32-S3, a Linux SoC, a different codec or a cloud media service.

## The result I keep from this incident

The team could correlate what was heard with what the network and firmware actually did.

The deeper value is the method. I started with a perceptual symptom, located the earliest layer that could create it, chose evidence that could see that layer, changed one variable, and checked the known-good invariants afterward. The process is slower than random tuning for the first build and dramatically faster by the tenth.

The short version of the lesson is: **Subjective quality becomes engineerable when each perceptual complaint has at least one independent instrumentation path.**

That is the standard I now use for embedded audio work. A fix is not convincing because the call sounds better once. It is convincing when the mechanism, measurement, artifact identity and regression behavior all agree about why it got better.
