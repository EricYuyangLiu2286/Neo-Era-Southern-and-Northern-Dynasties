# Spec review: Qin journal stages

Result: **0 findings**. Independent read-only source review; **ENGINE_NOT_RUN**.

Compared candidate `exports/qin-journal-stages-20261102-a` with `backups/pre-change-qin-journal-stages-20261102T132813Z/mod`, baseline Git `a7b445ba515d0e4842fb36ba3e6094d54e046012`. Full SHA comparison found exactly five changed files among 666, with no additions/deletions; Japan and Persia content remain unchanged. Ordered AST comparison preserved duplicate nodes and confirmed the narrow changes below.

Spec: `qin-stage-design.md`, SHA-256 `c7d3fe866dc5ad7ccb1859c2d0c0da02814955a4fe3faf42b9de75625e38da30`.

- “开局朝议主日志＋经济/军事两从日志＋文化团结”: bootstrap retains those entries. Both later entries require persistent opened flags; none are initialized at the ordinary opening. The four recovery regions initially belong to CNE.
- “朝议结算（胜利、超时或领土失效）后解锁”: all existing settlement paths reach `nesnd_qe1_close_agenda`; it sets done before unlocking. Monthly bootstrap performs later entry creation and maintains recovery access without recursive bootstrap.
- “提前控制……任一整地区”: recovery's OR predicate uses the same country-or-subject ownership primitive as the unchanged four-region completion predicate. Opened flags are never removed after territory loss.
- “未达到阶段不等于invalid/永久archived”: invalid/archive paths still use eligibility, not availability. Court's existing law/size/archive restrictions and recovery's done guard remain unchanged.
- “旧档已有JE仅登记opened标记”: existing active entries grant opened flags without clearing variables, choices, rewards, or progress. No positive self-JE requirement exists in the new entry predicates. Completion and terminal flags still prevent re-entry.

Read the 24 limited source-condition cases and zero-added Tiger report as corroboration, not engine evidence. No implementation defect, scope creep, or new entry deadlock identified. Catalog reports current game 1.13.11/build 24799966; native stage examples were reread.

Candidate SHA-256, paths relative to candidate:

| File | SHA-256 |
|---|---|
| `common/journal_entries/nesnd_qe1_court.txt` | `0dcc1910a39444ec376aed864e920ab68f6858c89dc3ad3e52e68489ecad6aad` |
| `common/journal_entries/nesnd_qe1_recovery.txt` | `459b1142e855a98d05160e078e6b1ed679b45eabda5719a0df67a5aff4ec4a88` |
| `common/scripted_effects/nesnd_qe1_agendas.txt` | `967f6606de5986a3df56611c67c4b86ccb8de8eb7e4c564bfd1436c27309f62c` |
| `common/scripted_effects/nesnd_qin_persia_lifecycle.txt` | `9f2d49f467def9ba622dd80dd8b6e90fced90f057efd12e4b631fe2474dc35f5` |
| `common/scripted_triggers/nesnd_qe1_campaign.txt` | `7d20bc753583912fcc1280083a95ee05962cadc724aca488071c7bcbfff0fc4b` |
