---
title: 'The Call Worked Until BYE: Debugging Dialog Routing in OpenSIPS and Drachtio'
url: /posts/the-call-worked-until-bye-debugging-dialog-routing-opensips-drachtio.html
date: '2024-12-19'
read_time: 29
excerpt: A call can establish, carry clean audio, and still fail at BYE when the dialog
  route set, backend affinity, or media cleanup path is wrong.
topic: telecom-voip
tags:
- opensips
- drachtio
- sip
- record-route
- dialog-routing
- freeswitch
- rtpengine
- '481'
draft: false
featured: false
language: en
eyebrow: OpenSIPS + Drachtio Production SIP · advanced
outputs:
- url: /posts/the-call-worked-until-bye-debugging-dialog-routing-opensips-drachtio.html
  template: cms/templates/posts/posts--the-call-worked-until-bye-debugging-dialog-routing-opensips-drachtio.tpl
  source: cms/templates/posts/posts--the-call-worked-until-bye-debugging-dialog-routing-opensips-drachtio.json
---

A SIP call that fails during setup is usually easier to understand than a SIP call that works perfectly for several minutes and then fails when someone hangs up.

That distinction became very real while I was building the SIP edge on my own infrastructure. The initial `INVITE` would arrive. Authentication worked. A backend was selected. FreeSWITCH answered. SDP was negotiated. RTP was flowing. Both sides could talk. From a user's point of view, the difficult part of the call had already succeeded.

Then one side sent `BYE`.

Instead of following the established signalling path cleanly back through the proxies that had created the call, the request could take a different route, hit the wrong component, or arrive somewhere that no longer recognized the dialog. Depending on where the routing state was lost, the result might look like a `481 Call/Transaction Does Not Exist`, a proxy-side “not here” response, or simply a call leg that did not clean up the way I expected.

That kind of failure exposes one of the most important concepts in SIP engineering:

**Routing the first request is not the same problem as routing the rest of the dialog.**

An `INVITE` can succeed because the proxy knows how to find a destination at that moment. A later `BYE`, re-INVITE, UPDATE, INFO, REFER, or other in-dialog request succeeds only if the participants retained enough routing state to reconstruct the signalling path established when the dialog was created.

That is where `Record-Route`, `Route`, dialog identifiers, transaction state, Contact targets, proxy topology and application state all start interacting.

This article documents how I learned to debug that boundary in a real OpenSIPS + Drachtio + FreeSWITCH architecture. The interesting part is not the syntax of `record_route()` or `loose_route()`. The interesting part is understanding the state they represent and knowing exactly what evidence to inspect when an initial call works but a later in-dialog request does not.

## The Architecture I Was Actually Debugging

My VoIP stack had several components performing different jobs. At one edge I had OpenSIPS acting as the infrastructure SIP proxy: authentication, registration, location handling, transaction routing, dialog tracking, dispatcher-based FreeSWITCH selection and RTPengine control.

```
SIP endpoint
     |
     v
 OpenSIPS
     |
     +---- registration / authentication
     +---- local registered destination
     +---- FreeSWITCH worker pool
     +---- RTPengine for media anchoring
```

In another path I had Drachtio acting as a programmable SIP layer, with a Node.js application deciding which FreeSWITCH workers were healthy and where an incoming request should go.

```
SIP request
    |
    v
drachtio-server
    |
    v
Node.js / drachtio-srf
    |
    +---- worker health
    +---- heartbeat freshness
    +---- destination selection
    +---- proxy transaction state
    |
    +----> FreeSWITCH 1
    +----> FreeSWITCH 2
```

These components overlap in some capabilities, but they do not have identical programming models. OpenSIPS gives me explicit SIP routing primitives inside the proxy configuration language. Drachtio gives me a programmable SIP application environment where JavaScript drives proxying and application logic while drachtio-server handles the protocol machinery.

The common problem remains the same: if either component needs to stay in the signalling path after the initial request, it must participate in establishing the dialog route set correctly.

