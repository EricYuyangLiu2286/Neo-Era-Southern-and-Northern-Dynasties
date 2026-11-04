# Standards review

Snapshot review: parent `c4626514277991a415283897af47769e12495138`; `pre-change-journal-war-feedback-20261103T222744Z/mod` → `journal-war-feedback-20261103-a`. GAME 1.13.11 / build 24799966, catalog CURRENT. Read-only gameplay review; no engine run.

## Documented-standard findings

1. **P1 — Unsafe AI conditions.** `events/nesnd_south_holdouts.txt:49` uses `relations:scope:nesnd_holdout_sender`, explicitly rejected in the project's recorded 1.13.11 failure. AI modifiers throughout this file also put conditions beside `factor`, while current native `events/balkans_events/balkan_wars_events.txt:1062` and the source report use a `trigger` block. Use the supported quoted `"relations(scope:nesnd_holdout_sender)"` form inside guarded modifier triggers; protect sender/CNE/USM reads independently of event/option eligibility. Rule: NESND `references/syntax-and-routing.md`, “引用安全” §§1–4 and “原生日志补证”.

2. **P2 — Royal-flight predicates still rely on short-circuiting.** `common/scripted_effects/nesnd_south_holdouts.txt:7` combines `exists = ruler` with a sibling ruler dereference. `common/scripted_triggers/nesnd_south_holdouts.txt:62–67` similarly combines `exists = capital` with `capital` access and reads the temporary fallen-court scope without its own guard. A missing ruler/capital or effect preview can still evaluate those reads. Nest existence branches and return explicit false. Rule: `syntax-and-routing.md`, “引用安全” §§1–3.

3. **P2 — Relocation is committed without verifying ownership.** `common/scripted_effects/nesnd_south_holdouts.txt:27–41` transfers the emperor, then writes the recipient's court/reference flags unconditionally. The caller subsequently transfers remaining characters to USM and annexes the old court. Confirm the same living character's `owner` equals the selected recipient before committing; otherwise ensure exile before annexation. Rule: `syntax-and-routing.md`, “宗室延续与无所属角色”; this batch's `ming-war-source.md`, “陷城吞并与同一皇帝保全”.

4. **P2 — Rebuilt Japanese bars initially discard the displayed score.** Both definitions in `common/scripted_progress_bars/nesnd_japan_absolute_counters.txt:3,8` start at zero and update only weekly; `common/journal_entries/nesnd_japan.txt:13,59` does not synchronize. A new/restored JE with score 2 or 5 therefore displays zero until the next weekly update. Add guarded absolute initialization in each JE's immediate/re-entry path. Rule: `references/journal-text-contract.md`, “阶段切换与数值同步”.

## Heuristics and limits

No actionable Fowler smell. Jomini scope chains, repeated options and database-specific files are intentional; no OO restructuring suggested. India `prev.prev.owner` resolves the queried capital's country, and HUS law callbacks use law→owner and country roots correctly. This review does not certify event timing, migration or character transfer in the engine.

## Correction re-review

The four initial findings are closed in the revised candidate: AI modifiers use guarded `trigger` blocks and quoted `relations(...)`; ruler/capital/fallen-country predicates now branch; royal relocation checks actual owner and falls back to native exile before allowing annexation; both Japanese JE immediate blocks set the absolute bar value.

The initial review's informal `prev.prev.owner` assessment is superseded: Tiger rejected that chain, and all three India callers now pass explicit `COUNTRY` parameters. The country JE and country tick pass `root`; the JE-root bar passes `root.owner`. No old unparameterized call remains.

HUS source confirmation: GAME `common/on_actions/00_code_on_actions.txt:5020` documents the activated law root and country owner. The callback enters owner and applies `has_game_started`; the new transition replacement retains native side effects and gates only JE initialization. Native `common/scripted_effects/00_scripted_effects.txt:720–728` confirms exile plus complete role cleanup. These sources do not establish runtime succession/transfer ordering.

### Remaining findings

