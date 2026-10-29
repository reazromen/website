---
title: "Before There Was Software Architecture, There Was the Carpenter"
draft: false
date: '2026-10-29'
language: en
url: /posts/before-software-architecture-there-was-the-carpenter.html
read_time: 8
excerpt: >-
  Long before computers, people designed systems to grow food, build houses, move goods, and repeat complex work. Modern software architecture has older roots than the computer industry.
eyebrow: "Perspectives · Systems Thinking"
tags: ["systems-thinking", "software-architecture", "craftsmanship", "design", "computing-history"]
---

# Before There Was Software Architecture, There Was the Carpenter

A carpenter measures timber before cutting it. A farmer plans around seasons, soil, water, and uncertainty. A shopkeeper keeps track of stock, debts, and deliveries. None of them needs a computer science degree to understand that a result depends on many connected parts—and that a small mistake in one place can cause trouble somewhere else.

They are designing systems.

I keep coming back to this because software architecture is often presented as if it began with servers, programming languages, databases, and cloud infrastructure. Those technologies matter, of course. But the deeper activity is much older: understanding a problem, arranging parts, deciding how they should interact, handling exceptions, and making the whole thing work reliably.

Computers did not invent systems thinking. They gave us a new medium in which to express and execute it.

## Every craft contains an architecture

Think about a carpenter building a door.

The carpenter has to understand the purpose of the door, the properties of the wood, the dimensions of the opening, the behavior of joints, the tools available, and the tolerances that determine whether the door will fit. The parts cannot be designed independently of one another. A perfect panel does not rescue a badly measured frame.

The work has structure, interfaces, constraints, dependencies, and failure modes. It also has feedback: measure, cut, test the fit, adjust, and test again.

A farmer faces a different set of materials, but the same kind of reasoning. Planting is connected to weather, water, soil, seed selection, labor, storage, and market timing. A decision that improves one part of the process can damage another. Irrigation that is useful in one condition may be wasteful in another. A harvest is not a single action; it is the outcome of a system maintained over time.

A merchant's ledger is another example. It represents a changing world—goods arriving and leaving, money owed, money received, and commitments that must not be forgotten. The ledger is a model of the business, not the business itself. If the model becomes inaccurate, decisions based on it become unreliable.

These people may never call their work architecture. Yet they routinely practice decomposition, coordination, state tracking, constraint management, and error recovery. Those are not exclusively digital ideas.

The comparison has limits. Building a door is not the same as designing a distributed system, and professional software architecture requires technical knowledge of concurrency, security, data consistency, deployment, and operational failure. The point is not that every craftsperson is already a software architect. It is that many of the habits architecture depends on were developed in practical work long before the profession acquired its modern name.

## The loom that made instructions replaceable

There is a particularly tangible link between craft and computing history: the Jacquard loom.

In 1801, Joseph Marie Jacquard demonstrated a loom mechanism controlled by a chain of punched cards. The holes determined which threads were raised as the fabric was woven. Changing the cards changed the pattern the machine produced. A complex design could be represented as instructions and reproduced by machinery.

