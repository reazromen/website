---
title: The Geography Was Larger Than the Firmware Optimization
url: /posts/embedded-audio-geography-larger-than-firmware-optimization.html
date: '2026-09-15'
read_time: 13
excerpt: Engineering time was being spent chasing tens of milliseconds in firmware
  while the media route crossed Bangladesh and Ohio twice.
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
- url: /posts/embedded-audio-geography-larger-than-firmware-optimization.html
  template: cms/templates/posts/posts--embedded-audio-geography-larger-than-firmware-optimization.tpl
  source: cms/templates/posts/posts--embedded-audio-geography-larger-than-firmware-optimization.json
---

# The Geography Was Larger Than the Firmware Optimization

This part of the LOUP audio investigation began with a deceptively simple symptom: engineering time was being spent chasing tens of milliseconds in firmware while the media route crossed Bangladesh and Ohio twice.

The test platform was the LOUP ESP32-S3 voice device with ES8311 playback, ES7210 capture, SIP/RTP media and a small speakerphone enclosure. The network codec was G.711 A-law/PCMA at nominal 8 kHz with 20 ms / 160-byte RTP payloads, while the physical audio path ran at 16 kHz in the recovered playback design. That mismatch between network time, device time and acoustic time is exactly why a vague word like “crackle” is not a diagnosis.

The evidence that matters for this article is specific: Observed connect-time approximations were about 287.761 ms on one side and 254.427 ms on the other; the recovery memo modeled roughly a 271 ms one-way WAN floor before jitter and endpoint buffers, while warning that TCP connect time is only an approximation. I keep those observations tied to the build and test where they were recorded. They are not universal ESP32 performance claims.

The engineering result was also specific: The next control became local/regional Asterisk with endpoint and firmware settings frozen. This article is about how I got from the symptom to that bounded conclusion, what the data did not prove, and what I would monitor before touching the same path again.

## How I framed this case

The most important design decision here was preserving reversibility. The problem was Engineering time was being spent chasing tens of milliseconds in firmware while the media route crossed Bangladesh and Ohio twice. I kept a known-good control, changed one layer, and required Observed connect-time approximations were about 287.761 ms on one side and 254.427 ms on the other; the recovery memo modeled roughly a 271 ms one-way WAN floor before jitter and endpoint buffers, while warning that TCP connect time is only an approximation. to justify keeping the change. The mechanism was A latency budget prevents local optimization from dominating attention when another layer is an order of magnitude larger. I explicitly avoided Deleting a 20–40 ms playout prime before testing a same-region PBX.. This let me return to the previous baseline when the experiment regressed audio instead of rationalizing the regression as progress. The retained result was The next control became local/regional Asterisk with endpoint and firmware settings frozen. The lesson I would carry to another product is Optimize the largest proven term in the latency budget first, and distinguish approximate network evidence from synchronized one-way measurement.

## Three timelines, not one latency number

I separate RTP media time, capture arrival time and execution time. RTP timestamps show where a packet belongs in the media timeline. PCAP arrival times show when the observation point received it. Firmware monotonic time shows when the device processed or played it. None is automatically synchronized with the microphone or loudspeaker in the room.

The PBX adds its own scheduler. If Asterisk receives a packet and forwards it 80 ms later, the endpoint cannot undo that delay. If the PBX forwards immediately but the ESP32 writes 80 ms later, the fault domain moves. Matched timestamps on both sides of the boundary are therefore more valuable than a single end-to-end “feels delayed” number.

## Case notebook

| Question | Recorded answer |
| --- | --- |
| Symptom | Engineering time was being spent chasing tens of milliseconds in firmware while the media route crossed Bangladesh and Ohio twice. |
| Evidence | Observed connect-time approximations were about 287.761 ms on one side and 254.427 ms on the other; the recovery memo modeled roughly a 271 ms one-way WAN floor before jitter and endpoint buffers, while warning that TCP connect time is only an approximation. |
| Mechanism | A latency budget prevents local optimization from dominating attention when another layer is an order of magnitude larger. |
| Rejected explanation | Deleting a 20–40 ms playout prime before testing a same-region PBX. |
| Retained result | The next control became local/regional Asterisk with endpoint and firmware settings frozen. |
| Rule carried forward | Optimize the largest proven term in the latency budget first, and distinguish approximate network evidence from synchronized one-way measurement. |