5. **P2 — Failed voluntary surrender has no retry.** `common/scripted_effects/nesnd_south_holdouts.txt:132` records `answered_round` and clears the choice before relocation. If `nesnd_ming_flight_blocked` prevents the commit at line 135, the country remains independent/unresolved, but `offer_due` is permanently false for that round and no resistance/north/surrender retry flag remains. Record the answer only after successful relocation/commit, or retain an explicit surrender retry. Rule: `references/syntax-and-routing.md`, complete lifecycle/cleanup; `references/numeric-scale-contract.md` §3 requires tracing failure through retry.

6. **P2 — Writing review evidence is incomplete.** `writing-keys.json` records source keys/hash and candidate strings but does not contain the original/candidate comparison or per-key editorial decisions. Add the required comparison covering all effective changed Chinese/English entries. Rule: `nesnd-player-writing/SKILL.md` §§4–5. This is a release-documentation gap, not a claim that the prose is incorrect.

Current result: four closed, two open (one execution-path closure, one documentation requirement). No engine run.

## Final correction review — 2026-11-04

**Remaining Standards findings: 0. All six recorded findings are closed.** No actionable smell.

Finding 5 is closed: voluntary surrender records answered/resolved only after the annexed country is no longer alive. Failed relocation, exile or annexation does not consume its answer; event after-cleanup removes the transient choice lock, leaving the existing offer/reply path available. The reviewed failure-injection cases cover those script branches, including the original heir and a guest emperor.

Finding 6 is closed: writing-comparison.md contains traceable original samples with file/hash/key/line, 39 Chinese/English pairs, per-key decisions, and the guest-emperor wording correction. All 78 final candidate strings were independently compared to that report and match.

Boundary evidence: boundary-tests.json reports 52/52 PASS. Every changed gameplay .txt file still matches its recorded source hash. The later localization wording was verified separately against the writing table; documentation updates are outside those executable cases. This records AST-subset branch evidence, not native game execution or UI validation. No game was launched.

Also reviewed the later actual-defeat registration and shared unresolved-holdout guards. The HUS activated-law callback and native exile role cleanup remain supported by the cited GAME sources.

### Reviewed changed-file SHA-256

These fingerprints bind the candidate before the root agent's announced trailing-whitespace-only cleanup. A final delivery manifest should record the resulting byte hashes and retain the AST-equivalence check.

| Candidate-relative file | SHA-256 |
|---|---|

| `.scratch/debug-release/issues/30-journal-war-feedback.md` | `d8fbdf6bae2af38c66623a6a02d2114d2ddd53dc5d2f14733b1151e7bd5a14c2` |

| `.scratch/debug-release/map.md` | `de70f620913217ae971a9302868ca57f1462d7f61fd371d481b315526035a1c4` |

| `common/diplomatic_plays/ce_diplomatic_plays.txt` | `63edfa304faede63e79500bc5d189f705a7ea0973457d810c99edcacd7c8ed46` |

| `common/journal_entries/ce_usm_the_last_days_of_ming.txt` | `c482208b9ead08097d343c25f64d84520d07ea2b6355966fb6d4d370149af49a` |

| `common/journal_entries/nesnd_india_core.txt` | `af568a569181bb34f7bccb9d61f3b73edb8e5c05c8dbe6d416376923abb02bd2` |

| `common/journal_entries/nesnd_japan.txt` | `441e466d927f1ad778a3509d800d56e8f9cd1a91c94dc01978ec46c9e8209e5b` |

| `common/journal_entries/nesnd_south_holdouts.txt` | `11dc2716e2ce6c6367e58e4a721a28fab6fed2b747b5c22ef59af19117d53237` |

| `common/journal_entries/zzzz_nesnd_hus_native_monarchy.txt` | `c0ffef0544ff4d97a26174abfd81ef876f512840e6d00e98169e204084477f5e` |

| `common/on_actions/nesnd_hus_monarchy_history.txt` | `40e1c24182cfb8598814f6e4422570f125b5a011133cad7f807fab3d8be47f72` |

