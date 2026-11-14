---
title: 'When Telecom Networks Trusted the Other Side: The SS7 Security Problem'
url: /posts/when-telecom-networks-trusted-the-other-side-ss7.html
date: '2026-11-14'
read_time: 9
excerpt: SS7 was built for a world of closed, cooperative telecom operators. As networks expanded and interconnection became a global business, an old assumption became a modern security problem.
topic: telecommunications-security
tags:
- ss7
- telecom
- network-security
- signaling
- trust-model
- infrastructure
draft: false
featured: false
language: en
eyebrow: Perspective · telecommunications and security
---

There is a particular kind of engineering mistake that does not look like a mistake when it is made. It looks like a reasonable assumption, perhaps even an elegant simplification. A system is designed for a small and familiar environment, its participants are known to one another, and the cost of verifying every interaction appears greater than the risk of trusting the people on the other side. Years later, the system has grown beyond that environment. The participants have multiplied, the boundaries have moved, and the original assumption is still quietly holding the architecture together.

Telecommunications has a remarkable example of this problem.

The Signalling System No. 7, better known as SS7, helped make the global telephone network work as one interconnected system. It was designed in an era when access to telecom signalling infrastructure was limited, operators had established relationships, and interconnection happened inside a comparatively controlled environment. The architecture therefore relied heavily on the expectation that a network admitted into the signalling ecosystem was a legitimate participant.

That expectation was not unreasonable in its original setting. The problem was allowing it to survive unchanged after the setting itself had disappeared.

## A network built for a smaller world

To understand the security problem, it helps to remember what SS7 was built to do. A telephone call is not established simply because one phone dials another. Behind the familiar action is a series of signalling exchanges that help networks discover where a subscriber is currently registered, establish a route, coordinate call setup, manage services, and eventually release resources.

SS7 provided the signalling framework that allowed telephone exchanges and mobile-network elements to coordinate those operations. Its roots go back to the 1970s, with standardisation and deployment developing through the following decade. It became foundational to traditional circuit-switched telephony and later to important parts of mobile networks, particularly 2G and 3G.

The design environment matters. The signalling network was not originally imagined as an open service in which arbitrary machines on the public internet could send requests to a subscriber database. It was an operator interconnection system. Access was expected to be controlled by telecom organisations, and those organisations were expected to behave according to established technical and commercial rules.

In other words, the architecture inherited a trust relationship from the institutions operating it.

This is the distinction that is easy to miss when looking at SS7 vulnerabilities today. The protocol was not simply a collection of badly written commands. It belonged to an ecosystem in which network membership itself carried a substantial degree of trust. A message arriving through an accepted signalling relationship could be treated as coming from a participant that had a legitimate reason to ask for something.

But being a recognised participant and being authorised to perform a particular action are two different things.

## The difference between identity and permission

Imagine a large office building. Every employee has an access card that proves they belong to the organisation. The card gets them through the main entrance. It does not automatically mean they should be able to enter the finance department, open the server room, read every employee's personnel file, or change the building's access-control configuration.

A secure building distinguishes between identity and permission. It asks not only who you are, but also what you are allowed to do, where you are allowed to do it, and under what circumstances.

A trust-heavy network can blur that distinction. If a signalling partner is accepted as legitimate, the receiving network may place too much confidence in the requests arriving through that relationship. The important question is no longer merely whether the message came from a known network. It is whether that network is entitled to request this particular operation for this particular subscriber at this particular moment.

This is the core of the SS7 security problem: trust at the interconnection boundary can become broader than the authority that should actually be granted.

It is worth being precise here. SS7 is a protocol family and a network architecture, not one single switch that either has authentication or has none. Different layers, deployments, and later security controls matter. The criticism is not that every SS7 message in every network is always accepted without any checks. It is that the original inter-operator trust model did not provide the kind of strong, granular, end-to-end authentication and authorisation that a modern threat environment demands.

## When interconnection became an attack surface

The world around SS7 changed. Telecommunications markets opened, roaming became a global service, and operators began connecting with a much larger range of partners and signalling providers. The interconnection environment grew more complex. Access that had once been limited to a relatively small group of established operators could be obtained through a broader commercial ecosystem.

The network became more connected, but the assumptions embedded in its design did not evolve at the same speed.

This is where the difference between a closed system and a globally interconnected system becomes important. In a closed environment, an organisation may know every participant and have a practical way to enforce agreements with them. In a global environment, the number of relationships increases, the chain of intermediaries becomes harder to reason about, and the security of one operator begins to depend partly on the controls implemented by others.