The rule carried forward is the part I want to survive the specific firmware version. Version numbers change; the debugging invariant should not.

A useful follow-up is to ask what would falsify the retained result. For this case, a repeat run on the same controlled topology should reproduce the relevant observation. If **Observed connect-time approximations were about 287.761 ms on one side and 254.427 ms on the other; the recovery memo modeled roughly a 271 ms one-way WAN floor before jitter and endpoint buffers, while warning that TCP connect time is only an approximation.** disappears while the symptom remains, then the old explanation no longer covers the new incident. If the observation returns without the symptom, then it may be contextual rather than causal. That is why I keep mechanism-level counters beside the listening test.

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

For **The Geography Was Larger Than the Firmware Optimization**, the next retest would therefore preserve the same topology and change only the variable tied to **A latency budget prevents local optimization from dominating attention when another layer is an order of magnitude larger.**. I would collect the same observation again, compare it with the known-good control, and only then decide whether a new firmware branch deserves to replace the baseline.

## Tools were chosen by the question, not by habit

The useful toolset for this layer was tcpdump/Wireshark/tshark-compatible RTP parsing, PBX scheduler/timer measurements, vmstat and matched receive/forward timestamps. I did not expect one tool to explain the whole call.

When the question was packet loss, I looked at RTP sequence and timestamps. When the question was device scheduling, I looked at monotonic callback and I2S timing. When the question was build identity, I used hashes and preserved artifacts. When the question was echo or timbre, packet capture stopped at the digital boundary and the next test had to include the physical speaker/microphone path.

That separation matters because every tool has a blind spot. UART logs can perturb timing. PCAP cannot hear the room. Far-end listening cannot prove which queue grew. Docker/Asterisk logs cannot prove the ESP32 played a sample. A codec detection scan cannot prove the channel mapping matches the DSP assumptions. The tool is evidence only for the layer it can actually observe.

This is also why I prefer small, named counters over giant debug dumps in realtime code. A counter such as “writes over 20 ms,” “max callback gap,” “queue underrun,” or “first callback to I2S start” has a defined semantic. It can be compared across builds without parsing thousands of lines whose own output may change the result.

## The evidence I trusted

The strongest evidence was: **Observed connect-time approximations were about 287.761 ms on one side and 254.427 ms on the other; the recovery memo modeled roughly a 271 ms one-way WAN floor before jitter and endpoint buffers, while warning that TCP connect time is only an approximation.**

I try to rank evidence by how close it is to the mechanism. A subjective report is important because it defines the product failure, but it is not enough to choose a patch. A log line is stronger only if the logging path does not perturb the timing being measured. A packet capture is strong for transport questions but weak for acoustics. A binary hash is excellent for identity and useless for explaining timbre. A synchronized measurement is valuable only if the clocks and capture points are understood.

For this investigation I used the evidence as a boundary. It allowed me to say what changed and, just as importantly, what did not change. That distinction prevented the later write-up from turning a plausible story into a fabricated root cause.

The mechanism underneath the observation is straightforward: A latency budget prevents local optimization from dominating attention when another layer is an order of magnitude larger. This is the part I would teach to another firmware engineer before giving them any patch, because without the mechanism the numbers are easy to misread.

## What this result proves—and what it does not

The result I am willing to claim is narrow: **The next control became local/regional Asterisk with endpoint and firmware settings frozen.** It is supported by the recorded observation: **Observed connect-time approximations were about 287.761 ms on one side and 254.427 ms on the other; the recovery memo modeled roughly a 271 ms one-way WAN floor before jitter and endpoint buffers, while warning that TCP connect time is only an approximation.**

