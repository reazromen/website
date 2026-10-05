---
title: Module-Level depends_on Can Make Terraform's Graph Much Bigger Than You Think
url: /posts/terraform-module-depends-on-expands-graph/index.html
date: '2022-08-20'
read_time: 8
excerpt: A module-level depends_on creates a broad ordering relationship between groups
  of resources. It can make plans more conservative and hide the specific dependency
  the system actually has.
topic: index
tags:
- terraform
- depends-on
- modules
- graph
draft: false
featured: false
language: en
eyebrow: Terraform Dependency Graph · Terraform systems note
outputs:
- url: /posts/terraform-module-depends-on-expands-graph/index.html
  template: cms/templates/posts/posts--terraform-module-depends-on-expands-graph--index.tpl
  source: cms/templates/posts/posts--terraform-module-depends-on-expands-graph--index.json
---

Terraform works best when dependencies come from actual data flow. If one resource reads another resource's attribute, the graph edge is precise and automatic.

## Module-level depends\_on is broad

When an entire module depends on another module, Terraform must conservatively order much more work than a single attribute reference would require.

That can reduce parallelism and cause downstream values to stay unknown longer during planning.

## Unknowns can spread

Broad dependencies make Terraform less certain about when values become available. A plan can fill with `known after apply` values even though only one internal object needed ordering.

## Prefer direct references

If an application module needs a subnet ID, pass the subnet ID. That tells Terraform exactly what the consumer depends on.

## Use depends\_on for hidden relationships

It is appropriate when the dependency exists operationally but is not represented by a value reference—such as policy propagation or an external side effect that must complete first.

The graph should mirror the real system as precisely as possible. Overly broad edges are safer than missing edges, but they are still architectural debt.

## Sources and further reading

- [depends\_on meta-argument](https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on)
- [Terraform apply graph execution](https://developer.hashicorp.com/terraform/tutorials/cli/apply)
