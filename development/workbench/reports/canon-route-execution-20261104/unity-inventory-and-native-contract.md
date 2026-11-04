# Unity inventory and native contract — 2026-11-04

Read-only research of candidate C=`WORK/exports/canon-route-execution-20261104-a`; GAME is installed **1.13.11 / Steam build 24799966**. `catalog.py status` returned CURRENT, changed_count=0. No gameplay files edited and no game launched. This is source evidence, not ENGINE_PASS. Source links, line anchors, and SHA-256 appear at the end. Candidate source SHA describes the research snapshot; implementation may subsequently change C.

## Coverage and exact insertion points

| System | Actual regimes / lifecycle | Existing control buttons | Shared policy insertion |
|---|---|---|---|
| `nesnd_qe1_unity_journal` / 帝国的稳定 | Only living `c:QE1`, while no `nesnd_qe1_dissolved`. No state-count entry threshold. Can revolution inherit, but eligibility still exact QE1. Starts unity=70, uprising=0. | **None on this JE**; uprising JE also has none. | Add monthly policy delta to `nesnd_qe1_unity_delta`; add same line to `nesnd_qe1_unity_bar.monthly_progress`; bind the two buttons on unity JE. |
| `nesnd_jp_cohesion` / 国民团结 | Living JAP, **JTK**, JIM. JTO is not this system's tag. Covers original/unified JAP and partition/reunification survivors because eligibility has no partition/unified condition. No revolution inheritance. | **None on this JE**. | Add policy delta to `nesnd_jp_cohesion_delta` and named bar line to `nesnd_jp_cohesion_bar`; bind both buttons here. |
| `nesnd_india_society` / 王朝与印度 | Living, centralized country owning a populated North/South India state, plus MUG/BHT/DRA **or** retained `nesnd_india_imperial_line`, reform_done and nationalism. Dynamic imperial-line successors are included; ordinary Indian princes, FRA/USM/TZ1 merely owning India are not automatically included. | `nesnd_india_dynastic_constitution`, `nesnd_india_republican_settlement`, requests 4,7,6. | Add policy delta to `nesnd_india_community_delta` and guarded `owner.<value>` bar line; bind both on society JE. This supports **common identity**, not the separate dynasty/monarchical legitimacy bar. |
| New TUR unity | None exists in researched candidate. Current scripted history creates **27 TUR-owned state objects**. Entry `num_states >= 36` is 9 above opening count and counts owned states, not provinces, entire state regions or subjects. | New pair. | New country state/JE/value/bar/maintenance chain; preserve distinct TUR identity and expansion entry. |

Evidence: Qin C01:L1–44, C02:L1/21, C05:L1–15, C09:L19–20; Japan C10:L1–21, C11:L1–7, C13:L18/36–49/85–97; India C18:L39–52, C19:L1–3/25, C20:L1–10, C21:L17–34, C22:L14–19, C23:L13–31, C24; TUR C27 (27 `country = c:TUR` assignments), native `num_states` country use G18:L7–19.

Do not mistake `nesnd_japan_unity_score`/`nesnd_japan_unification_bar` for culture unity: `nesnd_japan_reunification` is territorial reunification, sets `nesnd_japan_unified`, and adds a 120-month integration reward. It does not change its owner's tag in its completion block; JAP/JTK/JIM still meet cultural-cohesion eligibility afterward (C17:L49–69, C11:L1). French `ce_french_republican_unity` is an existing modifier/political objective rather than a generic national culture-unity variable. There is no current all-countries unity JE. India is deliberately included in this task as a related identity system, not relabeled as dynasty confidence.

## Current arithmetic and behavior

