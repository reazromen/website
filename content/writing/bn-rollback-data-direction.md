---
title: Rolling Back Code Is Not the Same as Rolling Back Data
date: '2020-11-03'
draft: false
language: en
url: /posts/bn-rollback-data-direction.html
topic: disaster-recovery
tags:
- rollback
- deployment
featured: false
read_time: 2
excerpt: >-
  Rollback usually sounds like restoring an older release. But if the new code changed
  the structure or meaning of data, whether the old code can still read that data is a
  separate question.
editorial_batch: 20261003-100-niches
---

Rollback usually sounds like restoring an older release. But if the new code changed the structure or meaning of data, whether the old code can still read that data is a separate question. Code can move backward more easily than data semantics.

Suppose a new release changes the meaning of a field. Starting the old binary does not magically restore the old meaning of the stored value. Before release, it is worth asking whether the change remains readable by older software.

Some migrations can be staged: first read both formats, then begin writing the new one, and only later remove the old path. The correct method depends on the application. What matters is knowing what data could be lost or misread on the way back.

A rollback plan should include more than a list of executable files. Data meaning, configuration, and external relationships belong in it too. A change that is difficult to reverse should not be hidden behind the language of an easy rollback.

Source: [official reference](https://www.postgresql.org/docs/current/backup.html).