RFC 3261 defines this directly. A proxy that wants future requests in the dialog to pass through it inserts a `Record-Route` value into the dialog-forming request. The endpoints then use those Record-Route values to construct the route set used by later requests such as `BYE`.

That sounds simple enough. The debugging difficulty begins because there are multiple kinds of state involved, and “the call exists” means something different to different components.

## Transaction State Is Not Dialog State

One of the most useful mental corrections I made while debugging SIP was to stop using the word “call” when I really meant several different protocol objects.

A SIP transaction is one request and its associated responses. A dialog is a longer-lived relationship between two user agents. The initial INVITE transaction helps establish the dialog, but the transaction and the dialog do not have the same lifetime.

A dialog retains state such as the Call-ID, local and remote tags, sequence information, the remote target and the route set. That state continues after the original INVITE transaction has completed.
Consider a normal successful call:

```
UAC                    Proxy                    UAS
 |                       |                       |
 |------ INVITE -------->|------ INVITE -------->|
 |<----- 100 ------------|<----- 100 ------------|
 |<----- 180 ------------|<----- 180 ------------|
 |<----- 200 OK ---------|<----- 200 OK ---------|
 |------ ACK ----------->|------ ACK ----------->|
 |======= media ================================>|
 |<====== media =================================|
 |------ BYE ----------->|------ BYE ----------->|
 |<----- 200 OK ---------|<----- 200 OK ---------|
```

The INVITE transaction is not sitting around waiting for the eventual BYE. The BYE is a new SIP request. It belongs to the existing dialog, but it has its own transaction.

That immediately explains why debugging a failed BYE by looking only at the original INVITE transaction is incomplete. The question is no longer “which backend did the INVITE transaction choose?” The better question is “what dialog route set was created, and where does the endpoint believe the next in-dialog request should go?”

This difference matters enormously in a load-balanced architecture. I can successfully distribute a new INVITE to FreeSWITCH worker A. If a later BYE is routed independently as though it were another new request, there is nothing preventing it from reaching worker B. Worker B may have no knowledge of that dialog. A `481` is then not mysterious; I have delivered an in-dialog request to a component for which that dialog does not exist.

## Record-Route Keeps the Proxy in the Conversation

A stateless mental model of SIP goes something like `client -> proxy -> server`. The client asks the proxy to find the server, and perhaps the proxy is no longer needed after that.

That is sometimes exactly what I want. It is not what I want when the proxy must remain involved in subsequent requests because it owns topology, accounting, media cleanup, routing policy, security policy, dialog visibility or downstream selection.

That is what `Record-Route` is for.

Suppose the initial INVITE passes through two proxies:

```
UAC -> Proxy A -> Proxy B -> UAS
```

If both proxies Record-Route themselves, the dialog-forming request contains values conceptually like:

```
Record-Route: <sip:proxy-b.example;lr>
Record-Route: <sip:proxy-a.example;lr>
```

The endpoints then build route sets from that information. A later request carries `Route` headers that keep the expected proxies in the signalling path. The Request-URI still identifies the remote target; the Route set identifies the signalling hops that must be traversed first.
Without that mechanism, a UA may send the BYE directly toward the remote Contact. If my edge controls RTPengine state, accounting or application state, bypassing it is not merely cosmetically different. It can leave resources behind or break the signalling model.

## OpenSIPS Makes the Dialog Path Explicit

The relevant part of my OpenSIPS routing logic is intentionally simple:

```
if (has_totag()) {
    if (is_method("ACK") && t_check_trans()) {
        t_relay();
        exit;
    }

    if (!loose_route()) {
        send_reply(404, "Not here");
        exit;
    }

    if (is_method("BYE")) {
        rtpengine_delete();
    }

    route(RELAY);
    exit;
}
```

There is a lot of SIP behavior hiding inside those few lines. `has_totag()` tells me that I am no longer looking at a normal initial request. Once the dialog exists, the routing problem changes.

