---
title: RTP Timestamps Are Not Wall Clocks
url: /posts/rtp-timestamps-are-not-wall-clocks.html
date: '2026-09-26'
read_time: 10
excerpt: A packet can arrive at 09:17:25 and carry an RTP timestamp like 2873419200.
  Those values describe different things. Confusing them is one of the fastest ways
  to make real-time audio timing harder than it already is.
topic: ''
tags:
- rtp
- audio
- jitter
- telephony
- timing
draft: false
featured: false
language: en
eyebrow: REAL-TIME COMMUNICATIONS · SYSTEMS NOTE
outputs:
- url: /posts/rtp-timestamps-are-not-wall-clocks.html
  template: cms/templates/posts/posts--rtp-timestamps-are-not-wall-clocks.tpl
  source: cms/templates/posts/posts--rtp-timestamps-are-not-wall-clocks.json
---

One of the easiest mistakes in real-time audio is to look at an RTP timestamp and mentally translate it into time-of-day. The field is called a timestamp, so the instinct is understandable. But RTP is not telling the receiver, “this packet was sent at 09:17:25.” It is telling the receiver where the media belongs on a sampling timeline.

That distinction looks academic until audio starts clicking, drifting, arriving in bursts, or slowly walking away from the clock used by another subsystem. Then it becomes the whole problem.

## There are several clocks in one call[#](#there-are-several-clocks-in-one-call)

A voice path can contain a microphone sample clock, an RTP timestamp clock, a sender operating-system clock, a network arrival clock, a receiver audio clock, and a wall clock used for logs. They may be related, but they are not interchangeable.

RFC 3550 defines the RTP timestamp as the sampling instant of the first octet in the packet. The sampling instant must come from a clock that advances monotonically and linearly so receivers can synchronize media and calculate jitter. For periodically generated media, the timestamp should follow the nominal sampling timeline rather than simply reading the machine's system clock at send time.

That is a very important design choice. Network scheduling can be messy. Media time should not become messy just because a task woke up late.

## A simple 8 kHz example[#](#a-simple-8-khz-example)

Imagine an 8 kHz G.711 stream packetized into 20 ms chunks. Twenty milliseconds contains 160 sampling periods. If one RTP packet starts at timestamp `T`, the next packet normally starts at `T + 160`, then `T + 320`, and so on.

```
packet 1  RTP ts = T
packet 2  RTP ts = T + 160
packet 3  RTP ts = T + 320
packet 4  RTP ts = T + 480
```

The packets do not need to hit the network exactly 20 ms apart for that media timeline to remain valid. A scheduler may delay one packet. Wi-Fi contention may delay another. A queue may briefly build and drain. The RTP timestamp still represents when those samples belong in media time.

RFC 3551 recommends 20 ms as the default packetization interval for packetized audio unless a payload format says otherwise. It also makes the tradeoff explicit: larger packets reduce header overhead, but increase delay and make a lost packet represent more missing audio.

## Sequence number and timestamp solve different problems[#](#sequence-number-and-timestamp-solve-different-problems)

The RTP sequence number increments once per packet. It helps the receiver detect loss and restore packet order. The timestamp advances according to media time.

Those are not the same axis.

If I receive sequence numbers 100, 101, 103, I can see that a packet is missing. If the corresponding timestamps advance by 160 samples per packet, I can also determine where the missing media belonged. A jitter buffer needs both kinds of information: packet identity/order and media timing.

This is also why deriving playout purely from packet arrival order is fragile. Arrival order tells me what the network did. RTP timestamps tell me what the media source intended.

## Jitter is about the difference between two timelines[#](#jitter-is-about-the-difference-between-two-timelines)

RFC 3550's interarrival-jitter calculation compares packet spacing at the receiver with packet spacing implied by RTP timestamps. In simplified terms, it asks how much the relative transit time is changing.

If the sender says two packets represent media 20 ms apart but the receiver observes arrivals 35 ms apart, that variation contributes to jitter. If the next pair arrives only 8 ms apart because a queue drained, that variation contributes too.

This is why a packet capture can show perfectly valid RTP timestamps while arrival times look ugly. The timestamp is not supposed to mirror network arrival time. The difference is exactly the signal the receiver needs in order to reason about jitter.

## A jitter buffer is not just a packet queue[#](#a-jitter-buffer-is-not-just-a-packet-queue)

A naive implementation can treat a jitter buffer as “hold N packets and then play them.” That can work in a friendly network, but it misses the timing model.

A useful jitter buffer maps packets onto a playout timeline. It absorbs arrival-time variation, reorders packets when possible, decides how long to wait for missing media, and eventually has to choose between latency and concealment. Wait too little and normal network variation becomes audible loss. Wait too long and a conversational call feels sluggish.

The buffer therefore needs to care about media timestamps, sequence numbers, arrival times, and the receiver's own playout clock. The hard part is not storing packets. The hard part is deciding when a packet has become too late to matter.