It does not prove that every LOUP board, every network path or every future firmware build behaves the same way. It does not turn a server-side packet capture into an acoustic measurement. It does not turn a stable AEC-off test into permission to remove AEC from a speakerphone. It does not make a hash a quality metric. Those distinctions sound obvious in hindsight and are easy to lose when a demo deadline rewards a simple story.

The useful causal statement is the one consistent with the mechanism: A latency budget prevents local optimization from dominating attention when another layer is an order of magnitude larger. If another experiment changes that mechanism, I expect the evidence to change too. If the evidence stays the same, I should question the theory before rewriting more code.

I also keep the rejected explanation visible: Deleting a 20–40 ms playout prime before testing a same-region PBX. That is part of the result. Knowing which layer did *not* create the step change prevents future debugging from starting at the same dead end.

## Reproducing the experiment without changing the experiment

If I had to hand this case to another engineer, I would ask them to preserve the same evidence boundary before attempting a fix:

- capture both receive and forward sides of the PBX where possible
- parse sequence, RTP timestamp and arrival time separately
- measure host scheduler/timer health before changing endpoint queues
- freeze jitter-buffer and endpoint settings for comparisons
- use a same-region PBX before attributing WAN delay to firmware

The point is not ceremony. Embedded audio is sensitive to hidden changes. A different softphone setting, a different PBX region, a new enclosure revision, a verbose log level or a queue added “for safety” can all change the result while leaving the test name unchanged.

For **The Geography Was Larger Than the Firmware Optimization**, the pass condition should be written in terms of the mechanism and evidence, not just “sounds good.” The subjective call still matters—it is the product—but the engineering result has to survive comparison.

## The production rule that survived the incident

Optimize the largest proven term in the latency budget first, and distinguish approximate network evidence from synchronized one-way measurement.

I translate that sentence into an operational rule. The metric or artifact that revealed the failure must remain available in future debug builds, but it must not create the same realtime cost. The known-good binary must remain recoverable. A new audio experiment must identify exactly which layer changed. A release candidate must be tested against the same user-visible behaviors that made the earlier baseline valuable.

This keeps debugging cumulative. Instead of starting every audio complaint with “maybe packet loss” or “maybe AEC,” the next investigation begins with a fault tree and a set of already-proven boundaries. The value of the V115/V127/V132A history is not the version numbers themselves; it is the accumulated map of which measurements are trustworthy and which changes have already regressed the product.

## What I would do differently on the next product

I would design the measurement points earlier. The RTP callback, playout clock, queue, I2S boundary, exact AEC reference, capture slots and acoustic test points would all have named interfaces and low-cost counters from the beginning. That would reduce the amount of forensic reconstruction needed after subjective complaints arrive.

I would also separate debug verbosity from realtime instrumentation by architecture, not convention. Realtime code would update fixed counters or ring-buffer events; a lower-priority task would export summaries. If a UART or network logger can block the media task, the design has already allowed the observer into the deadline path.

For multi-device validation I would automate the call matrix and preserve a compact evidence bundle per run: firmware identity, hardware revision, test endpoint, RTP summary, device timing summary and subjective/acoustic result. The point is not to collect everything. It is to make two runs comparable.

Most importantly, I would preserve the same failure-model discipline. A latency budget prevents local optimization from dominating attention when another layer is an order of magnitude larger. That principle remains true whether the next product uses ESP32-S3, a Linux SoC, a different codec or a cloud media service.

## The result I keep from this incident

The next control became local/regional Asterisk with endpoint and firmware settings frozen.

The deeper value is the method. I started with a perceptual symptom, located the earliest layer that could create it, chose evidence that could see that layer, changed one variable, and checked the known-good invariants afterward. The process is slower than random tuning for the first build and dramatically faster by the tenth.

The short version of the lesson is: **Optimize the largest proven term in the latency budget first, and distinguish approximate network evidence from synchronized one-way measurement.**

That is the standard I now use for embedded audio work. A fix is not convincing because the call sounds better once. It is convincing when the mechanism, measurement, artifact identity and regression behavior all agree about why it got better.
