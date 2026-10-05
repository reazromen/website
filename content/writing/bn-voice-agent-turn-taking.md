---
title: Voice-Agent Speed Is More Than Model Speed
date: '2024-07-12'
draft: false
language: en
url: /posts/bn-voice-agent-turn-taking.html
topic: embedded-audio-voice
tags:
- audio
- latency
featured: false
read_time: 2
excerpt: >-
  Voice-agent latency is often reduced to how quickly the model generates text. In reality,
  the conversation includes audio capture, network transport, end-of-speech detection,
  transcription, generation, speech synthesis, and playback.
editorial_batch: 20261003-100-niches
---

Voice-agent latency is often reduced to how quickly the model generates text. In reality, time is spent before the model receives the user's words and after the model produces its response. Audio capture, network transport, end-of-speech detection, transcription, generation, speech synthesis, and playback all contribute to the conversational wait.

Detecting whether a person has actually finished speaking is particularly difficult. If the agent responds to every short pause, it cuts people off. If it waits too long, the conversation feels heavy. Optimizing for speed alone is therefore not enough. A fast response delivered at the wrong moment is still a bad response; the system also needs to know when silence is appropriate.

Suppose the user corrects an answer halfway through. The agent must not only hear the new words, but also have a way to invalidate work based on the earlier interpretation. Stopping text generation and stopping audio already queued for playback are separate implementation problems even though the user experiences them as one interruption.

A voice system should therefore measure time at each boundary: when end-of-speech was inferred, when the first text appeared, when the first synthesized audio was ready, and when the user actually heard it. That timeline reveals where the delay really lives. A fast model cannot hide a slow end-to-end path. Human turn-taking remains the final test.

Source: [official reference](https://www.rfc-editor.org/rfc/rfc3550.html).
