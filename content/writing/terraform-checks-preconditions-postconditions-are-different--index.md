---
title: Terraform check, precondition, and postcondition Blocks Fail at Different Boundaries
url: /posts/terraform-checks-preconditions-postconditions-are-different/index.html
date: '2024-03-30'
read_time: 8
excerpt: Terraform has several validation primitives because not every rule should
  fail at the same time. Preconditions protect assumptions, postconditions protect
  guarantees, and check blocks report ongoing health without necessarily blocking
  a run.
topic: index
tags:
- terraform
- check
- precondition
- postcondition
draft: false
featured: false
language: en
eyebrow: Terraform Validation · Terraform systems note
outputs:
- url: /posts/terraform-checks-preconditions-postconditions-are-different/index.html
  template: cms/templates/posts/posts--terraform-checks-preconditions-postconditions-are-different--index.tpl
  source: cms/templates/posts/posts--terraform-checks-preconditions-postconditions-are-different--index.json
---

Terraform validation is not one feature anymore. Choosing the wrong primitive can make a useful warning block a deployment or make a critical invariant only print a warning.

## Preconditions validate assumptions

A precondition runs before Terraform performs operations on the enclosing resource, data source or output. It is appropriate for statements such as “the selected AMI must be x86\_64” or “this subnet set must span at least two zones.”

If the assumption is false, Terraform should stop before attempting the dependent operation.

## Postconditions validate guarantees

A postcondition checks the result after Terraform reads or creates the object. A failed postcondition can block downstream resources that depend on that object.

This is useful for guarantees the module promises to consumers: a created instance must receive a private DNS name, or a selected certificate must be valid for the required hostname.

## check blocks are non-blocking health assertions

Terraform evaluates `check` blocks after plan/apply. A failed assertion reports a warning and continues the operation. In HCP Terraform, checks can also participate in continuous validation.

That makes checks good for health observations whose temporary failure should not prevent infrastructure reconciliation.

## Failure semantics are architecture

If a rule protects safety—wrong account, unsupported architecture, missing encryption—it probably belongs in a blocking validation. If a rule reports availability—an HTTP endpoint is momentarily unhealthy—it may belong in a check.

## Error messages are part of the module API

Module users see these validations when their changes fail. A useful message should explain the violated invariant and the expected fix, not just repeat the condition expression.

Validation works best when it is placed at the boundary where the invariant becomes meaningful.

## Sources and further reading

- [Terraform validation overview](https://developer.hashicorp.com/terraform/language/validate)
- [Terraform check block](https://developer.hashicorp.com/terraform/language/block/check)
- [Terraform lifecycle conditions](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle)