| `common/on_actions/nesnd_south_holdouts.txt` | `f13c240c0dc60126cade2cb6e063e898d503fd56ddd7093b5a92b8cfe9a3d8ed` |

| `common/on_actions/nesnd_war_collapse.txt` | `f958381c45375325e0d0165135e1b4b304616f6f327d4592dde6cbfe3e36d833` |

| `common/script_values/nesnd_japan_absolute_counters.txt` | `40178a87e424a49df71394ca252c5f9da1dcd6bc07b39dd304912671f50eabe7` |

| `common/script_values/nesnd_south_holdouts.txt` | `b00bd47e8faef21715d60b81d88e934f7aaffcd3016433a4d192edbf4b76bed8` |

| `common/scripted_effects/nesnd_india_core.txt` | `341792ac43044155cb518cc79944ca72b388342e1b962b9e0659e789dbacc165` |

| `common/scripted_effects/nesnd_south_holdouts.txt` | `d804ee71293834f676def807aadf18f005aab13d2b8e4e0f5bf16dd7e17dc594` |

| `common/scripted_effects/nesnd_war_collapse.txt` | `476d4f4492d6c3815ea28565d021680dbc4dee41f768ab0bb6208e41cb3915ae` |

| `common/scripted_effects/zzzz_nesnd_hus_monarchy_entry.txt` | `7ececed165a03efa86aca54f60c281dcc427df8bc66fcd0a5b49dccd60679ea3` |

| `common/scripted_progress_bars/nesnd_india_core.txt` | `09fa294596f4f2cf4cb5ad1b10537d419b593dd89771afb785800851bf9111d2` |

| `common/scripted_progress_bars/nesnd_japan_absolute_counters.txt` | `67b5fe73153d830414567d57dc1fdd9213608e45e0a4b4b1e45661d6e5345eec` |

| `common/scripted_triggers/nesnd_court_followup.txt` | `5e2c086d88ac08aa840ed2de7929cd2a3de118a95c4d74910b86d173c8b1bede` |

| `common/scripted_triggers/nesnd_hus_monarchy_history.txt` | `fc983fca98b4b7b0e341d42004f783cbe68cbbe4290b0fad7d59af8f4e9e16f4` |

| `common/scripted_triggers/nesnd_india_core.txt` | `0622fab14d4db5208359b7d182fd76633926c28daa316487ac7f4fb718226548` |

| `common/scripted_triggers/nesnd_japan.txt` | `fd6886b1a96b8faf8dd0c5528150e79f3b54d903fbd9352ebae3fdb4d197aad4` |

| `common/scripted_triggers/nesnd_south_holdouts.txt` | `1af243f138263540a234bccd450a4fcfe75ff5e1d5616b9a31e56987bc301b05` |

| `common/scripted_triggers/nesnd_war_collapse.txt` | `0f23f251f6f98cb87c3b9b3920a780c9ce34db091cbe450a2d689e1b57863c69` |

| `events/nesnd_south_holdouts.txt` | `39cd6d19c7a4b8f02a1c549e283fed241d174fab55be342e7f365fcbff4dda97` |

| `events/usm_civilwar_events.txt` | `ec0d89c26219a1e00ad8c1d403f9194ef7e536127644ab2a257f16f357a448a0` |

| `localization/english/replace/zzzzzzzzzzzzzzzz_nesnd_journal_feedback_l_english.yml` | `37827d65bc5068e3ba7a92a00f9aa281bb554701fc747a944734891d8a636942` |

| `localization/simp_chinese/replace/zzzzzzzzzzzzzzzz_nesnd_journal_feedback_l_simp_chinese.yml` | `3ef5aaedf00df79a4e257669349ec0ecea4085ef39be15187a6e17a29ea668d0` |


Writing comparison SHA-256: `d04b638f0fd1d16da545806265a891afccce202525a97b6aecdb3c1697a73129`.
