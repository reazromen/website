---
title: A Saved Terraform Plan Is a Deployment Artifact, Not Just Pretty Diff Output
url: /posts/terraform-saved-plan-is-deployment-artifact/index.html
date: '2026-09-26'
read_time: 8
excerpt: A saved plan captures the exact actions Terraform intends to apply. In CI/CD
  it becomes the handoff between review and execution—and a sensitive artifact that
  must be protected.
topic: index
tags:
- terraform
- plan
- ci-cd
- approval
draft: false
featured: false
language: en
eyebrow: Terraform CI/CD · Terraform systems note
outputs:
- url: /posts/terraform-saved-plan-is-deployment-artifact/index.html
  template: cms/templates/posts/posts--terraform-saved-plan-is-deployment-artifact--index.tpl
  source: cms/templates/posts/posts--terraform-saved-plan-is-deployment-artifact--index.json
---

A common pipeline runs `terraform plan` in one job, shows the text to a reviewer, and later runs a fresh `terraform apply`. Those two commands can produce different plans.

## Speculative plans are for review

An unsaved plan describes what Terraform would do at that moment. Remote infrastructure can drift, input values can change, provider versions can differ, or a different commit can reach the apply stage later.

## -out creates the executable handoff

`terraform plan -out=tfplan` writes a saved plan. Applying that file executes the operations captured in the plan rather than calculating a new one. This is the cleanest basis for “review exactly what we will execute.”

## The plan file is sensitive

HashiCorp warns not to commit saved plans—binary or JSON—to version control because they can contain cleartext values needed by providers. CI artifact permissions, retention and encryption therefore matter.

## Approval should bind to commit and plan

A strong pipeline records source revision, environment inputs, provider lock file and saved plan together. If code changes after approval, regenerate the plan.

## Saved-plan apply does not prompt

Passing a plan file to `terraform apply` skips the normal confirmation prompt. Your pipeline approval is therefore the human safety gate.

A saved plan is best treated like a release artifact: immutable, short-lived, protected and tied to one deployment decision.

## Sources and further reading

- [Create a Terraform plan](https://developer.hashicorp.com/terraform/tutorials/cli/plan)
- [terraform apply](https://developer.hashicorp.com/terraform/cli/commands/apply)
