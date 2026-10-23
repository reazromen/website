---
title: "What Actually Happens Inside a Microcontroller When You Turn It On?"
draft: false
date: '2021-04-18'
language: en
url: /posts/what-happens-inside-a-microcontroller-when-you-turn-it-on.html
read_time: 8
excerpt: >-
  A microcontroller does not simply wake up and run your application. Reset logic, boot memory, startup code, clocks, and memory initialization prepare the chip before your first line of application code executes.
eyebrow: "Perspectives · Embedded Systems"
tags: ["embedded-systems", "microcontrollers", "firmware", "computer-architecture"]
---

# What Actually Happens Inside a Microcontroller When You Turn It On?

A microcontroller can appear almost magical from the outside. Apply power, and an LED blinks, a sensor reports a value, or a motor begins to move. But the processor does not immediately jump into the function you wrote. Before application code can run, a chain of hardware and software events establishes a state in which that code can execute.

Understanding this sequence makes debugging less mysterious. It explains why a board may fail before reaching `main()`, why startup files matter, and why a reset is not always the same as removing power.

## 1. Power becomes a valid operating condition

When power is applied, the supply voltage rises. The chip's power-on-reset circuitry holds the processor in reset until the voltage and other required conditions are sufficiently stable. This prevents the CPU from executing instructions while its internal circuits are operating outside their intended range.

Real boards complicate the picture. Regulators have startup times, peripherals may power up at different speeds, and external devices can drive pins before the microcontroller is ready. A brownout detector can reset the chip if the supply later falls below a configured threshold. If a board repeatedly restarts when Wi-Fi transmits or a motor starts, the problem may be power integrity rather than software.

## 2. The processor begins at a defined entry point

After reset is released, the processor follows its architecture's reset behavior. Depending on the chip, it may fetch an initial stack pointer and reset handler from a vector table, or begin execution from a defined boot address. The exact details differ across Cortex-M, Xtensa, RISC-V, and other architectures.

The first code may be a ROM bootloader. ROM is useful because it is available even when external flash is blank or application firmware is damaged. The boot code can inspect boot configuration, select a boot source, support recovery or flashing, and transfer control to the next stage.

On many ESP32 devices, the ROM bootloader and a second-stage bootloader work together to locate and load the application image from flash. Other microcontrollers may execute directly from internal flash or use a different boot arrangement.

## 3. Startup code prepares the C and C++ environment

The application does not necessarily begin at the `main()` function. A reset handler commonly configures low-level runtime state first. It may establish the stack, copy initialized variables from non-volatile storage into RAM, clear zero-initialized variables, configure memory regions, and run language-runtime initialization.

For example, a global variable such as `int count = 7;` usually needs its initial value copied into RAM. A zero-initialized global may be placed in a section that startup code clears. If this work is skipped or the linker script is wrong, variables can begin with unexpected values even though the source code looks correct.

C++ programs may also need constructors for global objects to run before `main()`. Embedded frameworks often hide these details, but they still form part of the firmware's execution path.

## 4. Clocks, memory, and peripherals are configured

The processor may begin using a conservative clock before switching to a faster source. Startup code or the framework configures clock trees, flash access timing, caches, external RAM, interrupt controllers, and memory protection where supported.

Not every peripheral is automatically ready. Your code or a driver must usually configure GPIO direction, pin multiplexing, timers, serial interfaces, ADCs, audio codecs, and other devices. Some frameworks perform much of this initialization before calling your application entry point.

This layered setup is why a fault can occur before a visible LED changes. A failure in clock setup, external memory initialization, or an early driver can prevent the program from reaching the code you expected.

## 5. Finally, application logic begins

In a simple bare-metal project, `main()` may enter an infinite loop that checks inputs and updates outputs. In an RTOS-based system, initialization code may create tasks, queues, timers, and synchronization objects before starting the scheduler. The first task then becomes the place where application behavior begins.

A useful debugging strategy is to mark these boundaries. Toggle a spare GPIO at the reset handler, after runtime initialization, and at the start of `main()`; or use a debugger breakpoint and reset vector inspection. A serial log is useful, but it cannot help if the UART itself has not been initialized or if execution fails before logging is available.

## Reset is not always a clean slate

A watchdog reset, software reset, brownout reset, and power-on reset may leave different evidence or affect different peripherals. Some RAM contents or peripheral states may persist depending on the device and reset type. Firmware should use the chip's reset-reason registers when diagnosing unexpected restarts rather than assuming every boot is identical.

## The practical lesson

A microcontroller startup is a small boot process. Power circuitry establishes safe conditions, hardware reset selects an entry point, boot code locates firmware, startup code prepares memory and runtime state, and the application configures the system it needs.

When a project does not reach its first visible action, debug these stages in order. Ask what has already run, which memory and clocks are available, and whether the reset source is known. That method is far more effective than changing application logic that may never have executed.

For chip-specific behavior, begin with the vendor's reference manual, boot documentation, startup assembly, linker script, and framework startup code. Those files reveal what actually happens on your particular board.