An attacker does not necessarily need to compromise a subscriber's handset to exploit a signalling weakness. Depending on the vulnerability, access, and network configuration, an attacker with access to a signalling network may be able to abuse legitimate signalling operations. The attack surface is not limited to the phone. It can exist in the control plane that tells the phone network where a subscriber is, how a call should be routed, or how a service should behave.

This is one reason SS7 attacks have attracted so much attention: they target the infrastructure that coordinates communication rather than relying only on compromising the endpoint.

## What can go wrong inside the signalling layer?

Mobile networks maintain subscriber state and location information so that calls and messages can reach people as they move between cells, cities, and countries. Signalling protocols carry the messages needed to maintain that state. If an unauthorised party can make a network process requests it should have rejected, the consequences can extend well beyond an ordinary protocol error.

Researchers and telecom security teams have documented classes of SS7 abuse that can expose subscriber information, reveal approximate location, interfere with call or SMS routing, and support fraud. The exact impact depends on the operator's network design, filtering, roaming relationships, and the attacker's level of access.

Location exposure is particularly revealing. A mobile network needs to know which serving network or area is currently associated with a subscriber. That information is operationally necessary. But a query that is legitimate in one context can become a privacy violation when issued by a party with no valid reason to know the answer.

Call and SMS interception or redirection are more serious examples. Signalling operations that exist to support mobility and service continuity can, when abused or insufficiently validated, be manipulated in ways that affect where communications are delivered. This does not mean that anyone with an ordinary internet connection can simply intercept any phone call. Access to the relevant signalling environment, the specific network conditions, and the effectiveness of operator-side controls all matter.

The lesson is not that the telephone network is universally exposed. It is that a control plane with excessive trust can turn legitimate operational capabilities into an attack surface.

## The legacy problem did not disappear with 4G

One might reasonably ask why a protocol associated with older mobile generations still matters in an era of LTE and 5G. The answer is that telecommunications networks do not replace themselves in a single clean migration.

Different generations coexist. Operators preserve older systems for coverage, roaming, device compatibility, and services that cannot be retired immediately. Interworking between generations is part of the architecture, not an accidental exception. As a result, a subscriber using a newer device or a newer radio technology may still depend on signalling relationships that connect to older network systems.

Diameter became an important signalling protocol in LTE-era mobile cores, while SIP is central to session control in IP Multimedia Subsystem environments, including voice services such as VoLTE. These newer protocols and architectures introduce their own security mechanisms and operational models, but changing the protocol does not automatically remove the underlying trust problem.

A system can modernise its transport and still inherit assumptions from an older generation. It can move signalling over IP while retaining interconnection relationships that need stronger validation. It can introduce a new protocol while leaving gateways, roaming arrangements, and legacy interfaces as bridges between different trust domains.

The risk is therefore not simply that an old protocol remains in use. It is that old and new systems must cooperate, and the boundaries between them become places where security policy can be inconsistent.

This is a familiar pattern in infrastructure engineering. A legacy component rarely exists alone. It survives because other systems depend on it, and those dependencies can preserve its influence long after the original design environment has changed.

## Trust is not the same as security

There is a broader architectural lesson here. Trust is useful. Distributed systems could not function without relationships in which one component accepts information or services from another. The problem begins when trust becomes implicit, unlimited, or difficult to audit.

A network operator may have a commercial agreement with another operator. That agreement does not prove that every message arriving through the interconnection is legitimate. A signalling peer may be authenticated as a network entity, but that does not automatically authorise every operation it attempts. A request may be syntactically valid and still be contextually suspicious.

Security needs to distinguish several questions:

- Is the sending network or peer genuinely who it claims to be?
- Is that peer authorised to send this category of message?
- Is the requested operation valid for this subscriber and this network state?
- Does the request make sense given the history and context of previous events?
- Can the operator detect, contain, and investigate behaviour that violates those expectations?

These are not interchangeable checks. Authentication establishes identity. Authorisation establishes permitted actions. Validation checks whether a request is structurally and contextually acceptable. Monitoring looks for patterns that individual message checks may not reveal.

A secure architecture needs all of them at the boundaries where trust is exchanged.

## How operators can reduce the risk

The answer is not to disconnect every operator from every other operator. Global roaming and interconnection are essential to the way telecommunications works. The goal is to make trust explicit, limited, observable, and continuously evaluated.

