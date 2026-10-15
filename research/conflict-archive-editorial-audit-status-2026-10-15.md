# Conflict Archive Editorial Audit Status — 2026-10-15

## Executive result

The 115 URLs in `research/conflict-archive-register-2000-2026.csv` were fetched on 2026-10-15. Article text was extracted from **115/115 URLs**. No fetch errors were returned, and **115/115 canonical URLs matched their expected URLs**. This establishes current public availability and URL consistency, not factual correctness of each article.

## Live-page checks

- Register entries checked: 115
- Article bodies successfully extracted: 115
- Canonical URL mismatches: 0
- Pages with a detected Further Reading / References / Sources / Bibliography heading: 111
- Pages whose extracted text mentions UCDP: 89
- Pages with an explicit URL visible in the extracted article text: 0
- Publication date exposed in live page metadata: `2026-10-15` for all 115 pages

The 2018–2026 randomized date mapping is still **planning metadata only**. It was not applied to the article pages. Do not present proposed random dates as verified historical publication dates; changing publication metadata requires a deliberate editorial decision and should not fabricate publication history.

## Editorial and UCDP status

The actor / active-year / conflict-identity / dyad reconciliation is **not complete**.

The current first-pass UCDP audit has 37 findings:
- 24 potential-missing or actor/theatre coverage leads
- 13 structural-overlap / parent-phase / intervention relationship findings

By review status, the findings are:
- 16 relationship reviews
- 11 needs-editorial-review
- 7 verify-existing-entry
- 3 needs-scope-review

The existing country-year screen is only a presence/coverage signal. It does not establish a one-to-one match between an archive entry and a UCDP conflict ID, dyad ID, actor ID, or dataset category. The full crosswalk must record the dataset version, ID type, parties/actors, active years, geography, inclusion/exclusion decision, and evidence for every match. A missing match remains a manual-review item, not proof that no conflict exists.

## Files created

- [Live URL audit CSV](conflict-archive-live-url-audit-2026-10-15.csv): one row per article with expected/canonical URL, fetched title, live publication metadata, extracted text length, and basic source-heading checks.
- [Editorial review matrix CSV](conflict-archive-editorial-review-matrix-2026-10-15.csv): all 115 entries with live-page results, existing coverage-screen status, known UCDP findings, and explicit pending fields for actor/year verification, one-to-one ID reconciliation, and retain/merge/split decisions.
- [Master register](conflict-archive-register-2000-2026.csv)
- [First-pass UCDP findings](ucdp-audit-findings-2000-2025.csv)
- [UCDP first-pass audit report](ucdp-first-pass-audit-2000-2025.md)
- [Crosswalk methodology](ucdp-crosswalk-methodology.md)
- [Country-year coverage screen](ucdp-country-coverage-screen-2026-10-15.csv)
- [Randomized publication-date mapping (not applied)](conflict-archive-randomized-publication-date-mapping-2018-2026.csv)

## Next required pass

1. Reconcile every state-based conflict ID active during 2000–2025 to an entry or a documented exclusion / parent-phase / cross-index decision.
2. Repeat for non-state conflict IDs, preserving actor-pair/dyad distinctions; do not automatically turn every dyad into a separate article.
3. For each of the 115 entries, verify exact parties, active years, geography, conflict category and episode boundaries against the official UCDP v26.1 row(s) and at least one reliable independent source.
4. Resolve the 37 existing findings, including possible missing entries, and document retain / merge-candidate / split / cross-index / exclude decisions with evidence.
5. Add direct source links and specific citations where the article's claims require them; a heading or a mention of UCDP alone is not source verification.
6. Re-run the live URL check after any editorial changes and deployment.

## Official dataset reference

UCDP Dataset Download Center: https://ucdp.uu.se/downloads/  
UCDP API documentation: https://ucdp.uu.se/apidocs/index.html

The latest annual UCDP/PRIO v26.1 and Dyadic v26.1 datasets cover through 2025. Events in 2026 need a separately dated provisional source snapshot and should not be represented as part of the finalized 2025 annual data.