For a new INVITE I may need to authenticate the caller, look up a registration, choose a FreeSWITCH destination, create dialog state and negotiate media. For an in-dialog BYE, I should not repeat that decision tree. I should follow the route set established earlier.

That is what `loose_route()` is doing. It analyses the `Route` headers and advances the request along the dialog route set. When that fails, I immediately ask a more useful sequence of questions:

```
Did the BYE contain Route headers?
If yes, do they contain the proxy I expected?
If not, did I Record-Route the original dialog-forming request?
If Record-Route was present, did the endpoint preserve and use the route set?
If the request reached the proxy, does the proxy recognize its own route URI?
If the request left the proxy, which next hop did loose routing resolve?
```

That is much more useful than a generic application log saying “BYE failed.”

## Why the Call Can Work Even When Dialog Routing Is Already Broken

This is what makes the problem deceptive. The media path can be fine. The call setup can be fine. The endpoints can speak for ten minutes. None of those facts proves that a future BYE will be routed correctly.

Imagine I forward the initial INVITE without inserting myself into the route set. The call establishment can still succeed. The remote endpoint returns a Contact. If the proxy is not part of the route set, the caller may later send the BYE directly to that Contact.

If that direct target happens to be reachable, the call may even terminate correctly and I might never notice my proxy left the dialog. If the Contact is private, container-local, NATed, rewritten incorrectly, or routed through a different infrastructure path, the BYE fails.

The configuration mistake happened during dialog establishment. The first visible failure may happen minutes later.

## Drachtio Expresses the Same Requirement Differently

On the Drachtio side, my application proxies SIP requests to a dynamically maintained set of FreeSWITCH workers. The core proxy call is conceptually:

```
await srf.proxyRequest(req, destinations, {
  recordRoute: true,
  followRedirects: true,
  provisionalTimeout: '1s'
});
```

The critical option here is `recordRoute: true`. Drachtio treats `recordRoute` as an alias for `remainInDialog`: insert Record-Route and remain on the signalling path for later dialog messages, including the terminating BYE.

That is exactly the behavior I want from a stateful signalling edge. Without it, the Node.js application could successfully proxy the initial INVITE to a FreeSWITCH worker and then disappear from the rest of the dialog.

The OpenSIPS and Drachtio APIs look different, but they are implementing the same SIP principle. OpenSIPS gives me `record_route()` during setup and `loose_route()` for later requests. Drachtio exposes the intent through the proxy API. Underneath, both designs are dealing with the dialog route set.

## Contact and Route Solve Different Problems

One of the easiest ways to misunderstand a failed BYE is to look at the Contact header and assume it tells the whole routing story. It does not.

Contact identifies the remote target for the dialog. Record-Route creates the route set. Those are related but different pieces of state.

Suppose a 200 OK contains:

```
Contact: <sip:[email protected]:5060>
Record-Route: <sip:edge.example.com;lr>
```

The remote target might be `sip:[email protected]:5060`, but the BYE should still traverse `sip:edge.example.com;lr` because that proxy is in the route set.

Conceptually:

```
BYE sip:[email protected]:5060 SIP/2.0
Route: <sip:edge.example.com;lr>
```

The Request-URI answers “who is the remote target?” The top Route header answers “which signalling hop do I send this through first?” Confusing those two is a reliable way to get lost while reading SIP captures.

## A Realistic Failure Pattern

The failure pattern I care about looks like this:

```
Phone
  |
  | INVITE
  v
OpenSIPS
  |
  v
Drachtio or FreeSWITCH edge
  |
  v
FreeSWITCH worker A
```

The dialog establishes successfully and worker A owns the call. Now imagine the route set is incomplete. Later the caller sends a BYE without the expected Route information. The request may reach FreeSWITCH worker B directly, or OpenSIPS may accidentally treat it like a new request and run fresh backend selection.

Worker B has no dialog matching the Call-ID and tags and returns `481 Call/Transaction Does Not Exist`.

That response is not evidence that FreeSWITCH is necessarily broken. It may be evidence that my routing layer delivered the request to the wrong owner of the dialog.

