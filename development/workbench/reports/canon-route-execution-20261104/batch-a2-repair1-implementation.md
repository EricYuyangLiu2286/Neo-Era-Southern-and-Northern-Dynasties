# A2 repair1 — READY_FOR_TEST

Frozen: `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\batch-a2-repair1-owned-freeze-20261104T164801Z\mod`

Manifest: `batch-a2-repair1-freeze.json`. 33 owned files, 13 changed from original A2 freeze (12 existing + 1 new helper). New freeze supersedes the original 32-owned A2 freeze for testing; original copy and failed evidence are retained. Main MOD, GAME, history/population and other candidate ownership were not edited.

Agent `/root/sol_c1_frozen_validation`, explicit `gpt-6.1-sol / medium`, root GO role transition from independent B2 reviewer to A2 repair editor. This is implementation delivery, not independent validation.

## A2-F1

Before: has_role archetypes rejected/missed existing commander.

Implemented: All A2 queries now use has_role_of_type for general/agitator/ruler. Existing role, fallback and transfer policy retained.

Review anchors: `common/scripted_effects/nesnd_american_restoration.txt:37`; `common/scripted_effects/nesnd_american_restoration.txt:162`; `common/scripted_effects/nesnd_native_khanate.txt:105`

## A2-F2

Before: First exodus reads absent global receipt.

Implemented: Numeric receipt comparison is inside has_global_variable branch; absent/different receipt proceeds to the existing once-only 70/30 whole-community lottery and no-destination terminal.

Review anchors: `common/scripted_effects/nesnd_a2_manchu_exodus.txt:1`

## A2-F3

Before: Missing HUS read before intended terminal.

Implemented: HUS scope/alive/state checks occur only inside true presence branch; missing HUS sets result3 and clears pending. Exile acceptance also branches before HUS reads.

Review anchors: `common/scripted_effects/nesnd_american_restoration.txt:12`; `common/scripted_effects/nesnd_american_restoration.txt:52`

## A2-F4

Before: Wrong same-pair DP could award humiliation/victory.

Implemented: Distinct original USA/HUS objects, NKH case object, each side epoch and both stored exact DP copies gate all on_enforced writes; terminal sides reject callbacks. Temporary creation authorization includes original pair/case/epoch and is removed immediately after create returns. Only a unique actual new DP is bound. Legacy binds before later add_war_goal, which therefore uses strict receipts.

Review anchors: `common/scripted_triggers/nesnd_native_khanate.txt:120`; `common/scripted_triggers/nesnd_native_khanate.txt:36`; `common/scripted_triggers/nesnd_native_khanate.txt:142`; `common/scripted_effects/nesnd_native_khanate.txt:521`; `common/scripted_effects/nesnd_a2_common.txt:101`; `common/scripted_effects/nesnd_a2_common.txt:20`

## A2-F5

Before: Preview skipped writes leave missing military vars/scopes.

Implemented: Barracks, both facility helpers and both army helpers branch on initialized numeric variables and saved scopes before reads. Army literal dispatch keeps one complete formation and omits zero unit rows. Mutation stays behind the existing hidden effect paths.

Review anchors: `common/scripted_effects/nesnd_a2_common.txt:2`; `common/scripted_effects/nesnd_native_khanate.txt:86`; `common/scripted_effects/nesnd_american_restoration.txt:311`; `common/scripted_effects/nesnd_native_khanate.txt:142`; `common/scripted_effects/nesnd_american_restoration.txt:330`

## A2-F6

Before: Unknown country date trigger.

Implemented: Use game_date with the same 1836..1861 NAH and 1836..1851 TWT windows, same seen/dead receipts.

Review anchors: `common/scripted_effects/nesnd_american_restoration.txt:97`

## A2-F7

Before: Alliance/defensive article used as action pact ID.

Implemented: Native every_scope_treaty + both binds + article type filter + withdraw. Only the original opponent/NKH pair containing alliance or defensive pact is withdrawn; mixed articles end with that treaty and break penalties are enabled. New bilingual notification states these consequences.

Review anchors: `common/scripted_effects/nesnd_native_khanate.txt:521`

## A2-U1

Before: Dynamic combat_unit.count unsupported by available source evidence.

