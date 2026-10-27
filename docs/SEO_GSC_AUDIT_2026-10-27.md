# Google Search Console indexing audit — 2026-10-27

## Scope and evidence

- Source: the supplied Google Search Console export for **Crawled — currently not indexed**.
- Export count: **497 unique URLs**; GSC report last updated 2026-10-23.
- Live HTTP checks were run against all 497 URLs from hserver. Redirects are followed by the checker, so final status is recorded rather than every intermediate redirect.
- CMS source, generated manifest, and generated sitemap were checked using an isolated checkout of `seo/noindex-test-page`. The production site was not changed.

## URL-level result

| Group | URLs | Result / action |
|---|---:|---|
| Production article URLs | 261 | All have matching CMS source, are generated, return HTTP 200, and have a canonical matching the source route. |
| Tag archives | 210 | All have matching taxonomy source. Apply the selective tag policy below; 143 become noindex/sitemap-excluded and 67 remain eligible. |
| HTTPS topic pages | 8 | All match CMS source and remain in the generated sitemap. |
| Portfolio projects | 3 | All match page source and remain in the generated sitemap. |
| Series and domain pages | 2 | Both match generated routes and remain in the generated sitemap. |
| Staging URLs on `dev.reazromen.com` | 4 | Return HTTP 200, canonicalize to production equivalents, and return `X-Robots-Tag: noindex, nofollow`. Keep them non-indexable and out of production sitemap signals. |
| Visitors app URLs/assets | 5 | Two font assets and three app routes on `visitors.reazromen.com`; not production editorial content and not in the website sitemap. Audit indexing controls in that app separately. |
| Legacy/utility URLs returning 404 | 4 | `http://reazromen.com/topics/call-center`, `/favicon.ico`, `/technophile-about-page/`, and `/technophil-contact-page/`. No current exact replacement was found for the two legacy content paths or call-center topic; do not invent redirects. The favicon endpoint is a utility fix, not an editorial page to index. |

The 4 URLs returning 404 are not suitable for indexing as-is. Keep a genuine 404 unless a semantically equivalent replacement is verified; if one is verified, add a direct redirect. The two `/posts/.../index.html` article routes use that exact URL in their CMS source and self-canonicalize; this is not a canonical mismatch.

## Tag archive policy

The CMS contains **1,226 tag archives**. Current source inventory:

- 1 tag has zero published posts.
- 764 tags have one published post.
- 148 tags have two published posts.
- 62 tags have three published posts.
- 251 tags have four or more published posts.
- Only 11 tag records currently have a non-empty description or body.

Policy implemented in the branch:

> A tag archive with fewer than three published posts and no unique description/body receives `noindex,follow` and is excluded from the sitemap. A tag with at least three published posts or unique editorial text remains eligible for indexing.

This is selective, not blanket noindex. Under the current source inventory, **905** tag archives meet the noindex rule and **321** remain indexable candidates. Of the 210 tag URLs in this GSC report, **143** meet the noindex rule and **67** remain eligible.

The eligible set is not guaranteed to be indexed; its titles, descriptions, article selection and distinct search intent still need ongoing editorial review.

## Article quality review

All **261 production article URLs** in the export matched a CMS source. Their body-level review found:

- **118 / 261** have fewer than 200 words; median body length is 233 words. Of those, **109** were published before July 2026 and are marked P1 in the URL matrix; the remaining **9** are marked P2 for review/monitoring.
- **259 / 261** have no body-level internal Markdown/HTML link.
- 1 lacks an excerpt, 61 lack a topic assignment, and 27 have no tags. An additional 40 posts that are not already in the short-article queue are marked P2 for missing topic/tag metadata.
- No exact duplicate body was found among these 261 production articles.
- The 80 articles above 800 words skew the mean substantially; the median is the more useful summary.

A missing inline link or a short word count alone is not proof of low quality. However, the 118 short articles—especially older articles with no links—are prioritized for a manual editorial pass. Rewrites should add concrete explanation, examples, limitations or evidence only when supported by the source; do not manufacture project measurements or personal experience.

The branch adds a **Related reading** block to published articles that have no body-level internal links, selecting up to three other published articles by shared topic/tags and matching language. It does not rewrite article bodies or link to drafts.

## Incomplete historical articles

Four archive-recovery placeholders have explicit `indexable: false` in the branch and are excluded from the sitemap:

- `/posts/how-i-took-cadvisor-from-428-mib-to-2028-mib.html`
- `/posts/monitor-the-log-pipeline-for-dropped-entries.html`
- `/posts/rtp-port-ranges-belong-in-the-network-design.html`
- `/posts/the-best-review-question-is-what-could-break.html`

The preservation baseline contains only short placeholder summaries (16–29 words), not the original article bodies, links or images. The original content could not be recovered from that baseline. Keep these pages non-indexable until original source material is found or the articles are deliberately rewritten and reviewed as new content.

## Build and release validation

The branch's CI now installs the CMS requirements, runs the content-preservation validator, runs the full CMS build, runs the validator again, and checks:

- the test page is absent from the generated manifest and sitemap;
- sitemap URLs are canonical-host URLs and all exist in the generated manifest;
- the selective tag policy is reflected in robots metadata and sitemap exclusions;
- explicitly non-indexable article placeholders are absent from the sitemap;
- unlinked articles receive a related-reading block with links to other generated articles.

The successful CMS build before the final three-post threshold change produced 1,916 published posts, 118 pages, 45 topics, 1,226 tags and 3,291 generated routes. The final three-post threshold and related-reading block passed the full CMS build and preservation validator in GitHub Actions. Final generated output: 1,916 published posts, 118 pages, 45 topics, 1,226 tag archives and 3,291 generated routes. The sitemap contains 2,369 canonical URLs after 909 non-indexable URL exclusions and canonical-alias exclusions.

## URL-by-URL matrix

The companion file [`seo-gsc-url-triage-2026-10-27.csv`](seo-gsc-url-triage-2026-10-27.csv) records each URL, last-crawled date where supplied, host/category, source match, live status/canonical, generated-manifest/sitemap status, source publication date, article metadata/quality signals, editorial-review priority and recommended action.

## Release status

**No merge or production deployment has occurred.** The changes remain on draft PR #21 until the latest CI result and review are complete.
