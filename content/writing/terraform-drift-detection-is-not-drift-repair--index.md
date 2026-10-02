---
title: Terraform Drift Detection Is Not the Same Thing as Drift Repair
url: /posts/terraform-drift-detection-is-not-drift-repair/index.html
date: '2026-09-26'
read_time: 8
excerpt: A normal plan refreshes reality before calculating changes. Refresh-only
  mode updates Terraform's recorded view without changing infrastructure. The real
  decision is which side is authoritative.
topic: index
tags:
- terraform
- drift
- refresh-only
- plan
draft: false
featured: false
language: en
eyebrow: Terraform State & Drift · Terraform systems note
outputs:
- url: /posts/terraform-drift-detection-is-not-drift-repair/index.html
  template: cms/templates/posts/posts--terraform-drift-detection-is-not-drift-repair--index.tpl
  source: cms/templates/posts/posts--terraform-drift-detection-is-not-drift-repair--index.json
---

Drift means configuration, state and remote reality disagree. Detecting that difference is easier than deciding how to resolve it.

## Normal plan usually reconciles toward code

Terraform refreshes managed objects before planning and then proposes changes that make remote infrastructure match configuration.

## Refresh-only reconciles state toward reality

`terraform plan -refresh-only` shows state changes Terraform would record from the remote system without proposing remote modifications. `apply -refresh-only` commits that view.

This is useful when an external change was intentional and Terraform should accept it.

## The old terraform refresh command is risky

HashiCorp deprecates the standalone command because it effectively applies state refresh without giving you the same review workflow. Wrong credentials can make objects appear missing and update state in dangerous ways.

## Repeated drift is an ownership problem

If an autoscaler or managed service legitimately owns one attribute, the solution may be an explicit ownership boundary rather than endless reconciliation. If humans keep editing production manually, the solution is process and access control.

A drift workflow should answer: what changed, who owns that field, and whether code or remote reality should win.

## Sources and further reading

- [terraform refresh and refresh-only](https://developer.hashicorp.com/terraform/cli/commands/refresh)
- [terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
