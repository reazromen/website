---
title: "Cargo Cult vs Understanding: Why “99% AI-Written Code” Is the Wrong Metric"
url: /posts/cargo-cult-vs-understanding-99-percent-ai-written-code.html
date: '2026-10-19'
read_time: 7
excerpt: "AI makes software easier to assemble, but code-generation percentages reveal little about engineering competence. The real test is whether a system is understood and verified."
draft: false
featured: true
language: en
eyebrow: "Engineering & AI · perspective"
---

Software has never been easier to assemble. With a few prompts, an AI assistant can generate a Docker Compose configuration, scaffold an application, configure a monitoring stack, write firmware, or produce an entire backend. Tasks that once required hours of documentation and experimentation can sometimes be completed in minutes.

But before celebrating this acceleration, we should ask a more fundamental question:

**Are we becoming better at engineering, or simply better at making things appear to work?**

A running application is not necessarily a well-engineered application. A green dashboard does not guarantee a healthy system. A successful deployment does not prove that the person who deployed it understands what is running.

This is the difference between reproducing the appearance of success and understanding what makes success possible.

## What Is Cargo Cult?

The term *cargo cult* became widely known through accounts of certain Melanesian communities, particularly during and after the Second World War. Some communities observed military personnel establishing airstrips and communication infrastructure associated with the arrival of supplies. In some cases, people subsequently recreated elements of that infrastructure in the hope of obtaining similar results.

Popular retellings often oversimplify this history, but the metaphor remains useful: reproducing visible conditions associated with an outcome without understanding the mechanisms that produce it.

Software engineering has its own version.

A developer copies a configuration because it worked in a tutorial. They adopt an architecture because a popular project uses it. They install a collection of tools because an experienced engineer recommended them. When the expected output appears, they conclude that the system works.

Imitation itself is not the problem. Developers have always learned from examples, documentation, and existing implementations.

**The problem begins when copying a solution replaces understanding why it works.**

## A Running System Is Not Proof of Understanding

Consider a developer deploying an application with Docker. They copy a configuration, execute `docker compose up -d`, and see that the containers are running.

What have they actually established?

Only that Docker started the containers. The application might still be malfunctioning, the database might be unreachable, persistent data might disappear after a restart, or the service might be exposed insecurely.

The same distinction applies throughout infrastructure engineering. A database can respond to queries while its storage is nearly exhausted. An API can return successful HTTP responses while background jobs silently fail.

The visible result is evidence, but its meaning is limited.

A successful backup upload does not prove that every required file was transferred or that the data can be restored. A monitoring dashboard does not prove that the correct metrics are being collected. An object detection system displaying a bounding box does not establish that its false-negative rate is acceptable.

The engineering task is to connect the indicator to the property that actually matters.

- **Backups:** Restore the data and verify its integrity.
- **Security:** Inspect network exposure, authentication, permissions, and logs.
- **Monitoring:** Trace metrics from their source through collection and storage to the dashboard.
- **Computer vision:** Evaluate the model against representative footage, including difficult cases.

These are not merely additional checks. They establish whether the system satisfies its intended requirements.

**A system should be judged by verified behavior, not by the success message it produces.**

## The AI Coding Debate Is Asking the Wrong Question

Consider the statement: “99% of my code was written by AI.”

Some interpret it as evidence of extraordinary productivity. Others see it as evidence that the developer lacks technical competence. Neither conclusion follows from the percentage alone.

A developer who writes every line manually can still produce insecure, unmaintainable software. Another might generate most of an implementation with AI while carefully reviewing the architecture, testing failure conditions, and validating the resulting behavior.

The relevant distinction is not who typed the code, but how the implementation was developed and verified.

This is where the analogy between AI and a compiler requires precision.

A compiler transforms a program according to the rules and semantics of a programming language. A generative AI system can produce the source code itself, interpreting requirements and proposing an implementation. A compiler can faithfully compile a program containing a serious logical error; AI can generate a plausible implementation that fails to satisfy the requirements in the first place.

They operate at different levels. They are not equivalent tools.

Nevertheless, neither compilation nor code generation proves that the resulting system is fit for production. That requires testing against actual requirements, examining failure modes, and evaluating the consequences of design decisions.

AI can accelerate implementation, but it cannot make its own output trustworthy simply by generating it.

**The percentage of AI-generated code measures authorship, not engineering competence.**

## AI Makes Cargo Cult Easier to Scale

Before AI-assisted development became widespread, assembling a complicated system often required considerable effort. Developers had to find instructions, resolve dependencies, adapt configurations, and work through errors.

That friction was frustrating, but it could also expose gaps in their knowledge.

AI removes much of that friction. A developer can request an entire infrastructure stack, receive hundreds of lines of configuration, and launch the resulting services without understanding every component.

This is a genuine productivity improvement. It also creates a potential gap between the ability to construct a system and the ability to maintain it.

A developer might assemble a sophisticated stack without knowing how to diagnose a storage failure, identify a networking fault, assess a security weakness, or explain instability under load.

When something breaks, they ask AI for a fix. The generated configuration replaces the previous one. Perhaps the problem disappears; perhaps another emerges. The cycle continues without a reliable explanation of what caused the failure.