Signalling firewalls and security gateways can inspect traffic at interconnection points, reject messages that should not originate from a particular peer, and apply rules based on message type, destination, and context. Operators can maintain allow-lists for legitimate signalling sources, restrict which operations each partner may perform, and apply rate controls to unusual request patterns.

Monitoring matters just as much. A single message may look valid in isolation, while a sequence of messages reveals an abnormal pattern. Detection systems can compare signalling activity against expected behaviour, identify unusual query volumes, and correlate events across protocols. Information sharing among operators also helps because an attack observed in one network may indicate a threat to others.

Standards work has continued to address these issues. GSMA guidance covers SS7 interconnect security monitoring and firewall practices. ITU-T Recommendation Q.3062, for example, addresses signalling procedures and protocols for enabling interconnection between trusted network entities, including mechanisms intended to support authentication of signalling exchanges. More recent work, including ITU-T Q.3066, provides principles for detecting and mitigating signalling attacks across legacy and modern protocol environments.

None of these controls should be interpreted as a magic switch. A firewall that is poorly configured can create a false sense of security. An allow-list that is never reviewed can become an outdated permission system. Monitoring without an operational response process can produce alerts that nobody acts upon. Security is an ongoing property of the network and the organisations operating it, not a product that can be installed once and forgotten.

## The same lesson applies to SIP and modern infrastructure

The SS7 story is especially relevant to anyone designing communication systems today. SIP networks, VoIP platforms, cloud services, APIs, and distributed applications all depend on trust relationships between components. A server may accept traffic from a known IP address. A SIP proxy may have a configured trunk to another provider. An API gateway may recognise a service account. These are useful starting points, but none should become a blanket permission to perform every action.

A known SIP peer should not automatically be allowed to impersonate arbitrary identities, redirect every call, or generate unlimited traffic. A trusted service account should not have unrestricted access to every customer record. A network path that is private should not be treated as proof that the data travelling through it is harmless.

The practical design principle is simple: trust should be scoped to a purpose. Authenticate the peer, authorise the operation, validate the request, limit the possible impact, and preserve enough visibility to understand what happened.

This is also why security boundaries deserve as much architectural attention as the components inside them. A system may have well-protected servers and carefully written applications, yet remain vulnerable at the point where it accepts instructions from another system. The interface between two organisations can be more consequential than the internals of either organisation.

## An assumption can outlive the world that created it

SS7 was not designed by engineers who expected the modern threat landscape and simply forgot to add a firewall. It emerged from a different period in the history of telecommunications, when the network's participants, commercial relationships, and operational boundaries looked very different. Its trust model made sense within that context, even if it left security properties that became inadequate as the ecosystem expanded.

That distinction matters because engineering history is rarely a story of foolish decisions. More often, a design is optimised for the world its creators can see. Then the world changes. The system becomes essential, replacing it becomes expensive, and assumptions that were once convenient turn into structural liabilities.

The deeper lesson is that security cannot depend only on the character or reputation of the organisations connected to a network. It must be enforced by the architecture itself. A partner can be legitimate and still make a request it has no right to make. A message can be valid and still be malicious. A connection can be trusted for one purpose and dangerous for another.

The question every interconnected system must eventually answer is not simply, *Do we trust the other side?*

It is: *What exactly are we trusting it to do, how do we verify that it is allowed to do it, and what happens when that assumption is wrong?*

That is the question SS7 left behind for the rest of network engineering.

## Further reading

- [ENISA: Signalling Security in Telecom — SS7, Diameter and 5G](https://www.enisa.europa.eu/publications/signalling-security-in-telecom-ss7-diameter-5g)
- [ITU-T Recommendation Q.3062: Interconnection between trustable network entities](https://www.itu.int/ITU-T/recommendations/rec.aspx?rec=15042)
- [ITU-T Recommendation Q.3066: Principles for detection and mitigation of signalling attacks](https://www.itu.int/epublications/publication/itu-t-q-3066-2026-01-principles-for-detection-and-mitigation-of-signalling-attacks-in-telecommunication-networks)
- [GSMA: Securing SS7 in a modern threat landscape](https://www.gsma.com/solutions-and-impact/technologies/security/t-isac-blog/ss7-securing-a-legacy-protocol-in-a-modern-threat-landscape-and-how-information-sharing-can-help-to-mitigate/)
- [OECD: Enhancing the Security of Communication Infrastructure](https://www.oecd.org/en/publications/enhancing-the-security-of-communication-infrastructure_bb608fe5-en.html)
