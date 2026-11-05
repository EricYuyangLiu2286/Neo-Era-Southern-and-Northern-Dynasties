# Data/database migration delivered

Applied to main MOD: **58 unique files**, zero deletions. All changes used guarded preimages; complete current main SHA256 values match `supplemental-release-manifest.json`. Independent preimages are in `applied-preimages/` and `map-followup-preimages/`; parent verified full backup is `pre-change-migration115-20261105T135256Z`.

Target native source: **Victoria 3 1.15.0 / build26453692**. Original baseline: 1.13.11 / build24799966. No game, Steam or workshop changes; no game launch.

## Delivered behavior and preservation

- Current native AI/database updates merged while retaining authored fictional tags, territories, populations, institutions, Japanese claims, HUS restrictions, Egypt treaty guards and custom French movement gates.
- Native current ideologies restored without old character `ideology_communist` masking the new IG ideology. Authored social democracy survives under its old valid key for direct event/template callers, with actual character-specific generation triggers disabled. Original bilingual labels/descriptions restored verbatim.
- Native copper capacities and cold bounds restored, with exact source lead redistribution only for unchanged original capacities. Five opening copper sites / ten levels remain: WestCountry6, Anhalt1, Kanto1, EasternCuba1 native fallback, SouthAustralia1. SouthAustralia native new site is owned by actual populated YN1 state, selected by real mine-hub province. Shikoku retains authored iron5; native new copper1 was withheld per root ruling, with new copper capacity available for construction.
- Native Russia current law variants, initialization, Cossack host setup and administration PM closure restored without importing native new borders/populations or re-enabling the authored-disabled Russian American company.
- Four renamed native state identities map to retained custom map identities; new Kostroma list coverage uses actual intersecting retained regions. Narrow per-object native home/capital replacements avoid full native-file locks. Retained Chukotka remains in formation/release/geographic coverage.
- Twelve stale native port province declarations corrected to current source. All twelve current MOD port locator objects and all twenty-four port/harbor anchor positions already equal current source, so no binary or locator mutation was necessary.
- New source province xBD5671 (200 pixels) is assigned to HEXI/CNE. Actual current bitmap gives seventy boundary edges, all six adjacent provinces HEXI/CNE. No population/building changes for this mapping.
- Removed native cultures north_caucasian and siberian restored under original keys. Original culture definitions/names/populations unchanged; current native heritage/language/tradition/religion/ethnicity/assets all resolve. Fifty-four personal/family name keys resolve in current bilingual localization; four culture labels restored verbatim with BOM. Effective bare/scoped legacy culture references now resolve, preserving valid old-save identifiers.

## Verification and limits

- Independent reviewer explicitly configured **gpt-6.1-sol / medium**. Initial/cross-path batch: 44 independent assertions; map followup: 119; culture supplement: 37. Reviews bind frozen SHA manifests.
- Local ordered-source/preservation checks: 69; copper exact-capacity/counterexample checks: 18. Original missing copper capacity was reproduced in nine masked map files; removing repaired capacity is detected.
- Full effective province-region closure: zero missing/extra/duplicate provinces, zero duplicate region IDs, zero outside-region owned-province tokens or hub declarations. Existing 268 raw duplicate ownership-token cases are unchanged authored history diagnostics; no claim that raw history has globally unique owner lists.
- Read-only native-map naval audit: 378 port/exit entries, zero recommended new changes, inherited/native exceptions documented. No new custom asset mutation. No engine or economic-balance certification.

## Information for root integration

- Cross-owner ideology call sites must use current character `ideology_communist_leader` where appropriate, while new `ideology_communist` remains IG-only. Removed `ideology_socialist` trigger closure remains script-owner responsibility.
- Two current-native fallback state-rename interfaces were reported to their owners: `customizable_localization/99_ru_custom_loc_V3.txt` and `scripted_effects/00_dynamic_state_names_europe.txt`. This batch does not write those domains.
- GUI/GFX informational scan: only differing native GUI override is culture_panel.gui, whose native source did not change A→B. Seven differing map assets lack old baseline; railroad script differences are authored market-scope guards. Localization native deltas are listed in `localization-native-key-deltas.json`; authored/retained map names were not replaced automatically.
- Cross-path `special_genes` source update concerns native `morph_genes/decals`; MOD EAC compatibility defines only `accessory_genes` in that root, with no overlapping native changed branch. No EAC asset copied or modified. Loader-level portrait behavior is not newly engine-certified.

Main supplemental delivery artifact: **supplemental-release-manifest.json**. Raw `history-proposal/` and `object-proposals/` directories are research only and MUST NOT be applied as release files.
