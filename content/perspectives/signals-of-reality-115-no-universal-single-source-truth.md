---
title: There Is No Universal Single Source of Truth
url: /posts/signals-of-reality-115-no-universal-single-source-truth.html
date: '2026-01-18'
read_time: 8
excerpt: "\"Single source of truth\" is useful within a bounded domain, but complex systems contain multiple authoritative sources for different facts and timescales."
topic: systems-thinking
tags:
- source-of-truth
- distributed-systems
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · The System Behind the Dashboard'
editorial_batch: signals-of-reality-200
---

Teams love the phrase:

single source of truth.

It promises an end to disagreement.

Put the canonical data here.

Make everything else derive from it.

Within a bounded domain, that can be excellent architecture.

The trouble begins when the phrase becomes universal.

A complex system rarely has one source authoritative for every question.

## Authority is scoped

A Git repository may be the source of truth for desired configuration.

The runtime is the source of evidence for what is actually deployed.

A database may be authoritative for account state.

An identity provider may be authoritative for authentication.

A billing platform may be authoritative for settled invoices.

A device may be authoritative for its current sensor reading.

Which one is the source of truth?

For which truth?

The question needs a domain.

## Desired state and observed state can disagree

Infrastructure-as-code says three instances should exist.

Runtime inspection shows two.

Which source wins?

For intention, the repository.

For current reality, the runtime.

The discrepancy is exactly what a reconciler needs to see.

If we insist one source is truth in every sense, we lose the ability to represent drift.

Healthy systems often preserve both desired and observed state deliberately.

## Historical truth needs another source

A current database row says the user's plan is Pro.

What plan did they have last month?

The current-state database may not know.

An event log, audit record, or warehouse may be authoritative for history.

The same entity has different sources for current and historical questions.

Time changes authority.

## Derived data can become operationally authoritative

A search index is derived from a database.

In theory, the database is canonical.

In practice, users experience the search index.

If indexing lags, the canonical database can be correct while the product remains wrong.

Operational truth includes derived systems because users interact with them.

"Just check the database" may explain source state without explaining experience.

## External reality outranks internal records

A logistics database says a package is in a warehouse.

A physical scan shows it is on a truck.

Which source is truth?

Ultimately, information systems model external processes.

The database's authority comes from a measurement and update chain.

When that chain breaks, the authoritative record can be authoritatively wrong.

This is why reconciliation with the physical world matters.

## Single source of truth is still a useful design goal

The critique should not become an excuse for uncontrolled duplication.

For a given field and business rule, choose a canonical owner.

Avoid multiple writable copies without clear reconciliation.

Document data lineage.

Make replicas and caches visibly derived.

Define conflict authority.

The phrase works well when scoped.

It fails when used as metaphysics.

## A better question

Instead of asking:

What is the source of truth?

ask:

Which system is authoritative for this claim, at this time, for this purpose?

Where is that claim derived elsewhere?

How stale can copies be?

What external observation can contradict the record?

How is disagreement reconciled?

These questions produce architecture.

The slogan alone produces comfort.

There is no universal single source of truth because complex systems contain many kinds of truth: desired, observed, historical, derived, external, and user-experienced.

Reliability comes from making their relationships explicit.
