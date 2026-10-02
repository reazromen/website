---
title: 'eBPF/XDP: The Verifier Passing Does Not Mean Your Network Program Is Safe'
url: /posts/ebpf-xdp-verifier-operational-safety.html
date: '2026-09-26'
read_time: 8
excerpt: The verifier proves classes of memory and control-flow safety. It does not
  prove that returning the wrong XDP action, updating the wrong map, or attaching
  at the wrong hook will preserve network connectivity.
topic: ''
tags:
- ebpf
- xdp
- linux
- networking
draft: false
featured: false
language: en
eyebrow: Linux & Networking · systems note
outputs:
- url: /posts/ebpf-xdp-verifier-operational-safety.html
  template: cms/templates/posts/posts--ebpf-xdp-verifier-operational-safety.tpl
  source: cms/templates/posts/posts--ebpf-xdp-verifier-operational-safety.json
---

The eBPF verifier is impressive enough that it is easy to give it a job it never claimed to do.

A program loads. The verifier accepts it. No out-of-bounds memory access is possible under the verifier's model. The control flow terminates. Helper usage is valid.

Then the host disappears from the network.

Nothing about that outcome contradicts the verifier.

## The verifier answers a narrower question[#](#the-verifier-answers-a-narrower-question)

The verifier exists to decide whether a BPF program can execute safely inside the kernel under the rules of the BPF execution model.

It reasons about register state, pointer bounds, helper contracts, loops, stack use, and reachable paths. That protects the kernel from broad classes of unsafe programs.

It does not know your intended network policy.

If an XDP program safely returns `XDP_DROP` for packets you meant to pass, it is a safe program implementing the wrong policy.

## XDP sits early enough to make mistakes dramatic[#](#xdp-sits-early-enough-to-make-mistakes-dramatic)

XDP runs at a very early point in packet reception. That is exactly why it can be fast—and why a bad decision there can remove the packet before the rest of the Linux network stack gets a chance to help you debug it.

The action space looks simple:

```
XDP_PASS
XDP_DROP
XDP_TX
XDP_REDIRECT
XDP_ABORTED
```

Operationally, those actions are not small details. A mistaken `DROP` can cut off SSH. A bad redirect can send traffic into the wrong interface or queue. A mistaken transmit path can create surprising loops or asymmetry.

## Attachment point is configuration[#](#attachment-point-is-configuration)

The same object file can behave differently depending on interface, driver mode, generic mode, namespace, and what else is attached.

So I treat BPF attachment state as first-class runtime configuration.

Before changing a production interface I want to know:

- what program is currently attached,
- which hook and mode it uses,
- which maps it depends on,
- how it will be detached,
- and whether an out-of-band path exists if management traffic is affected.

`bpftool` is not only a development utility here; it is part of the operational inspection path.

## Maps can make valid code behave incorrectly later[#](#maps-can-make-valid-code-behave-incorrectly-later)

Many useful BPF programs split logic between bytecode and maps. The verifier sees the program shape, but runtime map contents can still express bad state.

A firewall map can contain an overly broad prefix. A redirect map can point at the wrong interface. A rate-limit map can be initialized with a value that effectively blocks everything.

That means rollout testing must include map lifecycle: creation, pinning, schema compatibility, update ordering, and cleanup.

## CO-RE solves portability, not intent[#](#co-re-solves-portability-not-intent)

BPF CO-RE uses BTF information and relocations so one program can adapt to kernel type-layout differences across versions.

That is a major portability improvement. But “this binary successfully relocated on this kernel” is still different from “this policy is correct on this host.”

Portability removes one failure class while leaving interface topology, policy state, feature assumptions, and semantics untouched.

## Design the rollback before the attach[#](#design-the-rollback-before-the-attach)

The safest XDP rollout is the one where rollback does not depend on the network path being modified.

On a remote system, that can mean a second management interface, console access, a local watchdog, or a timer that detaches the new program unless a health check confirms success.

I like a staged pattern:

```
load program
 -> attach to test interface / namespace
 -> verify counters
 -> mirror or allow-only behavior
 -> attach to production
 -> confirm management + application traffic
 -> persist attachment
```

Do not make the first production packet the first realistic test.

## Observe decisions, not only packet totals[#](#observe-decisions-not-only-packet-totals)

A counter for “packets processed” can look healthy while the wrong packets are being dropped.

Useful telemetry separates actions and reasons: pass, drop, redirect, parse failure, policy miss, map miss, and fallback path.

Sampling selected headers or exporting structured events through ring buffers can help, but the observability path must itself be bounded so debugging does not become a new overload source.

## Kernel safety and service safety are different layers[#](#kernel-safety-and-service-safety-are-different-layers)

The verifier is doing exactly what it should do when it accepts a memory-safe program.

The operator still owns semantic safety: packet policy, attachment state, map contents, rollback, observability, and blast radius.

That distinction is useful far beyond eBPF. A system can be valid at one layer and catastrophically wrong at the next.

## Sources and further reading[#](#sources-and-further-reading)

- [Linux kernel documentation: libbpf and CO-RE](https://docs.kernel.org/bpf/libbpf/libbpf_overview.html)
- [Linux kernel BPF documentation](https://docs.kernel.org/bpf/)
- [bpftool documentation](https://docs.kernel.org/bpf/bpftool.html)
