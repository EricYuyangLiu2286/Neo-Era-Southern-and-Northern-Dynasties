# Independent cross-review: small states and Native Americas

Reviewer: `/root/astra_english_civic_phi`, configured `gpt-6-astra / high`, explicitly confirmed by parent. Assignment: read-only independent review of the other writer's two frozen English files. No localization or gameplay edits made in this review.

## Result

No blocking translation, omitted-paragraph, cultural-agency, number or outcome-branch defect found in the reviewed English. All 410 current Chinese and English entries were read, including retained entries. The author's report and comparison JSON were used as an inventory; this conclusion comes from reading the actual files and the script paths below, not from accepting the author's PASS statement.

The 95 small-state and 53 Native Americas rewrites restore the Chinese's social and political causation. I found no remaining long paragraph that simply retains the old abbreviated summary. The repeated diplomatic tooltips are appropriate shared actions. The longer events retain different actors and interests instead of repeating one stock conclusion.

One optional terminology polish remains in two retained Native Americas UI strings:

| Key | Current | Suggested | Reason |
|---|---|---|---|
| `nesnd_ui_restoration_no_dispute_tt` | Is not involved in a native restoration dispute. | Is not involved in an Indigenous restoration dispute. | Uses the file's established English term for 原住民 and avoids the other modding sense of “native”. |
| `nesnd_ui_restoration_native_population_tt` | The country still has a native population. | The country still has an Indigenous population. | Consistency with all surrounding population and movement descriptions. |

These are minor wording suggestions, not incorrect gameplay claims. No required correction is requested. Root retains final editorial judgment.

## Direct checks and judgments

### Small states: all 216 entries

- Read the complete paired files. Reasons for livelihood, economy, governance, regional economy, regional governance, order and dispute recover the Chinese's relationships between household income, taxation, services and political expectations. The translation does not introduce a foreign patron as a prerequisite for autonomy.
- Read `events/nesnd_small_states.txt:12-35`. Regional `.2` and `.6` descriptions require the matching far-south/Burma/Siam category, registered regional targets, no generic-region override and valid targets. The Australia/New Zealand and Upper/Lower Burma assertions are therefore not applied to generic reselections. The generic `.2.d` and `.6.d` remain geographically neutral.
- Read `common/customizable_localization/nesnd_small_regions.txt` and `common/scripted_triggers/nesnd_small_states.txt:76-130`. Current regional readouts name the whole registered group and state that market access is measured by population residing in states at 80% access. The required 75% regional coverage is not mislabelled as a single anchor state's market-access percentage. Far-south port employment remains 50% in each group.
- Read `common/journal_entries/nesnd_small_states.txt` and the monthly implementation in `common/scripted_effects/nesnd_small_states.txt:125-174`. Qualifying months are cumulative, not consecutive. Paused status correctly says the count does not increase. `.5.d` is reached by deadline expiry, so its “Years have passed” does not invent elapsed years for an immediate status-change cancellation. Existing schools and industries are not described as removed.
- Read `common/scripted_effects/nesnd_small_diplomacy.txt:1-85`. Autonomy, independence, market and defence descriptions match the four request kinds. Five-year defence treaties are created only after accepted requests. The thirty-day market failure clears request bookkeeping and announces failure; it does not revoke the grant-own-market pact. The English promises no such revocation.
- Read `events/nesnd_small_states.txt:36-60` and `common/scripted_effects/nesnd_small_politics.txt:41-111`. Organising versus suppression correctly distinguishes 1% and 2% radicalisation, and the respective 12-month terms. Five reform promises have 24-month deadlines, correct law families and +2 Approval. The success event follows enacted reform; the failed promise event requires both expiry and a still-live grievance. English avoids describing a mere promise as immediate legislation.
- All domestic political prose uses government, provinces, local communities and movements appropriately. It does not import an Assembly of Rites or Chinese court into Burma, Siam or generic small states.

### Native Americas: all 194 entries

