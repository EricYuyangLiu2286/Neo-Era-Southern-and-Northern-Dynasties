# Standards review — journal bug sweep

Review basis: `pre-change-journal-bug-sweep-20261104T005112Z/mod` → `journal-bug-sweep-20261104-a`, using `git diff --no-index`. GAME 1.13.11 / build 24799966; catalog CURRENT. Standards: main AGENTS.md, docs/agents/engineering-skills.md, NESND syntax/reference safety, journal text and numeric contracts, player-writing skill. This is a snapshot review, with the candidate still being assembled.

## Confirmed issue in the current snapshot

**P2 — Two Japanese buttons put the AI field in effect scope.** `common/scripted_buttons/nesnd_jp_politics.txt:50` and `:76` (`nesnd_jp_inspect_military`, `nesnd_jp_inspect_representative`) close the `if` and `hidden_effect`, then place `ai_chance` before the closing `effect` brace. This makes `ai_chance` an invalid effect and removes its original button-level meaning. The court button closes the new wrapper correctly. Close `effect` before `ai_chance` and remove the later extra closing brace. Rule: NESND `references/syntax-and-routing.md`, “作用域是 API 的组成部分” and preserving directory/context-specific API shapes. This is a field-scope error, not an indentation preference; the normal parser/Tiger pass should also catch it. Already sent to the implementing agent.

## Other inspected changes

- Qin settlement uses guarded economic/military victory predicates, preserves ten-year rewards and one-time closure, and does not require the completed JE to remain active. No new reward-lifecycle issue found.
- The Japanese funding preview and execution use the same bounded cost formula and six-month modifier. Current GAME `common/scripted_buttons/03_brazilian_amazon_scripted_buttons.txt:50` supports `show_as_tooltip`; effects still recheck eligibility.
- India waiting/cooldown/aid NOR blocks preserve the original conjunctions of NOT conditions; the foreign-country branch retains explicit false on missing objects.
- GAME `gui/journal_entry.gui:580` assigns gold to `noprogresstexture`; therefore the negative endpoint/right gold appearance is consistent with the current native rendering. No arbitrary sign reversal is justified by the color alone.
- The later southern completion labels preserve the original hidden victory predicate, and the accord button retains its execution effect inside `hidden_effect`.

No actionable Fowler smell; repeated Jomini option/database shapes are not OO design defects. Candidate content, localization/source records and pin changes were still incomplete during this pass. **One confirmed issue remains; this is not final release sign-off.** No game or UI was opened, and no gameplay files were edited.

## Extended-scope review

The initial button field-scope issue is closed. The twelve shared Japanese request previews now show the same bounded treasury cost plus a stable request explanation, while retaining the guarded original execution. The nine weaker candidates were not mechanically rewritten.

Reviewed against the completed task31 spec, including the PER resource/claim system and USM western-province mechanism. Three documented-standard issues remain:

1. **P2 — PER sync reads a temporary scope without a preview guard.** `common/scripted_effects/nesnd_per_resources.txt:5–14` saves `nesnd_per_resource_owner`, then dereferences it under only `has_journal_entry`. These effects are reachable from buttons; preview does not execute the preceding save, and `hidden_effect` does not establish an existence boundary. Protect both sync functions' reads with an independent `exists = scope:nesnd_per_resource_owner` branch, or use an independently valid JE owner. Rule: NESND `syntax-and-routing.md`, reference safety §§1–3.

2. **P2 — Native victory hooks do not prove the intended annexation.** `common/on_actions/nesnd_usm_western_provinces.txt:4–12` integrates every qualifying USM mainland state for any enforced demand/capitulation against a country retaining `usm_opposition_country`. An old opponent's later unrelated capitulation or non-territorial demand can therefore integrate unrelated later conquests. Restrict the hook to the actual relevant civil-war annexation/ownership transfer, ideally preserving the transferred state set. Rule: source-first complete-chain and callback scope/identity requirements; this batch's `usm-native-contract.md`, “吞并后整合：state scope及地域约束”.

3. **P2 — Automatic JE entry can bypass legacy migration.** `common/journal_entries/nesnd_usm_western_provinces.txt:6` uses eligibility without a migration gate. An old post-1850 save with all three states already incorporated can activate the JE, whose completion is date-blocked and failure already true, before weekly maintenance at `common/scripted_effects/nesnd_usm_western_provinces.txt:28–34` preserves that old success. Route automatic/explicit entry through the same migration preparation so callback order cannot select punishment versus preservation. Rule: NESND `journal-text-contract.md`, “非开局入口、终局回调与镜像条” and initialization/recovery contract.