Implemented: No add/create combat unit interface located in current registry. Approved finite 1..40 NKH and 1..24 restoration deficit dispatch uses positive literal counts, original quarter/20% and half/25% formulas, one complete formation per matching branch. Target tiers and capacity values untouched.

Review anchors: `common/scripted_effects/nesnd_native_khanate.txt:142`; `common/scripted_effects/nesnd_american_restoration.txt:330`

## A2-U2

Before: Dynamic set_capital lacks native instance.

Implemented: Root-approved finite dispatch over 800 effective land state_region definitions (17 effective input files; 9 filename overrides). Keeps original selected saved region/population sort; true presence and current owner guard precede literal STATE target. Provenance includes each input SHA and selected definition.

Review anchors: `common/scripted_effects/nesnd_a2_literal_capitals.txt:3`; `common/scripted_effects/nesnd_american_restoration.txt:301`; `common/scripted_effects/nesnd_american_restoration.txt:217`; `common/scripted_effects/nesnd_native_khanate.txt:15`

## A2-U3

Before: Mixed scripted button chance shape.

Implemented: All three A2 restoration buttons now use documented base and modifier={trigger={...} add=N}; probabilities and conditions retained. Turtle Island preserved native bodies have no AI block.

Review anchors: `common/scripted_buttons/nesnd_american_restoration.txt:1`; `common/scripted_buttons/nesnd_american_restoration.txt:8`; `common/scripted_buttons/nesnd_american_restoration.txt:19`

## A2-U4

Before: Invitation display/execution/cancellation differed.

Implemented: Shared live trigger covers exact saved applicant+nonce, pending, alive/independent/nonwar parties, proper applicant geography/IG/legitimacy and host state. Both accept/refuse triggers and execution reuse it; cancellation negates it. Delayed expiry compares nonce only after scope/variable existence branch.

Review anchors: `common/scripted_triggers/nesnd_american_restoration.txt:63`

## Source and prose review

Source chain: current native `italian_unification.txt:680–718` → treaty articles and withdraw; role DB/type predicates and executable role queries as recorded in `luna-a2-military-interfaces.md`; native Kazakh formation literal-count example; local effects registry; scripted button documentation; native exiles event cancellation. The finite capital generator remains in WORK, only generated MODscript is owned. `a2-literal-capitals-inputs.json` records effective GAME+candidate files, filename overrides, per-definition origin and SHA. No ocean/comment enumeration.

The three new paired localization keys are the actual treaty-withdrawal notification. Existing author passages `nesnd_native_khanate.2.d` and `nesnd_hus_registration.1.d` supplied the event prose samples: state who acted, explain the political commitment and show the resulting burden. New Chinese and English paragraphs were read together: whole mixed treaties end, the withdrawing original opponent bears break penalties, and third-power pairs are outside this withdrawal. No developer mechanics, nonce or test vocabulary appears in player text. Both locale files retain UTF-8 BOM and original headers; the original 131 pairs plus three new keys remain.

## Boundary and handoff

Only authoring delimiter parsing, local prose/format reading and SHA collection were done. **No behavior tests, Tiger, MCP or game launch.** All seven confirmed red examples and four interface/window items are implemented and await independent testing; none is labelled engine PASS. The original military target/capacity numbers and allocation formulas are retained exactly. Post-freeze testing must verify inherited distribution against real per-state capacity rather than infer success from the literal generator.

The independent test matrix must cover the original A2 cases plus creation-phase authorization cleanup and uniqueness, strict later goal callbacks, side-specific epoch/case/DP mismatches, all army literal deficit branches and zero deficit, all military skipped-write previews, all800 capital targets and missing/unknown/foreign-owned target no-op, invitation cancellation/old nonce/current eligibility, mixed treaty/third-party preservation and notifications. Native engine sequencing and UI behavior remain an explicit ENGINE boundary. Freeze is final for this edit stage; stop editing and wait for independent testing.

## Additional manual source concern

Escalated to root without running a test or expanding this edit: `nesnd_andean_restoration_host` at triggers:2–11 unconditionally rejects the global Andean resolved flag; successful recognition/settlement sets it at effects:4,141,272, while existing-TWT invitations still require that host through `can_recognize` and the live invitation guard. This may disable post-victory joining. It predates repair1 and needs a root decision/independent case. The frozen copy remains unchanged; any authorized follow-up requires a new freeze.
