---
title: "Interrupts Explained: How Microcontrollers React to Events Without Constantly Checking"
draft: false
date: '2021-08-29'
language: en
url: /posts/interrupts-explained-microcontrollers-polling.html
read_time: 9
excerpt: >-
  Interrupts let a processor respond to events without continuously polling every input. Their power comes with constraints: short handlers, shared-state discipline, latency, and careful event design.
eyebrow: "Perspectives · Embedded Systems"
tags: ["interrupts", "embedded-systems", "firmware", "real-time", "microcontrollers"]
---

# Interrupts Explained: How Microcontrollers React to Events Without Constantly Checking

Imagine a microcontroller waiting for a button press. One approach is to read the input repeatedly in a loop. Another is to configure the hardware to notify the processor when the pin changes. The second approach uses an interrupt: an event that causes the processor to suspend its current execution and run a designated handler.

Interrupts are essential in embedded systems, but they are not simply a faster way to call a function. They change the timing and concurrency assumptions of the program.

## Polling and interrupts solve different problems

Polling is easy to reason about. A loop checks a sensor, status register, or flag at regular intervals. The maximum response delay depends on how often the check occurs and how long the loop takes to return to it. Polling can be appropriate when the system is simple, the timing is predictable, and checking is inexpensive.

Interrupts are useful when events are asynchronous or when the processor should do other work while waiting. A timer can trigger periodic work; a UART can signal that data has arrived; an ADC can notify the firmware when a conversion completes. The CPU need not spend every cycle checking whether something happened.

Interrupts still have costs. Entering and leaving a handler consumes time, frequent interrupts can dominate the processor, and badly designed handlers can delay more urgent work.

## What happens when an interrupt fires?

A peripheral detects an event and sets an interrupt status flag. If the relevant interrupt is enabled and has sufficient priority, the interrupt controller requests service. The processor saves enough execution state to resume the interrupted context, then transfers control to the handler associated with that interrupt.

The handler should acknowledge or clear the event as required by the hardware, capture essential information, and return promptly. The exact sequence depends on the architecture and peripheral. Some events require a specific read or write sequence to clear; clearing the wrong flag can lose events or cause the handler to run repeatedly.

A timer interrupt may increment a tick counter. A UART interrupt may move received bytes into a buffer. A GPIO handler may record a timestamp or signal a task. Larger operations—parsing a packet, updating a display, writing flash, or waiting on a peripheral—usually belong outside the handler.

## Why handlers should be short

While a handler runs, it may block lower-priority interrupts or delay ordinary application code. If a handler waits for a mutex, performs lengthy logging, allocates memory, or calls an API that is not interrupt-safe, the system can deadlock or miss timing deadlines.

A common design is to split work into two stages: the interrupt captures the event, and the main loop or RTOS task performs the heavier processing. In an RTOS, use only the documented interrupt-safe APIs and follow the framework's rules for notifying tasks from an ISR.

## Shared state creates race conditions

Suppose an interrupt sets a flag while the main loop reads and clears it. The operations can interleave in ways that lose an event. Declaring the flag `volatile` may be necessary for visibility to the compiler, but it does not make a multi-step operation atomic.

If every event matters, a boolean flag may be the wrong representation. A counter, timestamp queue, or ring buffer can preserve more information. If main code must read a multi-byte value that the interrupt updates, the design may need an atomic type, a brief critical section, or another synchronization method supported by the platform.

Do not assume that every variable access is atomic just because it appears to be one C statement. Check the target architecture and compiler guarantees.

## Priority and latency matter

Interrupt priorities determine which events can pre-empt others. A high-priority interrupt can reduce response time for an urgent event but can also interfere with lower-priority work. Excessive nesting increases complexity and stack use. If the interrupt load is too high, the processor may spend most of its time servicing events rather than executing useful application logic.

Real-time design therefore considers worst-case latency, handler duration, event rate, and the amount of work that can safely be deferred. Measure these quantities under realistic load.

## A practical design checklist

- Keep handlers short and bounded.
- Follow the peripheral's exact flag-clearing procedure.
- Use ISR-safe APIs when an RTOS is involved.
- Protect shared data with appropriate synchronization.
- Decide whether events can be coalesced or must all be retained.
- Measure interrupt rate, latency, stack use, and worst-case execution time.
- Test under simultaneous activity, not only one event at a time.

Interrupts let a microcontroller react efficiently to the outside world. Reliable interrupt-driven firmware comes from treating each handler as a constrained real-time execution context, not as an ordinary function with unlimited freedom.
