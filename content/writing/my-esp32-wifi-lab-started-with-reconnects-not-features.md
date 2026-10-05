---
title: My ESP32 Wi-Fi Lab Started with Reconnects, Not Features
url: /posts/my-esp32-wifi-lab-started-with-reconnects-not-features.html
date: '2023-01-22'
read_time: 1
excerpt: An embedded network client is only useful if it survives AP loss, DHCP renewal
  and reconnect loops without wedging the application.
topic: embedded-firmware
tags:
- esp32
- wi-fi
- embedded
- reconnect
draft: false
featured: false
language: en
eyebrow: 2024 Telecom and Embedded Notes · intermediate
outputs:
- url: /posts/my-esp32-wifi-lab-started-with-reconnects-not-features.html
  template: cms/templates/posts/posts--my-esp32-wifi-lab-started-with-reconnects-not-features.tpl
  source: cms/templates/posts/posts--my-esp32-wifi-lab-started-with-reconnects-not-features.json
---

The first useful ESP32 Wi-Fi test was not a web page or sensor demo. It was turning the access point off and watching what the firmware did.

A desktop operating system hides a lot of network recovery. Embedded firmware has to decide how to handle disconnect events, authentication failures, DHCP loss and repeated reconnect attempts. A loop that retries immediately forever can consume CPU, flood logs or starve other tasks.

I moved connection state into an explicit state machine. Connected, disconnected, retry waiting and provisioning became separate states. Backoff prevented tight retry loops. Application tasks were not allowed to assume an IP address simply because the radio interface existed.

Then I tested ugly cases: wrong password, AP reboot, weak signal, DHCP delay and network return after several minutes. Those tests taught me more than the happy-path connection code. A device that connects once is a demo. A device that recovers predictably is the beginning of a product.
