---
title: Source of Truth vs Source of Record
url: /posts/signals-of-reality-116-source-truth-vs-source-record.html
date: '2026-02-26'
read_time: 7
excerpt: A source of record stores an authoritative record under a defined process. A source of truth is often a looser claim about which representation should guide decisions.
topic: systems-thinking
tags:
- source-of-truth
- database
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · The System Behind the Dashboard'
editorial_batch: signals-of-reality-200
---

A database can be the official record and still fail to describe the world perfectly.

That sounds contradictory only if *record* and *truth* are treated as synonyms.

They are not.

A source of record is an operational institution: the place an organization recognizes as authoritative for a class of records under a defined process.

A source of truth is often used more loosely to mean the representation everyone should rely on.

The distinction becomes important when systems meet the external world.

## A source of record is governed authority

A payroll system can be the system of record for employee compensation.

A Git repository can be the record for approved configuration.

A registrar can be the record for domain ownership.

The authority comes from process.

Who may write?

How are changes approved?

How are corrections made?

How are histories preserved?

The record is trusted because the organization has assigned it a role.

That is different from claiming the record can never be wrong.

## Records can lag reality

A device is physically replaced at 10:00.

Inventory is updated at 10:15.

For fifteen minutes, the inventory system remains the official record and is factually stale about the physical installation.

Nothing unusual happened.

Information propagation took time.

The important question is how the system reconciles with the external event.

Source-of-record design needs update mechanisms, not just authority labels.

## Records can contain error

Human entry.

Software bugs.

Failed integrations.

Duplicate identities.

Misapplied migrations.

An authoritative database can contain incorrect information.

Authority determines which copy should be corrected and propagated.

It does not turn error into truth.

This is why audit trails, validation, reconciliation, and correction workflows matter.

## Derived systems should know their parent

A cache, warehouse, search index, and reporting dataset may all derive from the source of record.

If the lineage is explicit, operators can reason about stale copies.

If lineage is hidden, every system begins to look equally authoritative.

Then disagreements become political.

Which dashboard is right?

Which export is right?

Which API is right?

Lineage turns the argument back into engineering.

## Sometimes the runtime is the stronger witness

Configuration management says a firewall rule should exist.

A packet is still blocked.

The desired-state repository remains authoritative for intention.

The running firewall is stronger evidence for actual enforcement.

Neither should replace the other.

The gap is the incident.

This is why systems need both configuration state and runtime verification.

## "Truth" is often too strong a word

Engineering benefits from narrower vocabulary.

Canonical source.

Authoritative record.

Observed state.

Derived view.

Cached copy.

Historical ledger.

Expected configuration.

These phrases tell us what role the data plays.

"Source of truth" often hides those distinctions under one reassuring label.

## Authority should be contestable by evidence

A healthy source of record has a correction path.

If physical evidence, independent records, or user reports reveal an error, the system can change.

An authoritative record that cannot be corrected becomes dangerous.

The record should stabilize coordination, not override reality.

Source of truth versus source of record is therefore more than terminology.

The first phrase tempts us toward metaphysics.

The second reminds us that authority is a designed institutional role.

A good system of record does not need to be infallible.

It needs to be identifiable, auditable, correctable, and explicit about what it is authoritative for.
