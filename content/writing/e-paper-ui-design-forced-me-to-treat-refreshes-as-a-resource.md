---
title: E-Paper UI Design Forced Me to Treat Refreshes as a Resource
url: /posts/e-paper-ui-design-forced-me-to-treat-refreshes-as-a-resource.html
date: '2026-09-14'
read_time: 1
excerpt: 'A slow monochrome display changes interaction design: information hierarchy
  matters more than animation.'
topic: embedded-firmware
tags:
- e-paper
- ui
- partial-refresh
- embedded
draft: false
featured: false
language: en
eyebrow: 2026 Production Voice Systems · intermediate
outputs:
- url: /posts/e-paper-ui-design-forced-me-to-treat-refreshes-as-a-resource.html
  template: cms/templates/posts/posts--e-paper-ui-design-forced-me-to-treat-refreshes-as-a-resource.tpl
  source: cms/templates/posts/posts--e-paper-ui-design-forced-me-to-treat-refreshes-as-a-resource.json
---

E-paper changes the UI problem because the display is not a tiny LCD that happens to refresh slowly. Full updates are expensive, partial updates have constraints, and animation is usually the wrong instinct.

I started designing screens around state changes rather than frames. A contact list needs a clear selection marker. Incoming call, active call, mute, volume, Wi-Fi and battery each need a stable representation that can be updated with minimal screen area.

That pushed more responsibility into information hierarchy. The user should know what the rotary control will do before touching it. A volume change can update one region instead of redrawing the whole screen. Temporary states should disappear cleanly without leaving ghosting artifacts.

The limitation was useful. It removed decorative motion and forced the UI to communicate device state directly, which fits a focused voice product much better than a phone-like interface.