## What 481 Actually Tells Me

`481 Call/Transaction Does Not Exist` is a clue, not a root cause. It says the receiving SIP element cannot associate the request with the dialog or transaction state it expects.

Possible causes include the wrong backend, dialog state lost after restart, malformed or mismatched tags, incorrect Call-ID, broken route set, state expiry, a B2BUA leg mismatch, or logic that treated an in-dialog request as a new request.
The first question I ask is therefore: **which component generated the 481?**

If FreeSWITCH worker B generated it while worker A owns the call, I have a routing problem. If the original worker generated it after a restart, I may have a state-loss problem. If OpenSIPS rejected the request before it ever reached a worker because `loose_route()` could not resolve the route set, I have a different failure again.

The response code becomes useful only after I identify the responding component.

## My Debugging Order Starts with the Wire

When SIP components disagree about what happened, I trust the SIP messages before I trust summaries of those SIP messages. Application logs are valuable, but they contain interpretations. A packet capture contains the protocol exchange.

For this class of failure I want the complete dialog, ideally filtered by Call-ID. In `sngrep` I select the call and inspect the full message flow. In `tcpdump` or Wireshark I want SIP traffic from all relevant interfaces.

The first thing I check is not the BYE. I go back to the initial INVITE and record:

```
Call-ID
From tag
initial Request-URI
Via
Contact
Record-Route
```

Then I inspect the 200 OK for the To tag, Contact and Record-Route. Only after that do I inspect the BYE for its Request-URI, Route headers, Call-ID, From tag, To tag, CSeq and actual destination IP/port.

That sequence tells me whether the BYE was constructed from the dialog state I thought I created. If I start at the failure response, I am debugging the end of the story without reading how the state was created.

## The Three Values I Compare First

For a failed in-dialog request, three identity values are especially useful: Call-ID, From tag and To tag.

```
Call-ID: 8b91a4f0@example
From: <sip:1001@example>;tag=a17c
To: <sip:1002@example>;tag=b992
```

If a later BYE carries the same Call-ID and tags, it at least appears to reference the correct dialog. If one tag differs, I am looking at a different dialog identity. The proxy cannot repair that merely by forwarding the packet to the right IP address.

This is why I separate routing correctness from dialog-identity correctness. A packet can reach the correct machine and still be invalid for the dialog.

## Then I Check the Route Set

Once the dialog identifiers look correct, I inspect the Route headers. If I expected `Phone -> OpenSIPS -> Drachtio -> FreeSWITCH` and both OpenSIPS and Drachtio must remain in the path, the established route set should reflect that topology.

If the BYE suddenly has no Route headers, that is a major clue. If it has only one of the expected proxies, that is another. If a Route URI refers to an address reachable only from another network namespace, that may explain why the message disappears. If the proxy receives the request but does not recognize the Route URI as local, that is a different failure.

Containerized SIP infrastructure makes this especially easy to get wrong because the same process can have several valid-looking identities:

```
container IP
host LAN IP
public IP
DNS name
internal Docker DNS name
```

Only some of those are valid from the endpoint's perspective.

## Docker Makes SIP Addressing Bugs Easier to Create

Imagine Drachtio is listening inside a container at `172.18.x.x:5060` while the host publishes `192.168.x.x:5060`. If the Record-Route header advertises the container address to a LAN SIP phone, that phone may later attempt to send its BYE to `172.18.x.x`, which it cannot reach.

The initial INVITE may still have worked because it entered through the published host port. The failure appears only when the endpoint follows the route set in the opposite direction.

This is a classic example of why a working initial request proves less than it seems. The routing path during setup may have been imposed externally; the routing path during the established dialog is reconstructed from SIP state. Those paths have to agree.

## `loose_route()` Is a Useful Truth Test

