# Live DP schema repair

Source/run: main9cdfd02 reported actually running by parent. Log read at2026-11-05 05:07:24UTC; actual two script writes finished05:08:50UTC. Executor GPT-6.1 Sol / medium. No game start/stop or console command issued.

The supplied engine log has exactly two parser failures at05:00:01, lines53–54: unexpected `handle_annexation_as_civil_war` in American restoration effects354 and native khanate effects186. Both creators supplied this field as `no`. All analogous MOD field uses are exactly these two; current GAME text search finds no use.

Native full chain checked: GAME `common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:474` uses country initiator + explicit `target_country` and dedicated DP; `events/japan_events/ep2_ezo_republic.txt:89` starts normal annex play with target and reverse goal; `events/heavenly_kingdom_events.txt:507` creates dedicated rebellion DP. `common/diplomatic_plays/00_diplomatic_plays.txt:939` normal annex DP supplies annex goal with no civil-war override, while its actual revolutionary play checks revolutionary actor and `civil_war_origin_country` near542. Our native countries are made by state-based country creation and own custom DP/goals; no actual revolutionary/civil-war constructor is introduced. Thus preserve normal annex semantics by omitting unsupported false override, not replacing it with a different geopolitical mechanic.

Cached engine-docs1.13.11 effects.log909–922 advertises this token (and stale implicit-target schema). The actual current1.13.11 executable rejects it. Cached generated help is therefore insufficient schema authority here; current native examples and returned engine parser take precedence. This corrects our earlier reliance on that documented optional field.

Exact repair: remove only ` handle_annexation_as_civil_war = no` once in each of the two effects files. Keep initiator execution scope, target_country, name, type, `war=yes`, retries, receipt filter, goals, target roles, annex/settlement and countries unchanged. No BOM change. Current running process loaded pre-fix scripts; disk fix is pending actual subsequent engine load.

Separate evidence directory retains before/after subsets, exact unified diff, old engine failure excerpt and after hashes. `verify_repair.py` checks actual ordered source AST creator fields and exact whole-file byte delta (no invented simulator). Original2 unsupported fields→candidate0, two source files parse. This is static regression plus real pre-fix engine evidence, not post-fix ENGINE_PASS.

Excluded from this narrow repair: unrelated global/model/unused-variable warnings, preexisting duplicate JE warnings, Egypt missing action localization, hidden regional legacy events, and original source encoding warnings. Parent may triage them separately. The original frozen StageB candidate and snapshots remain untouched by this new live repair evidence.
