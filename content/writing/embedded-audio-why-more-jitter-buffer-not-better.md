---
title: Why More Jitter Buffer Was Not Automatically Better
url: /posts/embedded-audio-why-more-jitter-buffer-not-better.html
date: '2026-09-15'
read_time: 12
excerpt: Increasing jitter tolerance seemed like the obvious response to bursty packet
  arrival.
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
- url: /posts/embedded-audio-why-more-jitter-buffer-not-better.html
  template: cms/templates/posts/posts--embedded-audio-why-more-jitter-buffer-not-better.tpl
  source: cms/templates/posts/posts--embedded-audio-why-more-jitter-buffer-not-better.json
---

# Why More Jitter Buffer Was Not Automatically Better

One of the easiest ways to lose days in embedded voice work is to collapse several layers into one symptom. In this case, increasing jitter tolerance seemed like the obvious response to bursty packet arrival.

The test platform was the LOUP ESP32-S3 voice device with ES8311 playback, ES7210 capture, SIP/RTP media and a small speakerphone enclosure. The network codec was G.711 A-law/PCMA at nominal 8 kHz with 20 ms / 160-byte RTP payloads, while the physical audio path ran at 16 kHz in the recovered playback design. That mismatch between network time, device time and acoustic time is exactly why a vague word like “crackle” is not a diagnosis.

The evidence that matters for this article is specific: JB100 added roughly a 20 ms target de-jitter delay and produced bounded forwarding; JB200 increased subjective lag while isolated loss/reorder still remained, so the larger setting was reverted. I keep those observations tied to the build and test where they were recorded. They are not universal ESP32 performance claims.

The engineering result was also specific: The accepted configuration favored bounded jitter absorption instead of maximum buffering. This article is about how I got from the symptom to that bounded conclusion, what the data did not prove, and what I would monitor before touching the same path again.

## How I framed this case

The most important design decision here was preserving reversibility. The problem was Increasing jitter tolerance seemed like the obvious response to bursty packet arrival. I kept a known-good control, changed one layer, and required JB100 added roughly a 20 ms target de-jitter delay and produced bounded forwarding; JB200 increased subjective lag while isolated loss/reorder still remained, so the larger setting was reverted. to justify keeping the change. The mechanism was A jitter buffer trades latency for resilience; it can reorder or absorb variation but cannot recreate packets that never arrive. I explicitly avoided Assuming a deeper queue can solve packet loss, scheduler starvation and acoustic problems simultaneously.. This let me return to the previous baseline when the experiment regressed audio instead of rationalizing the regression as progress. The retained result was The accepted configuration favored bounded jitter absorption instead of maximum buffering. The lesson I would carry to another product is Buffer depth is a product latency decision, not simply a reliability knob.

## Deadline math I use for playout

With nominal 20 ms telephony frames, I treat one frame as a useful unit of budget, not a guarantee of arrival. A receive callback can be early, late or bursty; the speaker still needs continuous samples. I therefore distinguish arrival-gap statistics from local callback-to-I2S time and from I2S write duration. They answer three separate questions: what the network delivered, how quickly firmware reacted, and whether the output boundary blocked.

For long calls I add drift. If the local playout clock differs from the media production rate, the queue can slowly walk even when every individual write is fast. That is why a short “no cutout” test and a long stability test are complementary rather than redundant.

## Case notebook

| Question | Recorded answer |
| --- | --- |
| Symptom | Increasing jitter tolerance seemed like the obvious response to bursty packet arrival. |
| Evidence | JB100 added roughly a 20 ms target de-jitter delay and produced bounded forwarding; JB200 increased subjective lag while isolated loss/reorder still remained, so the larger setting was reverted. |
| Mechanism | A jitter buffer trades latency for resilience; it can reorder or absorb variation but cannot recreate packets that never arrive. |
| Rejected explanation | Assuming a deeper queue can solve packet loss, scheduler starvation and acoustic problems simultaneously. |
| Retained result | The accepted configuration favored bounded jitter absorption instead of maximum buffering. |
| Rule carried forward | Buffer depth is a product latency decision, not simply a reliability knob. |

The rule carried forward is the part I want to survive the specific firmware version. Version numbers change; the debugging invariant should not.

A useful follow-up is to ask what would falsify the retained result. For this case, a repeat run on the same controlled topology should reproduce the relevant observation. If **JB100 added roughly a 20 ms target de-jitter delay and produced bounded forwarding; JB200 increased subjective lag while isolated loss/reorder still remained, so the larger setting was reverted.** disappears while the symptom remains, then the old explanation no longer covers the new incident. If the observation returns without the symptom, then it may be contextual rather than causal. That is why I keep mechanism-level counters beside the listening test.

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

For **Why More Jitter Buffer Was Not Automatically Better**, the next retest would therefore preserve the same topology and change only the variable tied to **A jitter buffer trades latency for resilience; it can reorder or absorb variation but cannot recreate packets that never arrive.**. I would collect the same observation again, compare it with the known-good control, and only then decide whether a new firmware branch deserves to replace the baseline.

## How I interpret the numbers

The measurements in this series are deliberately tied to their recorded tests. They describe one board, one firmware revision, one network path and one observation window unless the evidence says otherwise. I do not turn 0.457 ms into a product-wide latency claim, or 175.6 seconds into proof of indefinite stability, or a 20–28 ms network variation into a codec property.

I use distributions and boundaries wherever possible. A maximum speaker write tells me a deadline was missed, while incidence tells me how common the miss was. Packet p50/p95/p99 and maximum gaps reveal whether a path is usually healthy with isolated excursions or continuously unstable. Drift is a slope, not a single latency. AEC-off stability is a control result, not a shipping configuration. A binary hash proves identity, not quality.

