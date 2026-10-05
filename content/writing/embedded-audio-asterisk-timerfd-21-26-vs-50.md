---
title: timerfd Gave Me 21–26 Ticks When I Needed About 50
url: /posts/embedded-audio-asterisk-timerfd-21-26-vs-50.html
date: '2020-04-07'
read_time: 12
excerpt: Asterisk was configured for 20 ms media timing, yet packet forwarding arrived
  in scheduler-sized bursts.
topic: embedded-audio-voice
tags:
- esp32-s3
- embedded-audio
- loup
- rtp
- asterisk
draft: false
featured: false
language: en
eyebrow: 'Embedded Audio Debugging: RTP, PBX & Conversational Latency · deep-dive'
outputs:
- url: /posts/embedded-audio-asterisk-timerfd-21-26-vs-50.html
  template: cms/templates/posts/posts--embedded-audio-asterisk-timerfd-21-26-vs-50.tpl
  source: cms/templates/posts/posts--embedded-audio-asterisk-timerfd-21-26-vs-50.json
---

# timerfd Gave Me 21–26 Ticks When I Needed About 50

One of the easiest ways to lose days in embedded voice work is to collapse several layers into one symptom. In this case, asterisk was configured for 20 ms media timing, yet packet forwarding arrived in scheduler-sized bursts.

The test platform was the LOUP ESP32-S3 voice device with ES8311 playback, ES7210 capture, SIP/RTP media and a small speakerphone enclosure. The network codec was G.711 A-law/PCMA at nominal 8 kHz with 20 ms / 160-byte RTP payloads, while the physical audio path ran at 16 kHz in the recovered playback design. That mismatch between network time, device time and acoustic time is exactly why a vague word like “crackle” is not a diagnosis.

The evidence that matters for this article is specific: The PBX timerfd produced only 21–26 ticks in roughly one second when about 50 were expected for 20 ms cadence. I keep those observations tied to the build and test where they were recorded. They are not universal ESP32 performance claims.

The engineering result was also specific: The timer measurement turned an audio complaint into an OS scheduling investigation. This article is about how I got from the symptom to that bounded conclusion, what the data did not prove, and what I would monitor before touching the same path again.

## How I framed this case

For this experiment I wrote the expected observation before changing code. If the hypothesis was correct, **The PBX timerfd produced only 21–26 ticks in roughly one second when about 50 were expected for 20 ms cadence.** had to move in the predicted direction while unrelated parts of the path stayed stable. The product symptom was Asterisk was configured for 20 ms media timing, yet packet forwarding arrived in scheduler-sized bursts. The technical mechanism was Telephony bridges depend on timely scheduler/timer wakeups; a nominal 20 ms packetization setting is meaningless if the host cannot wake the media thread on schedule. That made **Treating Asterisk configuration values as proof of runtime timing.** a testable alternative rather than a competing story. After the run, I compared the captured evidence with the prediction and accepted only the narrower conclusion: The timer measurement turned an audio complaint into an OS scheduling investigation. This pre-commitment is useful in audio work because subjective listening can otherwise make every new build feel temporarily better.

## Three timelines, not one latency number

I separate RTP media time, capture arrival time and execution time. RTP timestamps show where a packet belongs in the media timeline. PCAP arrival times show when the observation point received it. Firmware monotonic time shows when the device processed or played it. None is automatically synchronized with the microphone or loudspeaker in the room.

The PBX adds its own scheduler. If Asterisk receives a packet and forwards it 80 ms later, the endpoint cannot undo that delay. If the PBX forwards immediately but the ESP32 writes 80 ms later, the fault domain moves. Matched timestamps on both sides of the boundary are therefore more valuable than a single end-to-end “feels delayed” number.

## Case notebook

| Question | Recorded answer |
| --- | --- |
| Symptom | Asterisk was configured for 20 ms media timing, yet packet forwarding arrived in scheduler-sized bursts. |
| Evidence | The PBX timerfd produced only 21–26 ticks in roughly one second when about 50 were expected for 20 ms cadence. |
| Mechanism | Telephony bridges depend on timely scheduler/timer wakeups; a nominal 20 ms packetization setting is meaningless if the host cannot wake the media thread on schedule. |
| Rejected explanation | Treating Asterisk configuration values as proof of runtime timing. |
| Retained result | The timer measurement turned an audio complaint into an OS scheduling investigation. |
| Rule carried forward | Runtime cadence counters are stronger evidence than configuration intent. |

