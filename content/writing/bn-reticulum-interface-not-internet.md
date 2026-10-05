---
title: A Reticulum Interface Is Not the Same Thing as the Internet
date: '2023-01-24'
draft: false
language: en
url: /posts/bn-reticulum-interface-not-internet.html
topic: lora-reticulum
tags:
- mesh
- protocols
featured: false
read_time: 2
excerpt: >-
  One of Reticulum's interesting properties is that communication does not have to be tied
  to a single medium. But adding an interface does not automatically give every application
  a conventional Internet connection.
editorial_batch: 20261003-100-niches
---

One of Reticulum's interesting properties is that communication does not have to be tied to a single medium. But adding an interface does not automatically give every application a conventional Internet connection.

A network stack provides rules for moving information. Applications still need a way to use those rules. An existing web application and a purpose-built messaging application do not necessarily have the same requirements just because both use a network.

Start by writing down the communication you actually need: small messages, files, sensor observations, or something else. Then compare that workload with the bandwidth and latency of the available medium. On constrained links, application design can matter as much as transport choice.

Designing an independent communication system does not require carrying every habit of the conventional Internet into it. Reducing the problem to the work that truly matters can make the system more practical. Understanding constraints does not reduce possibility; it makes possibility usable.

Source: [official reference](https://reticulum.network/manual/whatis.html).
