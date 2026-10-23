---
title: "RAM vs Flash vs EEPROM: Where Does Your Microcontroller Store Everything?"
draft: false
date: '2019-10-26'
language: en
url: /posts/ram-flash-eeprom-where-microcontroller-stores-everything.html
read_time: 8
excerpt: >-
  RAM, flash, and EEPROM have different roles, performance characteristics, and endurance limits. Knowing where code, variables, stack, heap, and persistent settings live makes firmware failures easier to understand.
eyebrow: "Perspectives · Embedded Systems"
tags: ["memory", "flash", "ram", "eeprom", "embedded-systems"]
---

# RAM vs Flash vs EEPROM: Where Does Your Microcontroller Store Everything?

A microcontroller project can fail because it runs out of RAM, writes flash too often, or stores a setting in a place that disappears at reset. These problems become easier to diagnose when you understand the different kinds of memory and the jobs they perform.

The names are not interchangeable. RAM is generally used for working state; flash stores code and persistent data; EEPROM, where available, is commonly used for small amounts of persistent configuration. Some devices provide EEPROM-like behavior through flash emulation rather than a physically separate EEPROM block.

## Flash: code that survives power loss

Flash is non-volatile memory, meaning its contents normally survive when power is removed. Firmware images are commonly stored there. The processor may execute code directly from flash, or the boot process may copy portions into RAM first.

Flash is not usually written like ordinary RAM. Erasing and programming follow device-specific rules, and erase operations commonly happen in sectors or pages larger than a single variable. Flash also has finite program/erase endurance. Frequently updating a counter or configuration value can wear out the storage if the design ignores those limits.

Many microcontrollers use external flash for application code and resources. Others include internal flash. Read the datasheet to understand capacity, alignment, erase units, write restrictions, and whether the chip can execute code while a particular flash operation is in progress.

## RAM: the working area

RAM holds values that the program needs while running. Global variables, local variables, buffers, task stacks, heaps, and peripheral-driver state may all consume it. Ordinary RAM contents are generally lost when power is removed, although some chips offer retention or special low-power memory.

A program can fit in flash and still fail because RAM is exhausted. A large network buffer, recursive call chain, oversized task stack, or repeated heap allocation can cause problems even when the firmware image is small.

Stack and heap failures can look different. A stack overflow may corrupt nearby memory or trigger a runtime guard if one exists. Heap exhaustion can make an allocation fail, while fragmentation may prevent a large allocation even when the total free space appears adequate.

## EEPROM and persistent settings

EEPROM is designed for non-volatile storage of small values, often configuration or calibration data. Not every modern MCU has a dedicated EEPROM peripheral. Frameworks may emulate EEPROM using a flash region, which inherits flash's erase granularity and endurance constraints.

For important settings, consider a versioned record format, validation, a checksum, and a recovery default. If power can fail during an update, use a strategy that leaves either the old valid record or the new valid record recoverable. A single write to a configuration structure is not automatically power-fail safe.

## Where variables live

The linker and startup code decide how program sections map into memory. Initialized global data often has an initial image in flash and a runtime copy in RAM. Zero-initialized globals occupy a different section that startup code clears. Constants may remain in flash, but exact behavior depends on the architecture and toolchain.

Local variables often live on a stack, though the compiler may keep values in registers or optimize them away. Dynamically allocated objects use a heap or allocator managed by the runtime. RTOS tasks commonly have their own stacks, so adding tasks consumes memory even before each task does useful work.

The map file and linker script are invaluable. They show where sections are placed and how much memory each part of the program consumes.

## How to diagnose memory problems

Check the firmware's flash size and RAM usage report. Monitor the minimum-ever free heap and task stack high-water marks if the framework exposes them. Test worst-case packet sizes, error paths, nested calls, and simultaneous tasks—not only the normal path.

For persistent data, calculate how often each location is written and compare that rate with the device's endurance specification. Use wear-leveling or a suitable storage system when frequent updates are unavoidable.

## The practical distinction

Flash stores what must survive power loss, RAM holds what the program needs while running, and EEPROM or an EEPROM-like store can hold small persistent settings. The exact implementation varies by microcontroller.

When firmware behaves unpredictably, ask three questions: where is this object stored, how much capacity remains, and what are the access and endurance rules for that memory? Those questions often reveal the problem before another round of code changes.
