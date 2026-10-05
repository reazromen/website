---
title: IPX4 Has to Be Designed Around Openings, Not Added at Certification
url: /posts/ipx4-has-to-be-designed-around-openings-not-added-at-certification.html
date: '2022-05-14'
read_time: 1
excerpt: Speaker, microphone, buttons and battery access all create splash-resistance
  paths.
topic: loup-engineering
tags:
- ipx4
- mechanical
- validation
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Factory & Production Validation · advanced'
outputs:
- url: /posts/ipx4-has-to-be-designed-around-openings-not-added-at-certification.html
  template: cms/templates/posts/posts--ipx4-has-to-be-designed-around-openings-not-added-at-certification.tpl
  source: cms/templates/posts/posts--ipx4-has-to-be-designed-around-openings-not-added-at-certification.json
---

I reached IPX4 Has to Be Designed Around Openings, Not Added at Certification through a repeatable lab problem rather than a design slogan. LOUP targets IPX4 while still using acoustic apertures, side controls and a serviceable rear battery plate.

That means membranes, gaskets, drainage, button geometry and screw compression have to be considered during enclosure design. Passing a late splash test is not enough if normal service can reinstall the back plate incorrectly and lose the seal.

The useful debugging step was separating signal path, state and timing instead of modifying all three and then guessing which change mattered. Evidence marker: `ipx4-target`.

Environmental ratings are architecture constraints. They belong in mechanical design and service procedure before compliance testing. That distinction also makes regressions cheaper to isolate when hardware, firmware and infrastructure are changing in parallel.

## Project evidence

LOUP engineering marker: `ipx4-target`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