For my in-dialog traffic I do not want to run the initial authentication and dispatcher logic again. I want to ask whether this request belongs to an established dialog and whether its Route set brings it through this proxy. If yes, follow that route.
That is why a failure in `loose_route()` is useful. It tells me the request did not contain the route information OpenSIPS expected to consume. That is far more specific than “BYE failed.”

## Why I Do Not Send an In-Dialog BYE Back Through Dispatcher Selection

My OpenSIPS dispatcher handles new backend selection. For an initial INVITE that is not destined for a locally registered endpoint, I can select a FreeSWITCH worker from the pool. The current configuration uses weighted round-robin and preserves additional destinations for serial failover.

That is appropriate before the dialog belongs to a specific backend. After the dialog has been established, redistributing sequential requests independently is dangerous.

Suppose the initial INVITE chose FS1. The BYE arrives later. If I run dispatcher selection again, the next weighted decision might be FS2. The architecture has now violated dialog affinity.

The correct mechanism is the existing dialog route. This distinction is more important than whichever load-balancing algorithm I use. A sophisticated dispatcher cannot compensate for treating dialog traffic as stateless traffic.

## Failure Routing Is Another Place State Can Be Lost

Backend failover is valid before a final dialog has been established. If FS1 times out or returns a server failure, OpenSIPS can mark it and try FS2. My current failure logic is intentionally selective because ordinary user-level outcomes should not be interpreted as worker failure.

A `486 Busy Here` can mean the user is busy. A `503 Service Unavailable` can mean the worker cannot serve the request. Failing over the first changes call semantics; failing over the second may be exactly what I want.

Once a 200 OK establishes the dialog, the question changes again. I am no longer choosing a backend for a new call. I am maintaining the routing relationship that already exists.

## ACK Is the Method That Forces Precision

ACK is one reason SIP routing discussions become confusing quickly. There is not one universal ACK behavior. ACK for a non-2xx final response is tied closely to the INVITE transaction, while ACK for a successful 2xx INVITE follows the dialog routing state.

That is why my OpenSIPS route handles transaction-associated ACK before normal loose routing:

```
if (is_method("ACK") && t_check_trans()) {
    t_relay();
    exit;
}
```

When debugging ACK I therefore ask first: ACK to what kind of response? Without that context, “ACK follows the transaction” and “ACK follows the route set” can both be misleading.

## CANCEL Is Not BYE

CANCEL and BYE can both stop something from the user's perspective, but they belong to different state machines. BYE terminates an established dialog. CANCEL attempts to cancel a pending request, normally the outstanding INVITE transaction.

That is why CANCEL belongs in transaction logic rather than dialog teardown logic.

## Media State Adds a Third Lifetime

The signalling dialog is not the only state I have to clean up. I also have RTPengine state.

When an initial INVITE contains SDP, OpenSIPS can call:

```
rtpengine_offer("replace-origin replace-session-connection symmetric")
```

and register an on-reply route. When the answer comes back with SDP, `rtpengine_answer()` updates the other half of the negotiation. RTPengine now owns media-session state associated with the call.

When the dialog ends, that state must be removed. That is why the BYE path contains `rtpengine_delete()`.

The interesting failure mode appears when the BYE bypasses OpenSIPS. The endpoints may terminate the call successfully while OpenSIPS never gets the opportunity to execute the media cleanup. Stale media state can then survive until timeout.

This is a good example of three lifetimes that overlap but are not identical:

```
INVITE transaction state -> short-lived
SIP dialog state         -> lifetime of call
RTPengine media state    -> lifetime of media session
```

The cleanup path has to respect all three.

## Multiple Stateful Proxies Make Route Sets More Important

If both OpenSIPS and Drachtio Record-Route, I also have to reason about ordering. Suppose the deliberate path is:

```
Phone -> OpenSIPS -> Drachtio -> FreeSWITCH
```

and both proxies must remain in the dialog. The Record-Route chain has to preserve that topology so later requests traverse those components in the proper direction.

This is not equivalent to independently asking “where is FreeSWITCH?” at every hop. The route set itself is the path.