**Qin.** Unity is clamped 0–100 each monthly JE callback. Existing terms: order +0.15; `(primary_cultures_percent_country - .65) * .8`; `heritage_count * -.05`; SoL rising >=.05 +.4 / falling <=-.05 -.6; bankruptcy -1.5; bureaucracy +.1 or -.4; school levels 1–4 each +.05, police>=2 +.05, health>=2 +.05; multicultural +.15, national supremacy -.25, segregation -.1, conscience +.05, total separation +.1, wartime mass conscription -.2; war -.2 then extra -.3 at 12 and 24 months; infamy thresholds 25/50/100 cumulative -.15/-.25/-.5; soldiers>3% -.15, soldier radicals>=25% -.3, armed forces approval>=5 +.1; victory +.15 and acquired land +.1; Persia subversion -1. These are source formulas, not difficulty measured in-game (C03:L8–42).

Above 75, monthly direct `change_pop_culture` converts 0.5% of each non-Sinosphere/non-cohort pop to `ce_xiyu`. Below 50 a qualified state has a 20% monthly identity-decline event chance; below 25 awakens uprising. The uprising advances +2 below 25, another +1 if wartime, another +1 for bankruptcy/high radicals, otherwise -1; 100 invokes breakup (C04:L5–34, C03:L43–64, C01:L26–44). Native assimilation speed modifiers **do not multiply this explicit scripted 0.005 conversion**. Preserve that distinction when saying the new buff improves assimilation.

**Japan.** Initial unity 70; monthly update waits for `nesnd_jp_statistics_ready`. Existing terms: legitimacy>=60 +.15 / <25 -.3; SoL>=15 +.25 / <9 -.5; monthly SoL change>=.05 +.25 / <=-.05 -.4; bankruptcy -1; schools>=1 and >=3 +.1 each; bureaucracy>=0 +.05 else -.2; radicals>=20% -.4; war -.25 plus -.25 from 12 war months; diplomatic humiliation -.2; victory +.3 / defeat -.4 (C12:L9–69, C13:L36–49). Below 25, `nesnd_jp_divided_councils` applies legitimacy -5 and turmoil effects +10%; above 75, 30% monthly chance to choose a qualifying state and convert 10 percentage points of its total population toward Japanese, or `ce_wuu` for JIM's Jiangnan policy. JIM initialization adds Japanese and ce_wuu as primary cultures and marks the policy (C13:L23–28/45–82; C16:L1). These explicit conversions are also separate from natural assimilation.

**India.** Common identity initial actual variable is **25**, clamped 0–100. Education +.5 when literacy>=25% and schools>=2; representative laws +.5 when neither autocracy nor oligarchy; turmoil>25% -.5; ethnostate -.5 (C20:L2/6–10, C21:L18–24). Bar definition start_value=50 is immediately overwritten by sync to actual variable, so do not derive starting balance from that cosmetic constant (C22:L14; C21:L64–69). Dynasty delta is separate and must not receive the new unity growth.

## Native contract for the two 12-month policies

The full vanilla analogue is famine JE -> relief-kitchen button -> 12-month country expense modifier -> modifier type definition + name/description. G04:L1–8 binds G03:L1–67; G03:L20–28 sets a 12-month flag and `add_modifier { name=... months=12 multiplier=... }`; G05:L39–42 defines `country_expenses_add = 1`; G01:L481–488 declares currency formatting. G06:L69–75 shows GDP-scaled multiplier arithmetic. Its nearby comment and actual arithmetic differ; reuse syntax, not uncritically the comment or its balance.

Country modifiers can aggregate `state_assimilation_mult`. Complete vanilla chain: `je_philippines_main` G07:L182 -> `je_philippines_main_ilustrado_button` G08:L4–48 -> country event `philippines.5`, G09:L342/376–383 -> `ilustrados_education_fervor_add`, G10:L18–22 -> `state_assimilation_mult=0.1`, G01:L1814–1821. Assets/localization are vanilla: `gfx/interface/icons/timed_modifier_icons/modifier_lightbulb_positive.dds`, G10:L19; modifier label in G19:L499. Thus `state_assimilation_mult = 0.1` in the policy's country modifier is native **+10% assimilation speed**, with vanilla assimilation eligibility still governing which populations assimilate.

