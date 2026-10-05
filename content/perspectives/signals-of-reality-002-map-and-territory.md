---
title: 'The Map Is Not the Territory'
url: /posts/signals-of-reality-002-map-and-territory.html
date: '2026-09-07'
read_time: 5
excerpt: A useful map earns its clarity by leaving things out. The trouble starts when we ask its carefully chosen simplifications to answer the wrong question.
topic: philosophy-science
tags:
- models
- interpretation
draft: false
featured: false
language: en
eyebrow: 'Signals of Reality · Reality Is Not What You See'
editorial_batch: signals-of-reality-200
---

In 1933, London Underground passengers received a map that made a useful bargain with geography. Routes followed horizontal, vertical, and diagonal lines. Stations were regularly spaced. The city’s irregular distances gave way to the legibility of a network.

Harry Beck had devised the diagram in 1931. The [London Transport Museum’s account](https://library.ltmuseum.co.uk/portal/Default/en-GB/RecordView/Index/106) records its first issue in 1933 and the basic geometry of the design. Its achievement was not to squeeze a more complete London onto the page. It made certain relationships easier to follow by relaxing others.

A passenger needed to know which line reached a destination and where to change. For that purpose, station order and connections could matter more than the exact bends of the tunnels or the street distance between platforms. The diagram treated those needs as design priorities.

That is a strong form of accuracy, provided we say what is accurate.

### A journey the diagram can answer

Consider an invented network with three stations in sequence: Orchard, Museum, and Harbour. A second line crosses the first at Museum. Draw the first line straight, put the stations equally far apart, and mark the interchange clearly. A traveler can discover that changing at Museum connects the two routes.

Now suppose Orchard is a short walk from Museum, while Museum is several kilometres from Harbour. The equal spacing has discarded that fact. A traveler who measures the drawn gaps and infers equal walking times is making a claim the diagram cannot support.

The diagram did not suddenly become useless. The question changed.

This separation is easy to understand in a toy network and surprisingly easy to forget elsewhere. A service architecture diagram may correctly show that one application depends on another while saying nothing about latency. A family tree may preserve descent while omitting who raised a child. Neither omission invalidates every statement the representation makes. Each limits what can legitimately be inferred from it.

There is a more subtle trap. A diagram might answer its intended question correctly and still leave a traveler stranded because a station is temporarily closed. That is a different failure from distorted spacing. One concerns which properties the representation preserves; the other concerns whether its information remains current. “Maps simplify” is too broad an explanation to tell these failures apart.

### Flattening has a price

Even a map designed to preserve geography must choose among incompatible demands. A globe can represent the broad geometry of Earth without flattening it. A world map on paper requires a projection. As the [U.S. Geological Survey explains](https://www.usgs.gov/publications/map-projections), projecting the round Earth onto a flat surface introduces distortion, and projection choice depends on the intended use.

An equal-area projection preserves relative areas but does not preserve every shape. A conformal projection preserves local angles but cannot also maintain the same area scale everywhere across a world map. “Accurate world map” therefore needs a second clause: accurate with respect to which property?

This is not an invitation to pick any picture one likes. If a map claims to preserve area, that claim can be checked mathematically. If its purpose is to compare the extent of forests, using a projection that greatly varies area scale can make visual comparison misleading. Different purposes justify different transformations; they do not erase standards.

The USGS’s [projection reference poster](https://pubs.usgs.gov/gip/70047422/report.pdf) is valuable partly because it places alternatives beside one another. The differences become explicit choices rather than invisible features of a supposedly neutral window.

The projection analogy also has limits. Not every flaw in a model is as unavoidable or as precisely understood as distortion in flattening a sphere. A fabricated road is an error, not an elegant tradeoff. Leaving an accessible entrance off a mobility map may defeat its stated purpose. Calling every omission “necessary simplification” gives bad work a philosophical excuse it has not earned.

### The missing legend

Imagine that the invented transit map uses a solid circle for an interchange and an open circle for an ordinary stop. Without a legend, a reader might assume the solid circles indicate larger stations or more frequent service. The marks are visible, but their intended meaning is missing.

A map is more than a collection of shapes. It includes conventions for reading those shapes. Scale, date, boundary definitions, and symbol meanings tell us how to turn marks into claims. When those supporting details disappear, a polished image can become harder to evaluate precisely because it looks so self-contained.

The same problem appears in a chart headed “city population.” Does the boundary include the surrounding urban area? Is the number a census count or an estimate? Are two cities measured using equivalent definitions? The dots can be plotted flawlessly while the comparison remains poorly specified.

These are questions about the connection between the representation and what it represents. They are not objections to counting or drawing. On the contrary, they are what allow counting and drawing to become trustworthy.

We can make the connection explicit by treating a map as a limited promise. It says that certain marks correspond to certain features, under stated conventions, with some level of resolution. The promise can be modest and still be useful. A sketch that reliably identifies the next turn may serve a walker better than a detailed survey printed too small to read.

There is no universal contest in which the map with the most information wins. Extra information competes for attention. If every pipe, property line, tree, and elevation contour were added to a transit diagram, essential route connections might become harder to find. Completeness can undermine the very task that justified the representation.

But the user should not have to guess the price of clarity. An honest simplification leaves its important limits available: not to scale, estimated boundary, seasonal route, last updated on a particular date. Such statements give readers a way to know when they need another source.

Return to Orchard and Museum. On the invented diagram, they are two circles a fixed distance apart. On the street, they could be separated by an easy walk or by a river with no nearby crossing. The sensible response is not to throw away the transit map. It is to use it for the journey it describes, then open the map that answers the next question.

### Sources

[London Transport Museum: who designed the diagrammatic Tube map?](https://library.ltmuseum.co.uk/portal/Default/en-GB/RecordView/Index/106) provides the historical details. The [USGS introduction to map projections](https://www.usgs.gov/publications/map-projections) and its [illustrated projection guide](https://pubs.usgs.gov/gip/70047422/report.pdf) explain the geometric tradeoffs. Orchard, Museum, and Harbour are fictional stations used only for the worked example.