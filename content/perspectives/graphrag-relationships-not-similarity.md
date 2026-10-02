---
title: GraphRAG Is Useful When the Question Is About Relationships, Not Similarity
url: /posts/graphrag-relationships-not-similarity.html
date: '2026-09-26'
read_time: 9
excerpt: Vector retrieval is excellent when the answer lives near semantically similar
  text. Graph-oriented retrieval earns its cost when the answer depends on relationships,
  communities, or evidence spread across multiple parts of a corpus.
topic: ''
tags:
- graphrag
- rag
- knowledge-graph
- retrieval
draft: false
featured: false
language: en
eyebrow: AI Systems & Retrieval · systems note
outputs:
- url: /posts/graphrag-relationships-not-similarity.html
  template: cms/templates/posts/posts--graphrag-relationships-not-similarity.tpl
  source: cms/templates/posts/posts--graphrag-relationships-not-similarity.json
---

GraphRAG discussions often start from the wrong end.

Someone has a working vector RAG system, sees a knowledge-graph diagram, and asks whether GraphRAG is the “next version” they should migrate to.

The better question is what class of query the current retrieval model cannot represent efficiently.

## Vector search is a similarity machine[#](#vector-search-is-a-similarity-machine)

Dense retrieval works beautifully when the question and the useful chunk occupy nearby semantic space.

Ask “What does the refund policy say about damaged items?” and a good embedding model can retrieve the paragraph that discusses damaged items and refunds.

The problem appears when the answer is not located in one semantically obvious chunk.

For example:

```
Which suppliers are connected to projects
that missed deadlines
and also appear in security incidents?
```

The evidence may be distributed across supplier documents, project status notes, incident reports, and organization relationships. No individual paragraph necessarily resembles the full question.

## A graph makes relationships first-class[#](#a-graph-makes-relationships-first-class)

Microsoft GraphRAG's indexing pipeline extracts entities, relationships, and claims from text, then performs community detection and generates summaries at multiple levels.

That creates a second retrieval surface beyond raw chunks.

The system can enter through an entity, expand through connected entities and relationships, use community reports, and combine that structured context with original text.

This is useful when the path between facts matters as much as semantic similarity.

## Local and global questions are different[#](#local-and-global-questions-are-different)

GraphRAG explicitly separates query modes.

Local Search is entity-centered: find relevant entities, then fan out through connected text units, relationships, covariates, and community reports.

Global Search is corpus-centered: reason over community summaries for questions such as “what are the major themes across this dataset?”

Baseline vector RAG is weak at that kind of global aggregation because there may be no single chunk that is “similar” to a request for the top themes of an entire corpus.

That distinction is more important than the label GraphRAG.

## The graph is generated data, not ground truth[#](#the-graph-is-generated-data-not-ground-truth)

Graph extraction introduces a new failure surface.

An LLM or extraction pipeline decides that two mentions refer to the same entity, that a relationship exists, or that a claim has a certain form. Those decisions can be wrong.

A graph can therefore make a hallucinated relationship look structured and authoritative.

I would keep provenance back to source text for every important entity/edge and design the answer path so retrieved graph facts can be inspected against the underlying documents.

Structure improves retrieval. It does not remove the need for evidence.

## Indexing cost moves work earlier[#](#indexing-cost-moves-work-earlier)

Standard RAG can be relatively cheap to ingest: split documents, embed chunks, write vectors.

GraphRAG adds extraction, entity resolution, relationship creation, community detection, summaries, and often additional embeddings.

That can be the correct trade if the corpus is queried repeatedly and relationship-heavy questions are valuable. It can be wasteful if the corpus changes constantly or most questions are simple document lookup.

The architecture should compare:

```
indexing cost
+ refresh cost
+ graph quality work
+ query cost
vs
accuracy gain on the target question set
```

## Freshness is harder with derived structure[#](#freshness-is-harder-with-derived-structure)

When one source document changes, a vector index may only need new embeddings for affected chunks.

A graph update can ripple. Entity attributes change, relationships appear or disappear, communities shift, and precomputed summaries can become stale.

That makes incremental update strategy part of the design.

If your corpus is a fast-moving operational dataset, the graph may need a very different refresh model from a relatively stable research archive.

## Hybrid retrieval is often the practical answer[#](#hybrid-retrieval-is-often-the-practical-answer)

The existence of GraphRAG does not imply vector retrieval should disappear.

Microsoft's own query engine includes a Basic Search mode for baseline RAG alongside local, global, and DRIFT search.

That makes sense. Different queries need different retrieval structures.

A practical system can route:

- direct factual lookup to lexical/vector search,
- entity relationship questions to graph-local search,
- whole-corpus synthesis to global/community search,
- and combine graph candidates with original chunks before generation.

## Evaluate by question class[#](#evaluate-by-question-class)

I would not benchmark GraphRAG with one global answer-quality score.

Create a test set labeled by query type:

- single-document fact,
- semantic lookup,
- multi-hop entity relationship,
- cross-document aggregation,
- whole-corpus theme,
- time-sensitive/freshness question.

Then compare baseline vector RAG and graph-assisted retrieval within each class.

If GraphRAG only wins on the relationship-heavy slice, that is not a failure. It tells you when to pay for it.

## Data structure should follow the question[#](#data-structure-should-follow-the-question)

A knowledge graph is useful because some information is fundamentally relational.

Vector search is useful because language has fuzzy semantic similarity.

Those are different primitives.

I would reach for GraphRAG when the missing capability is “follow and aggregate relationships across the corpus,” not because a graph looks more advanced than a vector database.

The retrieval structure should be justified by the questions humans actually ask.

## Sources and further reading[#](#sources-and-further-reading)

- [Microsoft GraphRAG overview](https://microsoft.github.io/graphrag/)
- [Microsoft GraphRAG: query engine overview](https://microsoft.github.io/graphrag/query/overview/)
- [Microsoft GraphRAG: Local Search](https://github.com/microsoft/graphrag/blob/main/docs/query/local_search.md)
- [Microsoft GraphRAG: Global Search](https://github.com/microsoft/graphrag/blob/main/docs/query/global_search.md)
- [Stack Overflow discussion: when to use GraphRAG instead of vector RAG](https://stackoverflow.com/questions/80000407/when-should-i-use-graphrag-instead-of-traditional-vector-based-rag)
