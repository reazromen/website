---
title: "lsof and /proc: Find Which Process Owns a File, Socket, or Resource"
draft: false
date: '2024-11-16'
language: en
url: /posts/linux-lsof-and-proc-filesystem-process-debugging.html
read_time: 2
excerpt: >-
  `lsof`, `/proc`, and `ss` help identify which process owns a file descriptor, socket, or other resource.
eyebrow: "Perspectives · Linux Tools"
tags: ["Linux","lsof"]
---

`lsof`, `/proc`, and `ss` help identify which process owns a file descriptor, socket, or other resource. If a port appears busy, inspect listeners with `ss -ltnp`. If disk space remains allocated after deleting a large file, look for a deleted-but-open descriptor; blocks remain in use until the process closes it.

`/proc/PID` exposes command-line details, descriptors, status, and memory information, subject to permissions and container boundaries. PIDs can be reused, so verify process identity before acting. Resource inspection should lead to an explanation, not an automatic kill command. Identify the owning component and choose the least disruptive fix.
