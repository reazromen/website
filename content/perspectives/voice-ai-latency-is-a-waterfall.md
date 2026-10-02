---
title: Voice AI Latency Is a Waterfall, Not One Number
url: /posts/voice-ai-latency-is-a-waterfall.html
date: '2026-09-26'
read_time: 9
excerpt: A voice agent can report fast STT, fast LLM, and fast TTS while still feeling
  slow because endpointing, network boundaries, tool calls, buffering, and playout
  delays accumulate between those component timers.
topic: ''
tags:
- voice-ai
- latency
- webrtc
- vad
draft: false
featured: false
language: en
eyebrow: Real-Time Voice & AI · systems note
outputs:
- url: /posts/voice-ai-latency-is-a-waterfall.html
  template: cms/templates/posts/posts--voice-ai-latency-is-a-waterfall.tpl
  source: cms/templates/posts/posts--voice-ai-latency-is-a-waterfall.json
---

A voice agent can have every component benchmark under a second and still pause awkwardly for three seconds before it answers.

That sounds contradictory only if latency is treated as one number.

In a real conversational pipeline, the user experiences a waterfall.

```
last spoken phoneme
  -> endpoint detection
  -> STT finalization
  -> network / orchestration
  -> model first token
  -> optional tool calls
  -> TTS first audio
  -> transport buffering
  -> playout starts
```

If each component reports only its internal processing time, the gaps between components disappear from the dashboard.

## Endpointing often owns the first hidden second[#](#endpointing-often-owns-the-first-hidden-second)

The system has to decide that the user has finished speaking.

Voice activity detection can detect silence quickly, but silence does not always mean turn completion. Natural speech includes pauses. Endpointing therefore balances responsiveness against cutting people off.

LiveKit's current endpointing options make this trade visible: minimum and maximum delay, fixed versus dynamic behavior, and the interaction with VAD or STT end-of-speech signals.

If STT already waits before declaring end-of-speech and the agent then applies another minimum delay, those waits can become additive.

That time is real to the user even though it belongs to neither “STT latency” nor “LLM latency.”

## STT finalization is different from partial transcription[#](#stt-finalization-is-different-from-partial-transcription)

Streaming speech recognition can produce partial text while the user is still talking. A dashboard may show that text arriving quickly.

The agent may still wait for a final transcript or a stable end-of-turn signal before sending the prompt downstream.

So measure at least two timestamps:

- first useful partial transcript,
- final transcript / turn committed.

They answer different questions.

## Model TTFT is not response latency[#](#model-ttft-is-not-response-latency)

Time-to-first-token is valuable because it measures how quickly generation begins.

But a voice pipeline may need enough text to form a speakable phrase before TTS can start. Some architectures stream tokens directly into TTS; others buffer punctuation, clauses, or complete sentences for quality.

A model with excellent TTFT can therefore feed a TTS stage that deliberately waits.

The useful boundary is not only:

```
prompt sent -> first token
```

but also:

```
first token -> first TTS request
first TTS request -> first audio byte
first audio byte -> first sample played
```

## Tool calls create a second waterfall[#](#tool-calls-create-a-second-waterfall)

If the model decides to call a CRM, calendar, database, search service, or custom function, conversational latency now includes another distributed system.

A single “LLM duration” metric can hide:

```
model decides tool
 -> tool RPC
 -> remote API
 -> database
 -> response serialization
 -> model resumes
 -> TTS
```

The correct optimization may have nothing to do with the language model.

Useful techniques include speculative acknowledgements, parallel tool work, cached context, local read models, tighter RPC budgets, and designing functions that return the minimum information needed to continue the turn.

## TTS first byte is not first audible sample[#](#tts-first-byte-is-not-first-audible-sample)

TTS services often expose time-to-first-byte or streaming chunk latency.

After that byte arrives, the system may still buffer audio, packetize it, pass through WebRTC jitter handling, cross a mobile audio stack, and wait for playout scheduling.

For the human, the clock stops when sound begins.

So capture a client-side “first sample played” event if the UX matters enough to optimize seriously.

## Realtime speech-to-speech removes boundaries, not physics[#](#realtime-speech-to-speech-removes-boundaries-not-physics)

Realtime models can consume and produce speech directly, bypassing a separate STT → text LLM → TTS cascade. LiveKit's documentation describes this as a distinct architecture and notes benefits such as richer speech context and full-duplex interaction.

That can remove serialization boundaries and reduce the places where buffering accumulates.

It also changes observability.

Instead of three clean services with separate metrics, you now need model-level audio input/output timing, turn detection, interruption events, transport timing, and tool-call timing around the realtime session.

Fewer boxes do not mean fewer clocks.

## Interruption latency is a separate product metric[#](#interruption-latency-is-a-separate-product-metric)

A natural voice system should stop speaking when the user barges in.

That path has its own waterfall:

```
user speech
 -> VAD detects speech
 -> interruption policy fires
 -> generation cancelled
 -> TTS cancelled
 -> queued audio discarded
 -> playout stops
```

A system can answer quickly and still feel terrible if it talks over the user for 800 ms after interruption.

I would measure interruption-stop latency separately from reply-start latency.

## Instrument boundaries, not vendors[#](#instrument-boundaries-not-vendors)

The best latency dashboard is usually a trace of the conversation turn.

Give one turn an ID and timestamp every boundary:

- speech start/end,
- VAD end,
- STT partial/final,
- prompt dispatch,
- LLM first token,
- tool start/end,
- TTS request/first byte,
- RTP/media enqueue,
- client playout start.

Then render the turn as a waterfall.

Once you can see the empty spaces, optimization becomes much less mystical.

## The human metric is turn gap[#](#the-human-metric-is-turn-gap)

Ultimately the most useful top-level number is simple:

```
first audible response
-
user's last audible speech
```

That is the silence the user experiences.

Everything else exists to explain it.

Voice AI latency is not an LLM benchmark. It is the sum of endpointing, recognition, generation, tools, synthesis, transport, buffering, and playout—plus every queue between them.

## Sources and further reading[#](#sources-and-further-reading)

- [LiveKit: Realtime models overview](https://docs.livekit.io/agents/models/realtime/)
- [LiveKit: Endpointing options](https://docs.livekit.io/reference/agents-js/interfaces/agents.voice.EndpointingOptions.html)
- [LiveKit Agents voice API](https://docs.livekit.io/reference/python/livekit/agents/voice/index.html)
- [LiveKit community: component timings under 1s but 3–4s end-to-end](https://community.livekit.io/t/high-end-to-end-latency-asr-llm-tts-total-1s-but-speech-end-to-reply-takes-3-4s-livekit-agents/1277)
