> Latest installed regional release: the ALT/SO1 and explicit flag supplement now has a combined16-file manifest in ../regional-autonomy-alt-20261105/. This report records the earlier14-file checkpoint.

# Regional local communities — applied

**STATIC_PASS; ENGINE_NOT_RUN.** Applied to the main MOD on2026-11-05. No game, UI, Git, live-log monitoring, diaspora changes, deletions, starting-border changes, or map-asset changes.

## Installed files

14 files: six modified and eight added. `applied-manifest.json` lists exact paths and hashes. All15 original preimages were checked before any write; the extra preimage is an unchanged shared value file. All14 installed hashes match the reviewed candidate digest `6b09144f50b2283d22b8271233248ccee7b9c11ff8e257b0d784105c4416b160`. Backups are in`pre-change/`.

- Modified the regional trigger, value and effect adapters, regional buttons, and existing English/Chinese regional localization files.
- Added `nesnd_regional_communities.txt` under country definitions, cultures, discrimination traits, customizable localization, and global history.
- Added two bilingual community localization files.
- Added the native filename override `common/history/pops/06_central_america.txt`, containing only three authorized population splits. Reversing those splits reproduces the complete native1.15 population AST. Its native source hash is recorded for later migrations.

The shared restoration effects, war goals, timers, settlement receipts, refugee/diaspora chain and military formulas are unchanged. `post-apply-verification.json` confirms14 hashes and10 ordered TXT parses.

## Hosts and founding regions

The actual opening trigger inventory finds four qualifying hosts: UCA, CLM, VNZ and BOL. Tests also cover formed GCO and the Central American successors GUA, ELS, HON, NIC, COS, PNM and ALT. `all-opening-hosts.json` records effective populations and ownership.

|Host|Founding government|Relevant opening population|Territory|
|---|---|---|---|
|BOL|Native AYM, Aimara/Catholic|Potosi159,996 total;121,996 Aimara|Whole Potosi; host capital retained|
|CLM|Native AMZ, Amazonian/Animist|Guaviare128,392 total;88,000 Amazonian|Whole Guaviare; conditional MUI/Catholic Cundinamarca fallback|
|VNZ/GCO|OR1 Guayana, Amazonian/Animist|Bolivar198,162 total;28,000 Amazonian|Whole Bolivar; Miranda/Caracas retained|
|UCA/GUA|Native MAY, Mayan/Catholic|Guatemala476,404 UCA residents;312,000 Maya|Three connected western highland provinces, named Los Altos|
|HON|HM1 Northern Mosquitia, Miskito/Protestant|388,204 total;3,000 existing Miskito|Three eastern provinces; Tegucigalpa retained|
|NIC|NM1 Río Coco, Miskito/Protestant|288,000 in the UCA portion;4,000 existing Miskito|Two northern provinces; Managua and every native MKT province excluded|
|ELS|NP1 Cuscatlán, native Nahua/Catholic|428,204 total;5,000 newly distinguished Nahua|One western inland province; host city retained|
|COS|BT1 Talamanca, Bribri/Catholic|83,992 total;2,000 newly distinguished Bribri|One southeastern highland province; San José retained|
|PNM|GY1 Guna Yala, Guna/Catholic|128,192 total;2,000 newly distinguished Guna|One Caribbean coastal province; Panama city/canal retained|
|ALT|Political community route only|Native UCA Chiapas16,667 total;9,251 Maya|No unsafe cut from its only tiny opening territory|

Gran Colombia is handled according to the actual project case: the frozen1851.7 save records GCO as a VNZ successor, matching the lore's retreat to Venezuela. The former adapter searched only Colombian regions. It now includes Zulia, Miranda and Bolivar and uses the real Amazonian population in Guayana. Its OR1 registry is separate from CLM's AMZ case.

The six province subsets were checked against the actual bitmap, province ownership, adjacency and retained city. They are connected and cannot take British Belize or existing MKT land. Exact sets are in`regional-profiles.json`; pixel area was used only for geography, never as a population estimate.

## Population and identity

The approved fixed recognition counts are5,000 Nahua in San Salvador,2,000 Bribri in Costa Rica and2,000 Guna in Panama. These are small authored representations, **not reconstructed1836 census estimates**. They are subtracted from the existing local central_american groups, preserving total population, religion and profession semantics. No people are created or converted at runtime.

Bribri/Guna represent Christian communities previously aggregated by the native data. Their existing Catholic religion and Christian name pool are preserved. The two languages use the current Chibchan language group. Fresh-game history adds the corresponding Bribri/Guna homelands, plus the documented Nahua homeland in San Salvador and Miskito homeland in Honduras. No ownership changes accompany these additions.

Whole-state routes retain the100,000 population, half-host,150,000 remaining and another inhabited-state safeguards. Original Aimara/Amazonian routes retain35% core share. Muisca/Guayana use10,000 actual community members and5% share. Province routes require1,000 members of the correct community,20,000 in the owner-state,50,000 in the host, the exact owned/controlled province set and the retained city. These are explicitly state-level population checks.

## Lifecycle and presentation

The adapters use native1.15 `create_country` province/state inputs and callbacks. No subject pact is created, existing MKT is untouched, and only the new government's owner-state is renamed. Political recognition still requires independence, legitimacy50, Rural Folk in government, peace and no pending request.

Preparation keeps the existing12-month timer and pressure75 threshold. At creation the original region, identity, ownership, controllers, tag availability and registry are checked again. A lost or occupied province, missing community, reused tag or invalid capital cannot silently switch the prepared region or transfer foreign land. Pending diplomatic requests keep their original counterpart; selection now supports every new polity with validity fallback.

Thirty-three English/Chinese pairs were supplied by the existing Astra UI agent:31 additions and two replacements in their original files. All are unique across the merged MOD. The preview binds an explicit named host and guards the selected-state fallback. Population/capital rows appear only when stored geography and identity still match. A purely political blocker no longer produces a false “no qualifying territory” message. Source and prose reviews are under`loc-draft/`.

## Validation and limits

- **285 source-AST cases against installed main files**, recorded in`main-seed-tests.json`: all11 viable host fixtures, ALT's constrained political route, original-owner changes, occupation, missing culture/tag/registry, political blockers, pending requests, missing selection and both preview regressions.
- **Seven original failure counterexamples** load pre-change trigger/value/pop AST: GCO, GUA, ELS, HON, NIC, COS and PNM all lacked a viable seed. GCO/ELS/COS also failed qualification. `test_original.py` remains reproducible after application by excluding newly added files absent from the preimage.
- **353 independent Sol checks**, including146 partner-selection subsets, plus **40 independent preview/identity checks**. See`sol-review.md`, `sol-validation.json` and`sol-preview-validation.json`. Both review-found implementation defects were repaired before application.
- Missing variable dereferences and unsupported test operations raise; explicit script-value defaults remain explicit. These tests do not execute the engine's country creation, population/building partition or war dispatcher.

ALT remains political-only while it lacks supported, viable founding land. Existing valid independent Indigenous partners remain available for agreements. No broken-save migration was added. Actual recruitment, budgets, markets, provincial population allocation and armed subject-host/overlord outcomes remain **ENGINE_NOT_RUN**.

Current native examples, generated API exports and source hashes are in`native-sources.json`; authoritative historical links and the project lore reference are in`historical-sources.md`. The inherited implementation agent's model metadata was not exposed. Sol was configuredgpt-6.1-sol/medium; the writing agent reportsgpt-6-astra/high. Required Luna delegation was attempted but rejected by the thread limit; root instructed continuation without another agent.