The table is deliberately stricter than a narrative summary. It forces the mechanism and the disproved explanation to live beside the successful result.

A useful follow-up is to ask what would falsify the retained result. For this case, a repeat run on the same controlled topology should reproduce the relevant observation. If **The PBX timerfd produced only 21–26 ticks in roughly one second when about 50 were expected for 20 ms cadence.** disappears while the symptom remains, then the old explanation no longer covers the new incident. If the observation returns without the symptom, then it may be contextual rather than causal. That is why I keep mechanism-level counters beside the listening test.

### Instrumentation sketch

```
for each RTP packet:
  seq_delta       = seq[n] - seq[n-1]
  rtp_time_delta  = ts[n]  - ts[n-1]
  arrival_delta   = cap[n] - cap[n-1]
  pbx_forward_ms  = tx_time[n] - rx_time[n]

sequence answers ordering/loss
RTP timestamp answers media progression
capture time answers arrival/scheduling
none alone equals acoustic mouth-to-ear latency
```

The snippet is not presented as drop-in production code. It documents the measurement model. I want the instrumentation to be cheaper than the deadline it observes, explicit about units, and easy to disable or summarize after the call. The most dangerous diagnostic is one that silently changes scheduler behavior while appearing to measure it.

For **timerfd Gave Me 21–26 Ticks When I Needed About 50**, the next retest would therefore preserve the same topology and change only the variable tied to **Telephony bridges depend on timely scheduler/timer wakeups; a nominal 20 ms packetization setting is meaningless if the host cannot wake the media thread on schedule.**. I would collect the same observation again, compare it with the known-good control, and only then decide whether a new firmware branch deserves to replace the baseline.

## The evidence I trusted

The strongest evidence was: **The PBX timerfd produced only 21–26 ticks in roughly one second when about 50 were expected for 20 ms cadence.**

I try to rank evidence by how close it is to the mechanism. A subjective report is important because it defines the product failure, but it is not enough to choose a patch. A log line is stronger only if the logging path does not perturb the timing being measured. A packet capture is strong for transport questions but weak for acoustics. A binary hash is excellent for identity and useless for explaining timbre. A synchronized measurement is valuable only if the clocks and capture points are understood.

For this investigation I used the evidence as a boundary. It allowed me to say what changed and, just as importantly, what did not change. That distinction prevented the later write-up from turning a plausible story into a fabricated root cause.

The mechanism underneath the observation is straightforward: Telephony bridges depend on timely scheduler/timer wakeups; a nominal 20 ms packetization setting is meaningless if the host cannot wake the media thread on schedule. This is the part I would teach to another firmware engineer before giving them any patch, because without the mechanism the numbers are easy to misread.

## Change one layer, freeze the others

The practical experiment design was to freeze as much of the call path as possible and change the narrowest variable that could test the hypothesis. That meant preserving the SIP identity and call flow, keeping the codec and I2S configuration stable unless they were the subject of the test, using app-only flashes where appropriate, retaining a rollback binary, and capturing the same small set of counters after each call.

For this topic the controlled variable was the mechanism described above, not the entire audio stack. The surrounding rule was: **Runtime cadence counters are stronger evidence than configuration intent.** A change that improves one symptom but also changes AEC, queue depth, volume, sample conversion and logging at once produces a better demo perhaps, but a worse experiment.

I also learned to keep the diagnostic path quiet during the actual call. Counters can increment in RAM. Histograms can accumulate. A summary can print after BYE. That pattern is much safer than serializing kilobytes of task state while a 20 ms media deadline is active. The quiet-V115 work made this principle measurable rather than theoretical.

The acceptance test should therefore include both the perceptual outcome and the mechanism-specific evidence. A call that sounds better but increases slow I2S writes is not automatically a win. A PCAP that looks cleaner while echo becomes objectionable is not a win either. The experiment passes only when the intended layer improves without violating the known-good invariants around it.

## What this result proves—and what it does not

