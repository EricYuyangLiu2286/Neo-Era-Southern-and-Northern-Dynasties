# Batch B implementation — repaired freeze ready for retest

Revision B-r2-country-supply; frozen 2026-11-04T13:07:11.605914+00:00. Gameplay editing is now STOPPED. The organizer already authorized sequential retesting after this freeze. No tests ran while this repair was edited.

Original core unity/policy/law-group changes remain as described in the archived first implementation. The repair is bounded to:

- Country-scoped TUR has_claim=prev, guarded for missing/dead TUR, with the state_region unchanged as prev. Existing72 claim targets,25-point cost and ownership/Egypt restrictions remain.
- Country military-reform modifiers now include unit_supply_consumption_mult−.20/−.25/−.15 in the three approved tiers. Actual native paraguay.6 executes the same interface on country; current19combat-unit types include infantry/artillery/cavalry/marines, while21ship types use separate materiel/upkeep definitions. Marine battalions are included; fleet-ship upkeep is outside this source-supported unit scope. Runtime goods orders remain unmeasured.
- Old three building supply definitions are inert compatibility shells. The existing state helper only removes old attachments with guards; no branch adds them and new-building/state-created attachment hooks are gone. Timed country benefits expire together. The pending/term callback safety remains.
- Military button native modifier previews carry the supply amount once. Three redundant custom amount tooltip calls/keys were removed. The action description clarifies battalions including marines. Current B localization137keys per language.
-21approvedtxt BOM targets normalized. Previously unchanged recovery triggers/values/modifiers/bar are included in the new34-file freeze.

Exact hashes: batch-b-freeze.json. Source proof: batch-b-repair-plan.md, batch-b-repair-source-hashes.json and batch-b-military-source-inventory.json. Editorial delta: batch-b-writing-comparison.md. Original150-warning failure, first freeze and old independent test snapshot remain preserved in batch-b-first-freeze-evidence/ and the original snapshot path.

No game launch. No claim of engine runtime verification.

