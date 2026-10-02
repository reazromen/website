---
title: 'Split-Horizon DNS: One Hostname, Two Network Paths, and a Lot of TLS Confusion'
url: /posts/split-horizon-dns-one-hostname-two-paths.html
date: '2026-09-26'
read_time: 8
excerpt: The same hostname can resolve to a local reverse proxy on LAN and a Cloudflare
  Tunnel externally. That is clean when DNS, SNI, certificates, and origin routing
  agree—and maddening when one layer quietly takes the other path.
topic: ''
tags:
- dns
- cloudflare
- tls
- reverse-proxy-98645a
draft: false
featured: false
language: en
eyebrow: DNS & Edge Networking · systems note
outputs:
- url: /posts/split-horizon-dns-one-hostname-two-paths.html
  template: cms/templates/posts/posts--split-horizon-dns-one-hostname-two-paths.tpl
  source: cms/templates/posts/posts--split-horizon-dns-one-hostname-two-paths.json
---

Using one hostname everywhere sounds like the simplest possible design.

Inside the LAN, `app.example.com` resolves directly to the local reverse proxy. Outside, the same name resolves through Cloudflare and a Tunnel. Users keep one bookmark and applications keep one origin.

The complexity appears because one name now describes two packet paths.

## DNS decides which architecture you are using[#](#dns-decides-which-architecture-you-are-using)

For an external client:

```
app.example.com
 -> public DNS
 -> Cloudflare edge
 -> Tunnel
 -> origin
```

For an internal client under split-horizon DNS:

```
app.example.com
 -> internal DNS
 -> LAN reverse proxy
 -> origin
```

The HTTP hostname is identical. The transport path is not.

When debugging, the first question is therefore not “is DNS correct?” but “which resolver answered this specific client, and what address did it return?”

## Browsers may not use the resolver you think they use[#](#browsers-may-not-use-the-resolver-you-think-they-use)

A command-line `dig` can query the system resolver while a browser uses encrypted DNS or another policy path.

That is how operators end up with the classic symptom: `curl` reaches the local proxy, the browser reaches somewhere else, and the certificate error appears irrational.

Capture the browser's actual destination IP and resolver behavior before changing certificates.

## SNI chooses the certificate path after DNS[#](#sni-chooses-the-certificate-path-after-dns)

Once the connection reaches a TLS endpoint, Server Name Indication tells that endpoint which hostname the client expects.

If internal DNS points at Nginx or Caddy, that local proxy must have a certificate and route for the same hostname. If public DNS points through Cloudflare, the browser sees Cloudflare's edge certificate while the Tunnel has its own origin-side relationship.

Two certificates for one hostname are not inherently a problem. They are terminating TLS on different paths.

The problem is ambiguity about which path a client is actually on.

## Keep origin TLS simple[#](#keep-origin-tls-simple)

A clean design assigns one responsibility at each hop:

- Cloudflare edge terminates public client TLS,
- Tunnel carries traffic to a known origin endpoint,
- LAN clients hit the local reverse proxy directly,
- the local reverse proxy presents a certificate trusted by those LAN clients for the same hostname.

A DNS-01 ACME flow can obtain a publicly trusted certificate without exposing port 80 or 443 from the LAN.

Alternatively, an internal CA can work if every client is deliberately enrolled to trust it.

## Hairpinning is a different architecture[#](#hairpinning-is-a-different-architecture)

Some networks avoid split DNS and let internal clients resolve the public path. The traffic leaves logically toward the public service and returns through Cloudflare/Tunnel or router hairpin behavior.

That reduces DNS differences but adds path length and dependence on external infrastructure for local access.

Neither design is universally correct. The mistake is accidentally operating both.

## Tailscale adds a third possible resolver view[#](#tailscale-adds-a-third-possible-resolver-view)

With Tailscale, a mobile or remote client may be “inside” from an access-policy perspective while physically outside the LAN.

MagicDNS, subnet routes, exit nodes, and split-DNS rules can therefore create a third answer for the same name.

I prefer to document resolution as a table:

```
LAN       -> 192.168.x.x
Tailscale -> 100.x.x.x or LAN route
Internet  -> Cloudflare
```

If two rows are supposed to be identical, make that explicit too.

## Debug name, route, TLS, and HTTP separately[#](#debug-name-route-tls-and-http-separately)

For a broken request I walk the stack in order:

1. Which resolver answered?
2. What IP/address family was returned?
3. Which interface/path did the client use?
4. Which TLS endpoint received SNI?
5. Which certificate chain came back?
6. Which reverse-proxy virtual host matched?
7. Which upstream origin handled the HTTP request?

This is faster than editing random DNS and proxy settings because each layer produces different evidence.

## One hostname is still worth it[#](#one-hostname-is-still-worth-it)

Split-horizon DNS is not inherently fragile. It is just two routing policies sharing one application identity.

Done deliberately, it gives local traffic a short path and external traffic a controlled edge path without forcing users to remember different URLs.

The design becomes confusing only when DNS, browser resolver policy, SNI, certificates, and origin routing are treated as one feature instead of five connected layers.

## Sources and further reading[#](#sources-and-further-reading)

- [Cloudflare Tunnel documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- [Caddy automatic HTTPS documentation](https://caddyserver.com/docs/automatic-https)
- [2026 self-hosting discussion: Cloudflare outside, wildcard/local DNS inside](https://www.reddit.com/r/selfhosted/comments/1s5yvqu/cloudflare_tunnel_from_the_outside_wildcard/)
