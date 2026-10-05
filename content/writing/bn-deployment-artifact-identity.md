---
title: Preserve Artifact Identity Through Deployment
date: '2022-04-11'
draft: false
language: en
url: /posts/bn-deployment-artifact-identity.html
topic: production-engineering
tags:
- deployment
- provenance
featured: false
read_time: 2
excerpt: >-
  Incident investigation becomes easier when a release can answer which source produced
  which artifact. A label such as latest is not enough. Latest changes with time; a commit
  or artifact identity does not.
editorial_batch: 20261003-100-niches
---

Incident investigation becomes easier when a release can answer which source produced which artifact. A label such as *latest* is not enough. Latest changes with time; a commit or artifact identity does not.

Suppose two people publish different builds under the same filename. The filename alone cannot tell you what a user actually received. Keeping the source identity—and, where useful, an artifact hash—alongside the deployed build makes that relationship traceable.

The same identity should connect testing to release. Was the artifact that passed testing the one that was actually deployed? During rollback, which exact identity are you returning to? Rebuilding a new file under an old name is not necessarily the same as restoring the previous artifact.

I think of release history less as a narrative and more as a chain of traceable relationships. When source, build, test, and deployment follow the same identity, less of the incident has to be reconstructed from guesswork.

Source: [official reference](https://git-scm.com/docs/git-rev-parse).
