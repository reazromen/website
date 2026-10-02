---
title: Why a SIP 401 Response Usually Did Not Mean the Call Failed
url: /posts/why-a-sip-401-response-usually-did-not-mean-the-call-failed.html
date: '2026-09-14'
read_time: 2
excerpt: Digest authentication made much more sense once I saw 401 as part of a challenge-response
  exchange rather than a generic failure code.
topic: telecom-voip
tags:
- sip
- authentication
- digest
- asterisk
draft: false
featured: false
language: en
eyebrow: 2020 VoIP Foundations · intermediate
outputs:
- url: /posts/why-a-sip-401-response-usually-did-not-mean-the-call-failed.html
  template: cms/templates/posts/posts--why-a-sip-401-response-usually-did-not-mean-the-call-failed.tpl
  source: cms/templates/posts/posts--why-a-sip-401-response-usually-did-not-mean-the-call-failed.json
---

Seeing `401 Unauthorized` in a SIP trace initially looked like a clear failure. In HTTP troubleshooting, a 401 often means the request did not have acceptable credentials, so I expected the same interpretation in SIP. In many SIP registration and call flows, however, the first 401 is part of the normal digest-authentication challenge. The server is asking the client to prove knowledge of a shared secret without sending that password directly in the request.

A typical REGISTER starts without an Authorization header. The registrar responds with 401 and includes a `WWW-Authenticate` header containing values such as realm, nonce and algorithm. The client then sends another REGISTER with an Authorization header calculated from the username, realm, password-derived value, request method, request URI and server nonce. If the calculation is accepted, the server returns success. The important trace is therefore not one response code but the complete challenge-response sequence.

This became a useful debugging pattern. If the first REGISTER receives 401 and the second succeeds, authentication is working as designed. If the client never sends a second request, it may not have credentials configured or may not understand the challenge. If the second request carries an Authorization header but receives another challenge or final rejection, I compare username, realm and credential configuration rather than changing network settings.

The nonce also matters because digest authentication is designed to avoid simply replaying a static credential value forever. Depending on the implementation, the server can expire or change a nonce and force a fresh calculation. This means two Authorization headers for similar requests do not necessarily contain the same response value, even though the user password has not changed. That behavior is easier to accept once the digest is understood as proof derived for a particular challenge.

The broader lesson was about protocol interpretation. A response code should be read in the state machine around it. A SIP 401 can be expected, while a sequence of repeated challenges can indicate a real problem. Looking at one red-colored line in Wireshark is rarely enough. The conversation before and after the line determines whether the protocol is progressing normally.
