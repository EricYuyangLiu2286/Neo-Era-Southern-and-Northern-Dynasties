# Standards integrity recheck

Scope: `git diff 044de73...870639a`; commits cf6ec2f, c0e11fe, 7d39018, 870639a. Reviewed active main MOD; fingerprints in standards-fingerprint.json. Native catalog is CURRENT: 1.13.11 / 24799966.

## Confirmed findings

No newly introduced Standards defect confirmed in this review.

**Inherited completeness omission (P2, English only):** seven active Poland localization keys are absent from both MOD/native English. `common/scripted_buttons/ce_poland_scripted_buttons.txt:13,100,1194,1232,1325,1405` references `ce_polish_script_bar_tt_{100,20,50,5,10,15}`; `events/ce_poland_events.txt:93` applies modifier `ce_backoff_on_territorial_claims`. Chinese definitions exist in `localization/simp_chinese/replace/ce_poland_l_simp_chinese.yml:89–94` and `localization/simp_chinese/replace/zz_nesnd_existing_modifier_labels_l_simp_chinese.yml:3`. Baseline 044de73 already contains these references and Chinese-only definitions. Violates NESND skill's bilingual-key parity rule; repair as existing English resource debt, not a regression caused by this diff. No new wording/design is required to restore parity.

## Checked closure

Independently parsed 71 changed common/events files and current native/MOD symbol databases. Found no missing scripted helper, technology, country, culture, religion, law, static modifier, journal, button, progress-bar, or literal gfx-file references in that set. Checked 488 explicit localization references with variable/bar identifiers excluded; only the inherited omissions above remain.

The reported CNE calls resolve to actual definitions at `common/scripted_triggers/nesnd_cne_programs.txt:250,253`. Existence alone does not diagnose CW262; root review owns the running CWTools investigation.

Native scope checks: `GAME/common/on_actions/00_code_on_actions.txt:10–13,3146–3148,6230–6234,7131–7138` corroborate lobby none-root, ruler character-root, war country-root, and state-owner callback usage. Native `common/journal_entries/journal_entries.md:42–44` corroborates country JE immediate scope; `gfx/media_aliases/media_aliases.txt:347–348` supplies the referenced contract video.

Standards: project AGENTS and engineering-skills; NESND syntax-and-routing/journal-text-contract. Repeated Jomini blocks were retained as semantic data, not flagged as OO smells. Optional absent JE status keys were not promoted to defects: numerous current native JEs use the same omission.

Boundary: source/reference review only. No game run, no engine verification, no blanket certification of every MOD behavior.
