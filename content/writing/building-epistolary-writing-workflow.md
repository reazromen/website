---
title: "From a Missing Route to a Working Writing Space: Building Epistolary into Romance Studio"
url: /posts/building-epistolary-writing-workflow.html
date: '2026-10-19'
read_time: 4
excerpt: A practical look at integrating a letter-writing workspace into an existing content platform with draft handling, CSRF protection, and workspace isolation.
topic: web-control-plane
tags:
- content-system
- security
- testing
- regression
draft: false
featured: false
language: en
eyebrow: "IMPLEMENTATION · CONTENT WORKFLOW"
---

## Define the feature boundary

The goal was a dedicated place to compose correspondence inside Romance Studio. The page needed to respect the active workspace and profile, make recent Epistolary drafts easy to revisit, and hand saved content into the existing Content workflow.

The form captures a title, sender, recipient, date, and letter body. Writing prompts support composition, but they do not change the publishing lifecycle: saving a letter creates a draft.

## Reuse the existing content lifecycle

Rather than creating a parallel storage or publishing mechanism, the implementation records the entry with `source="epistolary"`, `status="draft"`, and no scheduled publication time. After saving, the user is redirected to the existing content detail view.

This keeps the new experience discoverable while preserving the established review path. It also means the feature does not silently publish personal correspondence just because the user pressed Save.

## Security and validation belong on the server

The POST handler validates required fields and input limits, checks the CSRF token, enforces workspace/profile access, and follows the existing workspace identity rules. A duplicate fingerprint check helps avoid accidental duplicate drafts. These checks belong on the server; client-side validation alone is not an authorization boundary.

Workspace isolation received a dedicated regression test. A profile belonging to another workspace must not be accepted simply because its identifier was submitted in a form.

## Regression coverage

The focused HTTP test module passed 10 tests. The complete isolated regression suite passed **18 modules and 96 tests with zero failures**. The checks cover page/navigation rendering, saving a workspace-scoped unpublished draft, CSRF enforcement, and rejection of cross-workspace profile access.

## Implementation takeaway

A production-ready content feature needs a data contract, explicit publication state, server-side authorization, duplicate handling, and tests for negative cases. Those details make the workflow predictable and maintainable.
