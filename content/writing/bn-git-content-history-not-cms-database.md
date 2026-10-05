---
title: What Git History Adds to a Blog
date: '2024-01-12'
draft: false
language: en
url: /posts/bn-git-content-history-not-cms-database.html
topic: web-control-plane
tags:
- git
- publishing
featured: false
read_time: 2
excerpt: >-
  In a Git-backed blog, content files and their change history live in the same system.
  You can trace when a sentence changed, when metadata moved, and which edits can be
  reverted. But Git alone does not provide the entire publishing experience.
editorial_batch: 20261003-100-niches
---

In a Git-backed blog, content files and their change history live in the same system. You can trace when a sentence changed, when metadata moved, and which edits can be reverted. But Git alone does not provide the entire publishing experience.

A CMS may give an editor a simple form and convert that form into the correct file. A build then turns the file into a public page. Preserving history and publishing a page are two separate stages. A successful Git save does not prove that a reader can already see the new page.

If a bad tag or broken reference fails validation, the previous published version may remain intact. That is why build results matter. A successful save button is not sufficient evidence of successful publication.

For me, the advantage of this model is that changes become readable history. But the user still needs to know which stage is happening. The power of history becomes useful only when the delivery path is understandable too.

Source: [official reference](https://git-scm.com/docs/git-log).
