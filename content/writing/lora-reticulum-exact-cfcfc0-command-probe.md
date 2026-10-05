---
title: The Exact CF CF C0 05 01 17 Command Was a Compatibility Probe
url: /posts/lora-reticulum-exact-cfcfc0-command-probe.html
date: '2023-05-29'
read_time: 9
excerpt: Generic transparent traffic could fail for many reasons, so the investigation
  needed one manufacturer-documented transaction with a predictable reply.
topic: lora-reticulum
tags:
- lora
- reticulum
- rnode
draft: false
featured: false
language: en
eyebrow: 'LoRa & Reticulum: E22/EWM Failure Isolation · deep-dive'
outputs:
- url: /posts/lora-reticulum-exact-cfcfc0-command-probe.html
  template: cms/templates/posts/posts--lora-reticulum-exact-cfcfc0-command-probe.tpl
  source: cms/templates/posts/posts--lora-reticulum-exact-cfcfc0-command-probe.json
---

# The Exact CF CF C0 05 01 17 Command Was a Compatibility Probe

This experiment looked like a radio problem until I wrote down the layers. The actual issue was that Generic transparent traffic could fail for many reasons, so the investigation needed one manufacturer-documented transaction with a predictable reply.

This series comes from a small hands-on LoRa/Reticulum lab rather than a commercial coverage benchmark. The working set included Reticulum on Linux, RNode-class devices, a Waveshare ESP32-S3/LR1121 board, an ESP32-C6 bridge, an SX1262-class RNode, and EBYTE E22/EWM modules. Different devices used different bands and profiles; I keep those experiments separate instead of merging them into one imaginary “LoRa setup.”

The evidence for this case was specific: **The V2.5/V2.6 package sent CF CF C0 05 01 17 as the documented same-channel remote write and counted the expected reply separately.** I use it as evidence from that test topology, not as a universal radio claim.

The retained result was: **The exact write became the primary over-air compatibility probe.**

## How I framed the problem

I wrote down what the local node could prove and what it could not prove. The problem was Generic transparent traffic could fail for many reasons, so the investigation needed one manufacturer-documented transaction with a predictable reply. The observation The V2.5/V2.6 package sent CF CF C0 05 01 17 as the documented same-channel remote write and counted the expected reply separately. covered one side of the path. Because A narrowly specified command reduces ambiguity: if the topology and profile are correct, the remote device should recognize a known management transaction., it did not justify Sending arbitrary payloads and interpreting silence as a protocol diagnosis.. The useful result was The exact write became the primary over-air compatibility probe.

The E22/EWM investigation was valuable because it separated local module control from remote over-air state. Register reads, operating-mode GPIOs and AUX transitions can prove the local half while saying nothing definitive about the remote target. The exact documented management command gave us a narrow compatibility probe, but silence still had multiple possible causes.

The rule I carried forward was: **Use the smallest transaction whose expected response is unambiguous.** That rule is more useful than remembering one working frequency or one USB device name because it changes how the next experiment is designed.

## Evidence matrix

| Question | Recorded answer |
| --- | --- |
| Observed problem | Generic transparent traffic could fail for many reasons, so the investigation needed one manufacturer-documented transaction with a predictable reply. |
| Strongest evidence | The V2.5/V2.6 package sent CF CF C0 05 01 17 as the documented same-channel remote write and counted the expected reply separately. |
| Mechanism | A narrowly specified command reduces ambiguity: if the topology and profile are correct, the remote device should recognize a known management transaction. |
| Rejected shortcut | Sending arbitrary payloads and interpreting silence as a protocol diagnosis. |
| Retained result | The exact write became the primary over-air compatibility probe. |
| Carry-forward rule | Use the smallest transaction whose expected response is unambiguous. |

I keep this table because radio work is unusually vulnerable to folklore. A missing packet can become “bad antenna,” “wrong SF,” “dead module” or “too close” depending on which theory is most convenient. Writing the evidence beside the theory forces the conclusion to remain narrower than the timeout.

## The boundary I wanted to prove

```
Linux host / Docker
   |
   +--> Reticulum rnsd
   |      |-- RNodeInterface -> /dev/rnode -> USB/UART -> radio MCU
   |      `-- TCPServerInterface -> LAN peers
   |
radio firmware
   -> frequency + BW + SF + CR + sync word + power
   -> RF front end
   -> matched antenna
   -> propagation path
   -> remote radio profile/mode
   -> remote host / Reticulum
