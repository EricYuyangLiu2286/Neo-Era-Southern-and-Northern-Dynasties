# Batch B implementation — READY_FOR_TEST

Frozen: 2026-11-04T12:29:14.935532+00:00

Candidate: `WORK/exports/canon-route-execution-20261104-a`; parent b94582ecec7b0b6dd5620a184658190157fc1729. Main MOD/GAME/other mods remain outside this batch's edits. No behavior/Tiger/MCP tests and no game launch were run during the edit phase. The exact frozen gameplay/text hashes are listed below and in `batch-b-freeze.json`. Stop editing this batch until the organizer assigns tests or a specific correction.

## Implemented behavior

- Added two independent uncancellable12-month national policies to QE1 unity, JAP/JTK/JIM cohesion, imperial India common identity and new TUR unity. Each adds0.5/month and natural assimilation10%; the material policy adds the frozen native GDP-based weekly expense, plus primary-only0.001 monthly movement toward radicalism, capped12 applications in one country-level callback. Political policy subtracts10 legitimacy. Both may coexist; JE loss does not erase their national cost. AI affordability/legitimacy thresholds are not player restrictions.
- Qin's existing legal coefficients are partitioned into citizenship, church/state and army-model rows. India's common-identity distribution-of-power and citizenship rows are separate from social turmoil; its dynasty religion row uses the actual law-group name. Japanese existing economic/war/conversion coefficients are preserved. Existing Qin/Japan conversion and collapse effects files were not edited.
- New TUR unity first unlocks at36 directly owned states, initializes once to70, preserves the stock below27 and resumes at27. Inactive UI shows the actual native state-count requirement. Turkish contributes0; population-weighted Arab/Berber/Afro-Arab, Han, other African, Slavic, remaining groups contribute coefficients−1.2/−.9/−.6/−.35/−.15. Zero-population samples are0. Economic capacity, schools, SoL, bankruptcy, three law groups, sustained war, actual enforced-goal victory and acquisition callbacks affect the stock. Low/high bands are reversible and introduce no forced conversion/breakup.
- TUR expansion is independent of Tanzimat success. Existing three enthusiasm/reform tiers retained; all national/supply alternatives now share cleanup. A12-month term plus pending guard, delayed hidden event and weekly expiry fallback protect old-callback/new-renewal ordering. Tag invalidation removes benefits but leaves the pending term until its own expiration. The72 claim targets/effects are preserved; their malformed scripted-button ai_chance modifier blocks were changed to native value/if/add syntax.
- Added140 effective keys per language in a dedicated BOM-encoded zh/en pair, including72 existing state-name claim aliases. `batch-b-writing-comparison.md` records author samples, final text and per-key editorial conclusions. Policy text states real monthly radical movement and never claims sensitivity.

## Source and remaining boundaries

`batch-b-source-contract.md` and source hashes in `batch-b-freeze.json` bind native interfaces. Mandatory correction: Paraguay's barracks fragment is tooltip preview; its actual event applies the modifier to a country. Engine add_modifier accepts a building target and the unit modifier means maintenance-goods quantity, but building→unit propagation is not engine-verified. Timer expiry order, possible weekly fallback delay, budget billing, real natural-assimilation eligibility, callback ordering and UI rendering remain ENGINE_NOT_RUN. Monthly total+6/+12 estimates assume twelve accrual pulses; they are not guaranteed endpoint-order claims.

The planned test matrix in `batch-b-unity-plan.md` is NOT_RUN. This handoff is code/text closure, not STATIC_PASS or ENGINE_PASS.

## Frozen files

