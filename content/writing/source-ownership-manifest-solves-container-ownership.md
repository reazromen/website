---
title: A Source-Ownership Manifest Solved the 'Who Owns This Container?' Problem
url: /posts/source-ownership-manifest-solves-container-ownership.html
date: '2026-09-14'
read_time: 1
excerpt: Seeing a service in Portainer does not tell you which repository, runbook
  or backup path can recreate it.
topic: production-engineering
tags:
- ownership
- gitops
- inventory
- documentation
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Git and Provenance · advanced'
outputs:
- url: /posts/source-ownership-manifest-solves-container-ownership.html
  template: cms/templates/posts/posts--source-ownership-manifest-solves-container-ownership.tpl
  source: cms/templates/posts/posts--source-ownership-manifest-solves-container-ownership.json
---

The production host had managed apps plus external/shared runtimes such as VoIP components, Portainer, Komodo, tunnels and authentication services. Container discovery alone could not answer who owned each definition. Runtime inventory and source ownership had been conflated. A container name tells an operator what is running, not where the desired state, secret contract, backup class or recovery instructions live.

A Git-owned source-ownership registry now maps service families to repositories or paths, service records and readiness state. CI validates that managed application directories are represented.

Make ownership registration part of the definition of done for every new service. An undocumented container should be treated as an operational defect, not a harmless convenience. This is service ownership and configuration management. Production systems need an authoritative path from runtime object to source, owner, data location and recovery procedure. The concrete hserver evidence is commit 9d36c75, so this note is tied to an actual production change rather than a hypothetical failure.
