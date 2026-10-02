---
title: Routing Calls Across Two PBXs Without Turning Kamailio into a PBX
url: /posts/routing-calls-across-two-pbxs-without-turning-kamailio-into-a-pbx.html
date: '2026-09-14'
read_time: 2
excerpt: A two-PBX lab clarified the boundary between SIP routing at the proxy and
  dialplan or application behavior inside the PBX.
topic: telecom-voip
tags:
- kamailio
- asterisk
- freeswitch
- routing
draft: false
featured: false
language: en
eyebrow: 2021 SIP Infrastructure · intermediate
outputs:
- url: /posts/routing-calls-across-two-pbxs-without-turning-kamailio-into-a-pbx.html
  template: cms/templates/posts/posts--routing-calls-across-two-pbxs-without-turning-kamailio-into-a-pbx.tpl
  source: cms/templates/posts/posts--routing-calls-across-two-pbxs-without-turning-kamailio-into-a-pbx.json
---

Once I had more than one PBX in the lab, it became tempting to put every routing decision into one place. Kamailio was in front, so why not make it understand extensions, voicemail, application logic and media decisions as well? The better design was to keep the proxy focused on SIP routing and leave PBX behavior inside the systems built for it.

I used one Asterisk instance and one FreeSWITCH instance behind Kamailio. Each PBX owned a different extension range. Kamailio looked at the Request-URI and selected the appropriate downstream group. The PBXs still controlled their own dialplans, local features and endpoint registrations.

This made the signaling path easy to read. An INVITE for one range went to Asterisk; another went to FreeSWITCH. Responses came back through the transaction state in Kamailio. If a PBX was unavailable, the proxy could reject the request or try an alternate destination without pretending to provide the PBX application itself.

The lab also exposed the difference between routing by number and routing by registration location. Static prefix routing is simple and predictable, but user mobility or shared numbering may require a location service or external data source. I kept the first version deliberately static because I wanted to understand the failure modes before adding a database.

Health checking mattered once there were multiple targets. Sending traffic to a dead PBX and waiting for transaction timeout is technically a form of failure detection, but it is slow and unpleasant for callers. Dispatcher-style destination groups and active health checks provide a better foundation when the routing layer grows.

I also resisted anchoring media just because the signaling crossed Kamailio. If the two endpoints could exchange RTP directly and there was no policy reason to relay it, the proxy did not need to become the media path. When NAT or topology required rtpengine, I added it explicitly.

This lab was where the word 'SIP server' became too vague for me. A proxy, registrar, PBX, SBC and media relay may all process SIP-related traffic, but they have different responsibilities. Keeping those roles visible made the architecture easier to scale and much easier to explain.
