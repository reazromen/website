---
title: Speaker Writes Over 20 ms Became My Local Deadline Signal
url: /posts/embedded-audio-speaker-writes-over-20ms-deadline-signal.html
date: '2024-09-26'
read_time: 12
excerpt: Crackle and cutouts needed a device-side timing metric that was closer to
  the DAC than packet arrival.
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
- url: /posts/embedded-audio-speaker-writes-over-20ms-deadline-signal.html
  template: cms/templates/posts/posts--embedded-audio-speaker-writes-over-20ms-deadline-signal.tpl
  source: cms/templates/posts/posts--embedded-audio-speaker-writes-over-20ms-deadline-signal.json
---

# Speaker Writes Over 20 ms Became My Local Deadline Signal

This part of the LOUP audio investigation began with a deceptively simple symptom: crackle and cutouts needed a device-side timing metric that was closer to the DAC than packet arrival.

The test platform was the LOUP ESP32-S3 voice device with ES8311 playback, ES7210 capture, SIP/RTP media and a small speakerphone enclosure. The network codec was G.711 A-law/PCMA at nominal 8 kHz with 20 ms / 160-byte RTP payloads, while the physical audio path ran at 16 kHz in the recovered playback design. That mismatch between network time, device time and acoustic time is exactly why a vague word like “crackle” is not a diagnosis.

The evidence that matters for this article is specific: The V115 recovery tracked I2S speaker-write durations and counted >20 ms events, including a verbose maximum around 123 ms and a quiet-candidate maximum around 24.9 ms. I keep those observations tied to the build and test where they were recorded. They are not universal ESP32 performance claims.

The engineering result was also specific: Slow-write incidence became a direct regression metric for hot-path changes. This article is about how I got from the symptom to that bounded conclusion, what the data did not prove, and what I would monitor before touching the same path again.

## How I framed this case

For this experiment I wrote the expected observation before changing code. If the hypothesis was correct, **The V115 recovery tracked I2S speaker-write durations and counted >20 ms events, including a verbose maximum around 123 ms and a quiet-candidate maximum around 24.9 ms.** had to move in the predicted direction while unrelated parts of the path stayed stable. The product symptom was Crackle and cutouts needed a device-side timing metric that was closer to the DAC than packet arrival. The technical mechanism was A 20 ms PCMA packet cadence creates a natural timing budget; output operations that routinely consume or block beyond one frame can destabilize playout. That made **Using only average task CPU or queue depth to infer real-time behavior.** a testable alternative rather than a competing story. After the run, I compared the captured evidence with the prediction and accepted only the narrower conclusion: Slow-write incidence became a direct regression metric for hot-path changes. This pre-commitment is useful in audio work because subjective listening can otherwise make every new build feel temporarily better.

## Deadline math I use for playout

With nominal 20 ms telephony frames, I treat one frame as a useful unit of budget, not a guarantee of arrival. A receive callback can be early, late or bursty; the speaker still needs continuous samples. I therefore distinguish arrival-gap statistics from local callback-to-I2S time and from I2S write duration. They answer three separate questions: what the network delivered, how quickly firmware reacted, and whether the output boundary blocked.

For long calls I add drift. If the local playout clock differs from the media production rate, the queue can slowly walk even when every individual write is fast. That is why a short “no cutout” test and a long stability test are complementary rather than redundant.

## Case notebook

| Question | Recorded answer |
| --- | --- |
| Symptom | Crackle and cutouts needed a device-side timing metric that was closer to the DAC than packet arrival. |
| Evidence | The V115 recovery tracked I2S speaker-write durations and counted >20 ms events, including a verbose maximum around 123 ms and a quiet-candidate maximum around 24.9 ms. |
| Mechanism | A 20 ms PCMA packet cadence creates a natural timing budget; output operations that routinely consume or block beyond one frame can destabilize playout. |
| Rejected explanation | Using only average task CPU or queue depth to infer real-time behavior. |
| Retained result | Slow-write incidence became a direct regression metric for hot-path changes. |
| Rule carried forward | Choose timing counters at the physical-output boundary, not only at the network callback. |

The table is deliberately stricter than a narrative summary. It forces the mechanism and the disproved explanation to live beside the successful result.

A useful follow-up is to ask what would falsify the retained result. For this case, a repeat run on the same controlled topology should reproduce the relevant observation. If **The V115 recovery tracked I2S speaker-write durations and counted >20 ms events, including a verbose maximum around 123 ms and a quiet-candidate maximum around 24.9 ms.** disappears while the symptom remains, then the old explanation no longer covers the new incident. If the observation returns without the symptom, then it may be contextual rather than causal. That is why I keep mechanism-level counters beside the listening test.

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

For **Speaker Writes Over 20 ms Became My Local Deadline Signal**, the next retest would therefore preserve the same topology and change only the variable tied to **A 20 ms PCMA packet cadence creates a natural timing budget; output operations that routinely consume or block beyond one frame can destabilize playout.**. I would collect the same observation again, compare it with the known-good control, and only then decide whether a new firmware branch deserves to replace the baseline.

## The tempting explanation I did not accept

The attractive wrong turn was: **Using only average task CPU or queue depth to infer real-time behavior.**

Embedded audio is full of these traps because many failure modes sound alike. Packet bursts, resampler artifacts, AEC suppression, output starvation, clipping and acoustic echo can all be described as “robotic” by a listener. A large queue can hide packet jitter while making conversation sluggish. Turning AEC off can remove one processing cost while making the product unusable as a speakerphone. A warning in the log can look causal simply because it is the only visible abnormality.

