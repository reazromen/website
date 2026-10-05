---
title: Stateful Nomad Failover Gets Hard at the CSI Volume Boundary
url: /posts/nomad-stateful-failover-csi-boundary.html
date: '2025-12-31'
read_time: 9
excerpt: Nomad can decide that an allocation belongs on another node before the storage
  system has safely detached, unpublished, and made its volume available there. Scheduler
  failover and storage failover are connected state machines.
topic: ''
tags:
- nomad
- csi
- stateful
- failover
draft: false
featured: false
language: en
eyebrow: Orchestration & Storage · systems note
outputs:
- url: /posts/nomad-stateful-failover-csi-boundary.html
  template: cms/templates/posts/posts--nomad-stateful-failover-csi-boundary.tpl
  source: cms/templates/posts/posts--nomad-stateful-failover-csi-boundary.json
---

A stateless service makes rescheduling look deceptively simple.

A node disappears, the scheduler chooses another node, a replacement allocation starts, and service discovery catches up.

Add a single-writer block volume and the same event becomes a coordination problem between Nomad, CSI controller state, node plugins, the storage provider, the old allocation, and the new allocation.

## Placement is only the first decision[#](#placement-is-only-the-first-decision)

Nomad's scheduler is aware of CSI volumes and can constrain placement based on plugin availability and volume state.

Before a task starts, the volume must be claimed. If the provider uses a controller plugin, the controller may need to attach the volume to the selected node. Then the node plugin stages and publishes the filesystem or block device locally.

The state transition looks roughly like:

```
allocation placed
 -> volume claim
 -> controller attach
 -> node stage
 -> node publish
 -> task starts
```

Stopping reverses that path.

## Failure interrupts the reverse path[#](#failure-interrupts-the-reverse-path)

On a clean stop, Nomad can ask the node plugin to unpublish/unmount, notify the server, have the controller detach, and release the claim.

A lost node cannot necessarily perform those local cleanup operations.

Now the scheduler may know it needs a replacement while the storage provider still believes the old node owns the attachment.

That is the boundary where “Nomad rescheduled it” and “the stateful workload recovered” become different statements.

## Drain, migrate, reschedule, and replace are not the same event[#](#drain-migrate-reschedule-and-replace-are-not-the-same-event)

Nomad distinguishes planned drain migration from failed-task rescheduling and lost-node replacement.

The documentation explicitly notes that a node drain uses migration behavior, not the reschedule block. A lost node is replacement behavior. Failed allocations use restart/reschedule logic.

That distinction matters because storage cleanup opportunities differ.

A planned drain can keep CSI plugin tasks until volume-using tasks are stopped. A hard node loss cannot rely on the old node cooperating.

## CSI plugins are control plane after mount[#](#csi-plugins-are-control-plane-after-mount)

Once a task has a mounted volume, CSI plugins are not in the data path. The workload reads and writes the mounted device directly.

But the plugin is required again when the volume needs to be unpublished and detached.

This is why HashiCorp recommends leaving node/monolith plugins running until tasks using their volumes are stopped, and why drain handles plugin tasks last.

## Single-writer safety is supposed to be inconvenient[#](#single-writer-safety-is-supposed-to-be-inconvenient)

If the storage system refuses to attach a volume to node B because it still considers node A attached, that can look like bad availability.

It may also be preventing two writers from corrupting a filesystem.

The correct recovery process depends on the storage provider's fencing and attachment semantics. Force-detaching a volume is not a generic scheduler operation; it is a storage decision with data-integrity consequences.

## Observe the whole claim chain[#](#observe-the-whole-claim-chain)

For a stuck stateful allocation I want evidence from every layer:

- Nomad evaluation and placement decision,
- allocation status and predecessor/successor chain,
- volume claim state,
- CSI controller health,
- CSI node-plugin health on old and new nodes,
- provider attachment record,
- mount state on the target node.

If you only inspect the replacement allocation, the real blocker can look invisible.

## Test failover modes separately[#](#test-failover-modes-separately)

I would not use one “failover test.” I would test:

1. planned node drain,
2. task crash with healthy node,
3. Nomad client loss while host remains,
4. hard host power loss,
5. CSI node-plugin failure,
6. CSI controller failure,
7. storage API delay/unavailability.

Each breaks a different control path.

## Stateful HA lives outside the scheduler too[#](#stateful-ha-lives-outside-the-scheduler-too)

Nomad can make a good placement decision and still be unable to make a volume safe to mount.

The complete design includes storage replication, access mode, fencing, attach/detach guarantees, application crash consistency, and recovery time.

That is why stateful orchestration is harder than “add a volume stanza.” The scheduler owns where the workload should run. The storage system owns whether the bytes can safely follow.

## Sources and further reading[#](#sources-and-further-reading)

- [Nomad: Container Storage Interface architecture](https://developer.hashicorp.com/nomad/docs/architecture/storage/csi)
- [Nomad node drain command](https://developer.hashicorp.com/nomad/commands/node/drain)
- [Nomad reschedule block](https://developer.hashicorp.com/nomad/docs/job-specification/reschedule)
- [Nomad CSI volumes](https://developer.hashicorp.com/nomad/docs/stateful-workloads/csi-volumes)