The result I am willing to claim is narrow: **The timer measurement turned an audio complaint into an OS scheduling investigation.** It is supported by the recorded observation: **The PBX timerfd produced only 21–26 ticks in roughly one second when about 50 were expected for 20 ms cadence.**

It does not prove that every LOUP board, every network path or every future firmware build behaves the same way. It does not turn a server-side packet capture into an acoustic measurement. It does not turn a stable AEC-off test into permission to remove AEC from a speakerphone. It does not make a hash a quality metric. Those distinctions sound obvious in hindsight and are easy to lose when a demo deadline rewards a simple story.

The useful causal statement is the one consistent with the mechanism: Telephony bridges depend on timely scheduler/timer wakeups; a nominal 20 ms packetization setting is meaningless if the host cannot wake the media thread on schedule. If another experiment changes that mechanism, I expect the evidence to change too. If the evidence stays the same, I should question the theory before rewriting more code.

I also keep the rejected explanation visible: Treating Asterisk configuration values as proof of runtime timing. That is part of the result. Knowing which layer did *not* create the step change prevents future debugging from starting at the same dead end.

## Reproducing the experiment without changing the experiment

If I had to hand this case to another engineer, I would ask them to preserve the same evidence boundary before attempting a fix:

- capture both receive and forward sides of the PBX where possible
- parse sequence, RTP timestamp and arrival time separately
- measure host scheduler/timer health before changing endpoint queues
- freeze jitter-buffer and endpoint settings for comparisons
- use a same-region PBX before attributing WAN delay to firmware

The point is not ceremony. Embedded audio is sensitive to hidden changes. A different softphone setting, a different PBX region, a new enclosure revision, a verbose log level or a queue added “for safety” can all change the result while leaving the test name unchanged.

For **timerfd Gave Me 21–26 Ticks When I Needed About 50**, the pass condition should be written in terms of the mechanism and evidence, not just “sounds good.” The subjective call still matters—it is the product—but the engineering result has to survive comparison.

## The production rule that survived the incident

Runtime cadence counters are stronger evidence than configuration intent.

I translate that sentence into an operational rule. The metric or artifact that revealed the failure must remain available in future debug builds, but it must not create the same realtime cost. The known-good binary must remain recoverable. A new audio experiment must identify exactly which layer changed. A release candidate must be tested against the same user-visible behaviors that made the earlier baseline valuable.

This keeps debugging cumulative. Instead of starting every audio complaint with “maybe packet loss” or “maybe AEC,” the next investigation begins with a fault tree and a set of already-proven boundaries. The value of the V115/V127/V132A history is not the version numbers themselves; it is the accumulated map of which measurements are trustworthy and which changes have already regressed the product.

## What I would do differently on the next product

I would design the measurement points earlier. The RTP callback, playout clock, queue, I2S boundary, exact AEC reference, capture slots and acoustic test points would all have named interfaces and low-cost counters from the beginning. That would reduce the amount of forensic reconstruction needed after subjective complaints arrive.

I would also separate debug verbosity from realtime instrumentation by architecture, not convention. Realtime code would update fixed counters or ring-buffer events; a lower-priority task would export summaries. If a UART or network logger can block the media task, the design has already allowed the observer into the deadline path.

For multi-device validation I would automate the call matrix and preserve a compact evidence bundle per run: firmware identity, hardware revision, test endpoint, RTP summary, device timing summary and subjective/acoustic result. The point is not to collect everything. It is to make two runs comparable.

Most importantly, I would preserve the same failure-model discipline. Telephony bridges depend on timely scheduler/timer wakeups; a nominal 20 ms packetization setting is meaningless if the host cannot wake the media thread on schedule. That principle remains true whether the next product uses ESP32-S3, a Linux SoC, a different codec or a cloud media service.

## The result I keep from this incident

The timer measurement turned an audio complaint into an OS scheduling investigation.

The deeper value is the method. I started with a perceptual symptom, located the earliest layer that could create it, chose evidence that could see that layer, changed one variable, and checked the known-good invariants afterward. The process is slower than random tuning for the first build and dramatically faster by the tenth.

The short version of the lesson is: **Runtime cadence counters are stronger evidence than configuration intent.**

That is the standard I now use for embedded audio work. A fix is not convincing because the call sounds better once. It is convincing when the mechanism, measurement, artifact identity and regression behavior all agree about why it got better.
