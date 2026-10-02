---
title: OpenTelemetry Cardinality Is a Data-Model Problem, Not Just a Cost Problem
url: /posts/opentelemetry-cardinality-data-model.html
date: '2026-09-26'
read_time: 8
excerpt: ''
topic: ''
tags: []
draft: false
featured: false
language: en
eyebrow: ''
outputs:
- url: /posts/opentelemetry-cardinality-data-model.html
  template: cms/templates/posts/posts--opentelemetry-cardinality-data-model.tpl
  source: cms/templates/posts/posts--opentelemetry-cardinality-data-model.json
---

High cardinality usually enters an observability conversation through a bill.

A team adds `user_id`, `request_id`, a raw URL, or some other effectively unbounded attribute to a metric. The number of time series jumps, the backend gets slower or more expensive, and somebody says the obvious thing: remove the label.

That is real, but it is not the interesting failure.

The more dangerous failure is when the telemetry pipeline protects itself successfully and the dashboard still becomes wrong.

OpenTelemetry now makes this tradeoff explicit. A metric stream has a cardinality limit. The default specified limit is 2,000 unique attribute combinations per collection cycle unless the SDK or a View configures another value. Once the stream crosses the limit, new combinations can be folded into an overflow point marked with `otel.metric.overflow=true`.

The measurement is not necessarily lost. The dimensions are.

That changes the problem from “how much telemetry can I afford?” to “what questions does this metric still answer correctly?”

## Cardinality is state

Consider a request counter:

```
http.server.request.count

http.route=/checkout
http.request.method=POST
success=false
```

The metric SDK does not remember one number for that instrument. It keeps aggregation state for each unique combination of attributes.

If the service has 100 route templates, 5 methods, and 2 success states, the theoretical combination space is already:

```
100 × 5 × 2 = 1,000
```

That is still bounded.

Now add `tenant_id=<customer>`. If 10,000 tenants can be active, the model is no longer “one request counter with a useful label.” It is potentially millions of aggregation states depending on which dimensions combine in practice.

This is why cardinality belongs in system design. The attribute schema determines memory in the producing process, network/export volume, backend series or index state, query shape, and ultimately which operational questions remain cheap enough to ask.

The labels are not metadata decoration. They are part of the storage model.

## Overflow protects memory by changing semantics

OpenTelemetry's cardinality cap exists for a good reason: a buggy or malicious attribute must not be able to grow process memory without a bound.

When the configured limit is reached, the SDK can aggregate additional combinations into an overflow data point:

```
otel.metric.overflow=true
```

The important part is what disappears.

Suppose this measurement arrives after overflow:

```
http.route=/checkout
success=false
count=1
```

Its value can still contribute to the total request count. But the original attribute set is no longer attached to that contribution.

So these two queries no longer have the same quality:

```
sum(all requests)

sum(requests where success=false)
```

The first can remain numerically correct. The second can undercount, because some failed requests are now represented only by the overflow point and no longer carry `success=false`.

That is a subtle failure mode because the system looks healthy: the application did not crash, telemetry is still exporting, the backend still has data, the total traffic graph looks plausible, and no obvious pipeline error exists.

But an alert or SLO derived from an attribute filter may now be incomplete. A guardrail has changed query semantics.

## Low-cardinality attributes can become collateral damage

The attribute that caused the explosion might be `tenant_id` or a raw path, but overflow operates on the whole attribute combination. A perfectly bounded dimension such as `success=true|false` can disappear from the overflow point along with the high-cardinality attribute.

This is why “we only care about the boolean error label” is not enough.

If the metric stream's combinations overflow, every measurement attribute on those overflowed combinations is affected.

The better review question is not only “which attribute has high cardinality?” It is “which operational queries depend on attributes that share a metric stream with it?”

## The Collector is not the only place to solve it

Current observability discussions often ask where cardinality should be controlled: instrumentation, CI, Collector, or backend. These are different control points with different jobs.

