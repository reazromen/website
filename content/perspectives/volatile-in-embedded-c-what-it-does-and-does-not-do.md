---
title: "The volatile Keyword in Embedded C: What It Really Does—and What It Doesn't"
draft: false
date: '2020-09-07'
language: en
url: /posts/volatile-in-embedded-c-what-it-does-and-does-not-do.html
read_time: 9
excerpt: >-
  In embedded C, volatile tells the compiler that an object's value may change outside the visible program flow. It is important for hardware registers and certain shared variables, but it is not a universal concurrency fix.
eyebrow: "Perspectives · Embedded Systems"
tags: ["embedded-c", "volatile", "firmware", "interrupts", "microcontrollers"]
---

# The `volatile` Keyword in Embedded C: What It Really Does—and What It Doesn't

Few C keywords create as much confusion in embedded development as `volatile`. Developers are often told to add it whenever a variable is shared, accessed by an interrupt, or associated with hardware. The advice is incomplete. Used correctly, `volatile` prevents certain compiler optimizations that would make external changes invisible to the program. Used as a substitute for synchronization, it can leave serious bugs intact.

## The compiler is allowed to optimize

Consider a loop that waits for a flag:

```c
while (ready == 0) {
    /* wait */
}
```

If the compiler can prove that nothing in the visible execution path changes `ready`, it may load the value once and reuse it. In ordinary single-threaded code, that optimization can be valid. But suppose a hardware peripheral or interrupt handler changes the flag independently of the loop. Reusing the old value is no longer what the programmer intended.

Declaring the object as `volatile` tells the compiler that accesses are observable and that the value may change in ways not apparent from ordinary code flow:

```c
volatile uint32_t ready;
```

The compiler must respect volatile access semantics rather than treating the object like an ordinary value that never changes.

## Hardware registers are a classic use

Memory-mapped peripherals expose control and status registers at particular addresses. Reading a status register may return a fresh hardware state; writing a control register may trigger an operation. These accesses are not ordinary RAM operations.

Vendor headers typically declare register fields through carefully designed volatile-qualified types. If you write a register definition yourself, the access semantics must be correct for the device. A read can have side effects, a bit may be write-one-to-clear, and a register may require a particular access width. `volatile` does not document or enforce all those hardware rules; the reference manual does.

## Interrupt-shared flags

A simple flag set by an interrupt can also require `volatile`:

```c
static volatile bool sample_ready;

void ADC_IRQHandler(void)
{
    sample_ready = true;
}

int main(void)
{
    for (;;) {
        if (sample_ready) {
            sample_ready = false;
            process_sample();
        }
    }
}
```

This example illustrates the intent, not a complete universal synchronization pattern. Whether the flag is sufficient depends on the target architecture, compiler, type width, interrupt model, and whether losing an event is acceptable. If the interrupt fires between the main loop's test and clear, the main loop may erase a newly set flag. A counter, ring buffer, or critical section may be more appropriate.

## What volatile does not guarantee

**It does not make an operation atomic.** An increment such as `counter++` is a read-modify-write sequence. An interrupt can intervene between its component operations. On a narrow processor, even a read or write of a wider object may not be indivisible.

**It does not provide a complete memory-ordering protocol.** Volatile is not a replacement for C atomics, mutexes, critical sections, or the barriers required by a particular architecture and peripheral.

**It does not make arbitrary thread communication correct.** In standard C, unsynchronized access to shared objects between threads can constitute a data race and undefined behavior. Use the synchronization facilities supported by the runtime and compiler.

**It does not mean “never optimize anything nearby.”** The qualifier applies to accesses to the volatile object; it is not a general command to disable optimization for a whole function.

## Choose the right tool for the job

Use volatile for memory-mapped I/O and for specific values that can change asynchronously when the platform's compiler and interrupt model require it. Use atomics for supported lock-free communication between execution contexts. Use a critical section or interrupt masking when a multi-step operation must be protected, taking care to keep the protected region short. Use a queue or ring buffer when events carry data or when multiple events must not be collapsed into one flag.

Always inspect the compiler and platform documentation. Embedded C spans many architectures, and the correct solution depends on the language standard, toolchain, processor, and RTOS.

The essential rule is simple: `volatile` makes certain accesses happen as required by volatile semantics. It does not turn a fragile concurrency design into a correct one.
