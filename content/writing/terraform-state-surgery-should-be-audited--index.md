---
title: Terraform State Surgery Should Be Rare, Explicit, and Audited
url: /posts/terraform-state-surgery-should-be-audited/index.html
date: '2026-09-26'
read_time: 8
excerpt: state mv, state rm, state replace-provider, state pull and state push can
  change Terraform's ownership model without directly changing remote infrastructure.
topic: index
tags:
- terraform
- state-mv
- state-rm
- recovery
draft: false
featured: false
language: en
eyebrow: Terraform State & Drift · Terraform systems note
outputs:
- url: /posts/terraform-state-surgery-should-be-audited/index.html
  template: cms/templates/posts/posts--terraform-state-surgery-should-be-audited--index.tpl
  source: cms/templates/posts/posts--terraform-state-surgery-should-be-audited--index.json
---

Terraform's state subcommands are powerful because they can repair the mapping between code and infrastructure without touching the infrastructure itself.

## state mv changes identity

It rebinds a real object from one resource address to another. Modern moved blocks are often preferable because the migration remains visible in source control.

## state rm gives up ownership

The remote object stays, but Terraform forgets it. If configuration still declares the resource, a later plan may try to create a replacement.

## replace-provider rewrites provider association

This is useful during namespace changes or provider forks, but compatibility has to be verified afterward.

## state push is disaster-recovery territory

Terraform checks lineage and serial before accepting a manual push. Forcing past those protections can overwrite newer canonical state.

## Audit the operation

Capture a state backup, exact command, change reason, configuration revision and post-change plan. If the operation changes who Terraform thinks owns an object, it deserves the same review as a database migration.

## Sources and further reading

- [Terraform state commands](https://developer.hashicorp.com/terraform/cli/commands/state)
- [Backends and manual state push](https://developer.hashicorp.com/terraform/language/state/backends)
