---
title: PostgreSQL VACUUM Reclaims Space Without Giving the File Back to the Filesystem
url: /posts/postgres-vacuum-reuse-not-filesystem-shrink.html
date: '2026-09-26'
read_time: 8
excerpt: Standard VACUUM makes dead-tuple space reusable inside a table. It usually
  does not shrink the table file, which is why a successful vacuum and unchanged disk
  usage can both be correct.
topic: ''
tags:
- postgresql
- vacuum
- mvcc
- bloat
draft: false
featured: false
language: en
eyebrow: Databases & Operations · systems note
outputs:
- url: /posts/postgres-vacuum-reuse-not-filesystem-shrink.html
  template: cms/templates/posts/posts--postgres-vacuum-reuse-not-filesystem-shrink.tpl
  source: cms/templates/posts/posts--postgres-vacuum-reuse-not-filesystem-shrink.json
---

A PostgreSQL table grows to 300 GB. You delete half the rows. `VACUUM` completes successfully.

The filesystem still shows roughly 300 GB.

This feels like vacuum failed only if “reclaim space” is assumed to mean “return blocks to the operating system.” PostgreSQL usually means something else.

## MVCC keeps old row versions[#](#mvcc-keeps-old-row-versions)

PostgreSQL uses multiversion concurrency control. An `UPDATE` creates a new row version; a `DELETE` does not immediately erase bytes that older transactions might still need to see.

Once those old versions are no longer visible to any transaction, they are dead tuples.

Standard `VACUUM` makes that space available for reuse.

## Reuse is different from truncation[#](#reuse-is-different-from-truncation)

If free pages are scattered through the middle of a relation file, PostgreSQL cannot simply punch them out and keep the rest of the file layout unchanged.

So normal vacuum leaves the file mostly the same size and marks space reusable by future inserts/updates.

The database can stop growing even though `du` does not go down.

That is often the desired steady state for an update-heavy table.

## VACUUM FULL rewrites the table[#](#vacuum-full-rewrites-the-table)

`VACUUM FULL` can compact a table and return much more space to the filesystem because it rewrites the relation into a new file.

The cost is significant: it takes an `ACCESS EXCLUSIVE` lock and needs extra disk space while the rewrite exists alongside the old relation.

PostgreSQL documentation explicitly recommends routine standard vacuuming rather than treating `VACUUM FULL` as ordinary maintenance.

## Bloat is workload history made physical[#](#bloat-is-workload-history-made-physical)

A table with high update/delete churn can accumulate dead space faster than autovacuum cleans it, especially when row width is large or indexes amplify write churn.

But “bloat” should be measured against future reuse needs.

If a 300 GB table naturally oscillates between 250 and 300 GB every day, shrinking it to 250 GB every night only forces PostgreSQL to allocate the same space again tomorrow.

## Long transactions can hold dead tuples hostage[#](#long-transactions-can-hold-dead-tuples-hostage)

Vacuum cannot remove a row version that might still be visible to an old transaction snapshot.

That means a long-running transaction, abandoned idle-in-transaction session, or certain replication/slot conditions can prevent cleanup across many subsequent updates.

When vacuum “cannot keep up,” inspect transaction age and replication state before simply increasing vacuum workers.

## HOT updates change index churn[#](#hot-updates-change-index-churn)

Heap-Only Tuple updates can avoid creating new index entries when indexed columns are unchanged and page conditions allow it.

That can materially reduce index bloat for update-heavy tables.

Schema design, fillfactor, and which columns are indexed therefore influence how expensive MVCC churn becomes.

## Autovacuum thresholds should match hot tables[#](#autovacuum-thresholds-should-match-hot-tables)

Default autovacuum settings are cluster-wide compromises. Very large or very hot tables can need table-specific thresholds and scale factors so cleanup starts before dead tuples become a large fraction of the relation.

Useful observations include:

- dead/live tuple estimates,
- last autovacuum time,
- vacuum progress,
- transaction age,
- table and index size trends,
- update/delete rate.

## Indexes have their own bloat story[#](#indexes-have-their-own-bloat-story)

Shrinking heap churn does not automatically mean every index is compact. Indexes can accumulate unused/dead entries and may need reindexing strategies depending on access method and workload.

Tools such as `pg_repack` are popular because they can rebuild tables/indexes with less blocking than `VACUUM FULL`, but they are operational tools with their own requirements—not a replacement for healthy autovacuum.

## Ask which space you need back[#](#ask-which-space-you-need-back)

There are two different goals:

```
make dead space reusable by PostgreSQL
vs
return allocated filesystem blocks to the OS
```

Standard `VACUUM` is primarily about the first goal plus statistics, visibility-map maintenance, and transaction-ID safety.

If the second goal is actually required—perhaps after a one-time archival deletion—then a rewrite strategy may be justified.

The key is not to diagnose unchanged file size as a failed vacuum. In PostgreSQL, a stable large file full of reusable pages can be exactly what healthy steady-state maintenance looks like.

## Sources and further reading[#](#sources-and-further-reading)

- [PostgreSQL 17: Routine Vacuuming](https://www.postgresql.org/docs/17/routine-vacuuming.html)
- [PostgreSQL VACUUM command documentation](https://www.postgresql.org/docs/current/sql-vacuum.html)
