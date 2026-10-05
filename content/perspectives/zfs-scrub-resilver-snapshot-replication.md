---
title: ZFS Scrub, Resilver, Snapshot, and Replication Solve Different Failure Modes
url: /posts/zfs-scrub-resilver-snapshot-replication.html
date: '2025-06-19'
read_time: 8
excerpt: A scrub detects latent corruption, a resilver reconstructs missing redundancy,
  a snapshot preserves an earlier dataset state, and replication puts that state somewhere
  else. Calling all four 'backup' hides the failures each one cannot solve.
topic: ''
tags:
- zfs
- storage
- backup
- recovery
draft: false
featured: false
language: en
eyebrow: Storage & Reliability · systems note
outputs:
- url: /posts/zfs-scrub-resilver-snapshot-replication.html
  template: cms/templates/posts/posts--zfs-scrub-resilver-snapshot-replication.tpl
  source: cms/templates/posts/posts--zfs-scrub-resilver-snapshot-replication.json
---

ZFS has several features that feel like “data safety,” and that similarity creates bad recovery plans.

A scrub, a resilver, a snapshot, and a replicated dataset can all be part of a reliable storage system. They protect against different failures.

## Scrub: is the data still internally correct?[#](#scrub-is-the-data-still-internally-correct)

ZFS checksums blocks. A scrub walks the pool, reads data, verifies checksums, and—when redundancy exists—repairs damage using a good copy.

That is how latent corruption can be discovered before the last good replica is also lost.

A scrub does not bring back a file you intentionally deleted yesterday. The checksum of “file no longer exists” is perfectly valid state.

## Resilver: restore redundancy after a device falls behind[#](#resilver-restore-redundancy-after-a-device-falls-behind)

Resilvering is similar I/O machinery applied to a different question. Instead of reading everything to search for silent corruption, it reconstructs blocks ZFS knows are missing or out of date on a replacement or reattached device.

OpenZFS summarizes the distinction cleanly: scrub examines all data; resilver examines data known to be out of date.

That means replacing a failed disk and resilvering is not a substitute for a scrub schedule, and running a scrub does not create a second copy if the pool has no redundancy.

## Snapshot: preserve earlier logical state[#](#snapshot-preserve-earlier-logical-state)

A snapshot gives you a read-only view of a dataset at a point in time using ZFS's copy-on-write model.

That protects against logical mistakes such as deletion, overwrite, or a bad application migration—provided the relevant snapshot still exists.

It does not protect against losing the whole pool. A snapshot stored only on the failed pool disappears with the pool.

## Replication: move recovery state across a failure boundary[#](#replication-move-recovery-state-across-a-failure-boundary)

`zfs send` and `zfs receive` can replicate snapshots to another pool. Incremental streams transfer changes between snapshots.

The important word is “another.”

If the receiving pool is on another host, another rack, or another site, replication can protect against progressively larger failures. If it is another disk in the same chassis under the same power supply and operator account, the failure boundary is much smaller.

## Build a failure matrix[#](#build-a-failure-matrix)

I find it clearer to start from events:

```
latent bit corruption     -> scrub + redundancy
single disk failure       -> redundancy + resilver
accidental file deletion  -> snapshot
bad application migration -> snapshot
pool/controller loss      -> replicated copy / backup
host theft/fire           -> off-site copy
ransomware/operator error -> immutable/offline/isolated recovery copy
```

No one row solves the whole table.

## Checksums without redundancy detect but cannot repair[#](#checksums-without-redundancy-detect-but-cannot-repair)

ZFS can tell you a block is corrupt even on a single-disk pool. That is valuable evidence.

But without another valid copy, detection is not repair.

This matters because people sometimes hear “ZFS self-heals” and infer that checksums generate missing information. They do not. Self-healing needs redundancy.

## Long resilvers change risk[#](#long-resilvers-change-risk)

Large pools and large disks can spend a long time rebuilding, which is why operators worry about what happens if another device fails or unreadable data is discovered during the window.

The useful response is not panic; it is designing redundancy, spare strategy, scrub cadence, workload I/O, and backups so a rebuild is one layer of recovery rather than the only layer.

## Send streams are transport, not automatically an archive[#](#send-streams-are-transport-not-automatically-an-archive)

OpenZFS documentation notes that send streams are just bytes and can be stored in files, but a damaged byte can make the stream unusable. A received dataset is checksummed, scrubable, and can participate in normal ZFS recovery.

That is an important operational distinction between “I saved a stream file somewhere” and “I maintain a healthy replicated pool.”

## Recovery has to be tested[#](#recovery-has-to-be-tested)

A snapshot policy that has never restored a real directory is a theory. A replication job that has never promoted a receiver is a theory.

I would periodically test:

- restore one file from snapshot,
- receive an incremental stream,
- mount or promote the replica,
- replace a simulated failed device,
- and verify alerting around scrub/resilver errors.

Storage safety becomes real only when the recovery path is routine enough to execute under pressure.

## Sources and further reading[#](#sources-and-further-reading)

- [OpenZFS: Scrub and Resilver](https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Operations/Scrub%20and%20Resilver.html)
- [OpenZFS zpool-scrub manual](https://openzfs.github.io/openzfs-docs/man/master/8/zpool-scrub.8.html)
- [OpenZFS: Send and Receive](https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Operations/Send%20and%20Receive.html)
