---
title: Terraform import Blocks Make Brownfield Adoption Reviewable
url: /posts/terraform-import-blocks-make-brownfield-reviewable/index.html
date: '2024-03-15'
read_time: 8
excerpt: Configuration-driven import turns existing infrastructure adoption into code
  that can be planned, reviewed, repeated, and paired with the resource configuration
  it will become.
topic: index
tags:
- terraform
- import
- brownfield
- iac
draft: false
featured: false
language: en
eyebrow: Terraform Refactoring · Terraform systems note
outputs:
- url: /posts/terraform-import-blocks-make-brownfield-reviewable/index.html
  template: cms/templates/posts/posts--terraform-import-blocks-make-brownfield-reviewable--index.tpl
  source: cms/templates/posts/posts--terraform-import-blocks-make-brownfield-reviewable--index.json
---

CLI import changes state immediately and leaves the operator to reconstruct configuration afterward. Import blocks make adoption part of the configuration review.

```
import {
  to = aws_s3_bucket.logs
  id = "company-prod-logs"
}
```

## Import establishes identity, not intent

After import, Terraform can still plan changes because the HCL does not yet match the remote object. The brownfield workflow is not complete until the differences are understood and configuration represents the intended future state.

## for\_each scales adoption

Modern import blocks support `for_each`, allowing sets of related resources to be adopted declaratively. Stable keys matter because they become part of destination addresses.

## Provider aliases make target context explicit

In multi-account and multi-region estates, an import can specify the provider configuration instead of relying on whatever credentials are active in a shell.

## The goal is a boring plan

Brownfield adoption should end with a clear resource configuration, correct state binding, and a plan whose changes are understood. Import success alone is only the first step.

## Sources and further reading

- [Terraform import block](https://developer.hashicorp.com/terraform/language/block/import)
