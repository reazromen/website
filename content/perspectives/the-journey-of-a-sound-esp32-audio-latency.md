---
title: "The Journey of a Sound: What Happens Between Speaking and Being Heard?"
url: /posts/the-journey-of-a-sound-esp32-audio-latency.html
date: '2026-11-04'
read_time: 10
excerpt: "From microphone sampling and I2S DMA to RTP transport and jitter buffering, follow the engineering journey that turns a voice into sound at the other end of a network."
topic: embedded-audio-voice
tags:
- esp32-s3
- embedded-systems
- i2s
- dma
- rtp
- voip
- audio-latency
draft: false
featured: false
language: en
eyebrow: Embedded Systems & Real-Time Communications · Perspective
outputs:
- url: /posts/the-journey-of-a-sound-esp32-audio-latency.html
  template: cms/templates/posts/posts--the-journey-of-a-sound-esp32-audio-latency.tpl
  source: cms/templates/posts/posts--the-journey-of-a-sound-esp32-audio-latency.json
---

Imagine speaking into a small microphone. The sound leaves your mouth as a pressure wave, travels through the air, reaches a microphone, and somehow, a fraction of a second later, another person hears your voice from a speaker hundreds or thousands of kilometres away.

We have become so accustomed to this experience that it rarely feels remarkable. We press a button, establish a call, and begin talking. Yet, between those two moments of speaking and hearing, something extraordinary happens: a physical phenomenon is translated into electrical signals, transformed into numbers, divided into packets, transported through an unpredictable wireless environment, reconstructed at another endpoint, and finally returned to the physical world as sound.

I wanted to understand this journey more closely, not just as a sequence of software operations, but as a complete engineering system. So I built a 3D simulation of an ESP32-S3-based audio pipeline, allowing us to follow the signal through different stages and examine the machinery responsible for making real-time communication possible.

The interesting question is not simply how an electronic device transmits sound. It is how the device manages to do so without making the conversation feel delayed.

