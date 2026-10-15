# UCDP/PRIO country-year coverage screen — 15 October 2026

## Purpose

This is a first-pass coverage screen for the 115-entry Global Armed Conflicts Archive register. It maps each archive entry to one or more countries and counts matching records in official UCDP datasets. It is **not** a conflict-identity reconciliation and must not be used to claim that every entry is independently validated or that overlapping entries are duplicates.

## Dataset inputs downloaded and processed

- UCDP/PRIO Armed Conflict Dataset v26.1 (conflict-year, 1946–2025)
- UCDP Dyadic Dataset v26.1 (dyad-year, 1946–2025)
- UCDP Non-State Conflict Dataset v26.1 (conflict-year, 1989–2025)
- UCDP One-Sided Violence Dataset v26.1 (actor-year, 1989–2025)
- UCDP Georeferenced Event Dataset v26.1 (event-level, 2000–2025 subset)
- UCDP Candidate Events Dataset v26.0.8 (2026 candidate events)

Official source: https://ucdp.uu.se/downloads/

## How to read the CSV

- `state_rows` and `dyadic_rows`: records in the mapped country or countries, not a count of unique conflicts attributable to the archive entry.
- `nonstate_rows` and `onesided_rows`: different categories of organized violence; they are not interchangeable with state-based conflict.
- `ged_events`: events in the mapped country or countries during 2000–2025.
- `candidate_2026_events`: candidate-event rows in the August 2026 release for the mapped country or countries. Candidate events are provisional and should not be merged uncritically with finalized annual data.
- `audit_note`: flags entries requiring additional manual work.

Counts for multi-country theatres intentionally overlap. The same country-level records can therefore appear in several archive rows. This is a coverage indicator, not a unique-event total.

## Findings and limitations

The register contains 115 entries. The first-pass country screen found country-level records for most mapped entries; five entries returned no country match under the current country-name aliases: Palestinian factional armed clashes, Kosovo–Serbia armed incidents, Transnistria and Moldova, Korean Peninsula armed incidents, and East Timor post-independence violence. These are **alias/scope review flags**, not evidence that the relevant violence did not occur or that UCDP has no related record.

The screen also demonstrates why a country-level match is insufficient: distinct wars, campaigns, phases, external interventions and violence categories can share the same country-level dataset rows. Examples needing actor/phase-level review include India’s insurgencies, Sudan/Darfur, Ethiopia’s regional conflicts, Ukraine/Donbas, Myanmar’s ethnic theatres, the Philippines, Colombia’s FARC/ELN records, and broad transnational intervention entries.

## Next audit stage

1. Match each entry to UCDP conflict IDs, dyad IDs, actor names and active years.
2. Identify likely duplicates versus legitimate parent/phase/actor overlays.
3. Flag archive topics absent from UCDP without treating absence as disproof; use supplemental sources for events or categories outside dataset thresholds.
4. Keep 2026 candidate events separate from finalized 2025 annual data.
5. Update each register row only after its conflict/phase identity has been adjudicated.

Status after this screen: **country-year screening completed; actor/phase identity reconciliation remains pending**.
