---
title: Use Terraform -replace When the Object Is Broken but the Configuration Is Right
url: /posts/terraform-replace-is-better-than-taint-and-implicit-hacks/index.html
date: '2024-02-21'
read_time: 8
excerpt: Sometimes infrastructure is unhealthy in ways Terraform cannot infer from
  HCL. -replace makes that one-run replacement intent visible in the plan instead
  of mutating state ahead of review.
topic: index
tags:
- terraform
- replace
- taint
- operations
draft: false
featured: false
language: en
eyebrow: Terraform Lifecycle · Terraform systems note
outputs:
- url: /posts/terraform-replace-is-better-than-taint-and-implicit-hacks/index.html
  template: cms/templates/posts/posts--terraform-replace-is-better-than-taint-and-implicit-hacks--index.tpl
  source: cms/templates/posts/posts--terraform-replace-is-better-than-taint-and-implicit-hacks--index.json
---

A VM can have a corrupt filesystem while every configured attribute still matches state. Terraform sees no configuration reason to replace it.

## -replace adds operator intent to planning

`terraform plan -replace=aws_instance.web` tells Terraform to include replacement in the plan while leaving configuration unchanged.

The change becomes part of normal review before apply.

## This is cleaner than taint-first behavior

The older taint workflow modified state first so the next plan would replace the object. That separates the operational decision from the review artifact.

## replace\_triggered\_by is a different tool

A lifecycle `replace_triggered_by` rule is persistent configuration: when another managed object changes, this object should be replaced. `-replace` is a one-run instruction for an unhealthy object.

## Review the cascade

A new resource ID can cause downstream updates or replacements. Even when only one object is explicitly selected, the full plan still matters.

The clean model is: configuration is right, the object is unhealthy, and replacement intent is visible in the plan.

## Sources and further reading

- [terraform apply -replace](https://developer.hashicorp.com/terraform/cli/commands/apply)
- [lifecycle replace\_triggered\_by](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle)