`state_incorporation_speed_mult = 0.1` is **state administrative incorporation** (G01:L2012–2019, G19:L2138). It is not population assimilation. There is no generic `country_assimilation_mult` found; country-assimilation keys in G02:L428–456 are specific acceptance tiers. Use the country-applied state assimilation modifier for this population-integration request. Do not silently add state incorporation or bypass homeland/acceptance restrictions. If intended player terminology is “同化”, display it accordingly; administrative “整合” is a different benefit.

- Material subsidy: country expense modifier lasting 12 months + assimilation modifier + monthly unity term; a small **primary-culture-only discrete radicalization** each month, discussed below. The subsidy is an expense mechanic; if it must raise recipient SoL in addition, `add_culture_standard_of_living_modifier` is a separate **state** effect and needs an explicit disadvantaged-culture selection/renewal/territory contract (E01:L143–145). Money spending alone does not transfer income to targeted pops automatically.
- Political-presence subsidy: `country_legitimacy_base_add=-10` and `state_assimilation_mult=.1` for 12 months, plus monthly unity term. Legitimacy key is an additive 10-point penalty, not -10% (G01:L979–985). The penalty can push Japan/India into existing low-legitimacy growth penalties; this is real interaction, not a bug to erase.
- Put expensive GDP/treasury expressions in guarded country scope, keep preview and execution numerical source identical, use has_modifier/active marker guards in **possible and effect**, `months=12`, and no cancel button. Independent types may coexist if the task permits; same type cannot refresh/stack while active. Do not use `is_decaying=yes` for a fixed-strength subsidy.
- Country-level shared monthly upkeep should apply the discrete political cost once per country per pulse, even when several JEs/old stale entries coexist. Unity growth is consumed by exactly the live owning system; never put the same radical effect in each bar/JE callback. A 12-tick cap prevents duplicate callbacks from creating unlimited cost. Native timed-expiry ordering can yield a boundary difference at exactly the end date; report only at-most-12 pulses without a dedicated engine observation.
- No player cancellation for 12 months means invalidating a JE must not refund or clear the still-active national cost/benefit just to reset its cooldown. Let the country modifiers expire, keep national cost upkeep while active; unity additions only apply to an active eligible system. If country ceases to exist the object has no surviving national budget. Any transfer of a commitment to a successor must be explicitly designed, not guessed.

## Primary-culture radicalization: exact targeting, honest approximation

**No exact native primary-culture radical-sensitivity modifier exists in the searched current modifier definitions/log.** E01:L312–314 explicitly allows `add_modifier` only on country/building/character/institution/IG/JE/movement/power bloc/state, not pop or culture. Culture-specific special modifier APIs are acceptance (country, E01:L139–141) and SoL (state, E01:L143–145); neither can serve as an arbitrary radical-sensitivity modifier. `country_radicalism_increases_full_acceptance_mult` affects the full-acceptance tier, which may contain non-primary cultures, so it fails the requested targeting (G02:L458–486). `state_radicals_and_loyalists_from_sol_change_mult` also changes both directions and all qualifying populations; it is not the requested cost (G01:L2335–2343).

The exact current vanilla primary-culture radicalization pattern is G11:L148–155:

```text
every_primary_culture = {
    ROOT = {
        add_radicals = { value = small_radicals culture = prev }
    }
}
```

That event's ROOT is a country. E01:L367–380 says `add_radicals` is country-scope, its `culture` argument filters population, and `value` is a fraction of each pop moving toward radicalism. G12:L147–159 demonstrates the analogous state-scoped variant. For a reusable monthly country effect with arbitrary callers, save the country explicitly before iterating and target that saved scope; avoid assuming ROOT from every caller:

```text
# Called once from a country monthly maintenance action while material subsidy is active.
save_scope_as = nesnd_unity_policy_owner
every_primary_culture = {
    save_temporary_scope_as = nesnd_unity_policy_culture
    scope:nesnd_unity_policy_owner = {
        add_radicals = { value = 0.001 culture = scope:nesnd_unity_policy_culture }
    }
}
```

