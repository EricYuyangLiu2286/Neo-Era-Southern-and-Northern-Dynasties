# Spec — final Ming generation recheck

**No unresolved user-requirement findings.** Baseline: `pre-change-persia-journal-ui-20261103T005805Z/mod` (`f0463ff`). Candidate: `exports/persia-journal-ui-20261103-a`. Snapshot review used per-file reads and baseline `git diff --no-index --ignore-space-at-eol`. Catalog: 1.13.11 / build 24799966, CURRENT, zero source changes. No game run or implementation edits.

**Resolved P2 — GNG lineage.** The requirement is “GNG本宗朱氏复明，不请旧帝”. Rechecked `common/scripted_effects/nesnd_south_restoration.txt:202–203`: both ruler and heir priority paths now require `nesnd_ming_huai_line`; the heir availability and selected-character filters match. If neither qualifies, the Huai-only local/global/exile/void search and generation guard apply. A locally present Ning royal no longer bypasses Huai relatives.

**Newborn callback correction verified.** `common/on_actions/nesnd_ming_generation.txt:3–17` first requires an owner, ruler, and recognized lineage/historical parent. The effect at `common/scripted_effects/nesnd_ming_generation.txt:263–268` restricts naming to new nonhistorical heirs lacking generation metadata and identifies only their current parent. The global identity scan has been removed from this callback. Existing names remain unchanged.

**Accepted naming policy:** the earlier terminal-name advisory is closed under the parent's clarified user authorization permitting fictional/conflicting names. The finite author pools may reuse a collateral name after the final documented generation; this must not prevent creation when no recruitable royal exists. Counters advance through known generations, remain bounded at the documented terminal generation, and never reuse historical templates. Same names are not the same character and are not resurrection.

The four-tier search priority, explicit local/global/exile/void passes, matching generation guards, foreign ruler/heir protection, separate line counters, and settlement success checks remain present. No unrelated gameplay scope was identified in the 43-file baseline delta.

Primary interfaces were checked against current GAME `00_victoria_ip4_scripted_effects.txt:2028–2084,2105–2125`, `00_code_on_actions.txt:6751–6768`, engine effects/triggers docs, and author name-pool originals referenced by `ming-successor-generation.md` S01/S02. This is source/spec review only; it does not establish engine behavior.

Spec: 0 unresolved findings; prior P2 resolved; naming advisory closed by clarified authorization.
