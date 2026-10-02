---
title: Terraform for_each Keys Are Resource Identity, Not Loop Variables
url: /posts/terraform-for-each-keys-are-resource-identity/index.html
date: '2026-09-26'
read_time: 8
excerpt: The keys in for_each become part of resource addresses. Renaming a key can
  look like deleting one object and creating another even when the human thinks only
  a label changed.
topic: index
tags:
- terraform
- for-each
- identity
- resource-address
draft: false
featured: false
language: en
eyebrow: Terraform Resource Identity · Terraform systems note
outputs:
- url: /posts/terraform-for-each-keys-are-resource-identity/index.html
  template: cms/templates/posts/posts--terraform-for-each-keys-are-resource-identity--index.tpl
  source: cms/templates/posts/posts--terraform-for-each-keys-are-resource-identity--index.json
---

`for_each` looks like iteration, but Terraform uses its keys as durable instance identity.

```
aws_iam_user.user["alice"]
aws_iam_user.user["bob"]
```

## Key changes are address changes

If `alice` becomes `a.smith`, Terraform sees one old instance removed and one new instance introduced unless a moved mapping says they are the same remote object.

## Choose semantic stable keys

Good keys survive cosmetic edits: canonical service names, immutable account IDs, fixed environment names. Display labels and list positions are often poor long-lived identity.

## Keys must be known before apply

Terraform needs the graph before remote operations, so `for_each` cannot depend on keys that are only known after another resource is created.

## Sensitive keys are prohibited

Keys appear in resource addresses and normal UI output, so Terraform will not accept sensitive values as instance keys.

Design `for_each` keys like database primary keys. Once they exist in state, renaming them is a migration.

## Sources and further reading

- [for\_each meta-argument](https://developer.hashicorp.com/terraform/language/meta-arguments/for_each)
- [moved block](https://developer.hashicorp.com/terraform/language/block/moved)
