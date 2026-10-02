---
title: pgvector HNSW Can Return Fast Answers That Are Operationally Wrong
url: /posts/pgvector-hnsw-fast-operationally-wrong.html
date: '2026-09-26'
read_time: 9
excerpt: Approximate nearest-neighbor search is allowed to trade recall for speed.
  Add tenant or metadata filters after the ANN scan and a fast query can return too
  few candidates without being a database error.
topic: ''
tags:
- postgresql
- pgvector
- hnsw
- rag
draft: false
featured: false
language: en
eyebrow: Databases & Retrieval · systems note
outputs:
- url: /posts/pgvector-hnsw-fast-operationally-wrong.html
  template: cms/templates/posts/posts--pgvector-hnsw-fast-operationally-wrong.tpl
  source: cms/templates/posts/posts--pgvector-hnsw-fast-operationally-wrong.json
---

Vector search has a dangerous success condition: the query returns quickly and the answer looks plausible.

That can be enough for a demo. It is not enough for a production retrieval system.

pgvector makes the tradeoff explicit. Exact nearest-neighbor search gives perfect recall. HNSW and IVFFlat are approximate indexes: they trade some recall for speed.

The operational mistake is to measure only latency.

## Approximate search changes the meaning of “top 10”[#](#approximate-search-changes-the-meaning-of-top-10)

Without an ANN index, PostgreSQL can compute the distance against all eligible rows, sort them, and return the nearest results. That is expensive but conceptually simple.

With HNSW, the index traverses a graph and builds a candidate set. Parameters such as `hnsw.ef_search` control how broad that search is.

The result is “the best candidates found under this search budget,” not a mathematical promise that the globally nearest ten rows were found.

For many workloads that trade is excellent. But it has to be measured as recall, not assumed.

## Filtering is where surprises become production bugs[#](#filtering-is-where-surprises-become-production-bugs)

Consider a multi-tenant RAG table:

```
SELECT id, content
FROM documents
WHERE tenant_id = 42
ORDER BY embedding <-> $query
LIMIT 10;
```

A natural mental model is: filter to tenant 42, then find the ten nearest vectors.

With an approximate index, the execution behavior can be effectively the other way around: scan a limited ANN candidate set, then apply the filter.

The pgvector documentation gives a concrete example. If a condition matches 10% of rows and HNSW's default `ef_search` is 40, only around four candidates may survive the filter on average.

Your query asked for ten. The database can return fewer without anything “failing.”

## Iterative scans exist because post-filtering is real[#](#iterative-scans-exist-because-post-filtering-is-real)

pgvector 0.8 introduced iterative index scans. When filtering removes too many ANN candidates, the engine can continue scanning more of the index until enough qualifying rows are found or a configured limit is reached.

You can choose strict or relaxed ordering:

```
SET hnsw.iterative_scan = strict_order;

-- or
SET hnsw.iterative_scan = relaxed_order;
```

Relaxed ordering can improve recall at the cost of exact distance ordering. There are also controls such as `hnsw.max_scan_tuples` and `hnsw.scan_mem_multiplier`.

Those knobs reveal the real system: recall, latency, CPU, and memory are coupled.

## Tenant isolation changes both correctness and performance[#](#tenant-isolation-changes-both-correctness-and-performance)

pgvector explicitly warns that when multiple tenants share one approximate index, vectors from one tenant can affect recall and speed for another.

If tenant filters are highly selective, a shared global HNSW graph may spend much of its search budget exploring candidates that are later discarded.

Possible designs include:

- a normal B-tree filter plus exact vector search for small tenant slices,
- partial HNSW indexes for a small fixed set of categories,
- list partitioning by tenant or group,
- separate tables for strong isolation,
- or a shared ANN index with iterative scans and measured recall.

There is no universal winner. The right design depends on tenant count, vectors per tenant, update rate, memory, and query mix.

## RAG correctness is not database correctness[#](#rag-correctness-is-not-database-correctness)

A database can execute the query exactly as configured while the application still retrieves the wrong context.

That is why I would evaluate a vector index with an application-level test set:

1. run the same query using exact search,
2. record the relevant IDs and distances,
3. run HNSW under production filters,
4. measure overlap/recall,
5. vary `ef_search`, iterative-scan settings, and tenant selectivity,
6. measure latency and memory alongside recall.

Without an exact baseline, “retrieval quality looks okay” is mostly intuition.

## Deletes and churn belong in the test[#](#deletes-and-churn-belong-in-the-test)

Production indexes are not static benchmark datasets. Documents are inserted, deleted, re-embedded, moved between metadata categories, and invalidated.

pgvector notes that dead tuples can reduce the number of results found by ANN scans. PostgreSQL maintenance therefore becomes part of retrieval quality.

Vacuum behavior, table churn, index growth, and reindex strategy are not only DBA concerns when the index sits inside a RAG system. They can affect what context reaches the model.

## Fast is one dimension[#](#fast-is-one-dimension)

HNSW is valuable because it can dramatically reduce the work needed for nearest-neighbor search. The mistake is treating the speedup as free.

Approximate search gives you a budgeted exploration of vector space. Filtering, multitenancy, churn, and query planner behavior decide how much of that exploration turns into usable rows.

A fast query that returns seven plausible documents instead of the ten best qualifying documents may still produce a fluent answer.

That is exactly why the failure is dangerous.

For vector retrieval, latency is a benchmark. Recall under the real filter distribution is a correctness property.

## Sources and further reading[#](#sources-and-further-reading)

- [pgvector README: HNSW, filtering, multitenancy and iterative scans](https://github.com/pgvector/pgvector/blob/master/README.md)
- [PostgreSQL documentation: indexes](https://www.postgresql.org/docs/current/indexes.html)
- [PostgreSQL documentation: table partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)