That matters if either intermediary owns RTPengine cleanup, accounting, dialog counters, topology policy, security checks or application callbacks. Removing one intermediary from Record-Route may not be visible until a sequential request exercises the missing path.

## Record-Route Is Also a Security Boundary

Route headers influence where SIP requests go, so I do not treat `loose_route()` as a harmless forwarding convenience. A proxy that accepts arbitrary preloaded routes before applying the right authorization checks can create routing behavior it never intended.

The safer mental model is: first establish what class of request this is, then apply the correct authentication or dialog checks, then follow a valid route set. Protocol routing information is still input; syntactically valid SIP does not make it automatically trustworthy.

## Why Application Logs Were Not Enough

During this kind of debugging I can collect logs such as `proxying SIP request`, `transaction complete`, `BYE received`, or `dialog not found`. All of those are useful. None tells me the complete route-set story.

A particularly important difference is `Route` versus `Record-Route`. An application log may record neither, yet one missing header can explain the entire failure.

The application may log `target = FS2`, but that does not tell me whether FS2 came from dispatcher selection, Route processing, DNS resolution, Contact, or a manual rewrite. The packet does.

That is why my debugging hierarchy for SIP is roughly:

```
wire evidence
routing state
transaction/dialog state
application logs
higher-level dashboard interpretation
```

The logs are not untrusted. They are simply one layer further away from the protocol.

## Capture Point Matters

Even packet capture can mislead me if I capture at only one point. In a proxy chain I may need to compare the message entering and leaving the proxy.

For example, an incoming BYE may contain:

```
Route: <sip:opensips.example;lr>
Route: <sip:drachtio.example;lr>
```

After OpenSIPS consumes its own route entry, the outgoing BYE may contain only the Drachtio Route header. If I capture only downstream, I might incorrectly conclude OpenSIPS was never in the route set.

The correct question is whether OpenSIPS received the request with itself at the expected top of the route set, consumed that element correctly, and sent the resulting request toward the next hop.

## The Debugging Table I Use

When a call succeeds but BYE fails, I reduce the investigation to ten checks:

```
1. Did the initial INVITE contain the Record-Route values I expected?
2. Did the 200 OK preserve the appropriate Record-Route information?
3. What Contact became the remote target?
4. What route set did the endpoint build?
5. Does the BYE contain the expected Route headers?
6. Which IP/port received the BYE first?
7. Did that proxy recognize itself in the route set?
8. Which next hop did it select after route processing?
9. Does that next hop own the dialog?
10. Which component generated the failure response?
```

Those questions usually narrow the fault far faster than changing random SIP settings.

## When the Proxy Returns 404 but the Problem Is Still Dialog Routing

My OpenSIPS config deliberately returns a local failure if an in-dialog request cannot be routed with the expected route set:

```
if (!loose_route()) {
    send_reply(404, "Not here");
    exit;
}
```

That means not every broken dialog-routing case produces 481. Some produce 404 at the proxy.

This is useful because response codes reflect where the failure was detected. A 404 generated by the edge can mean “I received what looks like an in-dialog request, but its Route state does not tell me how to route it through this dialog.” A 481 generated by a FreeSWITCH backend can mean “the request reached me, but I do not know this dialog.”

Those can be different manifestations of the same upstream design error. If I look only at the response code, they appear unrelated. If I inspect the route set, they may have the same root cause.

## Proxy Restart Changes the Question

Another scenario is state loss. Record-Route routing can be encoded in SIP messages, so a stateless routing component may be able to continue forwarding after a restart. Other features may depend on process or database state.

OpenSIPS dialog tracking, accounting or topology handling can maintain additional state. Drachtio applications maintain worker health and application-level runtime state. FreeSWITCH maintains B2BUA call-leg state.

After a restart I therefore ask two questions separately:

```
Can this component still route the SIP request?
Can this component still perform the stateful operation the request expects?
```

Those are not identical. A proxy may still know where a BYE should go while a B2BUA that owned the dialog leg no longer knows the dialog itself.

