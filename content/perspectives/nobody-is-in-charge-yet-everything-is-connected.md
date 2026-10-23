---
title: "Nobody Is in Charge, Yet Everything Is Connected"
draft: false
date: '2026-10-24'
language: en
url: /posts/nobody-is-in-charge-yet-everything-is-connected.html
read_time: 8
excerpt: >-
  Complex systems rarely have a single controller. Order emerges from local decisions, shared rules, feedback loops and dependencies—and that is both their strength and their risk.
eyebrow: "Perspectives · Systems Thinking"
tags: ["systems-thinking", "complexity", "infrastructure", "networks", "feedback"]
---

# Nobody Is in Charge, Yet Everything Is Connected

Look at a city from above after dark. Roads form bright lines; neighbourhoods glow; trains and buses carry people through patterns that repeat every day. Somewhere, a hospital is receiving a patient, a server is processing a payment, a mobile network is handing a call from one cell tower to another, and a power station is adjusting its output to meet demand. No single person has designed every movement or knows what every part of the city is doing at this moment. Yet, most of the time, the whole arrangement works well enough that we barely notice it.

This is one of the strangest facts about modern life: **systems can behave as if they are coordinated without being controlled by one central mind.** The coordination comes from many smaller actions, shared rules, feedback, and relationships between parts. Systems thinking begins when we stop looking only at the individual components and start asking what happens between them.

## Order without a single organiser

A flock of birds can turn almost as one body. A traffic jam can appear even when there is no accident and no person has decided to stop the road. A market price can change because thousands of buyers and sellers respond to their own circumstances. The internet can route traffic across networks operated by different organisations, none of which controls the entire global system.

These are not identical phenomena, and it would be a mistake to call them all the same kind of self-organisation. But they share an important feature: large-scale patterns arise from local interactions. Each participant has limited information and follows some rules. The combined result can be orderly, unstable, useful, or destructive.

In complexity science, this is often discussed through the idea of *emergence*: properties of the whole that cannot be understood by examining each part in isolation. A single ant follows relatively simple behavioural cues. A colony can build, forage, defend, and reorganise without an ant issuing a complete master plan. The colony's behaviour is distributed across interactions, environmental signals, and accumulated feedback.

Human systems work differently because people can plan, communicate, and deliberately create institutions. Still, even carefully designed organisations develop informal networks, habits, bottlenecks, and unintended consequences that no chart of the hierarchy fully captures.

## Rules are not the same as a controller

A system does not need one controller to have structure. It may need common protocols, boundaries, incentives, and ways to resolve disagreement.

