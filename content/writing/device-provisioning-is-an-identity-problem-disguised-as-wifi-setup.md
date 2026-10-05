---
title: Device Provisioning Is an Identity Problem Disguised as Wi-Fi Setup
url: /posts/device-provisioning-is-an-identity-problem-disguised-as-wifi-setup.html
date: '2026-08-16'
read_time: 1
excerpt: Getting credentials onto a device is easy; binding the right device to the
  right backend identity is the security boundary.
topic: embedded-firmware
tags:
- provisioning
- identity
- wi-fi
- device-backend
draft: false
featured: false
language: en
eyebrow: 2024 Telecom and Embedded Notes · advanced
outputs:
- url: /posts/device-provisioning-is-an-identity-problem-disguised-as-wifi-setup.html
  template: cms/templates/posts/posts--device-provisioning-is-an-identity-problem-disguised-as-wifi-setup.tpl
  source: cms/templates/posts/posts--device-provisioning-is-an-identity-problem-disguised-as-wifi-setup.json
---

Provisioning initially looked like a screen where the user enters an SSID and password. That solves local connectivity and not much else.

A product device also needs an identity the backend can trust. The system has to distinguish a factory-fresh unit from a paired unit, prevent one user from claiming someone else's device, and decide what happens when ownership changes.

I separated local network configuration from device identity. Wi-Fi credentials get the unit online. A pairing credential or factory identity proves which physical unit is talking to the backend. The backend then issues the operational configuration appropriate for that device.

That split also made reset behavior clearer. Erasing Wi-Fi should not necessarily erase ownership. A factory reset should have a deliberate identity policy rather than deleting whatever happens to be in NVS. Provisioning became much easier once I treated it as lifecycle management instead of a setup wizard.