The rule I now use is that a theory must predict another observable fact. If I believe packet loss is causing a missing word, I should find the corresponding sequence gap or payload absence before the device. If I believe I2S is stalling, speaker-write timing should show it. If I believe the PBX is batching media, its receive/forward timestamps should expose the batch before the ESP32 sees it. If I believe echo is acoustic, changing volume or geometry should change the failure even when packet timing remains stable.

This is slower than guessing for the first ten minutes and much faster than carrying a wrong theory through ten firmware versions.

## Tools were chosen by the question, not by habit

The useful toolset for this layer was monotonic microsecond timers, callback-gap counters, I2S write-duration histograms, queue-depth counters and long-call summaries. I did not expect one tool to explain the whole call.

When the question was packet loss, I looked at RTP sequence and timestamps. When the question was device scheduling, I looked at monotonic callback and I2S timing. When the question was build identity, I used hashes and preserved artifacts. When the question was echo or timbre, packet capture stopped at the digital boundary and the next test had to include the physical speaker/microphone path.

That separation matters because every tool has a blind spot. UART logs can perturb timing. PCAP cannot hear the room. Far-end listening cannot prove which queue grew. Docker/Asterisk logs cannot prove the ESP32 played a sample. A codec detection scan cannot prove the channel mapping matches the DSP assumptions. The tool is evidence only for the layer it can actually observe.

This is also why I prefer small, named counters over giant debug dumps in realtime code. A counter such as “writes over 20 ms,” “max callback gap,” “queue underrun,” or “first callback to I2S start” has a defined semantic. It can be compared across builds without parsing thousands of lines whose own output may change the result.

## What this result proves—and what it does not

The result I am willing to claim is narrow: **Slow-write incidence became a direct regression metric for hot-path changes.** It is supported by the recorded observation: **The V115 recovery tracked I2S speaker-write durations and counted >20 ms events, including a verbose maximum around 123 ms and a quiet-candidate maximum around 24.9 ms.**

It does not prove that every LOUP board, every network path or every future firmware build behaves the same way. It does not turn a server-side packet capture into an acoustic measurement. It does not turn a stable AEC-off test into permission to remove AEC from a speakerphone. It does not make a hash a quality metric. Those distinctions sound obvious in hindsight and are easy to lose when a demo deadline rewards a simple story.

The useful causal statement is the one consistent with the mechanism: A 20 ms PCMA packet cadence creates a natural timing budget; output operations that routinely consume or block beyond one frame can destabilize playout. If another experiment changes that mechanism, I expect the evidence to change too. If the evidence stays the same, I should question the theory before rewriting more code.

I also keep the rejected explanation visible: Using only average task CPU or queue depth to infer real-time behavior. That is part of the result. Knowing which layer did *not* create the step change prevents future debugging from starting at the same dead end.

## Reproducing the experiment without changing the experiment

If I had to hand this case to another engineer, I would ask them to preserve the same evidence boundary before attempting a fix:

- quiet the call hot path before measuring it
- record callback gaps and speaker-write duration in RAM
- capture queue/underrun state without per-frame printing
- run a short quality call and a longer drift call
- compare against the same known-good playout path

The point is not ceremony. Embedded audio is sensitive to hidden changes. A different softphone setting, a different PBX region, a new enclosure revision, a verbose log level or a queue added “for safety” can all change the result while leaving the test name unchanged.

For **Speaker Writes Over 20 ms Became My Local Deadline Signal**, the pass condition should be written in terms of the mechanism and evidence, not just “sounds good.” The subjective call still matters—it is the product—but the engineering result has to survive comparison.

## The production rule that survived the incident

Choose timing counters at the physical-output boundary, not only at the network callback.

I translate that sentence into an operational rule. The metric or artifact that revealed the failure must remain available in future debug builds, but it must not create the same realtime cost. The known-good binary must remain recoverable. A new audio experiment must identify exactly which layer changed. A release candidate must be tested against the same user-visible behaviors that made the earlier baseline valuable.

This keeps debugging cumulative. Instead of starting every audio complaint with “maybe packet loss” or “maybe AEC,” the next investigation begins with a fault tree and a set of already-proven boundaries. The value of the V115/V127/V132A history is not the version numbers themselves; it is the accumulated map of which measurements are trustworthy and which changes have already regressed the product.

## What I would do differently on the next product

I would design the measurement points earlier. The RTP callback, playout clock, queue, I2S boundary, exact AEC reference, capture slots and acoustic test points would all have named interfaces and low-cost counters from the beginning. That would reduce the amount of forensic reconstruction needed after subjective complaints arrive.

I would also separate debug verbosity from realtime instrumentation by architecture, not convention. Realtime code would update fixed counters or ring-buffer events; a lower-priority task would export summaries. If a UART or network logger can block the media task, the design has already allowed the observer into the deadline path.

For multi-device validation I would automate the call matrix and preserve a compact evidence bundle per run: firmware identity, hardware revision, test endpoint, RTP summary, device timing summary and subjective/acoustic result. The point is not to collect everything. It is to make two runs comparable.

Most importantly, I would preserve the same failure-model discipline. A 20 ms PCMA packet cadence creates a natural timing budget; output operations that routinely consume or block beyond one frame can destabilize playout. That principle remains true whether the next product uses ESP32-S3, a Linux SoC, a different codec or a cloud media service.

## The result I keep from this incident

Slow-write incidence became a direct regression metric for hot-path changes.

The deeper value is the method. I started with a perceptual symptom, located the earliest layer that could create it, chose evidence that could see that layer, changed one variable, and checked the known-good invariants afterward. The process is slower than random tuning for the first build and dramatically faster by the tenth.

The short version of the lesson is: **Choose timing counters at the physical-output boundary, not only at the network callback.**

That is the standard I now use for embedded audio work. A fix is not convincing because the call sounds better once. It is convincing when the mechanism, measurement, artifact identity and regression behavior all agree about why it got better.
