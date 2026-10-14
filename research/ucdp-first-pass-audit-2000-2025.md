# UCDP First-Pass Crosswalk Audit: Global Armed Conflicts, 2000–2026

**Prepared:** 2026-10-15  
**Repository:** `reazromen/website`  
**Register reviewed:** `research/conflict-archive-register-2000-2026.csv`  
**Scope:** First-pass comparison against official UCDP/PRIO v26.1 annual datasets covering 2000–2025.

## 1. Sources and reproducible counts

Downloaded the official CSV ZIP files from the UCDP Dataset Download Center and inspected their headers and records.

| Dataset | Version / coverage | Rows in 2000–2025 window | Distinct IDs in that window | How to interpret it |
|---|---|---:|---:|---|
| UCDP/PRIO Armed Conflict Dataset | v26.1, conflict-year, 1946–2025 | 1,161 | 150 conflict IDs | State-based conflicts where at least one party is a state government |
| UCDP Non-State Conflict Dataset | v26.1, conflict-year, 1989–2025 | 1,513 | 846 conflict IDs | Communal/organized armed conflicts where neither party is a state government |
| UCDP One-Sided Violence Dataset | v26.1, actor-year, 1989–2025 | 997 | 301 actor IDs | Intentional attacks on civilians by governments or organized armed groups; not a separate conflict inventory |

These counts are dataset rows/IDs, **not a count of unique “wars” that can simply be added together**. The units of analysis differ. A UCDP conflict can span multiple years; one historical war can also contain multiple UCDP conflict IDs or dyads. One-sided violence should be used to check civilian-targeting context, not added as a third conflict count.

Official sources:
- https://ucdp.uu.se/downloads/
- https://ucdp.uu.se/apidocs/index.html
- https://ucdp.uu.se/

## 2. High-confidence structural overlap and phase issues

These are editorial-structure findings from the 115-entry register. They do not mean every pair is a duplicate article; they mean the archive needs explicit parent/child or cross-index relationships to avoid double-counting.

| Register entries | Finding | Recommended treatment |
|---|---|---|
| 3, 14, 15 | Iraq invasion/occupation, post-invasion insurgency and ISIS phase overlap | Keep a parent Iraq conflict page; make 14 and 15 clearly dated phase/theatre pages with reciprocal links |
| 16, 17 | Syrian civil war and Kurdish/SDF/anti-ISIS theatre overlap | Parent/child relationship; distinguish state-based conflict from non-state dyads |
| 19, 20, 111 | Yemen civil war, Saudi-led intervention, and external support in Yemen overlap | Keep 19 as main conflict; 20 as intervention phase; 111 as an intervention cross-index, not another war |
| 21, 23, 25, 33 | Red Sea/Houthi attacks, Gaza war, Israel–Iran confrontation and proxy-theatre umbrella overlap | Separate direct interstate episodes from linked theatres; umbrella pages must not be counted as independent wars by default |
| 29, 106 | Libyan wars and 2011 international intervention overlap | 106 is an intervention page linked to 29 |
| 34, 35, 60 | Darfur, Sudan war from 2023, and South Kordofan/Blue Nile are related but not interchangeable | Keep separate geography/period records with explicit links; do not merge them into one continuous war |
| 38, 39, 59 | DRC Kivu conflicts, M23 and Rwanda–DRC involvement overlap | Main DRC conflict page plus dated M23 phase and external-involvement cross-index |
| 42, 108 | Somalia conflict and international operations overlap | 108 is an intervention cross-index under 42 |
| 48, 110 | Boko Haram/Lake Chad conflict and regional operations overlap | 110 is an intervention cross-index under 48 |
| 49, 50, 51, 52, 107 | Mali, Burkina Faso, Niger, Central Sahel umbrella and French-led operations overlap | Keep national records; make 52 a regional synthesis and 107 an intervention page |
| 64, 65, 66, 112 | Russia–Ukraine conflict, Donbas, 2022 full-scale invasion and foreign support overlap | 64 is the parent; 65 and 66 are dated phases; 112 is an external-support cross-index |
| 67, 68 | Nagorno-Karabakh and Armenia–Azerbaijan border clashes are related but distinct | Keep separate records, with the 2020 and 2023 episodes dated precisely |
| 69, 70 | Chechen and wider North Caucasus/Dagestan insurgencies overlap | Define actor, geography and years; do not count the same insurgency twice |
| 75, 76, 77, 78, 90 | Myanmar nationwide conflict and named ethnic theatres overlap | Parent national overview plus dated theatre pages only where they add distinct history |
| 81, 82, 83 | Philippine communist insurgency, Mindanao/Moro conflict and Marawi siege overlap but are not identical | Keep distinct actors and periods; nest the siege under the Mindanao conflict |
| 91, 92, 93 | Colombian armed conflict, FARC dissidents and ELN overlap | Parent conflict page plus actor-specific pages that do not imply each actor is a separate independent war |
| 103–115 | Global War on Terror, operations, external support, ISIS affiliates, drones and private military companies are umbrella/actor/method indexes | These are relationship pages, not automatically additional conflicts; link each to a dated underlying theatre |
| 2, 104 | Afghanistan war and US-led Afghanistan operations overlap | 104 should be a campaign/intervention page linked to 2, not an independent war |
| 15, 105, 113 | ISIS in Iraq/Syria, Operation Inherent Resolve and transnational ISIS campaigns overlap | Separate local conflict pages from coalition-operation and organization-wide cross-indexes |