**Suggested modest candidate balance, not vanilla-mandated:** 0.001 per monthly pulse = 0.1% of each primary-culture pop moving toward radicalism; over 12 pulses at fixed population, at most 1.2% of population in attempted movements. It is not a guarantee of +1.2 percentage points net radicals (loyalists, caps, population changes, other effects matter), and not “radicalization sensitivity +X%”. Multiple primary cultures do not multiply an individual pop's cost because a pop has one culture. Re-evaluate the actual primary-culture list each month, including JIM's two cultures. No non-primary culture should enter this effect. If the implementation applies another severity, record that chosen value and bound in its balance report.

## TUR entry and population-weighted cultural burden

Opening state-object count from C27 is 27: DOBRUDJA, EASTERN_THRACE, ALBANIA, BOSNIA, SKOPIA, MACEDONIA, THESSALIA, WESTERN_THRACE, NORTHERN_THRACE, BULGARIA, MONTENEGRO, WESTERN_SERBIA, EASTERN_SERBIA, KOSOVO, HUDAVENDIGAR, AYDIN, KONYA, KASTAMONU, CYPRUS, TRABZON, ERZURUM, KARS, EAST_AEGEAN_ISLANDS, ANKARA, DIYARBAKIR, ADANA, DEIR_EZ_ZOR. This is initialization source counting, not a current save reading. The entry condition is living TUR + `num_states >= 36`; the native country `num_states` accessor is used with a zero guard in G18:L7–19. A persistent entered marker is a reasonable design for “expansion to 36 unlocks unity”; if the requirement instead means always requiring 36, loss below threshold needs a pause/invalid policy. Do not erase accumulated unity on ordinary temporary loss without making that design explicit.

Use **population shares**, not a count of cultures nor state count weighted equally. Native E02:L9546–9556 defines country `culture_percent_country`; G13:L516–519 uses `value = "culture_percent_country(scope:culture)"`, multiplied by total_population. `population_by_culture` is **state-only**, E02:L13619–13624, so do not apply that function directly to a country. C25 already uses country -> every_scope_culture -> prev(country) -> `"culture_percent_country(prev)"` (culture) consistently; C03:L7 demonstrates the same scope nesting.

Candidate country script value pattern, requiring no transient saved culture:

```text
# One group share, with empty/dead-country guard.
value = 0
if = {
    limit = { is_country_alive = yes total_population > 0 }
    every_scope_culture = {
        limit = {
            NOT = { this = cu:turkish }
            OR = {
                has_discrimination_trait = heritage_arab
                has_discrimination_trait = heritage_berber
            }
        }
        prev = { add = "culture_percent_country(prev)" }
    }
}
min = 0
max = 1
```

E02:L10277–10287 validates `has_discrimination_trait` and `has_discrimination_trait_group` in culture scope; E01:L4689 onward validates every_scope_culture iterator. `min`/`max` mean lower/upper clamp in this project. Weighted burden = negative weighted sum of **disjoint** group shares, with weights descending in the user's order. Each individual pop contributes to one bucket; Turkish contributes zero before fallback.

| Requested bucket | Current real keys / decision boundary | Evidence |
|---|---|---|
| Turkish exempt | `this = cu:turkish`; its actual heritage is `heritage_anatolian`. Do not exempt the whole Anatolian heritage unless requested. | G16:L5990–6000 |
| Arabian/North African strongest | `heritage_arab` OR `heritage_berber` is an explicit implementable mapping. Covers maghrebi, misri, mashriqi, bedouin, yemenite, berber, bidan, tuareg. There is no native `heritage_north_african`. | G14:L53/93; G16:L6294/6409/6519/6626/6715/16727/16991/20583 |
| Han large | `heritage_han`, so includes MOD Han-derived regional cultures, not only `cu:han`. | G14:L233; C26:L295/377/459/631/770/981/etc. |
| Sub-Saharan medium | `has_discrimination_trait_group=heritage_group_african`, excluding any earlier bucket. Includes native African diaspora and Afro-Arab heritages; this is broader than geographic “sub-Saharan”. If geographic intent is literal, enumerate African heritages excluding diaspora / explicitly classify Afro-Arab. | G15:L3–5; G14:L3/13/23 and remaining African traits |
| Slavic small | OR heritage_east_slavic / heritage_south_slavic / heritage_west_slavic. Heritage is appropriate for origin; language_group_slavic would classify by language instead. | G14:L163/453/533 |
| Other least | Remainder `1 - turkish_share - classified_group_shares`, clamp 0..1; or explicit none-of-above iteration. | Derived arithmetic using E02 country shares |

