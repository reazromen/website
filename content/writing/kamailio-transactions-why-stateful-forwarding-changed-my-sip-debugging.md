---
title: 'Kamailio Transactions: Why Stateful Forwarding Changed My SIP Debugging'
url: /posts/kamailio-transactions-why-stateful-forwarding-changed-my-sip-debugging.html
date: '2026-09-14'
read_time: 3
excerpt: Once I separated stateless forwarding from transaction-aware forwarding,
  retransmissions, replies and failure handling in Kamailio became much easier to
  reason about.
topic: telecom-voip
tags:
- kamailio
- sip
- transactions
- tm
draft: false
featured: false
language: en
eyebrow: 2021 SIP Infrastructure · intermediate
outputs:
- url: /posts/kamailio-transactions-why-stateful-forwarding-changed-my-sip-debugging.html
  template: cms/templates/posts/posts--kamailio-transactions-why-stateful-forwarding-changed-my-sip-debugging.tpl
  source: cms/templates/posts/posts--kamailio-transactions-why-stateful-forwarding-changed-my-sip-debugging.json
---

My first Kamailio configurations mostly looked like packet forwarding rules. A request arrived, I checked a few headers, selected a destination and relayed it. That model was enough for simple calls, but it became weak as soon as retransmissions, multiple replies and failure handling mattered. The missing concept was transaction state.

SIP runs over transports where retransmission behavior can be part of the protocol. With UDP, an INVITE may be retransmitted if no provisional or final response arrives in time. A proxy that treats every packet as unrelated traffic can make debugging confusing because the same logical request appears several times. Kamailio's transaction module gives the proxy enough state to associate those messages and manage downstream branches and replies coherently.

The practical change in my configuration was moving from a purely stateless relay toward `t_relay()` for requests that needed transaction handling. I started checking transaction behavior with `sngrep` and packet captures instead of only reading log lines. The same Call-ID and CSeq made it clear when several packets belonged to one SIP transaction rather than several independent calls.

State also matters when a destination fails. A transaction-aware proxy can react to timeout or negative responses and enter a failure route where another destination can be tried. That is much closer to how I wanted a SIP edge to behave than simply forwarding a packet and forgetting it. It also made the difference between transport failure and SIP rejection easier to see.

One useful lab had two downstream Asterisk instances. The first destination was deliberately stopped. Kamailio sent the request, waited according to transaction behavior, then the failure route selected the second destination. Watching the 408-style timeout behavior and the second branch in a trace made the control flow much clearer than the configuration syntax alone.

This was also a good reminder that SIP state exists at several levels. A transaction is not the same thing as a dialog. The INVITE transaction creates one piece of state; an established call has dialog identifiers and in-dialog requests such as BYE or re-INVITE later. Keeping those levels separate prevented me from using one mechanism to solve the wrong problem.

After this lab I stopped reading Kamailio configs as a list of `if` statements. I started reading them as a signaling state machine: classify the request, create or reuse transaction state, select branches, process replies, and decide what should happen on failure. That model held up much better as the routing logic became more complex.
