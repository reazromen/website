---
title: 'LoRa Field Tests: What We Can Learn About Wireless Comms'
url: /posts/lora-field-tests-what-we-can-learn-about-wireless-comms.html
date: '2026-10-27'
read_time: 6
excerpt: I reached around 20 km in my own LoRa field tests. The result was a reminder that real-world wireless range depends on the whole radio link, not a headline specification.
topic: radio-iot
tags:
- lora
- field-testing
- wireless-communication
draft: false
featured: false
language: en
eyebrow: Radio & IoT · field notes
---

# LoRa Field Tests: What We Can Learn About Wireless Comms

One of the things that gets me excited about wireless communication is the idea of sending a small piece of data through the air and having it reach a destination so far away that I cannot even see it.

Sure, Wi-Fi can cover impressive distances under the right conditions. But let’s assume that a router or an existing network is not an option. Imagine two radio nodes, separated by open space, with one simple job: exchange a message. How far could we push that link?

I have had my own turn testing the limits of LoRa communication. Like many embedded developers, I started with the familiar workbench experience: connect the hardware, send a message, receive a response, and wonder what would happen beyond the desk.

In my own field tests, I managed to communicate over a distance of approximately **20 kilometres**. That number is exciting, but the more interesting part is what a result like this can—and cannot—tell us about wireless communication.

A datasheet can describe radio capabilities and receiver sensitivity. It cannot fully predict what will happen between two antennas in every real environment. Placement, terrain, antenna performance, interference, radio settings, and the software controlling the devices all contribute to the outcome. That is why field testing matters.

## Bringing It Outdoors

Getting two development boards to communicate on a desk is a useful first step, but it proves very little about how they will perform across an open field or in a built-up area.

Outdoors, the environment becomes part of the system. Buildings, trees, terrain, and other obstacles can weaken or block a signal. Reflections can change what the receiver sees. Even the height and orientation of an antenna can make a noticeable difference.

This is where a field test becomes more than a demonstration. Moving away from the starting point changes the conditions of the radio link, and every new location gives you another opportunity to observe what is working and what is not.

LoRa is designed for low-power, long-range communication, particularly when devices only need to exchange small amounts of data. That makes it attractive for telemetry and remote sensing, where sending a short message can be more important than transferring large volumes of information.

But “long range” is not a guarantee of a particular distance. It is a capability to investigate under specific conditions.

## Twenty Kilometres Is a Result, Not a Universal Promise

Reaching around 20 km was a memorable result in my own testing. It is tempting to turn a distance like that into a simple claim about what LoRa can do, but a responsible engineering conclusion needs more context.

A successful message at a given distance establishes that communication was possible under those conditions. It does not, by itself, prove that the link will remain reliable over time, that every packet will arrive, or that another setup using the same radio will achieve the same range.

The maximum distance is only one measurement. Reliability matters too.

Can the devices exchange messages repeatedly? How often are packets lost? Does changing antenna height or orientation improve the result? What happens when the direct path is obstructed? Does the link behave the same way when the test is repeated?

Those questions help distinguish a moment of successful reception from a link that can be trusted in a real deployment. The 20 km figure is part of my experience, not a promise that every LoRa device will reach that distance.

## The Antenna and the Environment Matter

Radio modules are only one part of a wireless system. Antenna choice, matching, orientation, cable and connector losses, and placement can all influence the amount of useful signal that reaches the receiver.

A clear line of sight can help, but seeing the other endpoint does not automatically guarantee a reliable radio path. The surrounding terrain and the space around the direct path can also affect propagation.

This is why range comparisons between different experiments can be misleading. Two people might use similar modules and get very different results because their antennas, radio settings, device heights, and environments are not the same.

Transmit power matters, but it is not the whole story. Receiver sensitivity, bandwidth, spreading factor, interference, and the required reliability all influence the link. Increasing power alone cannot compensate for every problem, and radio settings always need to respect the rules that apply to the frequency and location being used.

The useful lesson is to treat the entire radio path as a system rather than looking for one specification that explains everything.

## What Long-Range LoRa Makes Possible

The practical appeal of LoRa is not simply that a message can travel a long way. It is that small devices can exchange useful information across areas where conventional network infrastructure may be unavailable or impractical.

Think of sensors distributed across agricultural land, environmental monitoring equipment in remote locations, or devices reporting status across a large site. These applications may need only a small reading or a short status message at intervals. They do not necessarily need a high-bandwidth connection or a direct internet link at every device.

LoRa is not a universal replacement for Wi-Fi, cellular networks, or satellite communication. Each technology has different strengths and constraints. But when the job is low-volume data over a long distance with limited power, LoRa is an interesting tool to have available.

The right design still depends on the actual application. A link that works for occasional sensor readings may not be suitable for frequent updates or a system that cannot tolerate missed messages.

## Testing Is How We Learn the Limits

A useful range experiment should record more than the furthest point at which a message arrived. The hardware, antenna arrangement, radio configuration, distance, device height, and environment all help explain the result. Repeating transmissions at each checkpoint gives a better picture of reliability than relying on a single successful packet.

Changing one variable at a time also makes the outcome easier to understand. If the antenna position, transmit power, and radio settings all change together, it becomes difficult to tell which change mattered.

That is the part of embedded engineering I enjoy: taking a question from the workbench into the real world, observing what actually happens, and using those observations to ask better questions. Sometimes the result matches expectations; sometimes it does not. Both outcomes are useful if the experiment is documented honestly.

My own result of approximately 20 km gave me a concrete example of what a LoRa link can achieve in a particular field test. It did not establish a universal range, and it did not remove the need to understand the conditions behind the result.

The distance is the headline, but the real value is what we learn by testing it.

## Beyond the Workbench

Wireless communication is easy to discuss in terms of specifications, theoretical limits, and impressive numbers. Field experiments bring those ideas into contact with the physical world.

Two small devices exchanging data over approximately 20 km is a reminder that useful communication does not always require a conventional network connection. It is also a reminder to be precise: the result belongs to the setup and conditions in which it was achieved.

For me, that is the point of experimenting with LoRa. Not merely to see how far a message can travel, but to understand what makes the link possible, what makes it unreliable, and how that knowledge can inform the next system we build.