The 37 claim buttons retain target revalidation and one-time resource expenditure; grant limits and clamp match the spec. The 15-cohort SoL function reuses the recorded native-impact estimate, samples before charging, affects radicals only, and expires snapshots; it remains an approximation, not an exact native SoL hook. The native event copy differs only at the two guarded law checks. Writing documentation is announced as pending and still needs final verification. No actionable smell or engine-verification claim.

## Correction closure

The three extended-scope findings are closed in the inspected revision:

- PER sync reads the country via each existing JE's `owner` and the safe resource script value; the temporary saved-owner dependency has been removed.
- USM native victory handling now requires an unsettled southern campaign and a dead opposition target. The scripted annexation paths separately check actual target death before integration, with the guarded total-victory event providing the final fallback. Routine non-territorial demands against living former opponents no longer invoke integration.
- Western eligibility requires the migration marker. Maintenance evaluates the old post-1850 incorporated-state preservation branch before any automatic or explicit JE entry can pass.

All twelve Japanese request adapters were independently token-compared: their `hidden_effect` bodies preserve the corresponding pre-change `effect` bodies exactly, ignoring whitespace/comments. Every displayed fee is `nesnd_jp_negotiation_cost * -1`, matching the shared helper's actual deduction. Chinese and English request text match the helper's 45-day validity and six-month cooldown; the request is sent one day later, without extending its stored clock.

**Remaining code-standard findings: 0. Four recorded code findings are closed; no actionable smell.** Final writing-evidence verification remains pending because `writing-comparison.md` has not yet been supplied. Native callback/annex ordering and rendered UI remain ENGINE_NOT_RUN; this closure certifies source structure only.

## Final closure inspection — code complete, writing binding pending

Remaining code findings: **0**. The initial field-scope defect and all three extended code findings remain closed. The latest additions were reviewed: scripted annexation samples the defeated country's mainland holdings before transfer; integration follows confirmed target death and the sampled flag; native hooks additionally require actual enrolled-round history. Western failure requires an opened instance, invalidation records a permanent archived/finished result, and neither exit repeats the four-culture penalty. Each Persian frontier JE now checks its own route before invoking the shared monthly writer, closing the late-invalid-instance double-tick path. External JE pinning is a default setting, not a periodic override.

The two remaining release-record items are:

1. **P2 — Numeric explanation omits the hostile-relations lower bound.** `writing-comparison.md`, “数值节奏”, says peaceful/fiscally sound governance growth is 1–3 per month. With QE1 relations <= -25, the actual base 1 minus 0.5 is 0.5 without either development bonus. Correct the stated range to 0.5–3 (20 points approximately 7–40 months; 40 approximately 14–80), or explicitly restrict the example to non-hostile relations. Rule: numeric-scale-contract.md §§2–4, source estimates and representative extremes.

2. **Writing evidence refresh announced but not yet present.** At inspection, writing-keys.json has 126 rows: the 45 PER/USM English rows retain their old line/SHA after Chengdu was inserted. referenced-existing-texts.json still names the old English STATE_SICHUAN='成都' row as effective. Refresh the 127-key final set and effective reference, and record the author sample-file SHA alongside its existing path/key/lines. This is an evidence-binding gap; the inspected new Chengdu text itself is correct.

No new gameplay defect or actionable smell was found. Writing categories, revision decisions and source/effect comparisons are otherwise present. The final byte fingerprints of this inspected candidate are in `standards-reviewed-hashes.json`; later localization or whitespace edits require their own refreshed delivery fingerprint. No game was opened; native callback order, SoL approximation and rendered UI remain outside this source review.

## Final Standards conclusion — all findings closed

**Remaining findings: 0 (code 0; writing/release evidence 0).** The two remaining release-record items are closed: the peaceful governance range is correctly documented as 0.5–3, with 20/40-point timelines of approximately 7–40/14–80 months; the author and two native English source hashes are explicitly linked and independently verified.

Final writing binding was independently checked: all **127 changed effective entries** and **9 referenced existing entries** match their candidate file, line, text and SHA-256. English STATE_SICHUAN resolves to the new **Chengdu** entry. All **46 changed gameplay/localization files** remain byte-identical to `standards-reviewed-hashes.json`; that reviewed fingerprint is retained unchanged.

This is the final Standards-axis source review for the candidate `journal-bug-sweep-20261104-a` against the recorded pre-change snapshot. No actionable Fowler smell remains. The result does not claim engine/UI verification, exact native SoL-event reproduction or verified callback timing; no game was opened.
