---
title: 'My First OSPF Lab: Watching Routes Appear Instead of Typing Them'
url: /posts/first-ospf-lab-watching-routes-appear.html
date: '2026-09-14'
read_time: 3
excerpt: OSPF became useful when I compared it directly with the static routes I had
  been maintaining by hand and watched neighbors and learned routes change with the
  topology.
topic: networking
tags:
- ccna
- ospf
- routing
- dynamic-routing
draft: false
featured: false
language: en
eyebrow: 2019 Routing, Linux & First VoIP · intermediate
outputs:
- url: /posts/first-ospf-lab-watching-routes-appear.html
  template: cms/templates/posts/posts--first-ospf-lab-watching-routes-appear.tpl
  source: cms/templates/posts/posts--first-ospf-lab-watching-routes-appear.json
---

Static routing taught me what a routing table needs, but it also made the maintenance problem obvious. In a three-router lab I could type every route myself. Add more routers or change a transit network and the amount of manual state grows quickly. OSPF was the first routing protocol I studied where I could watch routers discover neighbors and calculate reachability instead of entering every remote prefix by hand.

I kept the first topology small: three routers connected in a line, with a /24 LAN behind each edge and point-to-point networks between the routers. I enabled OSPF on the relevant interfaces in area 0 and then checked neighbor state before looking at the routing table. That order mattered. If the routers do not become neighbors, there is no point wondering why the remote routes are missing.

`show ip ospf neighbor` gave me a direct view of adjacency. I started paying attention to router IDs, neighbor state and the interface where each neighbor was seen. Once the adjacency reached the expected full state, `show ip route ospf` or the OSPF-marked entries in the full routing table showed the remote networks. The routes were not magic additions; they were the result of exchanged link-state information and a shortest-path calculation.

The area concept took longer to appreciate because a tiny lab does not need multiple areas. Area 0 feels like another number to memorize until the network is large enough for hierarchy to matter. For the small exercise, I treated area 0 simply as the common link-state domain and focused on getting the interfaces, network statements and addressing right.

I deliberately broke the adjacency in a few ways. A mismatched area prevented normal neighbor formation. An interface with the wrong IP subnet meant the routers were not actually Layer 3 neighbors even if the cable was correct. Passive-interface configuration could stop OSPF hellos where I expected a peer. Those failures were more useful than a clean configuration because each one showed which assumptions OSPF makes before it can exchange topology information.

Then I shut one transit link in a topology that had an alternate path. The routing table changed without me editing remote routes. That was the point where dynamic routing stopped being an exam topic and started looking operationally useful. The routers already had a model of the topology and could recalculate when an interface state changed.

I still checked the data plane separately. An OSPF neighbor can be up and a route can exist while an access-list, wrong host gateway or return-path problem breaks the actual application traffic. Routing protocol health is evidence about the control plane, not proof that every end-to-end flow works. Keeping those checks separate became increasingly important as the labs got more complicated.
