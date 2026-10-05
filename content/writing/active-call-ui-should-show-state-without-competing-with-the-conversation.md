---
title: Active Call UI Should Show State Without Competing with the Conversation
url: /posts/active-call-ui-should-show-state-without-competing-with-the-conversation.html
date: '2026-03-03'
read_time: 1
excerpt: During a call, the screen is for confirmation and control feedback rather
  than continuous content.
topic: loup-engineering
tags:
- active-call
- ui
- voice-device
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: E-Paper UI & Controls · advanced'
outputs:
- url: /posts/active-call-ui-should-show-state-without-competing-with-the-conversation.html
  template: cms/templates/posts/posts--active-call-ui-should-show-state-without-competing-with-the-conversation.tpl
  source: cms/templates/posts/posts--active-call-ui-should-show-state-without-competing-with-the-conversation.json
---

The acceptance condition for Active Call UI Should Show State Without Competing with the Conversation only became clear after the system was split into boundaries. LOUP active-call state needs only the information that helps the user understand who is connected and what controls are active.

Contact name, call state, mute status, volume feedback and basic connectivity can fit in stable regions. Avoiding animation reduces refresh noise and leaves physical controls in charge of immediate actions.

The design became clearer when configuration, runtime state and recovery behaviour were specified separately instead of being implied by implementation details. Evidence marker: `active-call-ui`.

A voice-first interface should become quieter after the call connects, not busier. Once that contract is written down, firmware and server changes can be reviewed against the same expectation instead of relying on memory.

## Project evidence

LOUP engineering marker: `active-call-ui`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
