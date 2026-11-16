---
title: "Everyone Is Talking About AI. What Are the Builders Actually Building?"
draft: false
date: '2026-11-17'
language: en
read_time: 11
excerpt: >-
  AI has become the loudest conversation in technology, but beneath the hype a
  quieter shift is taking place: enthusiasts are turning models into tools,
  agents, products and new ways of working. The history of personal computing
  and the web helps explain what is changing—and what remains uncertain.
eyebrow: "Perspectives · Technology and the Culture of Building"
tags: ["artificial-intelligence", "technology", "ai-economics", "computer-science", "open-models"]
---

There is a strange feeling in technology at the moment. Open a developer forum, watch a conference talk, scroll through a professional network, or listen to a podcast, and sooner or later the conversation arrives at artificial intelligence. Someone is discussing a new model, someone else is demonstrating an agent that can operate a computer, another person is building an application without writing much code, and a company is announcing that its next product will be AI-native. Even people who have spent years working in entirely different areas of computing now find themselves explaining what they think AI will change.

I notice the same thing in my own conversations. I am also talking about AI, perhaps more often than I expected. That raises a question worth examining before we add another prediction to the growing collection: what are the people who are most excited about this technology actually trying to do with it? Are they simply fascinated by a new interface, or are they beginning to build a different kind of computing environment?

To answer that, it helps to look beyond product announcements and listen to the people experimenting with the technology. Developers, independent builders, open-source contributors, researchers and technical enthusiasts are not all describing the same future. Some want to make software creation accessible to more people. Some are trying to delegate entire workflows to agents. Others are running models on their own machines, connecting them to private data, or questioning whether the current economics can last. Their experiments reveal more about this moment than the volume of AI marketing does.

## The conversation is changing from using AI to building with it

The first wave of public attention around generative AI was largely conversational. People discovered that they could ask a model a question, request a summary, translate a paragraph, generate an image or get help with a piece of code. The interface was remarkable because it made a complicated machine-learning system feel accessible through ordinary language.

That interaction still matters, but the developer community is moving beyond it. The 2026 Stack Overflow Developer Survey, which gathered 30,903 responses from technologists across 169 countries, provides a useful snapshot of that change. In the survey's AI-use data, 83 per cent of 17,464 respondents said they used at least one AI tool in their work. Coding assistants or coding agents were reported by 65.9 per cent, general-purpose chat tools by 62.5 per cent, and AI agents or automated workflows by 26.2 per cent. These categories overlap, so they should not be added together as if they represented separate groups. They do, however, show that AI is becoming part of the developer's working environment rather than remaining a separate destination for occasional questions.

The distinction is important. Asking a chatbot to explain a function is one kind of interaction. Giving a coding agent access to a repository, a terminal, a test suite and a defined task is another. In the second case, the model is not merely producing an answer. It is participating in a process that includes inspecting files, changing code, executing commands, observing errors and attempting corrections.

The model is only one component of that process. The surrounding tools, permissions, project context, memory, execution environment and verification steps determine what the system can safely accomplish. This is why discussions about agents increasingly involve architecture and workflow design, not just prompt writing.

The survey also shows that adoption does not mean unconditional trust. Forty-eight per cent of respondents in the trust question said they trusted AI output when they could easily verify it, while only 6.6 per cent said they trusted it for many tasks including important work decisions. Enthusiasm and caution are therefore developing together. Developers are finding useful ways to work with AI while remaining aware that a convincing answer is not the same as a verified result.

