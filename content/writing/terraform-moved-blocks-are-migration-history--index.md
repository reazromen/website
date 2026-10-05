---
title: Terraform moved Blocks Are Migration History, Not Cleanup Noise
url: /posts/terraform-moved-blocks-are-migration-history/index.html
date: '2025-05-21'
read_time: 8
excerpt: A moved block records that a resource address changed while the remote object
  did not. Removing it too early can make older module consumers see a destructive
  refactor.
topic: index
tags:
- terraform
- moved
- modules
- refactoring
draft: false
featured: false
language: en
eyebrow: Terraform Refactoring · Terraform systems note
outputs:
- url: /posts/terraform-moved-blocks-are-migration-history/index.html
  template: cms/templates/posts/posts--terraform-moved-blocks-are-migration-history--index.tpl
  source: cms/templates/posts/posts--terraform-moved-blocks-are-migration-history--index.json
---

Renaming a Terraform resource changes its address, even when the remote object should remain unchanged. Without migration information, Terraform can see the old address disappear and a new one appear.

## moved blocks preserve object identity

```
moved {
  from = aws_instance.web
  to   = aws_instance.app
}
```

Terraform checks state for the old address, re-associates the object with the new address, then plans from there.

## Migration belongs with the module

For shared modules, a moved block is better than telling every consumer to run `state mv`. Dev, staging and production can all upgrade through the same declared migration.

## Removing it can be breaking

A workspace that skips intermediate module versions may still carry the old address. HashiCorp explicitly treats removal of moved history as a compatibility decision.

## Plan the refactor like a schema migration

Review every moved instance, ensure preserved resources show address changes rather than destroy/create, and keep migration blocks until you intentionally drop compatibility with older state layouts.

## Sources and further reading

- [moved block reference](https://developer.hashicorp.com/terraform/language/block/moved)
- [Module refactoring](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)
