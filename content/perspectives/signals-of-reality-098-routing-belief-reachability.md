---
title: Routing Is a Belief About Reachability
url: /posts/signals-of-reality-098-routing-belief-reachability.html
date: '2026-07-11'
read_time: 7
excerpt: A route table is a distributed system's current belief about where packets should go, assembled from configuration and protocol messages rather than direct knowledge of end-to-end delivery.
topic: networking
tags:
- routing
- networking
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Protocols Lie Carefully'
editorial_batch: signals-of-reality-200
---

A router has a route.

That does not mean the destination is reachable.

It means the router currently has a rule telling it what next hop to use for traffic matching a prefix.

That rule can be excellent evidence.

It is not the same thing as end-to-end truth.

Routing is a distributed belief about reachability.

## A route is learned, not seen

Some routes are configured statically.

Others are learned through routing protocols.

A router receives advertisements, evaluates policy and metrics, and installs selected paths.

The route table is therefore constructed from messages.

No router observes the entire internet directly.

It knows what neighbors and configuration allow it to know.

This is why control-plane convergence matters.

When topology changes, beliefs need time to update.

## A valid route can lead to a dead path

Suppose the next-hop router remains reachable but a downstream link has failed.

The local route can remain installed until the routing protocol detects the failure and reconverges.

During that interval, packets follow a path that no longer reaches the destination.

The route exists.

Reachability does not.

This gap between control-plane state and data-plane behavior is one of the core failure modes of networking.

## Policy can override shortest paths

Routing is not merely geometry.

Networks apply policy.

An operator may prefer one provider.

A BGP policy may reject a route.

A firewall may allow only certain traffic.

A VPN may install a more specific route.

The selected path reflects administrative intent as much as physical connectivity.

The question "why did the packet go there?" is often answered by policy, not distance.

## Different routers can believe different things

During convergence, one router may know a link failed while another still advertises the old path.

Transient loops and blackholes can appear because distributed observers update at different times.

There is no contradiction.

There are multiple local routing states.

Eventually the protocol may converge on a shared topology.

Until then, the network contains several versions of present reachability.

## Forwarding proves more than the table

A route table is a prediction.

A packet capture is evidence of forwarding.

A traceroute is evidence about some sequence of responses.

An application-level probe is evidence that a higher-layer transaction completed.

Each step tests a stronger end-to-end claim.

This is why network debugging escalates from:

route exists,

to neighbor reachable,

to packet forwarded,

to remote endpoint responding,

to application succeeding.

The layers narrow uncertainty.

## Metrics can hide the reason

A routing protocol may assign costs.

Lower cost wins.

That sounds objective until we inspect how the cost is produced.

Bandwidth.

Delay.

Hop count.

Policy.

Local preference.

Administrative distance.

The metric is a representation of what the network considers desirable.

Change the metric and the "best" route changes without topology changing.

## The map is useful because it is not the territory

A route table is an extraordinary compression.

Millions of possible packet paths are reduced to prefix and next-hop decisions that can be executed at high speed.

Networking would be impossible without that abstraction.

The danger is treating the abstraction as proof.

When someone says, "There is a route, so the network is fine," the right response is:

a route proves the control plane currently believes in a next step.

Now send a packet.

Routing is a belief about reachability.

Forwarding is where the belief meets the wire.