### Instrumentation

This is where semantic mistakes should ideally be prevented. A route template such as `/users/{id}` is usually a useful metric dimension. A raw path such as `/users/874293` usually is not.

Request IDs, session IDs, arbitrary user input, full exception text, and similar values often belong in traces or logs rather than metric dimensions.

### SDK Views

Views are useful when an instrument is generally correct but its exported stream needs a different set of attributes or a different cardinality limit. This is earlier and safer than paying to export bad dimensions and cleaning them up later.

### Collector

The Collector is a valuable policy boundary, especially where many teams instrument services differently. It can normalize, delete, transform, or route attributes before telemetry reaches a backend. But using it to repair every instrumentation mistake can create a second schema system that only the platform team understands.

### Backend

The backend can detect expensive series, reject data, aggregate, or apply retention policies. By the time the problem is visible only here, however, application SDK memory and export volume may already have been affected.

I would not choose one layer and call the problem solved. I would define an attribute contract, enforce obvious rules near instrumentation, use Collector policy for organization-wide normalization, and keep backend cardinality monitoring as the final safety net.

## Delta temporality changes the active-state calculation

High cardinality is not automatically wrong. Sometimes a dimension is operationally necessary. A multi-tenant service may genuinely need per-tenant reliability data.

The question becomes how much state must exist at the same time.

With cumulative aggregation, the process can retain aggregation state across collection cycles. A large population that appears gradually can therefore accumulate. With delta aggregation, inactive metric points can be reclaimed by SDK implementations that support the behavior. That makes “active tenants per collection window” more relevant than “all tenants that have ever existed during this process lifetime.”

This does not make high cardinality free. It changes the capacity model.

A useful design review should include expected active combinations, collection behavior, process count, deployment churn, and the backend retention/indexing model.

The SDK's 2,000-point default is a local protection mechanism. It is not a promise that the backend will see only 2,000 series. A fleet can export different combinations from many processes over time. Local boundedness and global boundedness are different problems.

## Treat metric attributes like an API

The practical change I would make is simple: review metric attributes the same way we review an external API or a database schema.

1. Is the value bounded?
2. If it is unbounded, why must it be a metric attribute?
3. Which dashboards, alerts, SLOs, or autoscaling rules depend on it?
4. What happens when the stream overflows?
5. Can the same investigative value live in traces or logs instead?
6. Where is the contract enforced: instrumentation, View, Collector, or backend?
7. How will we detect `otel.metric.overflow=true` before a human notices a misleading graph?

If a critical SLO depends on attribute filtering, the presence of overflow in that metric stream is not an interesting debug detail. It is a data-quality event.

## Cost is only one symptom

High-cardinality telemetry can certainly make an observability platform expensive. But cost is often the easiest failure to notice.

A bill goes up. A query slows down. A storage system complains.

The harder failure is a telemetry system doing exactly what it was designed to do—bounding state, keeping totals, exporting successfully—while quietly losing the dimensions required by the questions operators care about.

That is why I think cardinality is better treated as a data-model problem.

The metric name tells you what you measured. The attribute schema determines what you can ask later. And the cardinality policy determines what happens when reality grows beyond the assumptions embedded in that schema.

## Sources

- [OpenTelemetry: Metric cardinality limits — practical guide](https://opentelemetry.io/blog/2026/cardinality-limits-in-opentelemetry/)
- [OpenTelemetry Metrics concepts](https://opentelemetry.io/docs/concepts/signals/metrics/)
- [OpenTelemetry Metrics SDK specification](https://opentelemetry.io/docs/specs/otel/metrics/sdk/)
- [OpenTelemetry .NET metrics best practices](https://opentelemetry.io/docs/languages/dotnet/metrics/best-practices/)
- [Community discussion: where to control metric cardinality](https://www.reddit.com/r/Observability/comments/1up0wq0/where_do_you_check_metric_cardinality_in_your/)

[← Back to Writing](/writing.html)