Sources: [Stack Overflow Developer Survey 2026](https://survey.stackoverflow.co/2026/) and its [AI data](https://survey.stackoverflow.co/2026/ai/data).

## The new builder is not necessarily a traditional programmer

One of the most visible ideas in the current community is that the distance between an idea and a working prototype is becoming shorter. A person who understands a problem but has limited programming experience can now describe an interface, ask an AI tool to generate an implementation, run it, report what failed and continue iterating. This is often described as vibe coding, although the phrase can hide a wide range of practices—from a quick disposable experiment to a serious application with tests, version control and a deployment process.

The interesting change is not that programming knowledge has suddenly become unnecessary. It is that some of the work required to express an idea as software can now be delegated. A builder can spend more time describing requirements, reviewing behaviour and deciding what should happen, while a model handles parts of the implementation.

That creates opportunities for people who were previously blocked by the cost of hiring a developer or learning an entire programming stack before testing an idea. It also creates a new responsibility. If the person building an application cannot inspect what the generated code does, understand its dependencies or test its failure conditions, the lower cost of creation may simply move the cost into maintenance and risk.

The 2026 developer survey offers a useful correction to the idea that AI has made conventional engineering irrelevant. Respondents reported using AI for implementation, debugging, tests, documentation and code review, but the importance of context remained clear. Project goals and requirements were identified as important context by 85.2 per cent of respondents, while code, repositories and technical documentation were identified by 73.3 per cent. An agent needs more than an instruction to build something. It needs to understand the system into which the change must fit.

This is a shift in the location of expertise, not necessarily the disappearance of expertise. Knowing how to write every line may become less central for some tasks, but knowing what should be built, how it should behave, what can go wrong and how to prove that it works remains essential.

## Coding agents are becoming part of the development process

The change is visible in the tools developers are choosing. In Stack Overflow's 2026 survey, Claude Code and GitHub Copilot were among the most widely reported coding assistants or agents, followed by tools such as OpenAI Codex and Cursor. The significance is not the ranking of individual products. It is that developers are experimenting with systems that can work across a project rather than only completing a line or suggesting a small block of code.

GitHub's 2026 Octoverse report describes a similar transition through activity on its own platform. GitHub reported 17.9 billion pushes during the preceding twelve months. It also reported that, by September, developers were starting more than 40 per cent of pull requests with an agent, compared with 17 per cent in March. These are platform-specific measurements, not proof that every agent-generated change is better or that productivity has increased by the same amount. They do show that agent-assisted work has moved quickly from experimentation into ordinary development activity for a substantial part of the platform's users.

An important detail is what happens after an agent produces code. The work does not end when the model says it has finished. The result still needs to be reviewed, tested and connected to the intended requirements. GitHub's report notes increased activity around AI-assisted code review and security tooling as developers adapt their review processes. That is a revealing part of the story: as the ability to generate code expands, the ability to evaluate code becomes more important.

A useful way to think about an agent is therefore not as an autonomous employee that can be trusted with any task, but as a system that can operate within a defined boundary. Give it a clear objective, the minimum necessary permissions, access to relevant context and a way to verify its work. The more consequential the action, the stronger the review and approval requirements should be.

Source: [GitHub Octoverse 2026](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/).

## Open models and local AI are about control as much as cost

Not every enthusiast wants to use the largest model through a hosted service. A substantial part of the technical community is interested in running models locally, experimenting with open-weight systems and building private AI infrastructure.

There are several reasons for this. Local inference can reduce dependence on a particular provider, keep some data inside an organisation's own environment, make experimentation possible without sending every request to an external API, and provide more control over model selection and deployment. Open-weight models also allow developers to inspect and adapt the available model artefacts within the terms of their licences.

But local AI is not automatically cheaper, private or better. Hardware has a cost. Memory capacity, inference speed, electricity, maintenance and model quality all matter. An open-weight release is not necessarily fully open-source in every sense, and having model weights does not reveal all the data and decisions involved in training. A local deployment can also be insecure if its network exposure, authentication and data handling are poorly designed.

The deeper motivation is architectural independence. Enthusiasts want to understand where computation happens, what information leaves their systems, which model is being used and whether they can replace one component without rebuilding everything. These are familiar engineering concerns, but AI has made them visible to a much larger audience.

The same questions appear in my own interest in infrastructure and connected devices. When an AI system is connected to a server, a phone, a database or an embedded device, it stops being an isolated chatbot. It becomes one component in a larger system whose behaviour depends on networks, permissions, hardware and operational design.

## The web had its enthusiasts too

It is tempting to think that the current excitement is unprecedented because AI dominates so much of today's online conversation. But earlier technologies also produced communities of enthusiasts who were convinced that they were witnessing a fundamental change.

In 1983, TIME named the personal computer its "Machine of the Year". The cover story did not describe computers as equipment reserved for large institutions. It explored how personal computers were entering homes, workplaces and unexpected areas of everyday life. The examples included people using computers to write letters, support medical work, customise insurance calculations and control stage effects. The question being asked was not merely how fast a machine could calculate. It was what ordinary people might do once computing became personally accessible.

The parallel with AI is striking. The personal computer moved computation closer to the individual. Generative AI is moving certain forms of computational assistance closer to ordinary language. In both cases, enthusiasts saw a general-purpose capability becoming available to people who had not previously been able to use it directly.

The World Wide Web followed a related path, although it developed through a different technical and social process. Tim Berners-Lee proposed the Web at CERN in 1989. In 1993, the National Center for Supercomputing Applications released Mosaic, a browser whose more approachable graphical interface helped the Web spread beyond its early research and technical communities. CERN records more than 500 known web servers by late 1993, and around 10,000 servers and 10 million users by the end of 1994. The first International World Wide Web Conference, held at CERN in May 1994, was attended by 380 users and developers and was described as the "Woodstock of the Web".

That description is useful because it reminds us that the Web was not initially experienced as an inevitable global utility. It was also a small, enthusiastic community discovering what a new medium could become. People built browsers, servers, directories, personal pages and early online services. They were not only discussing the technology; they were expanding it through use.

Sources: [TIME's 1983 Machine of the Year cover](https://content.time.com/time/specials/2007/article/0,28804,1704183_1704257_1704498,00.html) and [CERN's history of the Web](https://home.cern/science/computing/the-birth-of-the-web/short-history-web/).

## The hype can be real even when the business expectations are wrong

The comparison with the Web also brings us to the dot-com bubble. During the late 1990s, investors became convinced that the internet would transform commerce and that companies positioned around it could grow at extraordinary speed. Many businesses were funded before they had demonstrated durable revenue or a viable business model. The NASDAQ Composite peaked in March 2000 and then fell sharply. Many internet companies failed, but the underlying network continued to expand and became more deeply integrated into everyday life.

The lesson is not that AI will repeat the dot-com crash on the same schedule. Historical analogies are useful for identifying patterns, not for predicting dates. The internet and AI have different technical foundations, cost structures, infrastructure requirements and routes to adoption.

What the comparison does show is that a transformative technology and an overheated investment market can exist at the same time. Some products may be useful while the companies selling them are not sustainable. Some infrastructure may be overbuilt while the long-term demand for the underlying capability continues to grow. Some claims about productivity may be exaggerated even as real workflows are changing.

The IMF's review of asset-price bubbles describes the internet bubble as beginning around 1995 and deflating after its March 2000 peak, while research on the period shows how speculative expectations and business-model uncertainty shaped investment. That history is a reason to examine the economics of AI carefully, not a reason to dismiss the technology.

For a related discussion of the economics of model efficiency and the AI investment cycle, see [The AI Bubble: When Intelligence Becomes Cheap, What Happens to Its Value?](/posts/the-ai-bubble-when-intelligence-becomes-cheap.html).

Further reading: [IMF, Asset Price Bubbles: A Selective Survey](https://www.imf.org/external/pubs/ft/wp/2013/wp1345.pdf).

## What enthusiasts are really trying to change

If we look across the projects and conversations, a few ambitions appear repeatedly. Some builders want to make software creation accessible to people who are not professional programmers. Others want personal agents that can coordinate tasks across applications. Open-source contributors want models and tools that can be inspected, adapted and run outside a single provider's platform. Researchers are exploring whether AI can accelerate scientific work. Engineers are connecting models to databases, devices, networks and existing business systems.

These ambitions are related, but they are not identical. A chatbot that answers a question, a coding agent that edits a repository, a local model that searches private documents and a robot that acts in the physical world are different systems with different requirements. Grouping all of them under the label "AI" can make the current moment sound more unified than it really is.

There is also a gap between demonstrations and dependable systems. A short video can show an agent completing a task once. A production system must handle incomplete instructions, changing data, unavailable services, permission boundaries, unexpected inputs and failures that may not be obvious. The distance between a successful demonstration and a dependable service is where much of the engineering work remains.

This is why I find the builders' conversations more interesting than the endless stream of announcements. Their experiments reveal both the new possibilities and the difficult details that marketing tends to leave outside the frame.

## We may be looking at a new layer of computing

The personal computer did not eliminate the mainframe, and the Web did not eliminate the computer. Each introduced a new layer through which people could access and organise existing capabilities. AI may follow a similar pattern, but its role could be unusually broad because it can interpret instructions, generate content, write code and interact with tools.

Perhaps the most useful question is not whether AI will replace the applications we use today. It is whether the interface to computing will gradually change from operating individual applications to describing outcomes and supervising systems that coordinate the applications on our behalf.

That future is not guaranteed. Models can make mistakes, agents can exceed their useful boundaries, and many tasks still require human judgment. The economics of inference, the concentration of infrastructure, privacy, energy use and the distribution of benefits will all influence how the technology develops.

But the current enthusiasm is not simply a crowd talking about a fashionable subject. There are people building new interfaces, testing new workflows, publishing open models, creating products and discovering what becomes possible when language can act as a practical interface to software.

The personal computer generation asked what ordinary people could do if they had a computer of their own. The early Web generation asked what could happen if anyone could publish and connect information. The builders of this generation are asking what they could create if the machine could help translate an intention into a sequence of actions.

We should take that question seriously without accepting every promise made in its name. The most important evidence will not be how often we hear the word AI, or how many tools appear every week. It will be the systems people build, the problems those systems solve, the failures they learn to prevent, and the capabilities that remain useful after the excitement moves on.

Perhaps the defining feature of this moment is not that everyone is talking about AI. It is that an increasing number of people are trying to build with it. The difference between those two activities may tell us more about the future than the hype itself.

## Sources and further reading

- [Stack Overflow Developer Survey 2026](https://survey.stackoverflow.co/2026/)
- [Stack Overflow Developer Survey 2026 — AI data](https://survey.stackoverflow.co/2026/ai/data)
- [GitHub Octoverse 2026: Developers build with agents](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/)
- [CERN: A short history of the Web](https://home.cern/science/computing/the-birth-of-the-web/short-history-web/)
- [TIME: 1983 — Machine of the Year](https://content.time.com/time/specials/2007/article/0,28804,1704183_1704257_1704498,00.html)
- [IMF: Asset Price Bubbles — A Selective Survey](https://www.imf.org/external/pubs/ft/wp/2013/wp1345.pdf)

Related perspectives: [What Is a Computer, Really?](/posts/what-is-a-computer-in-the-age-of-ai.html) · [The AI Bubble](/posts/the-ai-bubble-when-intelligence-becomes-cheap.html)