| File | SHA-256 |
|---|---|
| `common/journal_entries/nesnd_india_core.txt` | `c6901de919fffe76f73479acb2621b56aab630722f58be7963cd1b08d5f298c7` |
| `common/journal_entries/nesnd_jp_cohesion.txt` | `aa442b68360bc6914305c250bf10b187a03ebff3bd2b5c2b8eee4c9f20128540` |
| `common/journal_entries/nesnd_ottoman_recovery.txt` | `52bfc26cb2bbc6a9505628f513e8f8877c04760ef53a073d27c4eb3c93956aa3` |
| `common/journal_entries/nesnd_ottoman_unity.txt` | `61e3251170764b1ffa504345389bba9f34631c679b8b2a0c302f70b87305acfd` |
| `common/journal_entries/nesnd_qe1_identity.txt` | `feb9996604bcf4f16c9420dffaca86fcb1967682922e30202709041550917c20` |
| `common/on_actions/nesnd_ottoman_recovery.txt` | `d8ef8e7746533a574b1da2a9599e704736f784a41e1ef7745151018eba0eb0d1` |
| `common/on_actions/nesnd_ottoman_unity.txt` | `8c81fef4553bf093d7cb50edbfcddec158385a1d64934d33a7f4d3cfd68d3787` |
| `common/on_actions/nesnd_unity_policies.txt` | `6622b18e3f1c521e340bb733198d25f722f506c634aa2fc66daf160a05088f1c` |
| `common/script_values/nesnd_india_core.txt` | `5e897f016decfae7603a660bd53e3d86b03857cedd836b6b5c0c6cfa46d89c6b` |
| `common/script_values/nesnd_jp_development.txt` | `d348f2e38785b23daeced592cd3114956621b1bbde1b5f23142d1c4fbd059551` |
| `common/script_values/nesnd_ottoman_recovery.txt` | `2698af90b1f329cb32ce992b11104c1b5a7f16d79d33bbf3f5962ebaced0cc61` |
| `common/script_values/nesnd_ottoman_unity.txt` | `62ceb0265ed9bb883528417ed2294802b1875d3ecf2915f9f870f7b63b41f8e8` |
| `common/script_values/nesnd_qe1_identity.txt` | `9e511e47cf3891b26ae38c8f2155df95ad23f9c6f1ee3b4a99e227f10d303d4f` |
| `common/script_values/nesnd_unity_policies.txt` | `156bf63af00bbb1270000ceab3c87f4260f715504e4e9136719c75dedecd5aee` |
| `common/scripted_buttons/nesnd_ottoman_claims.txt` | `3b1fb67c0aa920430a5bba9cd5646602ce86cba998aea6e72ca6460fcfbc8638` |
| `common/scripted_buttons/nesnd_ottoman_recovery.txt` | `334042d44a29080f97fd443c8a98269fe5a2c66bdfe2ece6b8bc9c4ca5f6a1f1` |
| `common/scripted_buttons/nesnd_unity_policies.txt` | `3b1da6e5061897f3867948bc469a4b64ccd4d704592e2e1240822604647b2fb5` |
| `common/scripted_effects/nesnd_ottoman_recovery.txt` | `ecfc46c09e0148b423d63d6b04e8361edc6782748b878de518783e991968d102` |
| `common/scripted_effects/nesnd_ottoman_unity.txt` | `9d0931dc50cd96e8432be74520d6716122fcf62916e3091d1a16f741e112c852` |
| `common/scripted_effects/nesnd_unity_policies.txt` | `11142a5e450d058875fe8c74e3fc9e5dcedf5ca37600a01300693b1779266cfb` |
| `common/scripted_progress_bars/nesnd_india_core.txt` | `4178c84be950890695bf594a2fdd134ac5d8787e84afea256a84200d553e7803` |
| `common/scripted_progress_bars/nesnd_jp_development.txt` | `740794fb30f3e1a59500bb272c4df76fd16188a46e9b9fc0f1e98ae13c8fb2a9` |
| `common/scripted_progress_bars/nesnd_ottoman_recovery.txt` | `931bf7a3fba6fbd5c9469a31de73f8444472f6d8d6fce1ccd6006588fc92afb8` |
| `common/scripted_progress_bars/nesnd_ottoman_unity.txt` | `2626f314c4d7e623c6d599ee29b2fdc52c7558e7e238fab1990e431d074ff694` |
| `common/scripted_progress_bars/nesnd_qe1_identity.txt` | `90d0aba58b1e7778410fe2045b3fcaa406e31fa1fc729efa0d8650f2b85fcea1` |
| `common/scripted_triggers/nesnd_ottoman_recovery.txt` | `d133d83333960597e4a8561381f573a22276cd6ea343d517888549cff9535c5b` |
| `common/scripted_triggers/nesnd_ottoman_unity.txt` | `1aa2c166bcbefcf35ffb7268ecfd4ccb65629589e870a8b151b649fc9bca4135` |
| `common/scripted_triggers/nesnd_unity_policies.txt` | `1ec3af1b158a277b5da7511111499ece96322ccf822dd77468c30c851f352c7a` |
| `common/static_modifiers/nesnd_ottoman_recovery.txt` | `2ad3a35ea3b5a91cf0e12edb769e0added3d0fa95014705716f9041599cde379` |
| `common/static_modifiers/nesnd_ottoman_unity.txt` | `12ea9465926074a915effebe21ac4d88b8892046e528e25964af0a3fd4dc65f3` |
| `common/static_modifiers/nesnd_unity_policies.txt` | `f481f4d46421ab5807a9a50117dc775e2e844aeb792e9db45a19f28e55cbc9f3` |
| `events/nesnd_ottoman_recovery.txt` | `c15dd0263968c61ceb852857657f598f9cb00d978f57e5aaa5057ebc590c681e` |
| `localization/english/replace/zzzzzzzzzzzzzzzzzzzz_nesnd_unity_policies_l_english.yml` | `3dbcc8daa65e689cbbe8b112b0bb13d3be6cb07736cf23b7fc903bd623e11acd` |
| `localization/simp_chinese/replace/zzzzzzzzzzzzzzzzzzzz_nesnd_unity_policies_l_simp_chinese.yml` | `92de070a8db257d224b2f60b6339044c1cbab44d3655b6405403c7463c373c62` |

## Completed repair validation

Isolated Batch B repair reached STATIC_PASS;14ordered-AST groups,13actualMCPqueries and0addedTigerdiagnostics against the fixed baseline. All34candidate/snapshot inputs and tool hashes remained frozen. See batch-b-validation.md/json for coverage and ENGINE_NOT_RUN boundaries. No further gameplay edits after the repair freeze.


## B-r3 display-only follow-up

Two TUR JE count predicates now use minimal Chinese/English tooltips. Thresholds27/36, ordered logical AST and all gameplay remain unchanged. Root observed the native num_states localization gap; the new checker explicitly rejects the old visible form. r3 STATIC_PASS evidence is in batch-b-validation.md/json; no engine run.

- `common/journal_entries/nesnd_ottoman_unity.txt` SHA256 `3110b040ad4d675459e621542fd70d2ab4f9f5c2bab68fea8ecb263fe756a62d`
- `localization/english/replace/zzzzzzzzzzzzzzzzzzzz_nesnd_unity_policies_l_english.yml` SHA256 `d937b9e4c55c8397c647ebca4371bdf3bcbed5d6e8a0c1006928514895ea66f8`
- `localization/simp_chinese/replace/zzzzzzzzzzzzzzzzzzzz_nesnd_unity_policies_l_simp_chinese.yml` SHA256 `3304a153048ec473510cac31a09916ad5b6d0b1653d8e05a29ab4ae807144a84`
