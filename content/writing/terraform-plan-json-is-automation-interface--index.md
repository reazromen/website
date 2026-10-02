---
title: terraform show -json Is an Automation Interface With a Security Footgun
url: /posts/terraform-plan-json-is-automation-interface/index.html
date: '2026-09-26'
read_time: 8
excerpt: The JSON form of a plan exposes structured resource actions, configuration
  and state for automation. It can also expose sensitive values in plaintext, so policy
  tooling must treat it as protected data.
topic: index
tags:
- terraform
- json-plan
- automation
- policy
draft: false
featured: false
language: en
eyebrow: Terraform CI/CD · Terraform systems note
outputs:
- url: /posts/terraform-plan-json-is-automation-interface/index.html
  template: cms/templates/posts/posts--terraform-plan-json-is-automation-interface--index.tpl
  source: cms/templates/posts/posts--terraform-plan-json-is-automation-interface--index.json
---

Parsing colored Terraform output with regular expressions is fragile. Terraform provides a structured representation specifically for tooling.

## JSON exposes proposed actions

`terraform show -json tfplan` gives automation a machine-readable view of resource changes, configuration, planned values and prior state. That enables policy checks, cost estimation, custom review UIs and change classification.

## Structured does not mean harmless

HashiCorp warns that sensitive values can appear in plaintext in JSON output. A pipeline that safely redacts terminal output can still leak secrets if it uploads plan JSON to an open artifact store.

## Inspect actions, not text

Use structured resource addresses and action arrays to identify creates, updates, replacements and destroys. The same representation is better for rules such as “database destroy needs extra approval” or “production IAM changes require security review.”

## Pin versions and test parsers

Automation should run against known Terraform versions and representative plans. If the parser encounters unfamiliar structure, fail closed rather than silently ignoring new change types.

## Keep human review

A machine can detect that a database will be replaced; a human may still need to understand whether that replacement is intentional after a module refactor.

The JSON plan is a powerful interface between Terraform and platform tooling. Treat it as both infrastructure data and a sensitive deployment artifact.

## Sources and further reading

- [terraform show](https://developer.hashicorp.com/terraform/cli/commands/show)
- [Terraform plan tutorial](https://developer.hashicorp.com/terraform/tutorials/cli/plan)