The internet offers a clear example. It is not a single network owned and operated by one global authority. It is a network of networks. Organisations manage their own infrastructure and exchange traffic under technical and commercial arrangements. Protocols make cooperation possible across systems that were built and are maintained separately. The Internet Society's explanation of how the technical community operates the internet describes this distributed coordination: many organisations and communities contribute to the system's functioning rather than one entity running every part ([Internet Society](https://www.internetsociety.org/blog/2025/07/how-the-technical-community-runs-the-internet/)).

The Border Gateway Protocol, or BGP, lets independently operated networks exchange reachability information. It does not create a perfect map of the internet, nor does it guarantee that every route is optimal or safe. It provides a shared mechanism through which networks can announce and select routes according to policy and available information ([RFC 4271](https://www.rfc-editor.org/rfc/rfc4271.html)).

That distinction matters. **A shared rulebook enables coordination; it does not guarantee a good outcome.** A protocol can be widely adopted and still have weaknesses. Organisations can follow their local incentives while collectively producing a fragile result. A system can be decentralised and still depend on a small number of critical providers, facilities, cables, or software packages.

Distributed does not automatically mean democratic, resilient, or fair. It means control and activity are spread across multiple actors. We still have to ask who holds influence, who bears the risks, and how failures travel.

## Connections create value—and dependence

A component becomes more useful when it can connect to other components. A phone is more useful when it can reach other phones. A payment service becomes more powerful when banks, merchants, identity systems, and settlement networks can work together. A hospital depends not only on clinicians and equipment, but also on electricity, water, communications, supplies, scheduling, and the systems that keep records available.

The value is in the relationships. But every relationship creates a possible dependency.

Imagine a simple chain: a customer uses an app, the app calls an API, the API checks an identity service, the service queries a database, and the transaction depends on a network and a power supply. Each component may be healthy in isolation. The experience still fails if one critical dependency is unavailable, slow, misconfigured, or unreachable.

This is why “the server is up” is not the same as “the service works.” A process can be running while DNS resolution is broken. A web server can respond while its database is overloaded. A telecom application can be healthy while a route, upstream provider, or signalling dependency is failing. The user experiences one service; the operator may be looking at dozens of separate components.

The same principle appears in social systems. A business may depend on a supplier that depends on a port, a transport company, a payment provider, and a stable energy supply. Those connections enable specialisation and scale, but they also allow a local disruption to spread far beyond its point of origin.

## Feedback is how systems adjust

A system with no feedback cannot reliably correct the difference between what is happening and what needs to happen. Feedback is information about the result of an action returning to influence later action.

A thermostat measures temperature and switches heating on or off. A network congestion-control algorithm responds to signals that indicate how data is moving. A city adjusts traffic lights based on observed flows. A team changes its process after monitoring shows that incidents are recurring.

Feedback can stabilise a system, but it can also amplify instability. If a response arrives too late, is too strong, or is based on misleading information, correction can overshoot. A driver who brakes suddenly can trigger a chain of braking behind them. A poorly designed automated controller can repeatedly overcorrect. In a market, fear-driven selling can change prices, which creates more fear and further selling.

The key questions are not simply whether a system has feedback, but how quickly information travels, whether it is trustworthy, and whether the response is proportional. A dashboard full of metrics is not useful if the measurements arrive too late or nobody has the authority and context to act on them. A policy is not adaptive if it ignores the effects it produces.

## Why local optimisation can damage the whole

People and organisations usually optimise what they can see and measure. A delivery team may be rewarded for completing more jobs. A software team may be measured on release speed. A hospital department may try to reduce its own waiting list. Each goal can be reasonable on its own.

Problems appear when local success shifts costs elsewhere. Faster releases can increase the burden on operations. A department can clear its queue by sending work into another department's queue. A delivery service can improve its own efficiency while making traffic and working conditions worse for others.

This is a classic systems-thinking trap: improving a part does not necessarily improve the whole. The system's structure determines where pressure moves. If performance measures reward only local outcomes, people may rationally make choices that produce collectively poor results.

The remedy is not to abolish measurement or local responsibility. It is to understand the wider flow: what enters the system, where work accumulates, which constraints limit performance, and who absorbs the side effects. Good measures make trade-offs visible rather than hiding them behind a single number.

## Failures reveal the architecture

When everything works, dependencies stay invisible. When something fails, the system's hidden structure becomes suddenly obvious.

A cloud outage can affect services that appear unrelated because they share an identity provider, a region, or a software dependency. A damaged undersea cable can force traffic onto alternate routes and increase latency. A power disruption can affect mobile sites, data centres, transport, and payment terminals at the same time. A time-synchronisation problem can complicate logs, authentication, ordering, and diagnosis across otherwise healthy machines.

These examples do not mean every failure will cascade. Well-designed systems use redundancy, isolation, fallback paths, rate limits, backups, and clear recovery procedures to contain damage. But redundancy only helps when the backup does not share the same failure mode. Two services in different containers are not truly independent if both rely on the same database, power feed, or network path.

Resilience therefore requires more than adding spare capacity. It requires mapping dependencies, identifying common points of failure, testing degraded modes, and learning from incidents. The goal is not to promise that nothing will break. The goal is to prevent one broken part from taking down everything connected to it.

## Seeing the system, not just the parts

Systems thinking is a practical discipline, not a mystical claim that everything affects everything equally. Some connections are weak; others are critical. Some delays matter; others do not. The work is to discover which relationships shape the outcome.

A useful starting set of questions is:

- **Boundary:** What system are we trying to understand, and what have we left outside it?
- **Dependencies:** Which components or organisations must work for the outcome to succeed?
- **Feedback:** What signals show whether the system is moving in the right direction?
- **Delays:** How long does it take for an action or failure to become visible?
- **Incentives:** What does each participant optimise, and who pays for the side effects?
- **Failure modes:** What happens when a component is slow, unavailable, incorrect, or compromised?
- **Recovery:** Can the system continue in a reduced mode, and can it return safely?

These questions are useful whether the system is a Linux service, a telecom network, a hospital, a supply chain, or a public institution. They shift attention from blaming the nearest visible component to understanding the conditions that made the outcome likely.

## Nobody is fully in charge. Responsibility still exists.

It is tempting to romanticise decentralisation, as if a system that organises itself must be wiser than one with a central authority. It is equally tempting to believe that appointing one person in charge will make complexity disappear. Neither view is sufficient.

Central coordination can establish standards, resolve conflicts, and mobilise resources. It can also become a bottleneck or a single point of failure. Distributed coordination can adapt locally and continue when one participant disappears. It can also spread misinformation, reproduce unfair incentives, and leave accountability fragmented.

The real question is not whether a complex system should have a centre. It is which decisions need central coordination, which should remain local, what information must be shared, and how responsibility is assigned when the result harms people.

A network can be decentralised in its operation while still needing clear ownership of safety, maintenance, and recovery. Nobody may control the whole system, but every participant can still be responsible for the part they operate—and for understanding the dependencies they create.

## The world is connected by relationships

Much of modern life feels effortless because countless independent systems cooperate through protocols, habits, contracts, infrastructure, and feedback. That cooperation is neither automatic nor guaranteed. It is continually maintained by people who update software, repair cables, operate networks, write standards, coordinate logistics, respond to incidents, and make decisions with incomplete information.

The deeper lesson is that the visible event is often only the final expression of a much larger structure. A dropped call may be a routing or power problem. A delayed service may be a queue hidden several layers away. A shortage may begin far from the shelf where it becomes visible. A local improvement may create a distant cost.

When we ask only, “Which part failed?”, we may repair the symptom and preserve the conditions that caused it. When we ask, “What relationships made this outcome possible?”, we begin to understand the system.

Nobody is in charge of everything. Yet everything is connected—not in the sense that every event has the same cause, but in the more useful sense that outcomes emerge from relationships. Understanding those relationships is how we build systems that are not merely connected, but dependable.
