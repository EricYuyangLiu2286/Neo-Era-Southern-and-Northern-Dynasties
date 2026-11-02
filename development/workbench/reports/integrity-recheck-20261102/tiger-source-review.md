# Tiger source review appendix

Reviewed 974 diagnostics from `global-before/tiger_raw.json` against installed 1.13.11/build24799966. Exact paths, source hashes, ancestry and all 26 character corrections are in `tiger-source-review.json`. M = main MOD; G = current native game; D = WORK/references/engine-docs-1.13.11-20261031. Read-only; no engine validation.

## Three error dispositions

- **Enum tool gap:** M `common/war_goal_types/nesnd_usm_annex.txt:6` exactly matches G `00_annex_country.txt:19`; ten native goals use `control_half_target_country_states`. Keep.
- **Native-supported flow discrepancy:** M `common/company_types/zz_nesnd_fujian_company_location.txt:33` preserves G `00_companies_china.txt:214–217` verbatim. D `modifiers.log:1503–1506` confirms ship mask, but does not document propagation. Do not delete the naval bonus merely to satisfy Tiger; propagation remains unobserved.
- **Confirmed inherited native no-op:** M `common/ai_strategies/00_default_strategy.txt:5610–5615` equals G:5606–5611: empty Russia branch followed by unconditional +500. Retain behavior; moving that weight is a policy change.

## High-confidence warning findings

- **26 wrong character→IG links:** 22 in `common/scripted_effects/ce_french_empire_journal_effects.txt`, four in `ce_japan_gov_effects.txt`. `ig:` requires country/political-movement (D `event_targets.log:335–339`); character `owner` returns country (:451–454). `set_interest_group` expects an IG (D `effects.log:36979–36983`). Resolve through actual owner, with existence protection for preview/exile lifecycle.
- **393 reports, three underlying references:** M/G `common/scripted_triggers/00_ai_triggers.txt:146–148` reads JE-local Donghak scopes from global law AI evaluation. Only producers are G `common/journal_entries/03_korea.txt:109–137`. Parallel `has_journal_entry` does not protect missing objects. Preserve the three intended law identities when fixing.
- **Law/type mismatch:** M/G `00_ai_triggers.txt:123` compares law-valued `imposed_law` to law-type-valued `scope:law.type`; compare like scopes.
- **Five missing CoA references:** `BUN_subject`, `JAP_theocracy`, `TSW`, M/G `common/flag_definitions/00_flag_definitions.txt:1821,5597,5608,10076,10077`. No definitions in native, main MOD or EACR. These are static references; no replacement invented.
- **Duplicate cancellation:** `events/ce_fra_unrest_events.txt:1064,1117` defines `fra_unrest.10.cancellation_trigger` twice. Preserve both parent-JE and object-lifetime checks in one guarded block.

Explicit tool gaps: formation `is_on_front`, culture heritage comparisons, and state-region `supply_hub` are supported by generated docs. Remaining warnings retain their uncertainty; inherited/native similarity is not blanket clearance.
