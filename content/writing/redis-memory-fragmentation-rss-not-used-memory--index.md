---
title: Redis used_memory Can Look Fine While RSS Keeps Growing
url: /posts/redis-memory-fragmentation-rss-not-used-memory/index.html
date: '2026-09-26'
read_time: 8
excerpt: Allocator fragmentation, active pages, copy-on-write during forks, and persistence
  work can make process RSS diverge from the logical size of the Redis dataset.
topic: redis-systems
tags:
- redis
- memory
- fragmentation
- rss
draft: false
featured: false
language: en
eyebrow: Redis Memory · Redis systems note
outputs:
- url: /posts/redis-memory-fragmentation-rss-not-used-memory/index.html
  template: cms/templates/posts/posts--redis-memory-fragmentation-rss-not-used-memory--index.tpl
  source: cms/templates/posts/posts--redis-memory-fragmentation-rss-not-used-memory--index.json
---

A Redis dataset can stay roughly constant while the operating system reports that the process is consuming more memory. That does not automatically mean a leak.

## There are several memory boundaries

Useful Redis allocator metrics separate allocated bytes, active pages, resident pages, and process RSS. The gaps between them tell different stories about internal and external fragmentation.

## Deleting keys does not force pages back to the kernel

Redis can free objects while the allocator keeps the pages for future reuse. From Redis's point of view, that memory may be available for new allocations even if `top` shows unchanged RSS.

## Active defragmentation spends CPU

Redis can move allocations to reduce fragmentation, but that work uses CPU. The monitoring metrics expose defragmentation activity because the cure can itself affect latency.

## fork changes the memory picture

RDB snapshots and AOF rewrites use `fork()`. Parent and child initially share memory through copy-on-write. When the parent keeps modifying pages, the OS must copy them. Under a high write rate, persistence can create substantial temporary RSS growth without a larger logical dataset.

## maxmemory is not the whole process limit

Redis still needs memory for replication buffers, client buffers, persistence work, allocator fragmentation and other overhead. Running a host with almost no headroom because `maxmemory` fits inside RAM is unsafe.

## Measure patterns, not one ratio

I would track logical used memory, allocator allocated/active/resident, RSS, fragmentation ratios, defrag state, AOF/RDB rewrite state, copy-on-write bytes, and host swap activity.

## Restarting destroys evidence

A restart often collapses fragmentation and makes the graph look normal, but it also removes the evidence needed to distinguish fragmentation from key growth or persistence pressure. Capture `INFO MEMORY`, persistence state and latency events first.

Reusable memory is not necessarily wasted memory. The question is whether Redis can reuse it efficiently and whether the host has enough headroom for the next persistence or replication event.

## Sources and further reading

- [Redis monitoring metrics](https://redis.io/docs/latest/operate/rs/monitoring/get-started/)
- [Redis latency monitor](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency-monitor/)
- [Redis 8.6 memory monitoring](https://redis.io/docs/latest/develop/whats-new/8-6/)