## Clock rate is a protocol property, not a guess[#](#clock-rate-is-a-protocol-property-not-a-guess)

For many audio formats the RTP clock rate matches the sampling rate, but this is not universally safe to infer. The payload specification defines the clock.

G.722 is the classic trap. RFC 3551 notes that although G.722 audio is sampled at 16 kHz, its RTP clock rate remains 8 kHz for historical compatibility. Code that assumes “codec sample rate equals RTP clock rate” can therefore be wrong while looking completely reasonable.

This is the kind of bug I distrust because it survives code review. The arithmetic is clean. The assumption underneath it is not.

## Wall-clock correlation belongs elsewhere[#](#wall-clock-correlation-belongs-elsewhere)

Sometimes a system genuinely needs to relate RTP media time to real time—for synchronization, recording, analytics, or aligning different media streams. RTP handles that relationship through RTCP sender reports, which can associate an RTP timestamp with an NTP-format wall-clock value.

That separation is healthier than forcing wall time into every RTP packet. RTP data packets can carry a compact media clock suited to high-rate transport; RTCP can periodically provide the mapping needed to correlate that clock with an external time base.

It also means that if I am debugging “what time did this happen?” I should not stare at the RTP timestamp alone. I need packet-capture arrival time, RTCP timing information, application logs, or another explicit clock correlation.

## Clock drift is where embedded audio gets interesting[#](#clock-drift-is-where-embedded-audio-gets-interesting)

Two oscillators marked with the same nominal frequency are not perfectly identical. A capture codec and a playback device can run slightly fast or slightly slow relative to each other. Over a short call this may be invisible. Over time it can accumulate.

Suppose the sender produces audio from its hardware sample clock while the receiver consumes it using another hardware clock. If their effective rates differ, a fixed-size buffer eventually trends toward empty or full even on a network with no meaningful jitter. Increasing the jitter buffer may delay the symptom without solving the rate mismatch.

This is why I separate three questions when debugging real-time audio: Are packets being lost? Are packets arriving with variable delay? Are the producer and consumer clocks running at slightly different rates? Those failures can sound similar but need different fixes.

## Do not timestamp audio from task wake-ups[#](#do-not-timestamp-audio-from-task-wake-ups)

Embedded firmware makes this especially tempting. A task receives a DMA buffer, wakes up, calls a millisecond timer, and uses that value to construct media timing. But task scheduling time is not necessarily sample time.

If a DMA block contains 160 samples from a continuous 8 kHz capture stream, the next media timestamp normally advances by 160 sampling periods whether the firmware task handled the block immediately or a few milliseconds late. Scheduling delay belongs to transport/processing latency, not to the media's sampling timeline.

When the timestamp follows task wake-ups, CPU scheduling jitter gets encoded as media jitter before the packet even touches the network. RFC 3550 explicitly warns that variation between sampling and transmission affects the reported jitter. In other words, a bad sender can manufacture “network jitter” locally.

## What I measure when audio timing looks wrong[#](#what-i-measure-when-audio-timing-looks-wrong)

I want the clocks separated in the trace. For each packet or audio block, I want at least the RTP sequence number, RTP timestamp, payload type/clock rate, local capture or enqueue time if available, network send time, receiver arrival time, jitter-buffer insertion time, and actual playout time.

Then I look at deltas rather than absolute values.

```
Δ RTP timestamp
Δ packet arrival time
Δ buffer depth
Δ playout time
```

If RTP advances smoothly but arrivals do not, I look at transport and scheduling. If arrivals are smooth but buffer depth steadily trends, I look for clock-rate mismatch or playout-rate issues. If RTP itself advances irregularly for fixed-rate capture, I inspect the sender's timestamp generation before blaming the network.

This way of debugging is less glamorous than changing codec settings until the audio sounds better. It is also much faster once the failure is timing-related.

## The useful mental model[#](#the-useful-mental-model)

I think of RTP timestamps as coordinates on the media timeline.

Sequence numbers answer: *which packet is this?*

RTP timestamps answer: *where does this media belong?*

Arrival timestamps answer: *when did the network deliver it?*

Wall clocks answer: *when did this happen in the outside world?*

Playout clocks answer: *when will the user actually hear it?*

Once those clocks are kept separate, jitter buffers, drift, packet captures, RTCP reports, and embedded audio pipelines become much easier to reason about. The timestamp field stops looking like a strange number in Wireshark and starts doing what RTP designed it to do: preserve the media's sense of time while the network does whatever networks do.

## Sources and further reading[#](#sources-and-further-reading)

- [RFC 3550 — RTP: A Transport Protocol for Real-Time Applications](https://datatracker.ietf.org/doc/html/rfc3550)
- [RFC 3551 — RTP Profile for Audio and Video Conferences with Minimal Control](https://datatracker.ietf.org/doc/html/rfc3551)
- [RFC 4856 — Media Type Registration of RTP Payload Formats](https://datatracker.ietf.org/doc/html/rfc4856)