## A B2BUA Changes the Model Again

FreeSWITCH is not just another stateless proxy. It commonly behaves as a back-to-back user agent, which means one apparent “call” may be two distinct SIP dialogs:

```
Phone A
   |
   | dialog A
   v
FreeSWITCH
   |
   | dialog B
   v
Phone B
```

Call-ID values, tags and route sets can differ across those legs. FreeSWITCH terminates one dialog and originates another. That is fundamentally different from OpenSIPS forwarding within a dialog topology.
This matters during 481 debugging. If I compare the wrong leg’s Call-ID or tags, I can convince myself the packet is malformed when it is actually valid for a different leg. I trace each leg separately and correlate them through the B2BUA rather than expecting identity fields to remain identical across that boundary.

## Why Drachtio Is Powerful Here—and Easy to Misuse

Drachtio is attractive because it lets me express SIP behavior in normal application code. My FreeSWITCH pool logic can reconcile configured workers, mark stale heartbeats unhealthy, rotate destination order and expose health metrics without encoding all of that logic in a proxy language.

That is useful, but application code also makes it easy to think in HTTP terms: request arrives, choose backend, forward request, done. SIP dialogs do not fit that model.

The first request creates state that changes how later requests must be handled. `recordRoute: true` is therefore not a cosmetic option when the application is expected to remain part of the signalling state machine.

## Sequential Requests Are Not New Load-Balancing Opportunities

A re-INVITE is not an excuse to load-balance an active call onto a different arbitrary worker. A BYE is not a fresh request that should go through generic backend selection. An UPDATE is not a chance to pick the least-loaded server.

These are sequential requests inside an existing dialog. Backend affinity was created when the dialog was established.

Scaling new calls and migrating active calls are different engineering problems. If I need real mid-call migration, I need architecture specifically designed for it. A general SIP dispatcher does not magically turn a stateful B2BUA session into a migratable object.

## Media Makes Mid-Dialog Migration Even Harder

Even if signalling state could be reconstructed, media may be anchored elsewhere. A single active call can involve dialog identity, a FreeSWITCH call leg, an RTPengine session, negotiated SDP addresses, codecs and application state.

Moving a later SIP request to FreeSWITCH B does not move the media state or B2BUA call leg that exists on FreeSWITCH A. This is why stateful communications infrastructure needs stronger affinity than a typical stateless REST service.

## Monitoring Needs to Understand the Dialog Lifecycle

A probe that proves UDP 5060 is reachable is weak. A process-health check is useful for supervision but says nothing about whether BYE routing works. Even an `INVITE -> 200 OK` synthetic test does not exercise the failure described here.

A more meaningful synthetic test should eventually verify the dialog lifecycle:

```
REGISTER
INVITE
provisional response
200 OK
ACK
media establishment where practical
BYE
200 OK to BYE
```

Only then have I tested call establishment and dialog teardown through the intended signalling path.

## What I Log Now

For SIP proxy troubleshooting I want enough structured information to correlate routing decisions without logging unnecessary secrets or entire payloads forever. Useful fields include method, Call-ID, source address, Request-URI, selected destination, final status, proxy failure reason, worker name, worker health state and the result of dialog-related routing.

On the Drachtio side I already maintain counters around proxy requests, successes, failures and “no healthy worker” outcomes. For the FreeSWITCH pool I care about configured workers, healthy workers, heartbeat age and online/offline transition reason.

For OpenSIPS I care about transaction classes, dialogs, registrations, dispatcher state and 5xx behavior. These metrics do not replace packet captures. They tell me where to look.

## Heartbeat Health and Dialog Routing Are Separate

My Drachtio application maintains a health model for FreeSWITCH workers. A node can be configured but not healthy. A stale heartbeat can mark it offline. Destination selection uses healthy nodes.

That answers one question: should a new call be sent to this worker?

It does not answer another: does this worker currently own an existing dialog?

