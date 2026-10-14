# Global Armed Conflicts Archive: Audit and Publishing Plan

Updated: 2026-10-15  
Owner: Reaz Romen

## Verified baseline

- The working register has 115 research leads; it is not an exhaustive census yet.
- Five article pages were checked live on 2026-10-15 and returned HTTP 200: Second Intifada, Afghanistan, Iraq, Darfur, and Pakistan insurgency.
- The Master Index and sitemap also returned HTTP 200.
- The CSV now separates publication status from dataset-audit status. Live availability does not mean historical completeness has been audited.
- Current editorial state: 5 live-verified articles, 102 planned entries, and 8 scope-review entries.

## Phase 1 — Dataset audit

1. Freeze the inclusion rules before adding more names.
2. Compare the register against UCDP/PRIO state-based conflict-year and dyad-year records for every year 2000–2025.
3. Cross-check UCDP non-state conflict and one-sided violence datasets so the archive does not silently omit relevant organized violence.
4. Record exact dataset release/version, access date, IDs, year range, parties, geography, classification, source links and disposition for each record.
5. Use the latest available 2026 UCDP Candidate Events data only as provisional evidence, with a visible cutoff date. Do not treat candidate events as finalized annual data.
6. Map each source record to a register entry, new candidate, merge, cross-index, monitor, or documented exclusion.
7. Preserve alternative names and parent/phase relationships to prevent double counting.

The current CSV is a manual editorial register, not yet a completed dataset reconciliation. Do not mark an item audited just because it appears in the list.

## Phase 2 — Scope review

Resolve all entries marked `scope_review_required`. For each one, either define a dated episode that meets the archive threshold, reclassify it as a contextual cross-index, or document exclusion. A coup, political crisis, high homicide rate, non-lethal standoff or displacement crisis is not automatically a war.

## Phase 3 — Publishing queue

### Queue 0: live articles and site quality
- Master Index plus the five live-verified articles.
- Add reciprocal links to the Master Index and related conflicts.
- Check sources, page titles, canonical URLs, mobile layout, and sitemap inclusion.

### Queue 1: South Asia
1. Sri Lanka’s final civil-war phase (2000–2009).
2. Nepal’s Maoist conflict and peace transition (2000–2006).
3. Kashmir insurgency and India–Pakistan armed crises, separated into dated episodes.
4. Baloch insurgency in Pakistan.
5. India’s Naxalite–Maoist insurgency.
6. Northeast India insurgencies, separated by actor and theatre.
7. Afghanistan–Pakistan border conflict.
8. Bangladesh entries only after scope and source review.

### Queue 2: Middle East and North Africa
1. Iraq insurgency and sectarian war (2003–2011).
2. Iraq and ISIS (2013 onward).
3. Syrian civil war and its intervention/theatre relationships.
4. Yemen civil war and external intervention.
5. Israel–Hezbollah conflict, including 2006 and later phases.
6. Israel–Hamas/Gaza conflict, separating earlier rounds from the war beginning in 2023.
7. Libyan wars by phase.
8. Sinai insurgency and AQAP in Yemen.

### Queue 3: Africa
1. Sudan war (2023 onward), linked to Darfur and South Kordofan/Blue Nile.
2. Democratic Republic of the Congo’s Kivu conflicts and M23 phases.
3. Somalia and al-Shabaab.
4. South Sudan.
5. Tigray war.
6. Boko Haram/ISWAP and Lake Chad Basin.
7. Mali, Burkina Faso and Niger, with national records plus a regional cross-index.
8. Cameroon’s Anglophone conflict and Mozambique’s Cabo Delgado insurgency.

### Queue 4: Europe and Eurasia
1. Russia–Georgia war (2008).
2. Russia–Ukraine conflict from 2014, with Donbas and the 2022 full-scale invasion linked as phases.
3. Nagorno-Karabakh, the 2020 war, 2023 offensive, and Armenia–Azerbaijan border clashes.
4. North Caucasus insurgencies, separated by place and period.

### Queue 5: East/Southeast Asia and the Americas
1. Myanmar’s nationwide conflict and distinct ethnic theatres.
2. Southern Thailand insurgency.
3. Philippine communist insurgency, Mindanao/Moro conflict, and Marawi siege.
4. Indonesia’s Papua conflict.
5. Colombia’s armed conflict, FARC dissidents, and ELN.
6. Mexico’s organized armed violence only where the chosen dataset and stated threshold support the framing.
7. Haiti and Ecuador only with explicit classification and source notes.

### Queue 6: cross-indexes
Publish umbrella pages for international interventions, transnational armed organizations, drones, and private military actors after primary conflict pages exist. Treat these as relationship indexes, not extra wars by default.

## Phase 4 — Minimum article standard

Every article must include scope, dates, geography, parties, a timeline, causes and context, civilian impact, displacement, casualty estimates with source and uncertainty, peace agreements or current status, disputed claims, authoritative sources, related links, and a review date for ongoing conflicts.

Do not present a single casualty figure as definitive where credible estimates differ. Distinguish battle deaths, civilian deaths, indirect deaths, missing persons and total deaths.

## Phase 5 — Release and maintenance

### Every publication
1. Validate frontmatter, tags, date, source links and internal links.
2. Run the build and verification workflow.
3. Confirm the deployment job succeeded.
4. Verify the deployed URL returns HTTP 200 and the expected title/content.
5. Confirm sitemap inclusion and canonical URL.
6. Only then mark the register entry `published_live_verified`.

### Weekly
- Publish 3–5 well-sourced articles only when research is ready; accuracy takes priority over volume.
- Hold one dataset-reconciliation session.
- Review one region and its related links.
- Recheck a batch of live URLs and update the register.

### Monthly
- Recheck ongoing conflicts and review dates.
- Check broken links, redirects, sitemap and indexing signals.
- Log additions, merges, exclusions, corrections and dataset-release changes.

## Completion criteria

Call the archive dataset-audited only when every included dataset record for 2000–2025 maps to an entry or documented exclusion; 2026 has a dated provisional cutoff; duplicates and phase/umbrella relationships are reviewed; borderline cases are labelled; and every eligible conflict has a live-verified article or transparent research status.

## Research sources

- [UCDP Dataset Download Center](https://ucdp.uu.se/downloads/)
- [UCDP Conflict Encyclopedia](https://ucdp.uu.se/)
- [UCDP API documentation](https://ucdp.uu.se/apidocs/index.html)

Record the exact dataset versions actually downloaded and used in the audit log.