## 3. Potential missing or under-specified records

These candidates arose from the state-based dataset scan or from prominent non-state conflict-year records. They require individual codebook/source review before being declared standalone wars. Some may belong under an existing regional article rather than receive a new article.

| Candidate | Evidence / reason to review | Provisional disposition |
|---|---|---|
| Kyrgyzstan–Tajikistan border conflict (2021 onward) | UCDP/PRIO v26.1 includes a state-based conflict ID for the two governments (candidate ID 13324) | Add a dated candidate entry; verify the episode boundaries and later agreement |
| Cambodia–Thailand border conflict (2025) | UCDP/PRIO v26.1 includes a state-based conflict ID for the two governments (candidate ID 294) | Add as a provisional dated interstate episode; do not describe it as a continuous war without evidence |
| Bangladesh: Government vs PBCP/PBCP-J | UCDP/PRIO v26.1 conflict ID 11350 appears in the 2005 window; current Bangladesh entry focuses on the Chittagong Hill Tracts and is not a sufficient match | Split into a distinct candidate for scope review; do not conflate the actors or theatres |
| China–ETIM armed conflict (2008) | UCDP/PRIO v26.1 conflict ID 11349 | Review whether to include a standalone, time-bounded conflict or a broader Xinjiang/Uyghur armed-violence context page |
| Myanmar: NSCN-K and other actor-specific insurgencies | UCDP/PRIO records include conflict IDs involving NSCN-K, KIO, KNPP, RCSS and other groups; current entries bundle several distinct theatres | Expand the actor/theatre index; avoid a single undifferentiated “Northeast India” or “Myanmar ethnic conflict” entry |
| India: GNLA, ULFA, NDFB, NSCN and Manipur actors | UCDP/PRIO v26.1 has multiple actor-specific conflict IDs in India | Keep the broad Northeast India overview, but add dated actor-specific pages where evidence and editorial value justify them |
| Sabah/Lahad Datu armed incursion (2013) | UCDP/PRIO v26.1 includes a state-based conflict ID involving Malaysia and the Sultanate of Sulu (candidate ID 11487) | Add a dated candidate entry for scope review |
| Georgia–South Ossetia armed conflict (2004) | UCDP/PRIO v26.1 conflict ID 393 predates the 2008 Russo-Georgian war and is not the same episode | Add a distinct dated candidate or a clearly separated pre-2008 phase |
| Afghanistan–Pakistan interstate border conflict (2024) | UCDP/PRIO v26.1 conflict ID 11639 | Existing register item 9 is relevant; make sure it covers the dated interstate episode separately from the Afghanistan war and Pakistan insurgency |
| China–India border clashes (2020) | UCDP/PRIO v26.1 conflict ID 274 | Existing item 86 is relevant; explicitly mark the 2020 lethal episode and distinguish it from non-lethal border tensions |
| Iran–Israel direct confrontation | UCDP/PRIO v26.1 has a state-based conflict ID for Iran–Israel (candidate ID 14609, first recorded in 2018); later episodes also need separate date review | Existing item 25 is an umbrella; create dated episode records only where supported |
| Israel–Syria and Israel–Yemen interstate episodes (2025) | UCDP/PRIO v26.1 includes state-based IDs for these dyads (candidate IDs 302 and 16470) | Check whether item 21/25 adequately links the episodes; add dated records if the archive covers short interstate clashes |
| Sudan–South Sudan border conflict (2011–2012) | UCDP/PRIO v26.1 includes interstate IDs 11344 and 11348 | Existing item 37 is relevant; ensure it identifies the specific episodes and is not treated as a continuation of Darfur |
| Ituri and intercommunal conflicts in eastern DRC | UCDP Non-State v26.1 includes Hema–Lendu (ID 4638), Luba–Batwa (ID 13225) and Banunu–Batende (ID 9282) | Expand the DRC overview with distinct non-state conflict/theatre records where the evidence supports them |
| Sudan/South Sudan intercommunal armed conflict | UCDP Non-State v26.1 includes Lou Nuer–Murle (ID 4660), Ma’aliyah–Rizeigat (ID 4666) and other conflict-year records | Add a cross-index or selected theatre pages; do not misclassify these as state-based wars |
| Nigeria communal armed conflicts | UCDP Non-State v26.1 includes Fulani–Tiv (ID 4973), Birom–Fulani (ID 4948), and other dyads | Add an organized non-state conflict section rather than limiting the Nigeria picture to Boko Haram/ISWAP |
| Mexico cartel conflicts | UCDP Non-State v26.1 has many actor-pair records, including Jalisco Cartel New Generation–Sinaloa Cartel (ID 13737) and Juarez Cartel–Sinaloa Cartel (ID 4652) | Existing item 94 is too broad for actor-level auditing; add a dataset-backed cartel-conflict appendix/cross-index, while carefully explaining the classification limits |
| Brazil organized non-state armed conflict | UCDP Non-State v26.1 includes Comando Vermelho–GDE (ID 14285) and Comando Vermelho–PCC (ID 13972) | Review under item 99; avoid treating general homicide or every criminal dispute as a war |
| Ecuador organized non-state conflict | UCDP Non-State v26.1 includes Los Choneros–Los Lobos (ID 15386) | Review under item 98; use explicit dataset/threshold labels and avoid equating organized crime with conventional warfare |
| Syria: IS vs SDF/PYD and other armed groups | UCDP Non-State v26.1 includes multiple actor-pair conflicts, e.g. IS–SDF (ID 13616) and IS–PYD (ID 13022) | Cross-link under Syria and the anti-ISIS campaign; avoid duplicating the same theatre as a new war for each dyad |
| Yemen: AQAP vs government forces and Ansarallah vs AQAP | UCDP Non-State v26.1 includes AQAP–PLC forces (ID 13587) and Ansarallah–AQAP (ID 4935) | Keep separate actor-pair/theatre records linked to Yemen; do not collapse them into one conflict |
| Somalia: Puntland vs IS (2024–2025) | UCDP Non-State v26.1 includes conflict ID 16734 | Add as a dated theatre under Somalia, subject to source review |
| Afghanistan: IS vs Taliban | UCDP Non-State v26.1 includes conflict ID 13540 | Link as a distinct non-state dyad under the Afghanistan overview |
| Indonesia: communal armed violence (2000–2004) | UCDP Non-State v26.1 includes Christians–Muslims in Indonesia (ID 4903) | Review whether to add a Maluku/communal conflict page or a documented cross-index |

