# Russian regional narrative, Victoria 3 1.15.0

Reconciled the 1836 map and sixteenth-century Western Qin settlement with the retained regional journals. Only the two new language replacement files were written in the MOD. Checked source and localization offline. No game launch or Git operations.

## Sources and scope

Read the effective native and modded Russian journal sources, the Persian Eastern Frontier, Tsar frontier development, the four event families, linked buttons, custom text, outcome tooltips and notifications. The source manifest covers eight journal roots, 93 source records and 587 associated bilingual keys, including shared labels and country names. The native scoring master itself is outside these regional overrides.

- `je_the_eastern_border`
- `je_caucasian_war`
- `je_circassian_expulsions`
- `je_pacify_the_steppes`
- `je_the_last_kazakh_khan`
- `je_conquest_of_central_asia`
- `je_eastern_frontier`
- `je_tp_pool_develop_frontier`

The map sources are common/history/states/00_states.txt and common/history/diplomacy/00_subject_relationships.txt. OZH is the actual Russian protectorate in the north. Kazakh culture can exist under another owner. Bukhara, Khiva and Fergana are places within Western Qin’s historical sphere, not three starting diplomatic actors. BKH is Bukey Orda, distinct from BUK. Russian and Circassian holdings in Kuban and Russian and Imamate holdings in Dagestan support the separate Caucasian war narrative.

Read the independent pre-update source (backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml lines 118, 136, 179 and 194). Retained its distinction between interested parties, actual power and claims. Mechanics use direct conditions. The adapted event flavour is unquoted and avoids attributing invented words to historical people.

## Results

- Russian eastern border and its three treaties: 6 pairs.
- Steppe pacification, khanate and settlement: 11 pairs.
- Russian approach to Central Asia: 9 pairs.
- Persian Eastern Frontier, Merv and eastern conquests: 11 pairs.

37 pairs changed (74 localized entries). The Caucasian War and Circassian expulsions preserve their actual local participants and agendas. The Tsar frontier-development journal describes existing Russian administration and its completion credit; it does not assert Central Asian sovereignty. These three roots needed no narrative replacement. Persian proceedings, requested resettlement and local conditional events remain available after actual territorial changes. Peaceful steppe consolidation no longer reports an execution. All three border proposals describe an eligible Chinese government holding its own parcel and do not identify Western Qin or the northern court as the automatic donor.

Both lobby records retain native DLC labels. The Persian captive passage retains its clickable resettlement explanation. Revolt and settlement previews are aligned to the regional compatibility candidate, including the land source, the greater-than-60 trigger, the exemption for Bukey Orda and the restricted local-claims outcome.

## Verification

Checked paired key sets, native-key existence, unique MOD definitions per language, UTF-8 BOM, physical lines, quote and bracket structure, bound-scope parity, alias and tooltip resolution, and serialized output against the final draft. Source inventory, per-key before/draft/final analysis, retained keys and file hashes are recorded in russian-frontier-audit.json and russian-frontier-writing-comparison.json.

## Changed keys

- `je_the_eastern_border_reason`
- `je_the_eastern_border_treaty_of_aigun_desc`
- `je_the_eastern_border_treaty_of_beijing_desc`
- `je_the_eastern_border_russia_chuguchak_protocol_desc`
- `russo_chinese.2.d`
- `russo_chinese.2.f`
- `je_pacify_the_steppes_reason`
- `je_pacify_the_steppes_lobby`
- `je_the_last_kazakh_khan`
- `je_the_last_kazakh_khan_reason`
- `kazakhstan_events.1.d`
- `kazakhstan_events.1.f`
- `kazakhstan_events.3.d`
- `kazakhstan_events.3.f`
- `notification_kazakhstan_ride_of_kenesary_notification_desc`
- `je_conquest_of_central_asia_reason`
- `je_conquest_of_central_asia_lobby`
- `russian_central_asia.1.d`
- `russian_central_asia.1.f`
- `russian_central_asia.2.t`
- `russian_central_asia.2.d`
- `russian_central_asia.2.f`
- `je_conquest_of_central_asia_turkmen_button_desc`
- `russian_central_asia.3.d`
- `je_eastern_frontier_reason`
- `greater_khorasan_button_desc`
- `persian_baluchistan_button_desc`
- `persia_resettle_merv_button_desc`
- `persia_events.1.d`
- `persia_events.1.f`
- `persia_events.3.d`
- `persia_events.3.f`
- `persia_events.5.d`
- `persia_events.5.f`
- `persia_events.2.d`
- `event_effects_kazakhstan_events.1_tt`
- `event_effects_kazakhstan_events.3_tt`
