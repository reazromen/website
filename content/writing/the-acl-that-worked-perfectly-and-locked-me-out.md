---
title: The ACL That Worked Perfectly and Locked Me Out
url: /posts/the-acl-that-worked-perfectly-and-locked-me-out.html
date: '2024-04-18'
read_time: 3
excerpt: 'My first memorable ACL mistake was technically correct: it blocked exactly
  what I told it to block, including the management traffic I still needed.'
topic: networking
tags:
- ccna
- acl
- security
- troubleshooting
draft: false
featured: false
language: en
eyebrow: 2019 Routing, Linux & First VoIP · intermediate
outputs:
- url: /posts/the-acl-that-worked-perfectly-and-locked-me-out.html
  template: cms/templates/posts/posts--the-acl-that-worked-perfectly-and-locked-me-out.tpl
  source: cms/templates/posts/posts--the-acl-that-worked-perfectly-and-locked-me-out.json
---

Access lists were one of the first places where a configuration could be logically correct and still be a bad operational change. In a lab I wanted to restrict traffic entering a routed interface. I wrote the entries, applied the ACL, and immediately lost the management path I was using. The router had not malfunctioned. It had enforced my policy exactly as written.

That incident made the implicit deny much more memorable than any study note. A classic ACL is processed top to bottom, and traffic that does not match an earlier permit or deny eventually reaches the implicit deny at the end. If I add only the rule I am thinking about and forget the rest of the legitimate traffic, the result can be much broader than intended.

Direction matters just as much. An ACL applied inbound evaluates packets as they enter the interface. Outbound evaluates them after the routing decision as they leave. I found it useful to draw one packet with a source, destination and arrow, then mark the interface where the ACL would see it. Without that step I could write a correct rule and apply it in a place where it never matched the traffic I wanted to control.

Standard and extended ACLs also encouraged different placement decisions. A standard ACL mostly matches source IPv4 addresses, so placing it too close to the source can affect more destinations than intended. An extended ACL can match source, destination, protocol and ports, which allows a more precise policy closer to where the traffic originates. The exam rules are useful, but the packet path explains why those rules exist.

My safer lab workflow became: write the intended policy in plain language, identify the flows that must continue working, build the ACL, inspect it before attachment, then apply it from a console or from a session I could afford to lose. After the change I tested both the traffic that should be blocked and the traffic that should still pass. Testing only the deny case is not enough.

Counters are useful too. `show access-lists` can show which entries are matching traffic. If a rule has zero hits while the supposedly controlled flow is active, either the ACL is in the wrong place, the match is wrong, or the traffic is taking a different path. A deny counter increasing rapidly may be evidence that the policy is working, or evidence that the policy is blocking something important.

The funny part was that the router taught the lesson better than the documentation did. There was no mystery to solve after I regained access and read the list carefully. The device had followed a deterministic sequence of rules. From then on I treated ACL changes less like syntax exercises and more like firewall changes: define the allowed behavior first, consider the management path, and assume the implicit deny will eventually catch anything I forgot.