## 4. Important caveats

1. This is a **first-pass crosswalk**, not a completed one-to-one reconciliation of every UCDP record to every register row. The candidate list is not exhaustive.
2. Dataset IDs in this report are identifiers from UCDP/PRIO v26.1; retain the version in citations because IDs and definitions can differ across versions.
3. The UCDP datasets have different units and thresholds. A state-based conflict, a non-state dyad, and one-sided violence actor-year record must not be treated as equivalent entries.
4. Some candidates are below the archive's preferred threshold, are short episodes, or are part of a larger conflict. Each needs a documented include/merge/cross-index/exclude decision.
5. The 2026 conflict picture is outside the finalized annual v26.1 window. Track 2026 separately using a dated provisional source snapshot, not as if it were part of the 2025 finalized annual data.
6. No article should be published solely because a dataset row exists. The article still needs source review, a clear scope, reliable context, and a reason to exist separately from its parent conflict.

## 5. Next audit steps

1. Add the candidate records to the register with a provisional status; do not silently insert them into the final count.
2. Assign every state-based conflict ID active during 2000–2025 to a register entry or a documented exclusion/merge decision.
3. Repeat the same process for all 846 non-state conflict IDs, prioritizing theatres and dyads with the strongest relevance to the archive and using a separate non-state appendix for the long tail.
4. Use One-Sided Violence v26.1 to enrich civilian-harm context and identify coverage gaps, not to inflate the conflict count.
5. Run a duplicate/phase review on the full register and only then freeze the canonical list.
6. Publish the methodology, dataset versions, access date, mapping decisions and corrections log.
