---
title: "DTMF: The Sound of a Button and the Event of a Button"
date: '2025-01-27'
draft: false
language: en
url: /posts/bn-dtmf-button-and-event.html
topic: telecom-voip
tags:
- sip
- audio
featured: false
read_time: 2
excerpt: >-
  Pressing a phone key is meant to trigger an action: enter a menu, select an option, or
  confirm information. In a phone system, however, that action may travel as an audible
  tone or as a separate media event. To the user it is the same button; to the system
  they are different paths.
editorial_batch: 20261003-100-niches
---

Pressing a phone key is meant to trigger an action: enter a menu, select an option, or confirm information. In a phone system, however, that action may travel as an audible tone or as a separate media event. To the user it is the same button; to the system they are different paths. That is why a caller may hear the tone while the IVR fails to recognize the digit.

In-band DTMF travels inside the audio. Compression, level changes, and transformations along the media path can then affect detection. Telephone-event signaling carries the digit as a separate representation, but both sides still have to agree on that method. A technique that works toward one endpoint or trunk should not be assumed to work identically everywhere.

Suppose the caller presses 2 and the menu does not respond. The first question should be what the phone actually sent. Then inspect what the PBX received, what it forwarded toward the trunk, and what the IVR expects. Simply toggling a configuration option and declaring success does not reveal which part of the path changed. Event duration and termination are part of the signal too.

This small problem contains a larger lesson. The same user action can have several protocol representations. Debugging requires translating from the user's language into the packet-level representation. Do not test only whether a tone is audible; test whether the action the button was supposed to trigger actually happened. Communication success often exists outside the audio itself.

Source: [official reference](https://www.rfc-editor.org/rfc/rfc4733.html).
