---
title: "Linux Shell Pipelines for Troubleshooting: Small Tools, Clear Evidence"
draft: false
date: '2021-03-08'
language: en
url: /posts/shell-pipelines-for-reliable-linux-troubleshooting.html
read_time: 2
excerpt: >-
  Small Linux tools work well together when each command answers a focused question.
eyebrow: "Perspectives · Linux Tools"
tags: ["linux","shell","operations"]
---

Small Linux tools work well together when each command answers a focused question. Use `journalctl` for service logs, `ss` for sockets, `df` and `du` for storage, and `ps` for process state. Add filters only after confirming the original output contains expected evidence. Quote variables and paths, and prefer machine-readable output over parsing unstable human-oriented text.

A pipeline can hide an earlier command’s failure unless its status is propagated. Preserve exit codes, send diagnostics to standard error, and inspect matched targets before destructive actions. Turn successful investigations into runbook checks with expected output, required privileges, and limitations. Clear commands that preserve evidence are better than clever one-liners nobody can safely audit.
