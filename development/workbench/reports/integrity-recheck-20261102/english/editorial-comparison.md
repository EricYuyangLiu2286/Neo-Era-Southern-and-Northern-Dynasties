# English editorial review

Drafts only; no game files were changed. `editorial-parity.json` is the application manifest, with target paths and source/draft SHA-256 values. The requested Qin/Persia file is at this directory's root; other drafts mirror their MOD-relative paths.

## Coverage and boundaries

- All 205 Qin/Persia keys were read and reviewed. The source contained 184 Chinese values; the draft contains none. Key order and dynamic expressions are unchanged.
- Fourteen recent CNE/USM override files received targeted prose edits. All keys in the supplied files have individual decisions in `editorial-key-review.json`; unchanged English is retained, including original event quotations.
- The independent Poland supplement supplies all seven missing English keys. A separate six-key draft translates the existing South Dayuan labels without changing their referents.
- Seventeen draft files contain 720 keys in total, of which 281 differ from source or are supplements. `coverage-inventory.json` inventories the wider NESND English files, including Chinese fallbacks in earlier supply, external-aid, Philippines and crisis text. Those files are outside this targeted draft and are not certified translated.

## Source-led editorial decisions

Twenty source samples, their exact keys/lines, full text and SHA-256 values are recorded in `editorial-sources.json`. Author samples come from the skill's approved `pre-update-20261030T233944Z/mod` baseline, not current AI overrides. Native samples come from the installed 1.13.11 game.

| Field | Source and observed practice | Before → draft decision |
|---|---|---|
| Political JE | Author `ce_cne_events_l_simp_chinese.yml:15`, `ce_usm_events_l_simp_chinese.yml:118`; native `content_3_l_english.yml`, `je_sick_man_bureaucracy_reason` | Preserve institutions, interests and historical causes. Qin's court dispute becomes a contest between reformers and military leaders, rather than an implementation checklist. |
| Imperial reform | Author `flavorCNE.3.d` and `flavorCNE.4.d`; native `je_french_foreign_legion_reason` | The Qin/Persia prose retains land, revenue, appointments and military ambitions. CNE civil-war text no longer reduces the land revolution to surveys and resettlement. |
| Buttons | Author `ce_french_support_dynasty_button_desc`; native reform journal phrasing | “Withdraw the benefits and military opposition associated with…” → “Suspend the reorganization of military estates in…”. Costs remain in the actual effect tooltip. |
| Status and conditions | Native `je_sick_man_syria_status`; project journal-text contract | “elapsed-time guard”, “monthly calculations”, “preparation snapshot” → months of compliance, continuing reform, and national preparations. Numerical gates remain exact. |
| State transfer | Current earlier-AI Ming tooltip, checked against its existing information | “that same character takes the throne” → “establish a monarchy under that ruler”. Existing forces, treasury, lands and tax system remain stated. |
| Reward | Native law/IG/SoL terminology; project numeric-scale contract | “loyalist momentum” → the effect on Loyalist growth. The 15%/10% relative bonuses and ten-year duration remain, without claiming population-wide conversion. |

World names follow original English `QE1_monarchy`, `dyn_c_per_han_regime` and `ce_xiyu`: Western Qin, Tang-Persian Empire, Western Regions Han-Qiang. New faction labels are Reform Faction/reformers and Military Faction; they describe the existing agendas. No new effects, thresholds or events were added.

## Parity and disclosure

Every draft has UTF-8 BOM and an `l_english:` header. Existing files retain their exact key order; dynamic expressions, dollar substitutions and icon tokens have zero differences. All numerical tokens match except two copies of `nesnd_south_pressure_detail_tt`: their unconditional forecasts of the assassination's dates and outcomes were removed to honor the instruction not to reveal untriggered plot developments. Current pressure, monthly change and the 70/100 succession thresholds remain. These exceptions are explicit in the parity report and require root review before application.

No original author English file was rewritten. These are editorially reviewed proposals, not proof of in-game layout or event execution.
