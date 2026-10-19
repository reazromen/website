---
title: "Anthropic's Workflow Does Not Make Engineering Practices Obsolete"
url: /posts/anthropic-workflow-does-not-make-engineering-practices-obsolete.html
date: '2026-10-19'
read_time: 5
excerpt: "A company's AI-heavy engineering workflow may be effective at exceptional scale. That does not prove Git, clean code, or design patterns are obsolete across the industry."
draft: false
featured: true
language: en
eyebrow: "Engineering Culture · perspective"
---

A company can change how it builds software without proving that everyone else should work the same way.

That distinction often disappears in discussions about AI-assisted engineering. A report about an unusually large engineering organization becomes a prediction about the entire industry. A workflow that works under exceptional conditions is presented as the inevitable future of software development. Established practices are then declared obsolete before the evidence supports such a broad conclusion.

This is not how engineering progress should be evaluated.

## A Company's Operating Model Is Not an Industry-Wide Verdict

Anthropic's engineering approach is a meaningful response to the scale and characteristics of its internal environment. Its reported use of AI agents and high-volume development workflows deserves attention because it can reveal new ways to coordinate work, produce changes, and manage software at scale.

But a specific company's operating model is not proof that Git, clean code, or design patterns are becoming obsolete across the industry.

Consider two figures sometimes cited in this debate: around 30,000 code changes per day and a 65% figure associated with Anthropic's product engineering team. Before drawing conclusions from either number, we need to understand the original source, what counts as a change, which teams are included, and how the percentage was calculated.

A figure scoped to one product engineering team cannot automatically be generalized to every pull request or software organization. Nor does a high volume of AI-assisted changes, by itself, tell us whether those changes improved maintainability, reliability, security, or long-term development costs.

The numbers may be evidence of a particular workflow's scale. They are not, without further evidence, a universal verdict on software engineering practice.

## Different Practices Solve Different Problems

The claim that AI-heavy development makes traditional practices obsolete also bundles together tools and principles that serve different purposes.

Git provides version control, change history, collaboration mechanisms, and a way to inspect or reverse changes. Clean code principles help developers manage complexity and make intent easier to understand. Design patterns describe recurring approaches to software design and the trade-offs they involve.

AI changes how quickly implementations can be generated. It does not automatically remove the need to track changes, understand code, manage dependencies, or choose appropriate abstractions.

In fact, generating code more quickly can make some of these concerns more important. When the volume of proposed changes increases, teams still need to understand what changed, why it changed, what behavior might be affected, and how to determine whether the change is safe.

That does not mean every conventional practice must remain untouched. Some workflows may need to change. Some patterns may be unnecessary in a given system. Some teams may find that AI agents change the best way to organize reviews or divide work.

The right question is not whether a practice is old or new. It is whether the practice solves a real problem in the context where it is being used.

## Scale Changes the Trade-Offs

An organization coordinating thousands of changes and agent-driven tasks faces different constraints from a small team building a focused application. Its tooling, review process, integration strategy, and definition of developer responsibility may need to reflect that scale.

A workflow that is efficient for one organization may be excessive for another. Conversely, a process that works for a small team may become a bottleneck when many contributors and automated agents work concurrently.

Neither context is automatically the universal model.

Engineering practices should be evaluated against the problems they solve, the constraints under which they operate, and the evidence that they remain effective. If a team has found a better method, the useful response is to understand the conditions that make it better and test whether those conditions apply elsewhere.

That is more informative than declaring an entire category of practice obsolete.

## Why This Matters for New Developers

Broad claims about obsolete practices can mislead people who are still learning software engineering.

A new developer may hear that AI writes most code at a leading company and conclude that version control, readable code, architectural reasoning, or design fundamentals no longer matter. That is a poor inference.

Learning these fundamentals is not the same as committing to one rigid workflow forever. Understanding Git does not require using every branching convention. Learning design patterns does not mean applying patterns everywhere. Writing clean code does not mean optimizing for aesthetic preferences at the expense of actual requirements.

Fundamentals give developers the tools to evaluate new workflows instead of merely copying them.

Without that foundation, a person can reproduce an AI-heavy process without understanding its assumptions or knowing when it is failing. That is the same cargo-cult problem that appears when someone copies a Docker configuration or deploys an infrastructure stack without verifying its behavior.

The surface changes. The underlying mistake remains the same.

## Emerging Practice Is Not Yet Universal Truth

Technological change often begins with experiments that work well in particular environments. Some eventually become widely useful. Others remain specialized, require substantial trade-offs, or are replaced by better approaches.

AI-assisted engineering deserves the same disciplined evaluation as any other change.

Ask what the workflow improves. Measure the quality of the resulting software, not just the volume of generated code. Examine review effectiveness, defect rates, security outcomes, maintenance burden, and the time required to diagnose failures. Identify which responsibilities have shifted from writing code to specifying, evaluating, integrating, and operating it.

These questions allow us to recognize genuine progress without overstating what the evidence shows.

**A successful company's experience is a reason to investigate a practice, not a reason to declare every alternative obsolete.**

Engineering practices evolve because the problems, constraints, and available tools evolve. The goal is not to defend every traditional convention. It is to understand what each practice is for, what has changed, and whether a better approach has actually been demonstrated.

Context matters. Evidence matters. And there is a meaningful difference between an emerging practice and an industry-wide shift.

Otherwise, we risk turning technological progress into another cargo cult: copying the visible behavior of a successful organization without understanding why it works for them—or whether it will work for us.