For **Why More Jitter Buffer Was Not Automatically Better**, the important interpretation is: A jitter buffer trades latency for resilience; it can reorder or absorb variation but cannot recreate packets that never arrive. The number is useful only because it narrows the fault domain.

When exact current data is not available, I would rather repeat the test than invent a value. The same applies to acoustic latency: without synchronized physical capture, the correct statement is that the network/device measurements bound parts of the delay, not that they measure mouth-to-ear time.

## The tempting explanation I did not accept

The attractive wrong turn was: **Assuming a deeper queue can solve packet loss, scheduler starvation and acoustic problems simultaneously.**

Embedded audio is full of these traps because many failure modes sound alike. Packet bursts, resampler artifacts, AEC suppression, output starvation, clipping and acoustic echo can all be described as “robotic” by a listener. A large queue can hide packet jitter while making conversation sluggish. Turning AEC off can remove one processing cost while making the product unusable as a speakerphone. A warning in the log can look causal simply because it is the only visible abnormality.

The rule I now use is that a theory must predict another observable fact. If I believe packet loss is causing a missing word, I should find the corresponding sequence gap or payload absence before the device. If I believe I2S is stalling, speaker-write timing should show it. If I believe the PBX is batching media, its receive/forward timestamps should expose the batch before the ESP32 sees it. If I believe echo is acoustic, changing volume or geometry should change the failure even when packet timing remains stable.

This is slower than guessing for the first ten minutes and much faster than carrying a wrong theory through ten firmware versions.

## What this result proves—and what it does not

The result I am willing to claim is narrow: **The accepted configuration favored bounded jitter absorption instead of maximum buffering.** It is supported by the recorded observation: **JB100 added roughly a 20 ms target de-jitter delay and produced bounded forwarding; JB200 increased subjective lag while isolated loss/reorder still remained, so the larger setting was reverted.**

It does not prove that every LOUP board, every network path or every future firmware build behaves the same way. It does not turn a server-side packet capture into an acoustic measurement. It does not turn a stable AEC-off test into permission to remove AEC from a speakerphone. It does not make a hash a quality metric. Those distinctions sound obvious in hindsight and are easy to lose when a demo deadline rewards a simple story.

The useful causal statement is the one consistent with the mechanism: A jitter buffer trades latency for resilience; it can reorder or absorb variation but cannot recreate packets that never arrive. If another experiment changes that mechanism, I expect the evidence to change too. If the evidence stays the same, I should question the theory before rewriting more code.

I also keep the rejected explanation visible: Assuming a deeper queue can solve packet loss, scheduler starvation and acoustic problems simultaneously. That is part of the result. Knowing which layer did *not* create the step change prevents future debugging from starting at the same dead end.

## Reproducing the experiment without changing the experiment

If I had to hand this case to another engineer, I would ask them to preserve the same evidence boundary before attempting a fix:

- quiet the call hot path before measuring it
- record callback gaps and speaker-write duration in RAM
- capture queue/underrun state without per-frame printing
- run a short quality call and a longer drift call
- compare against the same known-good playout path

The point is not ceremony. Embedded audio is sensitive to hidden changes. A different softphone setting, a different PBX region, a new enclosure revision, a verbose log level or a queue added “for safety” can all change the result while leaving the test name unchanged.

For **Why More Jitter Buffer Was Not Automatically Better**, the pass condition should be written in terms of the mechanism and evidence, not just “sounds good.” The subjective call still matters—it is the product—but the engineering result has to survive comparison.

## The production rule that survived the incident

Buffer depth is a product latency decision, not simply a reliability knob.

I translate that sentence into an operational rule. The metric or artifact that revealed the failure must remain available in future debug builds, but it must not create the same realtime cost. The known-good binary must remain recoverable. A new audio experiment must identify exactly which layer changed. A release candidate must be tested against the same user-visible behaviors that made the earlier baseline valuable.

This keeps debugging cumulative. Instead of starting every audio complaint with “maybe packet loss” or “maybe AEC,” the next investigation begins with a fault tree and a set of already-proven boundaries. The value of the V115/V127/V132A history is not the version numbers themselves; it is the accumulated map of which measurements are trustworthy and which changes have already regressed the product.

## What I would do differently on the next product

I would design the measurement points earlier. The RTP callback, playout clock, queue, I2S boundary, exact AEC reference, capture slots and acoustic test points would all have named interfaces and low-cost counters from the beginning. That would reduce the amount of forensic reconstruction needed after subjective complaints arrive.

I would also separate debug verbosity from realtime instrumentation by architecture, not convention. Realtime code would update fixed counters or ring-buffer events; a lower-priority task would export summaries. If a UART or network logger can block the media task, the design has already allowed the observer into the deadline path.

For multi-device validation I would automate the call matrix and preserve a compact evidence bundle per run: firmware identity, hardware revision, test endpoint, RTP summary, device timing summary and subjective/acoustic result. The point is not to collect everything. It is to make two runs comparable.

Most importantly, I would preserve the same failure-model discipline. A jitter buffer trades latency for resilience; it can reorder or absorb variation but cannot recreate packets that never arrive. That principle remains true whether the next product uses ESP32-S3, a Linux SoC, a different codec or a cloud media service.

## The result I keep from this incident

The accepted configuration favored bounded jitter absorption instead of maximum buffering.

The deeper value is the method. I started with a perceptual symptom, located the earliest layer that could create it, chose evidence that could see that layer, changed one variable, and checked the known-good invariants afterward. The process is slower than random tuning for the first build and dramatically faster by the tenth.

The short version of the lesson is: **Buffer depth is a product latency decision, not simply a reliability knob.**

That is the standard I now use for embedded audio work. A fix is not convincing because the call sounds better once. It is convincing when the mechanism, measurement, artifact identity and regression behavior all agree about why it got better.
