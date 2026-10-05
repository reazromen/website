---
title: Moving Terraform from count to for_each Is a State Migration
url: /posts/terraform-count-to-for-each-is-state-migration/index.html
date: '2025-03-26'
read_time: 8
excerpt: count identities are numeric indexes; for_each identities are keys. Switching
  syntax without mapping addresses can make unchanged infrastructure look like replacement
  work.
topic: index
tags:
- terraform
- count
- for-each
- migration
draft: false
featured: false
language: en
eyebrow: Terraform Resource Identity · Terraform systems note
outputs:
- url: /posts/terraform-count-to-for-each-is-state-migration/index.html
  template: cms/templates/posts/posts--terraform-count-to-for-each-is-state-migration--index.tpl
  source: cms/templates/posts/posts--terraform-count-to-for-each-is-state-migration--index.json
---

Converting `count` to `for_each` is often a good module improvement, but it changes every resource address.

```
# before
aws_instance.web[0]

# after
aws_instance.web["api"]
```

## Why count becomes fragile

If a list drives `count`, deleting an item in the middle can shift later indexes. Position is not always a stable identity.

## The conversion needs a mapping

Moved blocks can map each old index to the new stable key so the same remote object stays managed.

```
moved {
  from = aws_instance.web[0]
  to   = aws_instance.web["api"]
}
```

## Verify the old mapping first

Do not assume list order if the configuration has changed historically. Inspect state and real identifiers so index-to-key mapping is correct.

## Use the plan as migration proof

The desired result is address moves and intentional updates, not a wave of replacements. Changing meta-arguments changes identity, so treat it as state migration.

## Sources and further reading

- [for\_each meta-argument](https://developer.hashicorp.com/terraform/language/meta-arguments/for_each)
- [Module refactoring](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)
