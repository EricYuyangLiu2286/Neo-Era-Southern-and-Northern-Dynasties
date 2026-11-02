# Spec audit — 2026-11-02

Scope: `git diff 044de73...870639a`; commits cf6ec2f, c0e11fe, 7d39018, 870639a. Read-only review of main MOD against tasks 14–16 and `WORK/plans/two-empires/20261102-qin-persia-implementation.md`. Game catalog remains 1.13.11/build 24799966, unchanged. File fingerprints: `spec-source-fingerprints.json`.

## Missing / partial

**[P1] Seven newborn breakaway countries cannot enter the promised anti-Qin war.** `common/scripted_effects/nesnd_qe1_fracture.txt:233` (AFG), `:252` (KAL), `:271` (PER), `:290` (TIB), `:309` (KAS), `:328` (MGL), `:347` (TUV) set `nesnd_qe1_newly_restored` and create armies, but neither their creation callbacks nor post-transfer blocks set `nesnd_qe1_breakaway_attacker`, grant `nesnd_qe1_war_launch_window`, or schedule `nesnd_qe1_fracture.91`. The newborn marker is never read anywhere in the main MOD. Both the event (`events/nesnd_qe1_fracture.txt:11`) and monthly fallback (`common/on_actions/nesnd_qin_persia.txt:8`) require the missing attacker marker; the war effect additionally requires its 90-day window (`common/scripted_effects/nesnd_qe1_fracture.txt:53`). Thus newly restored members of these seven tags get territory and armies but never reach the scripted war/join path.

Requirement: implementation specification line 29, “新兴国对QE1发动明确目标战争”; final contract line 61, “各国加入同一反秦战争，90天启动窗口，一次开战锁”. Restore the launch closure for newly created countries while preserving existing-country/third-party safeguards.

## Scope creep

No actionable finding.

## Wrong implementation

No additional actionable finding. Traced all 12 Qin/Persia JE activation, initialization, parent-child, completion/archive and route-successor paths; directly checked the court/recovery reward locks, CNE child initialization and Polish delayed ultimatum/result guards. No additional missing definition or unreachable entry was established in those inspected closures.

This is source-level evidence, not engine validation. Population splitting, callback ordering and diplomatic-war dispatch remain ENGINE_NOT_RUN.