The [Computer History Museum's account of the Jacquard loom](https://www.computerhistory.org/storageengine/punched-cards-control-jacquard-loom/) describes how this approach to controlling a loom became part of the history of punched-card computing. Charles Babbage later proposed punched cards as a way to direct operations in his Analytical Engine. The [Smithsonian's history of punch cards](https://www.si.edu/spotlight/punch-cards/punch-cards-before-tabulating-machines) documents that connection as well.

This does not mean that software was simply invented by a weaver, or that the history of computing has one origin. The more careful lesson is that programmable machinery emerged partly from practical attempts to control complex, repeatable work.

The loom separated the pattern from the mechanism that wove it. The machine could remain largely the same while the instructions changed.

That distinction is familiar in software. We try to separate policy from implementation, data from processing, and configuration from code. We want to change what a system does without rebuilding every component that carries it out. The loom is an early, physical illustration of that idea.

The people who needed intricate textiles were not merely passive recipients of technology. Their work presented a problem that helped make a new form of control useful.

## Patterns existed before the pattern catalogues

Architect Christopher Alexander explored a related idea in *A Pattern Language: Towns, Buildings, Construction* (1977), written with Sara Ishikawa, Murray Silverstein, and their colleagues.

The book describes recurring problems in places where people live and work, then presents patterns that can be adapted to solve them. Its central contribution is not a collection of universal blueprints. It is a way to record design knowledge so people can reuse it while still responding to their own context.

That idea later influenced software design. Developers adopted patterns as a way to describe recurring problems in software and the structures that can address them. The [Christopher Alexander archive's entry for *A Pattern Language*](https://christopher-alexander-ces-archive.org/book/a-pattern-language/) documents the book and its wider influence.

But the underlying practice is older than the terminology. Craftspeople pass down ways to join materials, arrange a workspace, store tools, or sequence a difficult task because they have seen those arrangements work. Over time, repeated experience becomes shared knowledge. A pattern is a way to make that knowledge easier to recognize and adapt.

There is a useful distinction here between copying a solution and understanding a pattern. Copying says, “Build it this way.” A pattern says, “When this problem and these forces appear, this arrangement may help; examine the context before using it.”

Good software architecture needs the second kind of thinking. A design that works for one team or traffic profile may fail under different constraints. Patterns are useful because they carry reasoning, not because they eliminate the need to reason.

## The knowledge that never made it into the manual

Experienced people often know things they cannot easily explain as a list of rules.

A farmer may notice subtle changes in a crop. A carpenter may recognize that a joint will not hold before a measurement proves it. A mechanic may hear a change in a machine and know where to investigate. Such judgment grows from repeated contact with a real environment, including the consequences of being wrong.

Philosopher Michael Polanyi is associated with the idea of tacit knowledge: what people know is not always fully captured by what they can state explicitly.

This matters when software is built for a real occupation. The people doing the work often understand the exceptions, informal checks, workarounds, and unwritten priorities that never appear in a formal process document. If developers model only the visible steps, they may automate the wrong version of the work.

Imagine building an irrigation system from a soil-moisture sensor and a simple threshold. The implementation might be correct: when the reading falls below a value, open a valve. But the actual decision may depend on crop type, growth stage, recent rainfall, sensor placement, water availability, and whether the reading can be trusted. A technically correct program can still encode an incomplete understanding of the problem.

The solution is not to romanticize intuition or treat every experienced habit as infallible. Human judgment can also be inconsistent, and a rule that works in one context may not generalize. The task is to learn from practitioners, identify which parts of their knowledge can be made explicit, and preserve a way to handle conditions the model does not cover.

This is why good requirements work begins with observation and conversation, not a technology choice.

## From domain expert to software builder

Today, people outside conventional software engineering roles increasingly use spreadsheets, scripts, low-code tools, and automation platforms to build solutions for their own work. The term *citizen development* describes part of this movement.

A shopkeeper might connect an order form to an inventory sheet. A teacher might automate a routine grading task. A farmer might combine sensor readings with irrigation rules. These are not all production-grade software systems, and they do not all need to become one. But each begins with a person who understands a workflow well enough to improve it.

The domain expert has an advantage that an outsider may lack: knowledge of what actually happens. A software engineer has a different advantage: methods for expressing behavior in data structures, interfaces, tests, and programs that can be maintained and operated. The best outcome often comes from combining the two.

This also changes how I think software should be taught. Programming syntax is important, but it is not the beginning of every useful idea. Before writing code, a learner can map a process, identify the information it needs, mark its decision points, describe its exceptions, and ask what should happen when a step fails.

Those exercises are already a form of computational thinking. Code gives the model an executable form; it does not create the original insight from nothing.

## What changes when the system becomes software?

Software introduces properties that make the old craft analogy incomplete—and more interesting.

A physical object is constrained by its material and location. Software can be copied almost perfectly, distributed across networks, and changed after deployment. But its behavior may depend on remote services, concurrent requests, permissions, stale data, and components that fail independently. A small change can have effects far beyond the file in which it was made.

The architect's task is therefore not simply to draw a diagram. It is to make decisions about boundaries, responsibilities, dependencies, failure handling, and change. The work must account for both the people who use the system and the technical environment in which it runs.

Yet the fundamental questions remain recognizably human:

- What problem are we solving, and for whom?
- What are the parts, and how do they depend on one another?
- Which assumptions are we making?
- What happens when conditions change or a component fails?
- How will we know whether the result works?
- What knowledge should be preserved so the next person can improve it?

A carpenter asks versions of these questions with timber and tools. A farmer asks them with soil, water, weather, and time. A software architect asks them about services, data, interfaces, and operations. The materials differ; the discipline of thinking in relationships connects the work.

## The ancestors are not a metaphor

I would not claim that every craftsperson is a software architect in disguise, or that software engineering is merely traditional craftsmanship with computers added. That would ignore the distinctive mathematics, abstractions, and failure modes of computing.

But it would be equally mistaken to imagine that systems design began when the first software architecture diagram was drawn.

Long before computers, people were designing repeatable processes, coordinating interdependent parts, recording information, teaching patterns, and improving systems through observation. The Jacquard loom offers a documented bridge between industrial craft and programmable machinery. Alexander's work shows how knowledge drawn from human environments became influential in software design. Contemporary end-user development shows that people still build digital tools from their understanding of everyday work.

The history of software architecture is therefore not only a history of machines and programming languages. It is also a history of human beings learning to make complicated work understandable, repeatable, and improvable.

Perhaps we should teach system design by starting there: with the door that must fit, the crop that must survive, the stock that must be counted, or the workshop that must run without chaos.

Then we can ask what the person already understands, what the process leaves implicit, and what a computer could help execute.

The first lesson in software architecture may not be a diagram of servers. It may be learning to see the architecture already present in the world.
