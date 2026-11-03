# India Spec review

Snapshot: checkpoint-feedback-restoration-delivered-20261103T032233Z → india-development-20261103-a. GAME 1.13.11/build24799966; catalog CURRENT. Read-only script review; ENGINE_NOT_RUN. Root's recruitment/progress-bar fixes excluded. References below are candidate-relative.

- **P1 — Rollback may confiscate subsequently acquired territory.** `common/scripted_effects/nesnd_india_uprising.txt:106–112` and five equivalents return the entire current `region_state:IRn` after retries. `num_states = 1` does not exclude merging another country's portion of that same region. Lifecycle §3.13 requires “准确转地集合” and “不倒转第三国战果”. Record/guard subsequent territorial changes before rollback; unsuccessful residual cases must not receive the normal survival reward.

- **P2 — Establishing Tianzhu destroys existing preparations.** `common/scripted_effects/nesnd_commissions.txt:186–201` transfers land without migrating case owner/state references. `nesnd_india_uprising.txt:91–100` then closes these cases. The commission lore contract requires “不能USM一设司就让已建立的地区案件消失”. Transfer compatible prewar cases to TZ1 and preserve progress/cost identity.

- **P2 — Successful governance removes Tianzhu's defence interface.** All six suppression buttons exist only on `common/journal_entries/nesnd_commissions.txt:9–25`, which permanently completes. TZ1 remains a valid colonial target afterwards; no surviving JE hosts its responses. Design §X requires the colonial owner can investigate/suppress during preparation. Keep these actions on a persistent governance/security entry.

- **P2 — Preparation ignores the required local conditions.** `common/scripted_effects/nesnd_india_uprising.txt:92–98` adds a fixed five monthly whenever the sponsor is solvent and peaceful. Local unrest, manpower, transport and aid do not contribute or gate progress. Design §X explicitly says “资金、当地不满、可用兵员、交通和援助共同决定进度”.

- **P2 — Industry rejects the permitted supply routes.** `common/scripted_triggers/nesnd_india_core.txt:16–20` unconditionally demands domestic coal/iron/tools/steel levels. Design §VII permits “法国供给、进口、土邦协作和本国建设均可达成”. Add a real market/supply alternative, with appropriate industrial/military outcome checks.

- **P2 — Hierarchy transition leaves an impossible caste objective.** `common/scripted_triggers/nesnd_india_core.txt:26–31` neither gates the JE to caste hierarchy nor accepts its replacement. Native `common/law_groups/00_laws.txt:38–42` links the required laws exclusively to `british_indian_caste_system`. Implementation contract §4 requires default-hierarchy transition acceptance.

Native cross-checks: `events/central_america_events.txt:83` (owner-state creation); engine effects.log:37144 (`set_state_owner`); `common/journal_entries/journal_entries.md:70–158` (complete/invalid); `common/on_actions/00_code_on_actions.txt:7131` (state-owner change). No objection to IR1–IR6 representing only existing colonial owner-state populations or preserving existing princes.
