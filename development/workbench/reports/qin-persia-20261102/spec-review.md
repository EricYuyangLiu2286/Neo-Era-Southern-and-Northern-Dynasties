# Spec axis

Baseline: independent `pre-change-qin-persia-campaign-20261102T022528Z/mod` (`c0e11fe`). Candidate: `exports/qin-persia-campaign-20261102-a`. Ordered AST review covered 49 changed files, 47 scripts and 269 top-level definitions; fingerprints/creation sites are in `spec-coverage.json`. No game execution. This report records the reviewed snapshot, before parent fixes.

1. **P1 — Reversed clamps make every qualifying SoL bonus/penalty 5%.** Spec line21: “生活改善额外效忠+15%”; line19 requires proportional downside after timeout. `common/scripted_effects/nesnd_qe1_sol_bonus.txt:12` (and all 30 matching effects) ends `max=0 min=0.05`, so any positive calculated fraction becomes 0.05. Its divisor in `common/script_values/nesnd_qe1_sol_bonus.txt:1` likewise always becomes10. A 0.01 SoL increase therefore converts5%, not the intended small supplement. GAME `script_values.md:35–36` confirms operator direction. `nesnd_qe1_identity.txt:10` repeats the reversed lower-bound clamp, eliminating diversity penalties. Swap bounds and verify representative arithmetic.

2. **P2 — Recovery rewards omit substantial Northeast Asia.** Spec line33: “均授中国大陆及东北亚宣称”. `common/scripted_effects/nesnd_qe1_recovery.txt:1–65` omits SEOUL, BUSAN, SARIWON, PYONGYANG, TOKAI, HOKUSHINETSU and KYOTO, despite their active map definitions. Either victory option therefore grants incomplete claims. Complete the explicit region set.

3. **P2 — Aid events lack the required cooldown.** Spec line43: “有限期+冷却”. `events/nesnd_per_campaign.txt:2–18` has neither cooldown nor request lock; `common/scripted_effects/nesnd_per_campaign.txt:12–13` can draw the same six-month reward next month. Add event-specific cooldowns and exclude unavailable choices.

4. **P2 — Patronage persists after eligibility fails.** Spec line35: “条件不再满足即清修正”. Acquisition requires40%, but `common/scripted_effects/nesnd_qe1_court.txt:20–27` only clears below35%. A faction falling to38% retains patronage. Use the same eligibility threshold, or explicitly revise the spec for hysteresis.

5. **P2 — Military mobilization action is missing.** Spec line17: “另有军费/扩军动员行动形成可操作选择”. The army child attaches only `nesnd_qe1_army_petition_button` (`common/journal_entries/nesnd_qe1_agendas.txt:55`); that button requires all expansion objectives already complete. No military spending/mobilization action exists. Implement the promised action or remove the requirement through an explicit design decision.

**Summary:** 5 findings; worst P1 is the constant5% SoL conversion. Initialization, monthly+2/−1 ownership, three-pass paired conversion and mutually exclusive reform law changes showed no additional confirmed spec gap in this snapshot.