The issue is not that the developer relies on AI. Experienced engineers routinely use documentation, libraries, diagnostic tools, and external expertise.

The issue is that **complexity can accumulate faster than the ability to control it**.

AI makes it easier to produce systems whose operational complexity exceeds their creators' ability to reason about them.

## Failure Reveals the Difference

Imagine two developers managing the same production service. Both used AI to build it, deployed it successfully, and verified that the application responds to requests.

Then the server's disk begins to fill up.

The first developer asks AI for a fix. The proposed solution removes files, changes container settings, and restarts services. They apply the changes without establishing what is consuming storage or which files are safe to remove.

The second developer examines filesystem utilization, identifies the directories consuming space, inspects container storage, and checks which services depend on the affected volumes. They distinguish temporary files from persistent application data before choosing a remedy.

Both developers can use AI. The difference lies in the process.

One applies a plausible intervention. The other gathers evidence, forms a diagnosis, and evaluates the risks before acting.

In production, that distinction can determine whether a problem is resolved safely or turns into data loss, an outage, or a security incident.

A fix is not adequately justified merely because the immediate symptom disappears. The engineer must also consider what changed, what else might have been affected, and how recovery can be verified.

This is why troubleshooting is a core engineering skill, not simply the ability to find a command that works.

## Understanding Does Not Mean Knowing Everything

Genuine understanding does not require memorizing every command, API, protocol detail, or dependency implementation. Modern systems are too complex for that standard. Engineers routinely use libraries without reading every line of their source code, deploy databases without understanding every internal algorithm, and work in programming languages they have not mastered.

What matters is understanding the system at the level necessary to make responsible decisions.

Can you identify its critical dependencies? Recognize its assumptions? Determine what evidence is missing? Know when to consult documentation or seek specialist help?

An engineer who says, “I do not know why this component is failing yet, but here is what I have verified and how I will investigate the remaining possibilities,” is demonstrating a disciplined approach to uncertainty.

Confidence is not a substitute for evidence, and admitting a knowledge gap is not a failure of engineering.

**Understanding means knowing how to investigate what you do not know.**

There is a related trap: confusing technical vocabulary with practical competence. Someone can explain TCP, database transactions, container networking, or distributed systems in impressive detail and still fail to diagnose a real production problem.

Conceptual knowledge matters, but its value is demonstrated when it helps predict behavior, distinguish symptoms from causes, and guide decisions under actual constraints.

That is why building, observing, debugging, and testing systems matter as much as studying their underlying concepts.

## A Practical Standard for AI-Assisted Engineering

Rather than measuring engineering ability by how much code a person writes manually, evaluate the quality of their decisions and evidence.

Five questions provide a useful starting point:

1. **Can I explain the architecture?** Can I describe how the critical components interact and justify the major design choices?
2. **Can I identify failure modes?** What happens when storage runs out, a dependency becomes unavailable, credentials expire, or an input falls outside expected limits?
3. **Can I verify the requirements?** Can I demonstrate correct behavior through tests, logs, measurements, or restoration procedures rather than relying on a success message?
4. **Can I diagnose problems systematically?** Can I form and test hypotheses instead of repeatedly changing configurations until something appears to work?
5. **Can I assess the consequences of a change?** Do I understand its assumptions, risks, and potential impact on dependent services?

Nobody needs perfect answers to every question before starting a project. The point is to distinguish what has been demonstrated from what is merely assumed.

AI can help with every stage of this process. Ask it to explain its assumptions, propose failure scenarios, generate tests, compare alternative architectures, and suggest ways to verify its claims. Then validate important conclusions against authoritative documentation and observed behavior.

The goal is not to eliminate reliance on AI. It is to make that reliance informed and testable.

## Conclusion: Copying Is a Beginning, Not an Engineering Philosophy

There is nothing inherently wrong with copying an example, following a tutorial, adopting a framework, or asking AI to build something. These are legitimate ways to accelerate development.

The critical question is whether the resulting system becomes something you can explain, evaluate, and maintain—or remains a collection of components that happen to work under current conditions.

Cargo cult reproduces the visible form of success. Engineering investigates the mechanisms that make success possible.

That distinction applies regardless of who writes the code. Manual authorship does not guarantee competence, just as AI assistance does not imply incompetence. What matters is whether the implementation satisfies its requirements and whether the people responsible for it can evaluate its behavior and manage its risks.

So when someone says that AI wrote 99% of their code, the number itself tells us almost nothing.

Ask a better question:

**Can you explain the system you built, demonstrate that it works as intended, and make a responsible decision when it fails?**

If the answer is yes, AI may have made you dramatically more productive. If the answer is no, writing more code by hand will not necessarily solve the problem.

The ultimate measure of engineering is not how much code you produce or how quickly you produce it. It is whether you can turn an implementation into a reliable system—and take responsibility for the difference.

Are we becoming better at engineering, or simply better at making things appear to work?

**The answer depends less on which tools we use than on whether we can distinguish an output that looks correct from a system whose behavior we have actually verified.**
