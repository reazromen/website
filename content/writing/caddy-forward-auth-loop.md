---
title: Forward Auth Works, Then the Browser Gets Stuck in a Login Redirect Loop
url: /posts/caddy-forward-auth-loop.html
date: '2025-08-13'
read_time: 16
excerpt: Auth gateways need the original request context to decide and redirect correctly.
topic: caddy-reverse-proxy
tags:
- caddy
- forward_auth
- sso
- redirect-loop
draft: false
featured: false
language: en
eyebrow: 'Caddy User Problems: Authentication · intermediate'
outputs:
- url: /posts/caddy-forward-auth-loop.html
  template: cms/templates/posts/posts--caddy-forward-auth-loop.tpl
  source: cms/templates/posts/posts--caddy-forward-auth-loop.json
---

# Forward Auth Works, Then the Browser Gets Stuck in a Login Redirect Loop

**Question:** What problem are we actually solving?

**Answer:** Auth gateways need the original request context to decide and redirect correctly.

**Question:** What does the user see?

**Answer:** Login succeeds, but protected requests return to login again or never reach the application. The rest of this article keeps the same question-and-answer discipline so the diagnosis does not drift into unrelated Caddy features.

*Article format: Forward-auth troubleshooting Q&A.*

![Production Ops authentication boundary](../static/blog-media/caddy/ops-login.png "Production Ops authentication boundary")

*Production capture — Actual production Ops login boundary exposed by the Caddy ingress path.*

![Production gateway authentication redirect](../static/blog-media/caddy/gateway-auth.png "Production gateway authentication redirect")

*Production capture — Actual production gateway authentication view reached through the public Caddy path.*

## Walk one request end to end

I pick one concrete request and narrate it as if I were the packet. The browser resolves the public name, chooses an address and protocol, establishes transport, negotiates TLS if needed, and sends Host plus headers and a path. Caddy selects a server and route, evaluates matchers, may run authentication or rewrites, chooses an upstream, opens or reuses a connection, forwards a modified request, receives the upstream response, applies response handling, then sends the result back through any CDN or tunnel.

In this specific case the key discontinuity is: The auth gateway sees a different scheme, host, URI or cookie context than the browser. Missing forwarded context is a common cause. That is the point in the walk where the data stops meaning what the next component expects. Everything before it can be technically healthy and still contribute to a broken user experience.

Walking the request also exposes hidden state. DNS cache, connection reuse, TLS session state, auth cookies, CDN cache, health-check state and load-balancer memory can all make two apparently identical requests take different paths. When a bug is intermittent, I include that state in the walk instead of treating the request as a stateless curl command.

## Diagnostic ladder

I move down the ladder in order instead of changing several layers at once:

1. inspect auth decision logs
2. confirm the browser sends the session cookie
3. compare external scheme/host with forwarded values
4. prove a 2xx auth decision reaches the app

Each check has one interpretation. If the first failing step is name resolution, I do not change TLS. If TCP connect works but TLS identity fails, I do not rewrite application routes. If the upstream answers correctly from Caddy's context but the browser still fails, I move back toward the edge, cache, authentication, or browser policy.

This order preserves causality. Reverse-proxy incidents become slow when operators collect commands rather than evidence. The useful output of a command is not merely success or failure; it is a boundary decision. A successful DNS lookup narrows the problem. A successful socket connect narrows it again. A valid TLS handshake narrows it further. By the time I reach the application response, most unrelated hypotheses are already eliminated.

I write down the first failed contract before changing anything. That note becomes the rollback point for the experiment and later becomes part of the incident record. It also prevents a classic failure mode: a configuration change happens to make the symptom disappear, but nobody knows whether it fixed routing, changed timing, bypassed security, or merely moved the request to a different path.

## Security boundary

Caddy is often trusted with TLS private keys, authentication decisions, client-address normalization and routing to services that are otherwise private. That makes convenience changes security changes even when they look like ordinary troubleshooting.