- Read the complete paired files. The monarchy/community compact, land grievances, exodus, refugee settlement and khanate arguments preserve the current Chinese positions. “Court” is used for the Inca/Andean dynasty, “khan” and “Plains Compact” for the defined khanate, and “republic” for the authored republican states. No new historical quotation is claimed for the Earth Mother option.
- Read `common/scripted_effects/nesnd_a2_manchu_exodus.txt` directly. The 70/30 choice is per source population community, not a promise that exactly 70% of all people migrate one way. Each of the four descriptions matches both destinations, CNE only, USA only or neither. The inactive generic `.2.d` remains a fallback; actual outcome descriptions were separately reviewed.
- Read `common/scripted_effects/nesnd_american_restoration.txt:145-173`, `events/nesnd_american_restoration.txt:40-94`. Existing Inca court recognition is a 90-day invitation, not an immediate annexation. Acceptance annexes the applicant into the receiving court's country. Expiry and refusal descriptions preserve separate states and the possibility of later negotiations. They do not claim signed agreements were cancelled.
- Read `common/scripted_effects/nesnd_american_restoration.txt:405-425,481-502`. Unification is confirmed after the opponent loses all states and the original enemy territory is actually owned. A disappeared opponent without ownership of all its recorded land reaches the external-end event instead. `.5.d` and `.6.d`, and the corresponding notifications, preserve this distinction: victory/annexation versus interrupted conflict without complete acquisition.
- Read `events/nesnd_native_khanate.txt:16-28` and `common/scripted_effects/nesnd_native_khanate.txt:218-225`. The `.2.both`, `.2.one` and `.2.none` descriptions separately distinguish two, one and zero humiliation outcomes. The zero branch does not claim a battlefield victory. The survival event follows both outcome values becoming nonzero; the old unused `.2.d` was not treated as evidence that the active branches were fixed.
- Read `common/scripted_effects/nesnd_native_khanate.txt:157-178`. The intervener withdraws whole treaties binding itself and NKH if they contain alliance or defensive-pact articles. Other articles in those treaties disappear with them, and break penalties are applied to the withdrawing country. `.4.d` accurately describes these effects, without claiming every treaty with every country was cancelled.
- Mobilisation text preserves twelve months and the 75 pressure threshold. Event `.14` remains a preparation notice, not an assertion that war has already begun. The waiting, ready and war-started texts are separate.

## Boundary

This is an independent localization/editorial and script-contract review. It does not certify engine execution, gameplay balance, rendered line wrapping or every underlying script implementation. No game was launched. No source edits were made. Existing source assertions about history and political motives remain authored setting, not facts newly derived from runtime evidence.

Snapshot identity and comparison-integrity evidence follows.

```json
[
  {
    "file": "D:\\Users\\Eric Liu\\Documents\\Paradox Interactive\\Victoria 3\\mod\\Neo-Era Southern and Northern Dynasties\\localization\\english\\replace\\nesnd_small_states_l_english.yml",
    "entries": 216,
    "after_map_matches_comparison": true,
    "bilingual_key_set_matches": true,
    "English_SHA256": "21097fbc25530921cce098fa24c0c2206d1f9685a552bfc201c6b49f11a62ffe",
    "matches_report_hash": true,
    "Chinese_SHA256": "f6447d46d1b92b3835afb39632ad6c1e528b7b285578fe554c326dd5846ddefb"
  },
  {
    "file": "D:\\Users\\Eric Liu\\Documents\\Paradox Interactive\\Victoria 3\\mod\\Neo-Era Southern and Northern Dynasties\\localization\\english\\replace\\nesnd_native_americas_l_english.yml",
    "entries": 194,
    "after_map_matches_comparison": true,
    "bilingual_key_set_matches": true,
    "English_SHA256": "f11b41803d28ecac39eb883bd20c4b06655c6a01299cb0f4a9b2f192f9b0bb0a",
    "matches_report_hash": true,
    "Chinese_SHA256": "5ea527456d54a8bbae81275fa2e216fb89db218cad550a62757af4e4b4dc3f89"
  }
]
```