```

For this layer I wanted these checks before changing another parameter:

- read/configure the local E22 first
- prove local mode GPIO state
- observe AUX only as local-module evidence
- send the exact documented remote command
- count remote replies independently from TX activity

The experiment-specific mechanism was: A narrowly specified command reduces ambiguity: if the topology and profile are correct, the remote device should recognize a known management transaction. That sentence tells me where the next measurement belongs. If the disputed state is host serial ownership, changing LoRa SF is irrelevant. If the disputed state is remote Mode 0, increasing TX power is not the first diagnostic. If a preamble IRQ fires without a header, the receiver is telling me more than a binary “no packet” counter would.

## Investigation sequence

I separate configuration from reception. A local register read proves the local module. A local AUX transition proves local work. A preamble IRQ proves partial RF recognition. A valid header/CRC/RX proves more. A Reticulum announcement proves more again. Each layer earns a different claim.

The shortcut I avoided was **Sending arbitrary payloads and interpreting silence as a protocol diagnosis.** That shortcut would have changed a convenient variable without increasing observability. In radio debugging, a new parameter is not automatically a new experiment; it is only useful if the expected evidence is written down first.

## What would falsify the conclusion

The retained result is **The exact write became the primary over-air compatibility probe.** A useful conclusion must say what future observation would force me to revisit it.

If the same controlled topology produced evidence inconsistent with **The V2.5/V2.6 package sent CF CF C0 05 01 17 as the documented same-channel remote write and counted the expected reply separately.**, I would reopen the diagnosis. If a wired recovery read showed the remote module was already in the expected state, the fault domain would move back toward RF/profile compatibility. If a matched antenna and known-good peer produced clean packets, the earlier silence could not be used as proof that the local modem was defective. If Reticulum failed while direct packet exchange remained clean, the investigation would move up the stack.

This is how I keep RF work from turning into stories about invisible signals. The hypothesis has to predict an observable difference.

## Instrumentation I would keep

```
ESP32 -> UART -> local E22 -> RF ---> remote EWM -> reply
  |        |        |                 |
 GPIO     bytes    AUX              mode/profile/power
```

The instrumentation should make state transitions explicit rather than print only final success. For serial/host work I want device identity, open failures and interface initialization. For LoRa PHY work I want the full profile plus preamble/header/header-error/CRC/RX counters. For E22/EWM I want UART writes, AUX timing and remote reply counts separated. For Reticulum I want interface state and rnstatus-visible behavior.

The reason is simple: **The V2.5/V2.6 package sent CF CF C0 05 01 17 as the documented same-channel remote write and counted the expected reply separately.** was useful because it exposed an intermediate state. If I had recorded only “packet received = 0,” several very different failure modes would have looked identical.

I also preserve units and topology. Frequency is recorded in Hz or MHz explicitly, TX power in dBm, bandwidth in Hz/kHz, and distance only when the antenna/environment are controlled enough for the number to mean something. A number without its observation boundary is usually weaker evidence than it looks.

## Acceptance test

For a host/interface article, acceptance means the service survives restart and re-enumeration without silently binding to the wrong device. For a PHY article, it means two endpoints agree on the complete packet profile and produce valid RX evidence rather than only RF activity.

For this case the pass condition follows directly from the retained result: **The exact write became the primary over-air compatibility probe.** The test should observe that state, not infer it from a neighboring LED, process or log line.

## What I would do next at larger scale

I would stop treating every node as an interactive lab device. Radio identity, firmware identity, interface type and accepted PHY profiles would become inventory. A deployment test would validate the host serial mapping, interface initialization, pairwise packet exchange and Reticulum reachability before the node was allowed to act as transport.

For RF planning I would add a real link-budget worksheet and measured site data instead of extrapolating from desk tests. The question would become required margin for a defined path rather than “how far can LoRa go?” For mixed hardware, I would maintain compatibility profiles so a 433 MHz LR1121 experiment could never be confused with an 867 MHz SX1262 RNode configuration.

For **The Exact CF CF C0 05 01 17 Command Was a Compatibility Probe**, the mechanism still scales: A narrowly specified command reduces ambiguity: if the topology and profile are correct, the remote device should recognize a known management transaction. Scaling adds automation; it does not remove the need to know which layer a PASS actually proves.

## The next experiment I would run

The next test should try to break the conclusion on purpose. Keep the known-good side fixed, alter only the state described by the mechanism, and ask whether the evidence moves with it: A narrowly specified command reduces ambiguity: if the topology and profile are correct, the remote device should recognize a known management transaction.

The purpose is not to collect more logs. It is to remove one ambiguity. If the new test cannot distinguish two competing explanations, it is not yet the right next test.

## The rule I kept

**Use the smallest transaction whose expected response is unambiguous.**

The retained result was: The exact write became the primary over-air compatibility probe.

The main thing I learned from this radio work is that “no packet” is not a diagnosis. The host, bridge, target MCU, local modem, PHY, antenna, path, remote mode and overlay protocol can all fail independently. The productive debugging loop is to expose one boundary at a time and make each experiment answer a question that the previous one could not.

That is also what made Reticulum useful as an engineering exercise. It forced the radio to become part of a network system rather than an isolated demo. Once the interface has a role, a health state, a recovery path and reproducible configuration, the lab starts becoming infrastructure.
