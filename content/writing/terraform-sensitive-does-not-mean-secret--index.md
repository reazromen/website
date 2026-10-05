---
title: Terraform sensitive Does Not Mean Secret
url: /posts/terraform-sensitive-does-not-mean-secret/index.html
date: '2026-05-12'
read_time: 8
excerpt: Marking a value sensitive redacts normal CLI and UI output. It does not remove
  that value from Terraform state or saved plan files.
topic: index
tags:
- terraform
- sensitive
- state
- secrets
draft: false
featured: false
language: en
eyebrow: Terraform Security · Terraform systems note
outputs:
- url: /posts/terraform-sensitive-does-not-mean-secret/index.html
  template: cms/templates/posts/posts--terraform-sensitive-does-not-mean-secret--index.tpl
  source: cms/templates/posts/posts--terraform-sensitive-does-not-mean-secret--index.json
---

The word `sensitive` sounds stronger than the behavior it implements. Terraform uses the flag primarily to reduce accidental disclosure in normal human-facing output.

## Redaction is presentation control

A sensitive variable or output is hidden in standard plan and apply rendering. Expressions derived from sensitive values usually inherit the marking, which prevents routine terminal and CI output from displaying them.

## The value can still be in state

HashiCorp's documentation is explicit: sensitive values remain in state and saved plan files unless a newer ephemeral or write-only mechanism prevents persistence. Anyone who can read state may therefore be able to retrieve the value.

## Automation can reveal it

Machine-readable or raw output is designed for tools, not visual redaction. Some JSON and raw-output workflows can expose values that normal display hides.

## Backend permissions are security permissions

If state contains credentials, access to the backend is effectively access to those credentials. Encryption at rest protects storage media but does not replace authorization.

## Use the right property

```
sensitive = hide from routine display
ephemeral = omit from plan/state where allowed
write-only = pass to a managed resource without persisting
```

Those are different security properties. Treating `sensitive` as complete secret management leaves the most important artifact—the state—outside the threat model.

## Sources and further reading

- [Terraform sensitive data management](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)
- [Terraform outputs](https://developer.hashicorp.com/terraform/language/values/outputs)
