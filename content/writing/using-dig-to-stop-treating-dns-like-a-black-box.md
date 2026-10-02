---
title: Using `dig` to Stop Treating DNS Like a Black Box
url: /posts/using-dig-to-stop-treating-dns-like-a-black-box.html
date: '2026-09-14'
read_time: 3
excerpt: '`dig` gave me a way to separate resolver configuration, authoritative answers,
  record types and response timing instead of reducing DNS to ''name works'' or ''name
  fails''.'
topic: linux-homelab
tags:
- dns
- linux
- dig
- troubleshooting
draft: false
featured: false
language: en
eyebrow: 2019 Routing, Linux & First VoIP · intermediate
outputs:
- url: /posts/using-dig-to-stop-treating-dns-like-a-black-box.html
  template: cms/templates/posts/posts--using-dig-to-stop-treating-dns-like-a-black-box.tpl
  source: cms/templates/posts/posts--using-dig-to-stop-treating-dns-like-a-black-box.json
---

DNS was easy to ignore when it worked and easy to blame when anything involving a hostname failed. Using `dig` changed that because it exposed an actual query and response instead of giving me only an application error. I could see which record type I asked for, which server answered, whether the answer was authoritative, how long the query took and what flags came back.

A basic `dig example.com A` query is already more informative than a browser. The QUESTION section shows what I asked. The ANSWER section shows returned records. The SERVER line tells me which resolver I actually used. The query time gives a rough indication of latency. If the answer section is empty, the status code and authority information help distinguish 'the name does not exist' from 'the resolver did not answer'.

Record types also stopped being an abstract list. `A` maps a name to IPv4. `AAAA` does the same for IPv6. `MX` points toward mail exchangers. `NS` identifies authoritative name servers for a zone. `CNAME` creates an alias. `TXT` can carry a wide range of text-based policy and verification data. Querying each one separately made it obvious that DNS is not one giant hostname-to-address table.

The `+trace` option was useful when I wanted to see delegation rather than rely entirely on the configured recursive resolver. Starting from the root and following referrals down toward the authoritative servers showed the hierarchy directly. I did not need that for every failure, but it helped explain why changing a local resolver cannot fix a broken delegation at the authoritative side.

Caching became easier to understand too. TTL values are part of the response, and recursive resolvers can keep records until those timers expire. That means a DNS change is not instantly visible everywhere, even if the authoritative zone has already been updated. In a lab I could query the authoritative server directly and compare it with the cached answer from the normal resolver.

I also learned to test the resolver by address. `dig @8.8.8.8 example.com` or a query to a local DNS server bypasses part of the system's normal resolver selection and lets me compare behavior between servers. If one resolver answers and another times out, the problem is more specific than 'DNS is down'. If both return the same wrong record, the issue may be authoritative data rather than the recursive service.

The main benefit was precision. DNS troubleshooting became a set of questions: which resolver did the client ask, what exact record type was requested, what response code came back, where is the zone delegated, what does the authoritative server say, and could a cached value still be valid? Once those are visible, a lot of vague hostname problems turn into ordinary protocol analysis.
