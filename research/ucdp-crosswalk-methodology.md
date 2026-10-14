# UCDP Crosswalk: editorial rules and current seed

**Status:** partial, reproducible seed; not a completed UCDP-to-register crosswalk.  
**Dataset:** UCDP/PRIO v26.1 annual data, finalized coverage 1946–2025; this audit window is 2000–2025.  
**Last updated:** 2026-10-15.

## Purpose

The companion CSV records ID-level audit leads already cited in `ucdp-audit-findings-2000-2025.csv`. It is deliberately conservative: it does not claim that every one of the 150 state-based IDs or 846 non-state IDs has been reconciled. No master-index entry is added, deleted, merged, or promoted to confirmed solely from a dataset ID.

## Reproducible source inputs

1. Download the official UCDP/PRIO v26.1 State-Based Armed Conflict dataset and Non-State Conflict dataset from <https://ucdp.uu.se/downloads/>.
2. Preserve the original downloaded ZIP/CSV files, file names, access date, and SHA-256 checksums with the audit run.
3. Filter conflict-year records to 2000–2025; enumerate unique conflict IDs separately for each dataset. Do not mix one-sided violence actor-year IDs into the conflict inventory.
4. Join each unique dataset ID to this seed and the full archive register. A missing match means `needs_manual_review`, not automatic approval to publish.
5. For each ID, verify actor names, start/end years, geography, conflict type and episode boundaries against the original dataset and at least one reliable independent source before finalizing the editorial disposition.
6. Record the resulting complete crosswalk and its source checksums in a subsequent commit. Until then, label this file partial.

## Status vocabulary

- `matched_existing`: a reviewer verified that the existing page covers the ID's parties, geography and period.
- `proposed_new_entry`: a candidate for a new page; not confirmed or publication-ready.
- `needs_manual_review`: insufficient evidence to map confidently or choose a disposition.
- `relationship_review`: likely parent/phase/intervention/actor relationship requiring an explicit decision.
- `exclude_with_reason`: reviewer documents why the dataset record is outside the archive's declared scope.
- `duplicate_confirmed`: only after a human verifies equivalent scope, parties, geography and period; never based on title similarity alone.

## Editorial rules

1. **Parent and phase:** retain a parent page for broad context; a phase page is separate only if it has a distinct, bounded period and material historical narrative. Link both ways and avoid counting the phase as an additional independent war in archive totals.
2. **Intervention and external support:** normally use a relationship/cross-index unless the intervention is itself a separately bounded conflict meeting the archive's published inclusion criteria. Explain the distinction.
3. **Actor-specific and non-state dyads:** a UCDP non-state ID is not automatically a standalone article. Prefer a documented actor-pair appendix or theatre page when many dyads share a broader narrative. Preserve distinct actor pairs in the crosswalk even when editorially grouped.
4. **Short interstate episodes:** use exact dates and parties; do not imply continuity across years when the source records only a bounded episode.
5. **One-sided violence:** use it to enrich civilian-harm coverage, not to inflate the conflict count.
6. **Deletion and merge safety:** no published article is deleted or silently merged. A proposed merge must cite both entries, IDs, date coverage, independent evidence, rationale and a review decision.
7. **Publication gate:** article drafting may begin as a draft, but publication queue promotion requires source list, date coverage, actors, classification, uncertainty statement, parent/phase links and successful build/deployment verification.

## Seed interpretation

The companion CSV contains candidate IDs and relationship leads from the first-pass findings only. Several rows intentionally remain `needs_manual_review`; a grouped finding mentioning multiple IDs is not itself a one-to-one mapping. Resolve actor names and exact active years from the downloaded UCDP rows before calling this crosswalk complete.

## Official references

- UCDP Dataset Download Center: <https://ucdp.uu.se/downloads/>
- UCDP API documentation: <https://ucdp.uu.se/apidocs/index.html>
- First-pass findings: [`ucdp-audit-findings-2000-2025.csv`](ucdp-audit-findings-2000-2025.csv)
- Register: [`conflict-archive-register-2000-2026.csv`](conflict-archive-register-2000-2026.csv)