[Watch the multi-angle ESP32-S3 audio pipeline walkthrough](https://ops.reazromen.com/architecture/teardown/audio-latency-walkthrough.mp4) (the video endpoint may require Ops authentication).

## The moment sound becomes information

Sound is mechanical energy travelling through a medium. When we speak, our vocal cords create pressure variations in the surrounding air. A microphone detects these variations and converts them into an analogue electrical signal.

But a computer cannot directly understand a continuously changing electrical waveform. It needs a representation that can be stored, processed, and transmitted mathematically.

This is where an analogue-to-digital converter enters the picture.

In the simulated architecture, the ES7210 audio codec samples the microphone signal and converts it into digital values. At a sampling frequency of 16 kHz, the system measures the waveform 16,000 times every second. Each measurement represents the amplitude of the signal at a particular instant.

Think about what that means. A continuously changing physical event is being represented by a sequence of discrete numbers. The more frequently we sample the signal, the more temporal information we capture, within the limits imposed by the sampling theorem and the quality of the analogue front end.

The original sound has not disappeared. We have simply found a mathematical way to describe it.

## The invisible rhythm inside the processor

Once the audio becomes digital, the next problem is moving those samples efficiently.

The ES7210 communicates with the ESP32-S3 through I2S, a serial interface designed specifically for digital audio. Its clock and data signals coordinate the transfer, ensuring that samples arrive in the correct sequence and at the correct time.

One might imagine the processor receiving every sample individually and copying it into memory. But doing that continuously would waste a significant amount of CPU time.

Instead, the system can use Direct Memory Access, or DMA. This hardware mechanism transfers data between a peripheral and memory without requiring the processor to handle every individual movement.

A useful way to understand this is through a pair of alternating containers. While one container is being filled with incoming audio samples, the processor works on the other. When the first becomes ready, their roles switch. This is commonly called ping-pong buffering.

Consider a system sampling at 16,000 samples per second, with each DMA block containing 128 samples. The time represented by one block is:

`T = 128 / 16000 = 0.008 seconds`

Eight milliseconds.

That means a new block of audio becomes available every eight milliseconds. The processor must handle each block within the available time, otherwise the continuous stream can be interrupted.

This is one of the fascinating characteristics of real-time engineering: the system is not merely required to calculate the correct answer. It must calculate the correct answer before the next deadline arrives.

## When software has to obey time

The ESP32-S3 is not doing only audio processing. It may also be managing network communication, device controls, memory, and other background operations.

An operating system such as FreeRTOS helps coordinate these activities through tasks and scheduling.

But scheduling introduces another dimension to the latency problem. An audio task might be ready to execute, yet another task could be occupying the processor. The audio task must wait until it receives CPU time.

A few milliseconds here and a few milliseconds there may not seem significant in ordinary computing. In a continuous audio stream, however, these small intervals matter.

This is why embedded audio engineering is not simply about making a processor faster. It is about designing a system in which tasks finish predictably, buffers are handled before deadlines, and one operation does not unnecessarily block another.

A processor can have enormous computational capacity and still produce poor real-time audio if its scheduling and buffering strategy is badly designed.

## From numbers to packets

After acquisition and processing, the audio must be prepared for transport.

Digital audio is commonly represented as Pulse Code Modulation, or PCM. The samples are grouped into frames and, depending on the chosen codec, encoded into a format suitable for transmission.

Here, the relationship between time and data becomes particularly interesting.

Suppose we collect 20 milliseconds of mono PCM audio at 16 kHz, using 16 bits per sample. The resulting frame contains:

`16000 × 0.020 × 2 = 640 bytes`

That is 640 bytes representing just 20 milliseconds of sound.

If the system uses conventional G.711 at 8 kHz with 8-bit samples, the equivalent 20-millisecond frame contains:

`8000 × 0.020 × 1 = 160 bytes`

These are different audio formats, with different bandwidth and processing characteristics. A 16 kHz microphone capture does not automatically become 16 kHz G.711; the encoding configuration and any required resampling determine the transmitted format.

There is also a subtle cost to packetization. If the system waits until an entire 20-millisecond frame has been collected before transmitting it, the first sample in that frame has already waited almost 20 milliseconds.

The system has introduced delay before the packet has even reached the network.

## A conversation is not the same as a data transfer

When we think about sending information across a network, we often imagine that the objective is simply to deliver the data successfully. Real-time communication has a different requirement.

The data must arrive not only correctly, but at a useful time.

This is where SIP and RTP enter the architecture.

SIP is responsible for establishing and managing the communication session. RTP carries the actual real-time media. The two protocols have different responsibilities: one helps establish the conversation, while the other transports the audio.

RTP also carries timing information and sequence numbers, allowing the receiving side to understand the order and media timing of packets.

The distinction is important because a call can be successfully established while the audio itself performs badly. A connected session does not guarantee a low-latency media path.

## The unpredictable journey through Wi-Fi

The packet now leaves the processor and enters the wireless network.

Unlike a dedicated physical connection, Wi-Fi is a shared radio environment. Multiple devices compete for access to the same medium. Interference, channel congestion, retransmissions, and access point scheduling can all influence when a packet is actually transmitted.

A packet might travel quickly one moment and take considerably longer the next.

This introduces a distinction between latency and jitter.

Latency describes the time taken for information to travel from one endpoint to another. Jitter describes the variation in packet arrival timing.

Imagine two networks. The first consistently delivers packets in 20 milliseconds. The second delivers them in 8 milliseconds sometimes, 35 milliseconds at other times, and occasionally takes much longer.

The second network may have a lower average delay, but its unpredictable behaviour can make continuous audio more difficult to reproduce.

For a real-time voice device, predictability can be just as important as raw speed.

## Why the receiver deliberately waits

There is something almost paradoxical about the next component.

After all the effort spent reducing delay during transmission, the receiving system intentionally waits before playing the audio.

This is the job of the jitter buffer.

Because network packets do not always arrive at perfectly regular intervals, the receiver temporarily stores them and releases the audio at a controlled pace. This helps prevent interruptions caused by variations in packet delivery.

But the buffer introduces its own delay. A larger buffer provides more protection against network jitter, but the listener must wait longer to hear the sound.

A smaller buffer makes the conversation feel more immediate, but packets that arrive late can cause gaps or audio interruptions.

There is no universally perfect buffer size. The correct choice depends on network conditions, packet timing, and the application's tolerance for glitches.

The engineering challenge is to preserve enough information to make playback continuous without keeping the listener waiting unnecessarily.

## The sound returns to the physical world

Eventually, the received audio is decoded and delivered to the output codec.

In this architecture, the ES8311 performs digital-to-analogue conversion. It transforms the sequence of numerical samples into an electrical waveform that can drive the speaker's amplification stage.

The speaker diaphragm begins moving, creating pressure variations in the surrounding air.

And there it is: the original phenomenon has travelled through a chain of physical, electrical, mathematical, and computational transformations, only to become a pressure wave again.

A person at the other end hears a voice.

What makes the whole process remarkable is that the system has to repeat this journey continuously. It cannot wait several seconds to collect everything and process it later. It must keep moving, frame after frame, while maintaining a rhythm that feels natural to human conversation.

## The physics of a delay

When we examine the complete architecture, latency stops looking like a single property of the processor or network. It becomes a collection of delays distributed across the system.

`Ttotal = Tcapture + Tprocessing + Tpacketization + Tnetwork + Tjitter + Tplayback`

Each stage contributes something to the total.

Some components have relatively predictable timing. Others vary according to scheduling, wireless conditions, and packet arrival patterns. In practice, the system also needs to account for clock behaviour, codec processing, buffering, and the exact measurement boundaries used.

The simulation accompanying this article uses adjustable parameters to illustrate how these delays accumulate. Its default latency figures are illustrative estimates, not measurements taken from a physical ESP32-S3 device. Actual performance requires instrumentation of the firmware and measurement across the real hardware and network path.

That distinction matters. A simulation helps us understand the relationships between components; a measurement tells us how a particular implementation actually behaves.

## A system is more than the sum of its components

Perhaps the most interesting lesson from building this model is that low latency is not something we can purchase by selecting a faster microcontroller.

We can have an efficient ADC, a well-configured DMA engine, and a powerful processor, yet still create a slow communication system through careless buffering or network scheduling. We can reduce packetization delay and then lose the improvement by introducing an unnecessarily deep jitter buffer.

Every local optimization changes the behaviour of a larger system.

This is a recurring idea in engineering. A system's behaviour often emerges from the relationships between its components, rather than from the specifications of any one component. The same principle appears in distributed computing, control systems, telecommunications, and even the physical networks that make up the natural world.

A voice travelling through an ESP32-S3 is therefore more than an audio-processing exercise. It is a small demonstration of how modern engineering connects physics, mathematics, electronics, operating systems, and communication protocols into one coordinated process.

I find that particularly fascinating: something as ordinary as hearing another person's voice depends on an extraordinary amount of carefully coordinated work happening almost entirely out of sight.