Those are different questions. A worker might stop accepting new calls while still handling established calls. At larger scale I would want worker state closer to `healthy for existing dialogs`, `accepting new dialogs`, `draining`, `offline`, and `failed` rather than a single Boolean.

## What I Would Change at Larger Scale

The hserver design is intentionally small, which makes every path visible. At larger scale I would formalize several things further.

I would separate ingress-proxy responsibility from application signalling logic more aggressively. I would make dialog affinity and worker-draining semantics explicit. I would avoid process-local state where restart should not destroy routing knowledge. I would ensure advertised Record-Route identities are stable service identities rather than ephemeral container addresses.

I would test both directions of sequential requests. I would add full synthetic dialog-lifecycle tests rather than only REGISTER or OPTIONS probes. I would correlate signalling metrics with media quality and RTPengine state.

I would also treat routing configuration as an API contract. A change to Record-Route, Contact rewriting, advertised addresses, dispatcher behavior or dialog handling can affect protocol state carried by live endpoints. It deserves the seriousness of a schema migration.

## The Failure Changed How I Think About SIP Proxies

Before working through this class of problem, it was easy to imagine a SIP proxy mainly as a device that answers “where should I send this request?” That is only the first layer.

A production SIP edge also has to answer whether the request is new or part of an existing dialog, which state owns it, which proxies promised to remain in the route set, which backend owns the B2BUA leg, which media session belongs to it, what can fail over before dialog establishment, what cannot fail over after establishment, and which state survives restart.

Those questions are where OpenSIPS, Drachtio, FreeSWITCH and RTPengine stop looking like a pile of VoIP software and start looking like a distributed state machine.

## The Most Important Packet in the Capture Was Not the 481

The 481 was the visible symptom. The more valuable packet was usually earlier.

Sometimes it was the initial INVITE missing the Record-Route I expected. Sometimes it was the 200 OK advertising a target that made sense only inside a container network. Sometimes it was the BYE missing the Route set. Sometimes the route set was correct but my own routing logic sent the request to the wrong backend.

That changed my debugging habit. When a SIP call fails late, I go backward. I do not begin with “why did BYE fail?” I begin with “what state did we create when the dialog was established?”

## A Compact Failure Model

```
INITIAL INVITE
    |
    +-- authenticate?
    +-- choose destination?
    +-- Record-Route correctly?
    +-- create dialog?
    +-- anchor media?
    v
200 OK
    |
    +-- preserve Record-Route?
    +-- valid Contact?
    v
ACK
    |
    +-- transaction or dialog routing?
    v
ESTABLISHED CALL
    |
    +-- sequential requests follow route set?
    +-- same B2BUA worker?
    +-- media state still valid?
    v
BYE
    |
    +-- correct Call-ID/tags?
    +-- correct Route set?
    +-- correct next hop?
    +-- correct dialog owner?
    +-- RTPengine cleanup?
    v
200 OK
```

Every arrow is observable and every transition can fail. That is a much stronger debugging model than simply asking whether port 5060 is open.

## Final Takeaway

The most useful lesson I took from the BYE/481 debugging work was not a particular OpenSIPS function or Drachtio option. It was this: **SIP routing decisions create protocol state that future messages depend on.**

The initial INVITE can work even when that future state is already wrong. `record_route()` in OpenSIPS and `recordRoute: true` in Drachtio are declarations that the proxy intends to remain part of the dialog. `loose_route()` consumes the route state created earlier and applies it to sequential requests such as BYE and re-INVITE.

Once I started debugging the system in terms of transaction state, dialog state, route set, remote target, backend ownership and media state, the apparently random late-call failures became much less mysterious.

A call that works until BYE is not evidence that “SIP mostly works.” It is evidence that call establishment works.

Dialog routing is a separate engineering problem, and in a production SIP platform I need both to be correct.

## References

- RFC 3261, SIP: https://www.rfc-editor.org/rfc/rfc3261
- OpenSIPS Record-Route / loose routing documentation: https://docs.opensips.org/
- Drachtio API and dialog documentation: https://drachtio.org/docs/
