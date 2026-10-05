---
title: LoRa Radio and the LoRaWAN Network Are Different Layers
date: '2022-04-24'
draft: false
language: en
url: /posts/bn-lora-lorawan-stack-boundary.html
topic: radio-iot
tags:
- lora
- protocols
featured: false
read_time: 2
excerpt: >-
  The name LoRa is often used as if it describes an entire network. But the way information
  is represented over the radio and the rules for operating a multi-device network are
  different layers. LoRa and LoRaWAN are a useful example of that boundary.
editorial_batch: 20261003-100-niches
---

The name LoRa is often used as if it describes an entire network. But the way information is represented over the radio and the rules for operating a multi-device network are different layers. LoRa and LoRaWAN are a useful example of that boundary.

Sending a direct message between two devices is not the same requirement as building a network with gateways, identity, and servers. Success at the first does not imply every feature of the second. The larger stack is also not mandatory for every small use case.

Start by writing down where the data must travel. How many devices are involved? How often do they transmit? Is a response required? How is identity verified? Those questions narrow the architecture much more effectively than a distance claim alone.

In radio projects, I prefer to name the layers clearly. Physical communication, network rules, and application behavior should not be blended together. Once the layers are explicit, both capabilities and missing features become easier to see.

Source: [official reference](https://resources.lora-alliance.org/infographic/lora-and-lorawan).
