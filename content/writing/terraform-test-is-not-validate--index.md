---
title: terraform test Is Not terraform validate — and It Can Create Real Infrastructure
url: /posts/terraform-test-is-not-validate/index.html
date: '2026-09-26'
read_time: 8
excerpt: validate checks syntax and internal consistency. terraform test can run plan/apply
  test cases and assertions, including real provider operations, so it belongs in
  a different CI risk class.
topic: index
tags:
- terraform
- terraform-test
- validate
- testing
draft: false
featured: false
language: en
eyebrow: Terraform Testing · Terraform systems note
outputs:
- url: /posts/terraform-test-is-not-validate/index.html
  template: cms/templates/posts/posts--terraform-test-is-not-validate--index.tpl
  source: cms/templates/posts/posts--terraform-test-is-not-validate--index.json
---

Terraform now has enough validation features that “we validate in CI” is ambiguous.

## validate checks configuration consistency

`terraform validate` verifies syntax, types and internal consistency without testing a specific remote environment. It is cheap and appropriate for routine module checks.

## plan adds environment context

A plan includes variables, state and provider reads for a target environment. It answers what would change here.

## terraform test executes test scenarios

`terraform test` loads `.tftest.hcl` files, runs plan or apply operations, evaluates assertions and can provision actual infrastructure. HashiCorp explicitly warns that tests can create billable resources.

## Tests and validations express different things

Use validations for invariants that must always be true when the module is consumed. Use tests to exercise behaviors under chosen inputs, mocks or integration environments.

## Cleanup belongs in the test design

Integration tests need temporary accounts/projects, deterministic destroy behavior and budget controls. A failed assertion should not leave expensive infrastructure behind.

## Layer confidence

```
fmt
 -> validate
 -> terraform test
 -> target-environment plan
 -> policy/approval
 -> apply
```

Infrastructure testing is safer when each tool answers one clear question instead of using the heaviest possible command for everything.

## Sources and further reading

- [Terraform testing overview](https://developer.hashicorp.com/terraform/cli/test)
- [terraform test command](https://developer.hashicorp.com/terraform/cli/commands/test)
- [terraform validate](https://developer.hashicorp.com/terraform/cli/commands/validate)
