---
title: 32x32 MIMO Made More Sense When I Stopped Counting Antennas
url: /posts/32x32-mimo-made-more-sense-when-i-stopped-counting-antennas.html
date: '2020-04-05'
read_time: 2
excerpt: Large antenna arrays are interesting because of beams, spatial layers and
  RF chains, not because the front panel contains a big number of elements.
topic: mobile-networks
tags:
- mimo
- 5g
- ran
- beamforming
draft: false
featured: false
language: en
eyebrow: 2023 Mobile and 5G Notes · advanced
outputs:
- url: /posts/32x32-mimo-made-more-sense-when-i-stopped-counting-antennas.html
  template: cms/templates/posts/posts--32x32-mimo-made-more-sense-when-i-stopped-counting-antennas.tpl
  source: cms/templates/posts/posts--32x32-mimo-made-more-sense-when-i-stopped-counting-antennas.json
---

The first time I saw a 32x32 MIMO specification I treated the number as a simple antenna count. That is an easy way to get lost. What matters operationally is how many RF chains, antenna elements, beams and spatial layers the radio can use, and those are related without being identical concepts.

A large active antenna unit contains many radiating elements arranged so their phases and amplitudes can be controlled. By adjusting those signals, the radio can shape energy in space instead of broadcasting the same pattern in every direction. That is the practical reason beamforming appears everywhere in modern RAN discussions. The array gives the system spatial control.

MIMO adds another dimension. If the radio channel supports it, multiple independent data layers can be transmitted at the same time. The number of physical elements can be much larger than the number of simultaneous user layers. Saying “32 antennas means 32 streams” is therefore wrong. The scheduler, channel conditions, UE capability and implementation all limit what is actually useful.

The RF side also changed how I thought about network troubleshooting. In IP networks a link is often treated as either up or down with counters describing quality. Radio adds geometry, reflections, interference, polarization and time-varying channel conditions. Two UEs connected to the same cell can have very different effective channels even at similar distances.

The useful mental model for me became: elements provide aperture, the radio controls weights, those weights create beams, and MIMO layers exploit independent spatial paths when the channel allows it. That is much more useful than memorizing marketing labels. It also explains why opening a massive-MIMO unit and counting visible radiators would tell only part of the story; a large fraction of the engineering is in the RF chain, calibration and baseband control behind them.
