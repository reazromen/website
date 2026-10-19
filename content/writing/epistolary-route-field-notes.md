---
title: Four Field Notes from the Romance Studio Epistolary Implementation
url: /notes/epistolary-route-field-notes.html
date: '2026-10-19'
read_time: 2
excerpt: Four concise engineering notes on the missing route, draft lifecycle, security boundaries, and production verification of Romance Studio's Epistolary feature.
topic: web-control-plane
tags:
- debugging
- content-system
- testing
- regression
draft: false
featured: false
language: en
eyebrow: "FIELD NOTES · CONTENT PLATFORM"
---

## 01. Root cause: the route did not exist

The failure was not solved by changing CSS. The backend route, navigation entry, and dedicated template were missing, so the fix required a real Epistolary page.

## 02. Implementation: save as a draft

The page writes through the existing Content workflow with `source=epistolary` and `status=draft`. Saving does not auto-publish or schedule correspondence.

## 03. Security and regression coverage

Server-side validation, CSRF checks, workspace/profile authorization, and duplicate detection protect the save path. The focused suite passed 10 tests; the full isolated suite passed 18 modules and 96 tests with zero failures.

## 04. Deployment verification

The route and stylesheet returned HTTP 200, health/readiness checks passed, and an authenticated browser showed the form and recent-drafts section. No test letter was submitted to production.

## Read the full case studies

- [The Missing Page That Wasn't a Frontend Bug](/posts/romance-studio-epistolary-route-debugging.html)
- [Building Epistolary into Romance Studio](/posts/building-epistolary-writing-workflow.html)
- [Verifying an Epistolary Feature](/posts/romance-studio-epistolary-testing-verification.html)
