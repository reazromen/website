---
title: Terraform Policy Is Not Just Sentinel Rewritten in HCL
url: /posts/terraform-policy-hcl-is-not-just-sentinel-rewrite/index.html
date: '2026-03-01'
read_time: 8
excerpt: HashiCorp's 2026 Terraform Policy beta evaluates provider-aware infrastructure
  policies using HCL and a dedicated tfpolicy test workflow. It changes where platform
  teams can encode guardrails, but it is still beta.
topic: index
tags:
- terraform
- policy
- hcp-terraform
- hcl
draft: false
featured: false
language: en
eyebrow: Terraform 2026 · Terraform systems note
outputs:
- url: /posts/terraform-policy-hcl-is-not-just-sentinel-rewrite/index.html
  template: cms/templates/posts/posts--terraform-policy-hcl-is-not-just-sentinel-rewrite--index.tpl
  source: cms/templates/posts/posts--terraform-policy-hcl-is-not-just-sentinel-rewrite--index.json
---

Policy-as-code around Terraform has traditionally meant Sentinel in HashiCorp environments or OPA/Rego in broader platforms.

In 2026, HashiCorp is introducing Terraform Policy: an HCL-based policy framework integrated with Terraform providers and HCP Terraform.

## The language is familiar, the execution model is different

Policy files use HCL syntax, but they are not ordinary Terraform configuration. They define provider, resource and module policies evaluated against infrastructure data during HCP Terraform runs.

## Provider awareness is the interesting part

A policy can target resource types and their attributes using provider schemas rather than requiring every team to translate Terraform plan JSON into a separate generic policy model.

That can lower the barrier for Terraform practitioners who already understand HCL and provider resources.

## Policies have their own test lifecycle

The `tfpolicy` CLI validates and tests `.policy.hcl` files with `.policytest.hcl` cases. HashiCorp's current documentation requires Terraform 1.16 or later for the policy CLI workflow.

That makes policy behavior something that can be versioned and tested before enforcement.

## Enforcement can be scoped

HCP Terraform policy sets can target organizations, projects, workspaces, Stacks and tags depending on framework/support. Enforcement levels determine whether a violation warns or blocks.

## It is beta

HashiCorp repeatedly labels Terraform Policy beta and explicitly advises against using beta functionality in production environments. Stacks policy support has additional current limitations and version requirements.

That means the right 2026 posture is evaluation: test expressiveness, CI workflow, provider coverage and migration from existing Sentinel/OPA controls without assuming the framework is already the default production answer.

## The strategic change

Terraform is moving policy closer to the same provider-aware model practitioners use for infrastructure code. If the framework matures, platform teams may be able to express guardrails with less translation between IaC and policy languages.

## Sources and further reading

- [Terraform Policy overview](https://developer.hashicorp.com/terraform/policy)
- [Define Terraform policies](https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement/define-policies/terraform-policy)
- [Install tfpolicy CLI](https://developer.hashicorp.com/terraform/policy/install)
- [Policy enforcement for Stacks](https://developer.hashicorp.com/terraform/cloud-docs/stacks/policy-enforcement)