**Boundary requiring explicit recorded interpretation:** `haratin` and `sudanese` have `heritage_afro_arab` (African group) and Arabic language, G16:L16358–16363/L18691–18696. Arab+Berber places them in the African-medium bucket. To interpret Arabian/NorthAfrican inclusively, add `heritage_afro_arab` (or Arabic language, which has broader effects) to highest bucket and exclude it from African medium. There is no single engine category resolving geography automatically. Recommend Arab+Berber+Afro-Arab as a stated broad Arab/North African group if the desired political distinction includes Arabic-speaking Saharan peoples. Weights themselves are task balance decisions; this report does not invent absolute penalties.

## Victory, expansion and lifecycle contracts

Native on-action roots are explicit: G17:L6230–6234 `on_wargoal_enforced`: ROOT=beneficiary country; `scope:target`=country enforced against; diplomatic_play and wargoal_impact are available. It may fire **per enforced goal**, not once per war. G17:L6988–6991 `on_war_end`: ROOT=diplomatic play, actor=initiator and target=target; actor is not automatically winner. G17:L7125–7185 `on_state_owner_change` / `on_state_created` use state scope, with current `owner`. Guard owner existence before country effects. Do not read ROOT as country in on_war_end, and do not treat any state transfer as war victory.

Current Qin: owner-change marks new owner only if its unity JE live, new-land prestige 12 months; enforced-goal marks victory 24 months with one-year cooldown (C07:L13–25). It does not register `on_state_created`, so new state object creations can differ from transferred existing state objects. Any acquisition triggers its current expansion benefit, including peaceful transfer. Japan enforced-goal sets winner +victory 24 months with 12-month lock and target defeat 12 months with 12-month lock (C15:L15–30). Those native-like locks prevent many wargoals multiplying rewards, but current code does not establish a canonical once-per-war winner record.

For TUR use actual ownership after transition and a live-country/eligible-system guard. Register both owner-change and state-created if acquisition is meant to cover splits/new states, with a shared country cooldown or a snapshot comparison to avoid double-counting. New state partition alone can increase num_states; if the user intends territorial acreage rather than owned administrative state count, that is a separate rule. Count subject states only if specifically requested; current `num_states` is own country.

Cleanup facts: Qin unity has `invalid` but **no on_invalid cleanup** (C01:L12); breakup sets dissolved before further work (C08:L500–502), which invalidates unity/uprising through C02/C01. Japan on_invalid removes divided_councils only (C10:L9–10), does not reset persistent cohesion. India society invalidates when society_live fails and has no on_invalid block (C18:L39–52). Keep subsidy costs/timers independent of these journal invalidations to honor the fixed 12-month commitment; stop bar growth when that bar no longer belongs to an eligible live country. Initialization should create missing variables without resetting existing progress or removing active commitment. Preview functions need safe defaults for absent variables and no dangling JE scope after invalidation.

## External validation cases for implementation

Check eligibility of QE1, JAP, JTK, JIM, MUG/BHT/DRA, imperial-line successor, ordinary prince, FRA/USM, and unrelated country. TUR opening 27 / 35 / 36 / 37; no pop country; Turkish-only country; each group-only and mixed shares; Afro-Arab boundary; total shares sum to 1 (within numeric tolerance) and Turkish contribution zero. Each policy: first click, repeated click during active months, both active, expiry, budget sign, negative legitimacy interaction, no-cancel path, JE loss, two JE callbacks in same country, tag change. Monthly radical targeting must emit each primary culture once, non-primary never; 12-pulse maximum and no code path uses a global radicalism modifier. Confirm bar named monthly line equals actual delta and initial sync preserves existing saves. These are source/AST/unit checks; real duration expiry, on-action ordering and modifier aggregation remain engine semantics unless reused evidence is fingerprint-compatible.

