---
title: Terraform Ephemeral Values and Write-Only Arguments Change the Secret-Handling
  Model
url: /posts/terraform-ephemeral-write-only-change-secret-handling/index.html
date: '2026-09-26'
read_time: 8
excerpt: Terraform 1.10+ ephemeral values and 1.11+ write-only arguments let temporary
  values pass through a run without being persisted in state or plan artifacts when
  providers support them.
topic: index
tags:
- terraform
- ephemeral
- write-only
- secrets
draft: false
featured: false
language: en
eyebrow: Terraform Security · Terraform systems note
outputs:
- url: /posts/terraform-ephemeral-write-only-change-secret-handling/index.html
  template: cms/templates/posts/posts--terraform-ephemeral-write-only-change-secret-handling--index.tpl
  source: cms/templates/posts/posts--terraform-ephemeral-write-only-change-secret-handling--index.json
---

Historically, a value needed by a managed resource often became part of state. Recent Terraform versions add a different path for temporary values.

## Ephemeral values exist for the operation

Variables, child outputs and provider-defined ephemeral resources can carry values during planning and apply without persisting them into normal artifacts.

## Write-only arguments are terminal endpoints

Providers can expose managed-resource arguments whose values are consumed during the operation and then discarded rather than stored in state.

## No stored old value means no ordinary diff

If Terraform does not remember a write-only value, it cannot compare old and new values later. Providers often pair the field with a version attribute that Terraform does store; incrementing that version becomes the update signal.

## Provider support defines the boundary

Practitioners cannot convert arbitrary existing arguments into write-only fields. The provider schema must support the behavior.

## Short-lived credentials fit better

Temporary credentials from a secret broker can now flow through a run without becoming long-lived Terraform metadata, reducing the amount of sensitive material that survives the operation.

State still needs strong protection, but ephemeral values finally let some secret-dependent infrastructure operations avoid persisting the secret itself.

## Sources and further reading

- [Terraform ephemeral values](https://developer.hashicorp.com/terraform/language/manage-sensitive-data/ephemeral)
- [Terraform write-only arguments](https://developer.hashicorp.com/terraform/language/manage-sensitive-data/write-only)
