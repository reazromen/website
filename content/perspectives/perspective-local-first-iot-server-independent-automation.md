---
title: "Local-First IoT: What Happens When the Dashboard Server Goes Offline?"
url: /posts/local-first-iot-server-independent-automation.html
date: '2026-10-17'
read_time: 5
excerpt: "A presence sensor exposed an architectural weakness: when a desktop-hosted dashboard disappears, useful automation should not disappear with it."
topic: radio-iot
tags:
  - embedded
  - firmware
  - resilience
  - home-server
  - automation
draft: false
featured: true
language: en
eyebrow: IoT · architecture notes
---

# Local-First IoT: What Happens When the Dashboard Server Goes Offline?

One of the clearest architecture tests is turning off a machine and seeing what stops working. In my presence-aware PC power-saving experiment, a dashboard and listener depended on a desktop being available. When that desktop was off, the dashboard stopped responding too.

That is not necessarily a bug in the dashboard. It is an architectural dependency that became visible during normal use. A small IoT device may be physically independent, yet still depend on a server for decisions that should remain possible when the server is unavailable.

## Separate the control loop from the control panel

A dashboard is an interface for people. It can show sensor status, expose configuration, display history and help diagnose problems. The control loop is different: it receives sensor events, tracks occupancy and timers, and decides whether a power action is safe.

If a nonessential dashboard outage prevents the control loop from working, the two responsibilities are coupled too tightly.

For a modest presence sensor, the device can keep basic logic locally: maintain its current state, apply a conservative absence delay and avoid repeating a command. A local listener can handle operating-system integration. A server can provide history, remote configuration and richer visualization when it is available. The server improves the experience without becoming a mandatory link in every action.

## Design explicit failure behavior

“Local-first” should describe behavior, not just where a service runs. I would define the failure cases before adding more components:

- **Dashboard unavailable:** sensing and the safe local control loop continue.
- **Wi-Fi unavailable:** the device indicates that it is disconnected and does not pretend that remote actions succeeded.
- **PC listener unavailable:** the sensor records or exposes the pending state and retries conservatively rather than assuming the PC slept.
- **Server returns:** buffered events can be reconciled, with timestamps and sequence information so that old events are not mistaken for current commands.
- **Sensor data becomes stale:** the automation falls back to a safe state instead of treating silence as proof that the room is empty.

Not every small device needs a database or message broker. A few explicit states and a bounded event queue may be enough. The right design is the smallest one that makes failures understandable and recoverable.

## Avoid a second single point of failure

Moving everything from a desktop to a home server would improve availability in some circumstances, but it would not make the design independent. The home server can also reboot, lose power, run out of storage or lose network connectivity.

The important question is which functions truly require the server. Telemetry aggregation, long-term history and remote access are natural server responsibilities. A simple local decision with a clear safe default often is not.

This does not mean every device must be fully autonomous. Some actions genuinely need a central policy, shared state or credentials. It means the dependency should be intentional, and the device should know what to do when that dependency disappears.

## Test the boundary, not just the happy path

A useful reliability test is to run the automation, then deliberately stop the dashboard, disconnect the server from the network, reboot the PC listener and restore each component. Check whether the sensor still reports a truthful state, whether pending timers behave sensibly, and whether recovery creates duplicate or stale actions.

I also want the interface to distinguish **last known state** from **current confirmed state**. A green indicator left over from yesterday is not proof that a device is reachable now.

## The design principle

The goal is not to eliminate servers. It is to avoid making a server responsible for every small action merely because a dashboard happens to live there. Keep essential behavior close to the device, use the server for capabilities that benefit from centralization, and make every dependency visible.

A system is not local-first because it has an ESP board. It is local-first when useful behavior survives the loss of optional infrastructure—and when the user can tell exactly what still works.
