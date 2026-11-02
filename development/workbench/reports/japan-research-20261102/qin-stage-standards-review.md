# Standards review — Qin journal stages

Result: **0 documented-standard violations; 0 actionable smell findings. SOURCE_ONLY / ENGINE_NOT_RUN.**

Scope: `WORK/exports/qin-journal-stages-20261102-a` against `WORK/backups/pre-change-qin-journal-stages-20261102T132813Z/mod`, baseline Git `a7b445ba515d0e4842fb36ba3e6094d54e046012`. Independently hashed both snapshots: 666 files each, exactly five changes, no additions/deletions; both match `qin-stage-source-manifest.json`.

Rules: main MOD `AGENTS.md`, `docs/agents/engineering-skills.md`; NESND skill `journal-text-contract.md` (“非开局入口、终局回调与镜像条”) and `syntax-and-routing.md` (“引用安全”, “覆盖与编码”).

- Entry/terminal separation is preserved: both JE files:5–6 use `available`; court:21–22 and recovery:13–14 retain permanent `eligible` termination. Campaign triggers:20–22,31–37 retain law, state-count, archive and reward locks. Waiting for a stage cannot itself archive either journal.
- Lifecycle effects:21–24 share availability checks with automatic entry. Lines 40–52 only register persistent opened flags; old active journals retain progress/rewards, and losing a foothold does not revoke entry. Agenda effects:64–69 register completion before unlocking. Initialization never adds its own JE; the new helper neither calls bootstrap nor resets values.
- Monthly maintenance remains wired at `common/on_actions/nesnd_qin_persia.txt:1–5`; terminal law and territory cleanup remains independent. No new unsafe object/variable reads appear. BOM/LF conventions are preserved.
- Smell baseline reviewed: shared availability/unlock logic is appropriately extracted; names distinguish eligibility, availability and opened state. Repeated four-region lists express different AND/OR semantics. Database placement and valid Jomini repetitions do not justify OO restructuring.

Native protocol: catalog CURRENT, 1.13.11/build 24799966; all three recorded native hashes match. Verified `japan_shinto.txt:65–90` → `07_japanese_religion.txt:1–118` → `japan_religion_events.txt:825–861`, and `meiji_restoration.txt:133–158` → `00_meiji_restoration.txt:744–775`. Documentation confirms explicit add bypasses possible; candidate guards both paths. Citation clarification: the religion completion callback is at 113–118, beyond design's 1–96 range. Existing UI/resources remain unchanged.

Recorded evidence: 24 source-condition checks pass; Tiger reports no additions. Neither establishes engine behavior.

Current SHA-256 (paths relative to candidate `common/`):

| File | SHA-256 |
|---|---|
| `journal_entries/nesnd_qe1_court.txt` | `0dcc1910a39444ec376aed864e920ab68f6858c89dc3ad3e52e68489ecad6aad` |
| `journal_entries/nesnd_qe1_recovery.txt` | `459b1142e855a98d05160e078e6b1ed679b45eabda5719a0df67a5aff4ec4a88` |
| `scripted_effects/nesnd_qe1_agendas.txt` | `967f6606de5986a3df56611c67c4b86ccb8de8eb7e4c564bfd1436c27309f62c` |
| `scripted_effects/nesnd_qin_persia_lifecycle.txt` | `9f2d49f467def9ba622dd80dd8b6e90fced90f057efd12e4b631fe2474dc35f5` |
| `scripted_triggers/nesnd_qe1_campaign.txt` | `7d20bc753583912fcc1280083a95ee05962cadc724aca488071c7bcbfff0fc4b` |
