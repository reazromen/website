---
title: "96 Tests, a Live Route Check, and an Authenticated Browser: Verifying an Epistolary Feature"
url: /posts/romance-studio-epistolary-testing-verification.html
date: '2026-10-19'
read_time: 4
excerpt: How I verified a new Romance Studio feature with focused regression tests, production health checks, and authenticated browser automation.
topic: web-control-plane
tags:
- testing
- regression
- release-engineering
- security
draft: false
featured: false
language: en
eyebrow: "VERIFICATION · PRODUCTION ENGINEERING"
---

## Use more than one kind of evidence

For a route-level feature, I wanted evidence from the code, test suite, running service, and authenticated browser. Each answers a different question: does the code compile, do expected behaviours hold, is production healthy, and can a signed-in user see the page?

## Code and regression checks

Python compilation passed and `git diff --check` found no whitespace errors. The focused HTTP tests passed all 10 cases. The full isolated regression suite completed with **18 modules, 96 tests, and zero failures**.

The added tests cover navigation and page rendering, workspace-scoped draft creation, CSRF rejection, and preventing a profile from another workspace from being used. These are behavioural checks, not just assertions that the route returns HTML.

## Production health and route checks

The running Romance Studio container reported healthy. The `/health` endpoint returned HTTP 200, and `/ready` confirmed the database was ready with the expected schema. The new `/epistolary` route returned HTTP 200 with the expected form and save-action text; the stylesheet also returned HTTP 200.

## Authenticated browser verification

I opened the application with an authenticated browser profile and verified that the page loaded as the application rather than a login screen. The Epistolary navigation, profile selector, form fields, save button, and recent-drafts section were visible, with no visible browser errors.

I deliberately did not submit a test letter through production. That avoided creating artificial user content while still verifying that the form was present. Save behaviour was exercised in the isolated regression tests instead.

## What this proves—and what it does not

The checks support that the route is deployed, the application is healthy, the authenticated interface renders, and tested draft/security behaviours pass. They are not a substitute for separate visual design sign-off or a production data-creation test.

The release lesson is straightforward: verify the contract at every boundary, and be precise about what each check demonstrates.
