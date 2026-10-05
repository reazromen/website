---
title: Terraform Provider Upgrades Are Schema Migrations, Not Dependency Chores
url: /posts/terraform-provider-upgrades-are-schema-migrations/index.html
date: '2021-12-29'
read_time: 8
excerpt: A provider defines resource schemas, planning behavior, defaults, import
  rules, and state upgrades. Changing its version can alter plans even when no HCL
  changes, so provider upgrades deserve infrastructure review.
topic: index
tags:
- terraform
- providers
- upgrade
- schema
draft: false
featured: false
language: en
eyebrow: Terraform Providers · Terraform systems note
outputs:
- url: /posts/terraform-provider-upgrades-are-schema-migrations/index.html
  template: cms/templates/posts/posts--terraform-provider-upgrades-are-schema-migrations--index.tpl
  source: cms/templates/posts/posts--terraform-provider-upgrades-are-schema-migrations--index.json
---

It is tempting to treat a provider upgrade like bumping a normal library version.

A Terraform provider is more deeply involved: it defines how configuration maps to API requests, how remote objects are refreshed into state, and which attribute changes require replacement.

## The provider owns resource schema

State contains provider-versioned resource data. New provider releases can include schema migration logic so old state is upgraded when read.

That means provider version changes can affect state interpretation even before an apply changes remote infrastructure.

## Defaults and normalization can change plans

A provider can alter default handling, computed fields, diff suppression, API normalization or replacement behavior. The HCL can remain identical while the plan changes after upgrade.

## Upgrade one layer at a time

I prefer a dedicated provider-upgrade change: update constraints/lock file, run init, inspect the full plan, and avoid mixing it with a large module refactor or application deployment.

## Read breaking-change notes before plan surprises

Major provider releases often remove deprecated fields or change resource semantics. A clean lock-file diff does not tell you those behavioral details.

## State and provider version are coupled

HashiCorp's `terraform show -json` guidance notes that state may need to be upgraded with the current provider schema before certain JSON representations can be produced. That is a useful reminder that state is not independent of provider code.

## Rollbacks are not always trivial

After state is upgraded or new resource features are used, downgrading the provider may no longer understand the state/configuration. Test rollback assumptions before a production upgrade, especially across major versions.

A provider upgrade is infrastructure behavior changing beneath the same HCL. Treat it like a schema/API migration, not housekeeping.

## Sources and further reading

- [Terraform provider requirements](https://developer.hashicorp.com/terraform/language/providers/requirements)
- [terraform show and provider schema note](https://developer.hashicorp.com/terraform/cli/commands/show)