For this problem, I ask a narrow question: what new authority would the proposed fix create? The underlying cause is The auth gateway sees a different scheme, host, URI or cookie context than the browser. Missing forwarded context is a common cause. If I solve that by broadening trust instead of correcting the mismatch, the edge may start accepting information from sources that were never meant to be authoritative. Examples include trusting arbitrary X-Forwarded-For values, exposing the admin API, passing user-controlled identity headers, or disabling certificate verification on an internal hop.

The safer pattern is to keep trust directional and explicit. The browser trusts Caddy's public or private certificate. Caddy trusts only the upstream CA it needs. The application trusts identity headers only from Caddy. Caddy trusts client-IP headers only from known ingress proxies. Admin endpoints remain local or tightly controlled. This chain is easier to audit because every identity claim has one writer and one verifier.

## Read the configuration as a contract

The fix pattern for this case is: **Start from forward\_auth and explicitly pass the request context required by the gateway; copy only authenticated identity headers on success.** I read that sentence as an ownership rule, not as a copy-paste instruction. The Caddyfile should say which host or path Caddy owns, which upstream it contacts, and which transformations are intentional. Anything not required for that contract stays out of the first version.

A minimal expression is:

```
app.example.com {\n    forward_auth auth:9091 {\n        uri /api/authz/forward-auth\n        header_up X-Forwarded-Proto https\n        copy_headers Remote-User Remote-Groups Remote-Email Remote-Name\n    }\n    reverse_proxy app:8080\n}
```

From there I ask what each directive changes. Does it change routing? Does it change the request seen by the upstream? Does it change TLS trust or SNI? Does it change response status or body? Does it change browser policy? A directive without a clear answer is a candidate for removal during diagnosis.

I also inspect the adapted configuration when route behavior is surprising. The Caddyfile is an adapter-friendly human format; the runtime sees structured configuration. Looking at the adapted form is especially useful around handle blocks, route blocks, matchers, imported snippets and global server options because it shows what the server will actually execute instead of what indentation makes me think it will execute.

## Build the smallest reproduction

I remove every optional layer I can without changing the failure. CDN caching, SSO, extra headers, a second reverse proxy, observability middleware and convenience redirects all make sense in production, but they create more possible owners during diagnosis. The smallest reproduction should answer one question at a time.

The core configuration I start from is:

```
app.example.com {\n    forward_auth auth:9091 {\n        uri /api/authz/forward-auth\n        header_up X-Forwarded-Proto https\n        copy_headers Remote-User Remote-Groups Remote-Email Remote-Name\n    }\n    reverse_proxy app:8080\n}
```

I am not claiming this is the final production configuration. It is a diagnostic baseline. If the failure persists here, I have proved the problem is fundamental to routing, network reachability, TLS, or the upstream contract. If the failure disappears, I add the removed policy back one layer at a time until the exact interaction returns.

The same rule applies to commands. A curl from my laptop is not equivalent to a request made by a Caddy container. A DNS lookup on the host is not equivalent to Docker DNS inside the Caddy network. A browser success through Cloudflare does not prove the origin certificate is valid from the tunnel process. Reproduction has to run from the same execution context as the component making the failing hop.

## Test matrix

| Test | What it proves |
| --- | --- |
| Origin path | Call the upstream from the Caddy network context. |
| Proxy path | Call the Caddy hostname or listener directly. |
| Full user path | Call through CDN, tunnel, auth and browser-visible hostname. |
| Negative path | Deliberately send the condition that should be rejected. |
| Recovery path | Remove the dependency or break it, then restore it and observe recovery. |

A test matrix prevents the common mistake of proving only the happy path. A valid HTTPS request does not prove a forged forwarded-IP header will be rejected. A successful health probe does not prove user traffic survives when one upstream disappears. A SPA homepage does not prove deep links, API misses and WebSockets route correctly. I deliberately include a negative case because security and routing boundaries are defined as much by what must fail as by what must succeed.

I run the matrix before and after the fix. The before-state confirms the reproduction is real; the after-state proves the change corrected the intended boundary rather than simply changing timing. For higher-risk changes such as authentication, retries, client-IP trust or TLS verification, I keep the matrix as a regression test so the same shortcut cannot quietly return in a later refactor.

## Failure tree