## Source fingerprints

The E sources are previously generated engine documentation, read without modifying their encoding. GAME sources remain authoritative for current examples.

| ID | Source anchor | SHA-256 |
|---|---|---|
| C01 | [common/journal_entries/nesnd_qe1_identity.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/journal_entries/nesnd_qe1_identity.txt:1>) | `920050951b575606fe7e7bc57b5965a3a18d176ece1e1446b7cf90274d3a4b68` |
| C02 | [common/scripted_triggers/nesnd_qe1_campaign.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_triggers/nesnd_qe1_campaign.txt:1>) | `7d20bc753583912fcc1280083a95ee05962cadc724aca488071c7bcbfff0fc4b` |
| C03 | [common/script_values/nesnd_qe1_identity.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/script_values/nesnd_qe1_identity.txt:1>) | `7235f8eb25af1098c4a14dd87bf192f2b4bcddcd710e7e4683fea1798559dbe7` |
| C04 | [common/scripted_effects/nesnd_qe1_identity.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_qe1_identity.txt:1>) | `33bd8f871ce7163aa3d1539a8a56a125cee153ab0408d0c6e81748aef2894e49` |
| C05 | [common/scripted_effects/nesnd_qe1_agendas.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_qe1_agendas.txt:1>) | `0e28aa113d8785afe7524de0f3ca4c5c0c18909a963f426edcc21459598427a4` |
| C06 | [common/scripted_progress_bars/nesnd_qe1_identity.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_progress_bars/nesnd_qe1_identity.txt:1>) | `de72efa886872348700742c1f46e1421e1f5f0ce85a95eb7e25782a76509003c` |
| C07 | [common/on_actions/nesnd_qin_persia.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/on_actions/nesnd_qin_persia.txt:1>) | `a214df9ea9c9e8b5a58dcf5fd65458e2ef72bbcd919dc5d788174d27ee58c512` |
| C08 | [common/scripted_effects/nesnd_qe1_fracture.txt:L500](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_qe1_fracture.txt:500>) | `11a814786835155fbe56093cf5b55ccf89e08c43936cb567202c6a7c8c892bed` |
| C09 | [common/scripted_effects/nesnd_qin_persia_lifecycle.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_qin_persia_lifecycle.txt:1>) | `d6409edf6bde440767e4e4ce07ef1d70377043abb0189966c5de4a2fd1872861` |
| C10 | [common/journal_entries/nesnd_jp_cohesion.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/journal_entries/nesnd_jp_cohesion.txt:1>) | `09745d74aef515706c4149609b38dc9af3d596f03635d95c9574c61531f3bab7` |
| C11 | [common/scripted_triggers/nesnd_jp_development.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_triggers/nesnd_jp_development.txt:1>) | `7c73e027b05b81bf7fc042a24ff69fd3449c493a27a3d1267ce2abfa3aad020b` |
| C12 | [common/script_values/nesnd_jp_development.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/script_values/nesnd_jp_development.txt:1>) | `bc9510df686d934bc66802fbf59bae283f9a8ab8ac38042a57b915e5cc8ada74` |
| C13 | [common/scripted_effects/nesnd_jp_development.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_jp_development.txt:1>) | `9c5e839f0c214bcb72d7899a44cdbbfda95f70a9047b124238e2da6c3f310a82` |
| C14 | [common/scripted_progress_bars/nesnd_jp_development.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_progress_bars/nesnd_jp_development.txt:1>) | `3be517ca466ca2e9bed8ca82db5dbcea235eca1997c55551f276642c7d22fc1e` |
| C15 | [common/on_actions/nesnd_jp_development.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/on_actions/nesnd_jp_development.txt:1>) | `aaacaa7328dee17c9513f47b5548c9ac9cbeff25502f0805c646f88274aca094` |
| C16 | [common/static_modifiers/nesnd_jp_development.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/static_modifiers/nesnd_jp_development.txt:1>) | `aae2be57dfb92473418bf3f4aec7b4936c5f93d2da43d209052dbc04f86c6f00` |
| C17 | [common/journal_entries/nesnd_japan.txt:L49](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/journal_entries/nesnd_japan.txt:49>) | `441e466d927f1ad778a3509d800d56e8f9cd1a91c94dc01978ec46c9e8209e5b` |
| C18 | [common/journal_entries/nesnd_india_core.txt:L39](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/journal_entries/nesnd_india_core.txt:39>) | `15d5f84faf514af67056797141f6aea867f10b80be35e37f18311d81bd1793d3` |
| C19 | [common/scripted_triggers/nesnd_india_core.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_triggers/nesnd_india_core.txt:1>) | `0622fab14d4db5208359b7d182fd76633926c28daa316487ac7f4fb718226548` |
| C20 | [common/script_values/nesnd_india_core.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/script_values/nesnd_india_core.txt:1>) | `558382f1b1f8992d672a728e7bbd2d034dd2a562daaa387f93c9b27872603be3` |
| C21 | [common/scripted_effects/nesnd_india_core.txt:L17](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_india_core.txt:17>) | `341792ac43044155cb518cc79944ca72b388342e1b962b9e0659e789dbacc165` |
| C22 | [common/scripted_progress_bars/nesnd_india_core.txt:L14](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_progress_bars/nesnd_india_core.txt:14>) | `09fa294596f4f2cf4cb5ad1b10537d419b593dd89771afb785800851bf9111d2` |
| C23 | [common/scripted_buttons/nesnd_india_reform.txt:L13](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_buttons/nesnd_india_reform.txt:13>) | `91cb05f6cfa7cae8191ad6404a1c80a5143f5a5346581f2157aec36a77fcf804` |
| C24 | [common/scripted_buttons/nesnd_india_diplomacy.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_buttons/nesnd_india_diplomacy.txt:1>) | `4af1617e360ded6b76f430f7eba59c1b79432c99fbb842efcf97b9cd86f80e39` |
| C25 | [common/script_values/nesnd_qe1_heritages.txt:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/script_values/nesnd_qe1_heritages.txt:1>) | `dea7f1a5c3d4229d5b6a353fc60eb522224a5c95637a88e2e119b44d97670cad` |
| C26 | [common/cultures/CE_cultures.txt:L456](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/cultures/CE_cultures.txt:456>) | `deab0fd04a418e17f063665669610d3930d1af007a513d38da6b86247fe400b0` |
| C27 | [common/history/states/00_states.txt:L131](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/states/00_states.txt:131>) | `a07cb15be572ca63c8cd1cc3706d1c78ca55f7edbc955a031bff30c00b9e1caa` |
| G01 | [common/modifier_type_definitions/00_modifier_types.txt:L481](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/modifier_type_definitions/00_modifier_types.txt:481>) | `b07822b507cdf169cc7df5edd41214857a80d95ce6ba79de7d11e688a86a6dbe` |
| G02 | [common/modifier_type_definitions/06_country_modifier_types.txt:L428](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/modifier_type_definitions/06_country_modifier_types.txt:428>) | `2833d246665a3016dbdc54e705dacdefbd6f60cacd07494f23525f2e418847b7` |
| G03 | [common/scripted_buttons/04_indian_famines_buttons.txt:L1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/04_indian_famines_buttons.txt:1>) | `f41ed2874eddbede21f182a82443af034bde3e993446d7e07ff71cc668cdec58` |
| G04 | [common/journal_entries/04_indian_famines.txt:L1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_indian_famines.txt:1>) | `d074e156bb5bf461d9152bab39ee9e8f0bad9a4da58d9d7db7bf3533d5b6d90c` |
| G05 | [common/static_modifiers/00_ip2_02_modifiers.txt:L39](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/00_ip2_02_modifiers.txt:39>) | `61c792b1ec254ccf6c03c448f7c7eae6966eab12725a5c15f67ef467119fa985` |
| G06 | [common/script_values/event_values.txt:L69](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/script_values/event_values.txt:69>) | `2bde5cecb435cf0e41ed83987e7acd72adb41578ebc39df5970f176a39469581` |
| G07 | [common/journal_entries/06_philippines_je.txt:L182](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/06_philippines_je.txt:182>) | `199e4c1620eef9d82ba8a2f9ca5e859c49e7826c65c833d68098ddfcbf54a92b` |
| G08 | [common/scripted_buttons/06_philippines_buttons.txt:L4](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/06_philippines_buttons.txt:4>) | `fdb5cb087347ce28568269f503d025aa214b3059e5f8771508897939d7bc0294` |
| G09 | [events/iberia_events/philippines_events.txt:L342](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/iberia_events/philippines_events.txt:342>) | `dbbde8588c4000fb4279c437f5deda9133c7831198de76ea9f96458c66481d42` |
| G10 | [common/static_modifiers/00_ip4_03_modifiers.txt:L18](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/00_ip4_03_modifiers.txt:18>) | `1f3b87060863700be41db2944dac7cc91c7e36d10038461eb77aefcf01abd4e9` |
| G11 | [events/balkans_events/subjecthood_events.txt:L148](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/balkans_events/subjecthood_events.txt:148>) | `e31c475b1d1513bf6df213863cb5bd8cd85287438cccb019850c53f717fc1fa9` |
| G12 | [events/paralegal_discrimination_events.txt:L147](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/paralegal_discrimination_events.txt:147>) | `b687b7c432b28efdd03510103364afcff928234387ec4eae1e0fa7bfbac0cdc9` |
| G13 | [common/script_values/ip4_je_values.txt:L516](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/script_values/ip4_je_values.txt:516>) | `b2ecefcdbb0c9fa8ebee117d04d593223abaa7cd433f83971aab79dbea5486fd` |
| G14 | [common/discrimination_traits/00_cultural_heritages.txt:L53](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/discrimination_traits/00_cultural_heritages.txt:53>) | `06d6638c64c1185a3e8a01102958bfaa5ef57a9c657bf82528cd89f4ec622443` |
| G15 | [common/discrimination_trait_groups/00_cultural_heritage_groups.txt:L3](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/discrimination_trait_groups/00_cultural_heritage_groups.txt:3>) | `fe6b455356ad6b4df783abd86a244e0bba7037060fa7321d5e07b082071de35a` |
| G16 | [common/cultures/00_cultures.txt:L5990](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/cultures/00_cultures.txt:5990>) | `30c8a1085257fb130634d3e5cc187d2eef7717a07db5fa7b390846dd319e5baa` |
| G17 | [common/on_actions/00_code_on_actions.txt:L6230](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:6230>) | `ec3e3e97140777b10d4d99f41c528ec1dc6f1499429e3e2f566b3819a36e63bb` |
| G18 | [common/script_values/je_values.txt:L7](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/script_values/je_values.txt:7>) | `9de128fb4ed48275dce3eca776ba58832840a4fde7f6f66c874f261630c2a9d3` |
| G19 | [localization/english/modifiers_l_english.yml:L499](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/modifiers_l_english.yml:499>) | `c1c8a313827a2536e6f8c61edd0ec6237585aa263ccbb46e2cd2800b2cb0d32f` |
| E01 | [effects.log:L139](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:139>) | `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1` |
| E02 | [triggers.log:L9546](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log:9546>) | `ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e` |
| E03 | [modifiers.log:L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/modifiers.log:1>) | `1d8ea1f6fb6bc0e2677d4591d45e21ef8f94ba4931074aa871583d61a63ceeff` |
