---
title: 'Ubuntu 18.04 on a Lab Machine: The Networking Commands I Kept Reusing'
url: /posts/ubuntu-18-04-lab-machine-networking-commands.html
date: '2026-09-14'
read_time: 3
excerpt: Ubuntu 18.04 was a good excuse to stop relying on desktop network icons and
  start reading interface state, routes, sockets and DNS configuration directly from
  the system.
topic: linux-homelab
tags:
- ubuntu
- linux
- networking
- netplan
draft: false
featured: false
language: en
eyebrow: 2018 Network Foundations · beginner
outputs:
- url: /posts/ubuntu-18-04-lab-machine-networking-commands.html
  template: cms/templates/posts/posts--ubuntu-18-04-lab-machine-networking-commands.tpl
  source: cms/templates/posts/posts--ubuntu-18-04-lab-machine-networking-commands.json
---

Ubuntu 18.04 arrived at a useful point in my networking study because it pushed me toward the command line instead of treating the operating system as a black box. The release used the 4.15 Linux kernel and Ubuntu Server moved toward Netplan for network configuration. For a lab machine, the exact desktop experience mattered less than learning how Linux represented interfaces, routes, listeners and name resolution.

The command I used most was `ip addr`. It answers basic questions without interpretation: what interfaces exist, whether they are up, which IPv4 and IPv6 addresses are assigned, and what prefix length each address uses. If I expected `192.168.50.10/24` on an Ethernet interface and it was not there, there was no reason to troubleshoot DNS or a remote server yet. The local interface state had to be correct first.

The next command was `ip route`. An address tells me who the host is on a network; the routing table tells me where the kernel intends to send packets. A typical small configuration might have a connected route for `192.168.50.0/24` and a default route through a gateway on another interface. Reading that table made the idea of a default gateway much more concrete. It is simply the route used when no more-specific route matches.

For link information I used `ip link`. It is useful for separating an address problem from a Layer 2 problem. An interface can exist but be administratively down. A physical cable can also be disconnected while the configuration file looks perfect. Commands that expose link state keep those cases separate.

Once applications were involved, socket state became important. `ss -lntup` shows listening TCP and UDP sockets, along with process information when permissions allow it. If I start an SSH or web service and nothing is listening on the expected port, the network is not the first suspect. If the service is listening only on `127.0.0.1`, a remote host will not reach it through the Ethernet address. That distinction later became important with databases, PBXs and containerized services as well.

DNS troubleshooting needed its own checks. In that period, `systemd-resolve --status` was useful for seeing resolver state on systems using systemd-resolved. I also used `dig` when available because it shows the DNS transaction more directly than a browser error message. A failed name lookup and a failed TCP connection are different problems even if both appear to the user as a website that does not open.

Netplan added another layer worth understanding. The YAML file under `/etc/netplan/` describes intended network configuration, while the runtime state still appears through the `ip` tools. I learned not to confuse configuration with state. A correct-looking YAML file does not prove that an interface has the expected address after applying it. The runtime commands are the evidence.

The workflow that stayed with me was simple: inspect link, inspect address, inspect route, test a nearby IP, test the gateway, test a remote IP, then test DNS and the application. The commands have changed less than the surrounding tools, and the troubleshooting order still works.
