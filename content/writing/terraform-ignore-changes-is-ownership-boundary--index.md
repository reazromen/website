---
title: Terraform ignore_changes Is an Ownership Boundary, Not a Drift Fix
url: /posts/terraform-ignore-changes-is-ownership-boundary/index.html
date: '2026-09-26'
read_time: 8
excerpt: ignore_changes tells Terraform that selected attributes may be controlled
  elsewhere after creation. Used casually, it can hide real drift and make configuration
  stop describing production.
topic: index
tags:
- terraform
- ignore-changes
- drift
- ownership
draft: false
featured: false
language: en
eyebrow: Terraform Lifecycle · Terraform systems note
outputs:
- url: /posts/terraform-ignore-changes-is-ownership-boundary/index.html
  template: cms/templates/posts/posts--terraform-ignore-changes-is-ownership-boundary--index.tpl
  source: cms/templates/posts/posts--terraform-ignore-changes-is-ownership-boundary--index.json
---

`ignore_changes` is often used to silence noisy plans. That is safe only when the noise comes from a legitimate second owner.

## The rule changes enforcement

Terraform can use an attribute during create but ignore later remote changes when planning updates. The configured value may stay in HCL while Terraform deliberately declines to restore it.

## That is shared ownership

Autoscaling desired capacity is a common example: Terraform creates the group, then an autoscaler owns the live count. Ignoring that field can be correct.

Ignoring encryption settings, firewall rules or image versions because people edit them manually is a very different risk.

## Document the other controller

Every ignored field should have an answer: who owns it, through which mechanism, and how is that mechanism monitored?

## Temporary ignores can become permanent blind spots

Workarounds for provider bugs often outlive the bug. Review ignored attributes periodically and remove them when Terraform should resume ownership.

A quiet plan can mean infrastructure matches configuration—or that Terraform was told not to care about the differences. Treat `ignore_changes` as an ownership declaration.

## Sources and further reading

- [Terraform lifecycle meta-argument](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle)