I reduce the incident to a branching tree instead of a list of guesses. Start with the symptom: **Login succeeds, but protected requests return to login again or never reach the application.** If Caddy never receives the request, the problem lives at DNS, port ownership, NAT, a CDN/tunnel or client-side resolution. If Caddy receives it but cannot reach the upstream, inspect Docker networking, host routing, DNS, port, protocol and listener binding. If the transport succeeds but identity fails, inspect Host, SNI, certificates, forwarded headers or auth context. If the upstream returns a response and the browser still fails, inspect redirects, cache, CSP, WebSockets or SPA behavior.

The value of a failure tree is that each branch has a different owner and a different next command. It also limits blast radius. I do not need to touch certificate settings while the upstream name fails to resolve, and I do not need to rebuild containers while the only failing condition is a browser CSP rule.

For recurring incidents, I turn the tree into a runbook. A new operator can then follow the same evidence sequence instead of relying on memory. That is especially useful in a home lab or small team where one person may have built several layers and unconsciously carries the architecture in their head.

## Five-minute runbook

1. **Freeze the symptom.** Save the exact hostname, path, status, browser message and timestamp. Do not restart anything yet.
2. **Identify the ingress owner.** Determine which Caddy instance or external proxy first receives the request.
3. **Test the next hop from that component.** Resolve, connect and negotiate the protocol from the same namespace.
4. **Inspect identity.** Compare Host, SNI, forwarded scheme/host, client address and authentication headers.
5. **Read the response boundary.** Determine whether the upstream produced a response or Caddy failed before one existed.
6. **Reduce to minimal routing.** Temporarily remove optional middleware in a controlled environment.
7. **Apply the smallest ownership fix.** Change only the layer that failed.
8. **Validate and reload.** Keep the previous config available.
9. **Run positive and negative tests.** Confirm expected requests work and forbidden or malformed ones still fail.
10. **Record the reason.** The runbook should end with the failed contract and the evidence that proved the correction, not only the final config diff.

For this article, the key correction is: **Start from forward\_auth and explicitly pass the request context required by the gateway; copy only authenticated identity headers on success.** The runbook is intentionally generic around that rule so it can be reused when the visible status code changes but the underlying boundary remains the same.

## Production operations

A configuration that works once is not yet an operational solution. I want to know what happens during reload, restart, certificate renewal, container recreation, upstream failure, DNS change and a partial outage. The production version should have a predictable state transition for each of those events.

I validate before reload, reload instead of restarting for ordinary config changes, and probe the exact route I changed after the reload. When there are multiple Caddy instances, I record which instance owns the public hostname, which one terminates internal TLS, and which one is application-local. That prevents an operator from making a correct edit to the wrong proxy.

I also keep rollback small. The best rollback is often the previous validated Caddyfile plus the ability to gracefully reload it. If the change included a DNS record, private-CA trust distribution, application base URL, Docker network, or authentication gateway setting, those are separate rollback items. Treating the Caddyfile as the only state in the system is how partial rollbacks create new failures.

## Draw the boundary before touching config

The root cause lives at a boundary. In this case, the technical reason is: The auth gateway sees a different scheme, host, URI or cookie context than the browser. Missing forwarded context is a common cause. That sentence is more useful than the status code by itself. A 502, 404, redirect, TLS error or browser failure is an outcome; the boundary tells me which component can actually fix it.

I sketch the path as:

```
client -> Caddy edge -> Caddy / forward_auth / SSO boundary -> upstream application -> response
```

Then I annotate each arrow with one question: can the previous component resolve the next hop, connect to it, negotiate the expected protocol, preserve the intended identity, and receive the expected response? This turns a broad reverse-proxy problem into a short sequence of falsifiable checks.

The important operational distinction is between **reachability**, **identity**, and **application semantics**. Reachability asks whether the next socket can be opened. Identity asks whether Host, SNI, forwarded client information, or authentication state still means what the downstream expects. Application semantics asks whether the request path, redirect, retry, health probe, or browser policy is valid. Caddy sits at the intersection of all three, which is why a problem can appear to be 'a Caddy problem' even when the correction belongs elsewhere.

## Observability that answers the real question

