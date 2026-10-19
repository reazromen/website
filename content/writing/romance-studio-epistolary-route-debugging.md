---
title: "The Missing Page That Wasn't a Frontend Bug: Debugging Romance Studio's Epistolary Route"
url: /posts/romance-studio-epistolary-route-debugging.html
date: '2026-10-19'
read_time: 4
excerpt: How I traced a broken Romance Studio Epistolary URL to a missing backend route, then built and verified a dedicated writing page.
topic: web-control-plane
tags:
- debugging
- routing
- content-system
- http
draft: false
featured: false
language: en
eyebrow: "CASE STUDY · ROUTE DEBUGGING"
---

## Start with the request, not the assumption

When a route does not behave as expected, it is tempting to begin with CSS, client-side navigation, or a browser-console error. I first wanted to establish a simpler fact: did the application actually have a route that could serve `/epistolary`?

I checked the production response and the application structure. The route was missing from the backend route definitions, navigation configuration, and page templates. There was no dedicated Epistolary view for the browser to render.

## Why that distinction mattered

A frontend can only render a route the application exposes or explicitly handles. If the backend does not register the path, styling changes will not create the missing request handler. A fallback can make the symptom look like a frontend issue, but it does not implement the intended feature.

The practical debugging path is URL, router, handler, template, and data access. Following that chain distinguishes a missing route from a rendering defect or failed database query.

## The fix was a real page, not a redirect

I added a dedicated Epistolary route and page to Romance Studio. The navigation now points to it, and the page uses the active workspace and profile context. It presents a letter-writing form and recent Epistolary drafts instead of sending users to an unrelated section.

The save action connects to the existing Content workflow. A letter is stored as a draft with the source marked `epistolary`; it is not automatically published or scheduled.

## What I would repeat next time

- Confirm the HTTP response before editing presentation code.
- Check route registration, navigation, template, and data access as one feature boundary.
- Reuse the existing content lifecycle where it fits.
- Verify the deployed route and the authenticated user-visible page.

The useful result was not merely that the URL started working. It was identifying the layer that was missing and implementing the feature there.
