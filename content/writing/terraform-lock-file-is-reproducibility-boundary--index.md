---
title: The Terraform Dependency Lock File Is Part of Your Reproducibility Boundary
url: /posts/terraform-lock-file-is-reproducibility-boundary/index.html
date: '2022-02-26'
read_time: 8
excerpt: required_providers constrains acceptable versions; .terraform.lock.hcl records
  the exact provider selections and checksums Terraform should install. Committing
  one without understanding the other creates false confidence.
topic: index
tags:
- terraform
- lock-file
- providers
- supply-chain-3f4126
draft: false
featured: false
language: en
eyebrow: Terraform Providers · Terraform systems note
outputs:
- url: /posts/terraform-lock-file-is-reproducibility-boundary/index.html
  template: cms/templates/posts/posts--terraform-lock-file-is-reproducibility-boundary--index.tpl
  source: cms/templates/posts/posts--terraform-lock-file-is-reproducibility-boundary--index.json
---

Terraform configuration often specifies a provider version range such as `>= 5.0, < 6.0`. That range is not a reproducible build.

## Constraints describe compatibility

A module should declare which provider versions it is compatible with. Root configurations then resolve one version that satisfies all constraints.

## The lock file records the selection

`.terraform.lock.hcl` stores the selected provider version and package checksums. Future `terraform init` runs use that selection until you intentionally upgrade it.

This is the infrastructure equivalent of a package lock file.

## Commit it for root configurations

Without the lock file, two engineers or CI runners can initialize the same HCL at different times and receive different provider versions inside the allowed range.

That means the same configuration can produce a different plan.

## Cross-platform teams need checksum coverage

`terraform providers lock` can pre-populate hashes for multiple target platforms. This matters when developers run macOS or Windows while HCP Terraform runs Linux.

## Mirrors do not remove integrity requirements

The lock command can record official checksums even when future installations use a filesystem or network mirror. That lets Terraform verify the mirror is serving the expected provider package.

## Upgrade the lock file intentionally

A provider upgrade should be a reviewed change with its own plan. Running `terraform init -upgrade` casually in a deployment job makes provider selection part of every deployment.

Provider code participates directly in planning and resource lifecycle behavior. Pinning it is part of making infrastructure changes reproducible.

## Sources and further reading

- [Terraform provider requirements and lock file](https://developer.hashicorp.com/terraform/language/providers/requirements)
- [terraform providers lock](https://developer.hashicorp.com/terraform/cli/commands/providers/lock)