| Candidate-relative file | SHA-256 |
|---|---|
| `common/journal_entries/nesnd_india_core.txt` | `c6901de919fffe76f73479acb2621b56aab630722f58be7963cd1b08d5f298c7` |
| `common/journal_entries/nesnd_jp_cohesion.txt` | `aa442b68360bc6914305c250bf10b187a03ebff3bd2b5c2b8eee4c9f20128540` |
| `common/journal_entries/nesnd_ottoman_recovery.txt` | `52bfc26cb2bbc6a9505628f513e8f8877c04760ef53a073d27c4eb3c93956aa3` |
| `common/journal_entries/nesnd_ottoman_unity.txt` | `f67f121b4aba1800109529a8ed6372290f0ab49bb504704714a4741ce74ad698` |
| `common/journal_entries/nesnd_qe1_identity.txt` | `feb9996604bcf4f16c9420dffaca86fcb1967682922e30202709041550917c20` |
| `common/on_actions/nesnd_ottoman_recovery.txt` | `fabd5a7b4f843e1f2d143d1fbed8aa847b4dbcdc619a234376dc540bfbb1a75c` |
| `common/on_actions/nesnd_ottoman_unity.txt` | `ad409a1f89bb32d5cbd23cdad9e45757bc44a3716d12e70d2631a60f32b91326` |
| `common/on_actions/nesnd_unity_policies.txt` | `d09a31662df3e35b4ed5b6d552c0a7e488fc3bcb4a44bc15c3662eabe366b1ac` |
| `common/script_values/nesnd_india_core.txt` | `5e897f016decfae7603a660bd53e3d86b03857cedd836b6b5c0c6cfa46d89c6b` |
| `common/script_values/nesnd_jp_development.txt` | `d348f2e38785b23daeced592cd3114956621b1bbde1b5f23142d1c4fbd059551` |
| `common/script_values/nesnd_ottoman_unity.txt` | `ebb2f82eb7bc52669a5a2cf49ef21fd1de220e4ee0f9b0c61b53c65d9b0e884c` |
| `common/script_values/nesnd_qe1_identity.txt` | `9e511e47cf3891b26ae38c8f2155df95ad23f9c6f1ee3b4a99e227f10d303d4f` |
| `common/script_values/nesnd_unity_policies.txt` | `4d5ee404183c3951fab937248b4bbca9d1535e9a59fdda089273e07646e3550f` |
| `common/scripted_buttons/nesnd_ottoman_claims.txt` | `3b1fb67c0aa920430a5bba9cd5646602ce86cba998aea6e72ca6460fcfbc8638` |
| `common/scripted_buttons/nesnd_ottoman_recovery.txt` | `30dea1055cd1fe52b5afd0f02b96278283d570a3824034b22373da64a157a578` |
| `common/scripted_buttons/nesnd_unity_policies.txt` | `0a31d5a9ba95f5ea5216851f8e530d03bcc3a07f61744d26f30c377c875c5294` |
| `common/scripted_effects/nesnd_ottoman_recovery.txt` | `8fbe11489e617ea6a1ecee0243091d55beb23660948d752fb99b8d17d154b8ce` |
| `common/scripted_effects/nesnd_ottoman_unity.txt` | `d5806edd386d50d61615f8d8342a9d80c22b257c30801fe3caf259d81f1cfc03` |
| `common/scripted_effects/nesnd_unity_policies.txt` | `372a0ddee697ce78e47e1510e4203151cee6f821769b1d70e239c446226214cb` |
| `common/scripted_progress_bars/nesnd_india_core.txt` | `4178c84be950890695bf594a2fdd134ac5d8787e84afea256a84200d553e7803` |
| `common/scripted_progress_bars/nesnd_jp_development.txt` | `740794fb30f3e1a59500bb272c4df76fd16188a46e9b9fc0f1e98ae13c8fb2a9` |
| `common/scripted_progress_bars/nesnd_ottoman_unity.txt` | `71ab30de0d7f1861ce9576ae98a229a3f9ccd9802066faef44be016b970aeda5` |
| `common/scripted_progress_bars/nesnd_qe1_identity.txt` | `90d0aba58b1e7778410fe2045b3fcaa406e31fa1fc729efa0d8650f2b85fcea1` |
| `common/scripted_triggers/nesnd_ottoman_unity.txt` | `320492bac60ebbd287d011e663a32ce5bb46cb5b25590aef16f31d1b670292d7` |
| `common/scripted_triggers/nesnd_unity_policies.txt` | `11be547f0b3f206578c25559704b8cb4903709afe2ea2d51244dd7fe16d48407` |
| `common/static_modifiers/nesnd_ottoman_unity.txt` | `4b8acbacb791d4e5d7fb11e5525d283e45c873cc7dd1ff1965d630467dce7f1f` |
| `common/static_modifiers/nesnd_unity_policies.txt` | `519ba6200d3426d80aaf2b930a83a2cb0a47d8507b4b825399c9d58044cacbd0` |
| `events/nesnd_ottoman_recovery.txt` | `ccde4fdf0afc75710ea7487ef5af4ea443a00e30fdef9e86566cc8603b412a39` |
| `localization/english/replace/zzzzzzzzzzzzzzzzzzzz_nesnd_unity_policies_l_english.yml` | `2c0cf656a12b7f0c7fba916df05847a0d23f2e511a08037a29630d168fcf9512` |
| `localization/simp_chinese/replace/zzzzzzzzzzzzzzzzzzzz_nesnd_unity_policies_l_simp_chinese.yml` | `7c5156802d596adbdc5f356bbb8bfd6fbd1176b592b8246e9e4441d0b424646e` |
