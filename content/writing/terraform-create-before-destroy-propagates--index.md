---
title: Terraform create_before_destroy Can Propagate Through the Dependency Graph
url: /posts/terraform-create-before-destroy-propagates/index.html
date: '2026-09-26'
read_time: 8
excerpt: create_before_destroy changes replacement ordering to reduce downtime, but
  naming constraints, quotas, dependencies, and temporary double-capacity decide whether
  that strategy is actually safe.
topic: index
tags:
- terraform
- create-before-destroy
- lifecycle
- replacement
draft: false
featured: false
language: en
eyebrow: Terraform Lifecycle · Terraform systems note
outputs:
- url: /posts/terraform-create-before-destroy-propagates/index.html
  template: cms/templates/posts/posts--terraform-create-before-destroy-propagates--index.tpl
  source: cms/templates/posts/posts--terraform-create-before-destroy-propagates--index.json
---

`create_before_destroy` flips replacement order so a new object is created before the old one is removed. It is useful, but the lifecycle is not isolated to one line of HCL.

## Dependency ordering can propagate

Terraform may need compatible create-before-destroy behavior on dependencies to preserve a valid graph during replacement.

## Unique names can make it impossible

If a provider requires the replacement to use the exact same globally unique name, old and new cannot coexist. Zero-downtime design may need generated names plus DNS or another stable indirection layer.

## Double capacity consumes quota

For large fleets or databases, the transition temporarily requires both generations. IP space, service quotas and budget can block the plan even when the lifecycle rule is valid.

## External systems may see both generations

Monitoring, service discovery or security integrations can observe old and new objects simultaneously. If uniqueness is an application invariant, overlap can be worse than brief downtime.

Replacement ordering is architecture. Enable create-before-destroy only when the surrounding system supports overlapping generations.

## Sources and further reading

- [Terraform lifecycle create\_before\_destroy](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle)