I want logs and metrics that tell me which leg failed, not simply that Caddy is running. Access logs should let me identify host, URI, status, duration and the client identity Caddy actually derived. Runtime error logs should explain dial, DNS, TLS or handler failures. Upstream health and request metrics should show when one backend is failing while the proxy process remains healthy.

The most useful dashboard separates three states: edge availability, upstream availability and user-visible success. Those can disagree. Caddy can be healthy while an upstream is down. An upstream can be healthy while a route matcher sends users somewhere else. Both can be healthy while a browser policy blocks the frontend. A single green process-health light does not capture those distinctions.

During an incident, I correlate one request through all available evidence. I note the public timestamp, Caddy access record, any proxy error, upstream log and monitoring sample. That gives me a timeline rather than a pile of independent logs. If the request passed through Cloudflare or another proxy, I keep its cache and origin status separate from Caddy's status so one layer does not impersonate another.

## Tradeoffs I accept deliberately

A reverse proxy can usually solve the immediate symptom in several ways. The important question is which solution preserves the properties I care about: explicit trust, stable naming, low operational surprise, debuggable routing and correct HTTP semantics. I do not optimize for the shortest Caddyfile if the shorter version hides ownership.

For this problem, the preferred direction is: **Start from forward\_auth and explicitly pass the request context required by the gateway; copy only authenticated identity headers on success.** That choice may require one more Docker network, one more CA mount, one more application base-URL setting, or one more health endpoint. I accept that extra configuration when it makes the boundary explicit and testable. I am less willing to accept a shortcut that works only while a container IP stays unchanged, a browser ignores a warning, or an operator remembers a hidden dependency.

I also distinguish product tradeoffs from infrastructure tradeoffs. A maintenance page that returns 200 may look better behind a CDN but changes monitoring semantics. A wildcard certificate simplifies certificate count but increases key authority. A subnet of trusted proxy addresses can simplify client-IP handling but broadens the trust boundary. These are legitimate choices when documented; they become bugs when introduced accidentally during troubleshooting.

## Rollout and rollback plan

I stage the change in the smallest reversible sequence. First I validate syntax and adaptation. Second I change only the dependency required for the fix, such as a network attachment, certificate trust file, application base URL or proxy route. Third I reload Caddy gracefully. Fourth I run the test matrix. Only after the user path is proven do I remove temporary diagnostics.

Rollback is the mirror image. I keep the previous validated configuration, but I also record non-Caddy state changed during the rollout. If I added a Docker network, changed a Cloudflare origin name, distributed a private CA, changed a cookie domain, or enabled a new application setting, restoring only the old Caddyfile may leave the system in a mixed state.

For high-risk authentication or client-identity changes, I test rollback before I need it. I maintain a local or out-of-band route to the host so a bad edge policy does not lock me out of the machine that must repair it. That is operationally more valuable than another layer of clever configuration.

## Sources and version notes

The configuration examples in this article are intentionally minimal and should be checked against the Caddy version and modules actually running in production. Caddy evolves, and behaviors around upstream HTTPS, certificate automation, plugins and transports can change between releases.

- https://caddyserver.com/docs/caddyfile/directives/forward\_auth

I treat documentation as the authority for directive semantics and public issue reports as evidence of failure patterns, not as universal configuration recipes. A GitHub issue or forum post can show that a symptom exists; the production fix still has to be validated against the local network, Caddy build, upstream application and trust model.

## The rule I keep

**Start from forward\_auth and explicitly pass the request context required by the gateway; copy only authenticated identity headers on success.**

The durable lesson is not the exact snippet. The durable lesson is that the auth gateway sees a different scheme, host, uri or cookie context than the browser. missing forwarded context is a common cause. Once that ownership boundary is explicit, Caddy becomes easier to operate because every directive has a reason, every failure has a first diagnostic step, and every change has a test.

That is the standard I use for a reverse proxy: not 'does this Caddyfile work today?' but 'can I explain why the request takes this path, who is trusted at each hop, what will fail when a dependency disappears, and how I will know?' If those answers are clear, the configuration is usually small enough to maintain and strong enough to survive the next change.
