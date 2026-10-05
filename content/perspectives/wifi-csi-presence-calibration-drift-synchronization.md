---
title: Wi-Fi CSI Presence Detection Fails First at Calibration, Drift, and Synchronization
url: /posts/wifi-csi-presence-calibration-drift-synchronization.html
date: '2024-03-24'
read_time: 9
excerpt: CSI is extremely sensitive to the radio channel—which is why it can sense
  motion and why uncontrolled rooms, clocks, channels, furniture, fans, and hardware
  differences can swamp a naive detector.
topic: ''
tags:
- wifi-csi
- esp32
- presence
- signal-processing
draft: false
featured: false
language: en
eyebrow: RF Sensing · systems note
outputs:
- url: /posts/wifi-csi-presence-calibration-drift-synchronization.html
  template: cms/templates/posts/posts--wifi-csi-presence-calibration-drift-synchronization.tpl
  source: cms/templates/posts/posts--wifi-csi-presence-calibration-drift-synchronization.json
---

Wi-Fi CSI demos are visually convincing.

A person walks through the room and subcarrier amplitudes move. A classifier shows “motion.” A graph looks almost like radar.

The dangerous conclusion is that sensitivity automatically becomes reliable presence detection.

CSI is useful precisely because the wireless channel changes with the environment. Production sensing fails when the system cannot distinguish the change it cares about from all the other changes the channel experiences.

## The baseline is a model, not a number[#](#the-baseline-is-a-model-not-a-number)

A naive detector often calculates a baseline in an empty room and treats deviation from that baseline as motion.

But the baseline moves with temperature, device clock behavior, access-point rate adaptation, channel changes, automatic gain, furniture, doors, fans, other people outside the target room, and radio interference.

So “calibrated once” is usually not enough.

You need a policy for slow baseline adaptation without teaching the system that a stationary human is the new empty room.

## Motion and occupancy are different signals[#](#motion-and-occupancy-are-different-signals)

Walking creates large temporal changes and is comparatively easy.

A seated person may produce only subtle breathing or posture changes. A fan may create persistent multipath variation larger than those micro-motions.

If the classifier is tuned for motion energy, it can report an empty room once the person sits still.

Presence requires temporal features and state beyond a threshold on “motion dB.”

## Phase is powerful and annoying[#](#phase-is-powerful-and-annoying)

CSI phase can encode fine path changes, but raw phase is affected by synchronization offsets, carrier-frequency offset, sampling-frequency offset, packet detection delay, and hardware-specific effects.

That is why many CSI pipelines perform phase sanitization, detrending, reference subtraction, or focus more heavily on amplitude-derived features.

Using phase without understanding those offsets can produce a beautiful graph of your radio clocks.

## Sampling rate has to be measured, not assumed[#](#sampling-rate-has-to-be-measured-not-assumed)

If feature extraction assumes 100 packets per second while the collector is actually producing 10 irregular samples per second, frequency-domain and temporal windows stop meaning what you think they mean.

Always timestamp packets and compute the observed sample interval distribution.

Then design filters/window sizes in seconds, not just “N samples.”

## Multiple boards create a synchronization problem[#](#multiple-boards-create-a-synchronization-problem)

Adding receivers can improve spatial coverage and reduce blind spots, but multiple ESP32s do not magically share a phase-coherent clock.

If the application combines observations, you need a synchronization model appropriate to the feature being fused.

For coarse activity scores, aligned timestamps may be enough. For phase-sensitive or fine Doppler-style analysis, clock and RF synchronization requirements become much stricter.

## Room transfer is a domain-shift problem[#](#room-transfer-is-a-domain-shift-problem)

A model trained in one room learns some combination of human motion and that room's propagation geometry.

Move the same hardware to another room and path lengths, reflectors, antenna orientation, AP position, channel, and interference change.

This is why a detector can look excellent in a demonstration room and fail after deployment.

I would explicitly evaluate:

- different room sizes,
- different AP/receiver placement,
- day/night RF conditions,
- doors open/closed,
- fans and moving curtains,
- pets,
- people in adjacent rooms,
- stationary occupancy.

## Calibration should generate evidence[#](#calibration-should-generate-evidence)

A useful calibration flow should report what it learned: noise floor distribution, baseline feature ranges, actual sampling rate, channel, RSSI range, subcarriers used, and confidence that the room was sufficiently static.

If calibration produces only “Success,” later false positives have no context.

## Keep raw data long enough to debug features[#](#keep-raw-data-long-enough-to-debug-features)

When a detector misclassifies, aggregate motion scores alone are often insufficient.

Keep a bounded window of raw or lightly processed CSI around events so you can reconstruct what happened, then store compact long-term features separately.

That lets you answer whether the failure came from acquisition, normalization, feature extraction, thresholding, or classification.

## Sensitivity is not robustness[#](#sensitivity-is-not-robustness)

Espressif's ESP-CSI project correctly emphasizes that CSI is sensitive enough to infer physical environmental changes, including subtle motion.

That sensitivity is the sensing mechanism and the source of false positives.

The engineering work is building enough calibration, synchronization, environmental modeling, and evaluation around CSI that a change in the radio channel maps reliably to the physical event you care about.

## Sources and further reading[#](#sources-and-further-reading)

- [Espressif ESP-CSI](https://github.com/espressif/esp-csi)
- [Espressif Wi-Fi CSI API documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/wifi.html)
