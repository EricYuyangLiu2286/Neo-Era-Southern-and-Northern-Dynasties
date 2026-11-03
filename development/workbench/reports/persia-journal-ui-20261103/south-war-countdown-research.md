# Ming–Wu civil-war countdown regression: source research

Date: 2026-11-03. Scope: research only; no MOD source changes, no game launch, no save modification. Current native installation: **Victoria 3 1.13.11 / Steam build 24799966**; catalog status `CURRENT`, zero changed native fingerprints. Proposed patch is unexecuted. This is source evidence, not engine acceptance.

## Finding and minimal recommendation

**The current main-war creation path lost the original `add_escalation = 90`. Restore it after all synchronous scripted backers have been added. Also correct the CNE joining helper's `root` to `prev` so the USM-root caller adds CNE as intended.** This is a demonstrated source regression, so the user's “leave it alone if already correct” condition does not apply to the countdown itself.

The preserved original starts `dp_usm_civil_war` in `usm_civilwar.2`, then marks its play and ends the opening operation with `add_escalation = 90`. See [original creation](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/events/usm_civilwar_events.txt:415>) and [original countdown](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/events/usm_civilwar_events.txt:469>) (effect at line 481). The backup event file is byte-for-byte identical to Git original `f18b6c45525351f5bf1a86ab29cccff9fee49500` (`git show f18b6c4:events/usm_civilwar_events.txt` comparison: `True`).

Current `usm_civilwar.2` now delegates in its immediate block to `nesnd_open_southern_war`. That replacement creates and marks the play, adds the chosen participants, then returns with neither an initial escalation nor `add_escalation` anywhere in the effect. See [current caller](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/usm_civilwar_events.txt:369>) and [replacement war opening](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_crisis_effects.txt:281>). No other current gameplay creator of `dp_usm_civil_war` exists under `common/` or `events/`; the only remaining active `add_escalation = 90` in `usm_civilwar_events.txt` belongs to a different Japanese protectorate conflict.

The native defines explicitly identify the consequence: opening ends at 21; closing/countdown begins at **80**, with the comment “After this, it isn't possible to join/sway further countries”; war starts at 100. See [native escalation thresholds](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/defines/00_defines.txt:1135>). The UI also says taking sides is unavailable during closing, and maps closing to `concept_countdown_to_war`: [native join restriction](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/diplomatic_plays_l_english.yml:65>), [native phase label](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/diplomatic_plays_l_english.yml:89>). Consequently, restoring 90 closes the ordinary joining/swaying phase while retaining a pre-war countdown and the possibility of backing down.

## Current caller and participant lifecycle

| Stage | Existing behavior and source | Implication for placement |
| --- | --- | --- |
| Accession and invitations | `flavorUSM.4` sets the crisis flags, queues southern replies/JAP for day 7, adds the civil-war JE, and calls foreign notification. [invitation chain](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/flavorUSM_ce.txt:577>) | Initial allegiance choices precede play creation. |
| CNE policy | Foreign notification queues CNE day 2; `nesnd_crisis.20.c` explicitly sets `nesnd_north_intervention` and calls join helper. [notification helper](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_crisis_effects.txt:169>); [CNE intervention option](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_crisis_events.txt:170>) | CNE can be a deliberate scripted participant; its flag is not itself a bug. |
| War timing | `ce_usm_civilwar_journal` has a three-month start buffer and fail/timeout routing to `.2`. [JE lifecycle](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_usm_the_last_days_of_ming.txt:297>) | No need to postpone countdown for normal replies. |
| Creation | `.2 immediate` invokes opening for USM. Opening selects an opposition leader, frees USM opposition subjects, creates and marks the play. [caller](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/usm_civilwar_events.txt:369>); [create/mark](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_crisis_effects.txt:269>) | Root remains the initiating USM country; selected opposition leader is a saved country scope. |
| Scripted opposition | All independent opposition countries other than target are added by `add_target_backers = { prev }`. [opposition backers](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_crisis_effects.txt:312>) | Must precede countdown. |
| Follow-up notices | `usm_civilwar.2` notices are queued for day 1. Current receiver options add JE/modifier/stance/court or notifications; none adds backers. [notice queue](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_crisis_effects.txt:327>); [receiver options](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/usm_civilwar_events.txt:391>) | These delayed notices do not require a normal joining window. |
| CNE commitment | CNE with `nesnd_north_intervention` calls the same helper synchronously; it attempts to add a backer to the marked non-war play if independent and not already marked joined, but currently uses the wrong `root` under this nested caller (see below). [CNE opening join](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_crisis_effects.txt:344>); [join helper](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_crisis_effects.txt:158>) | Preserve this join before countdown. |
| JAP commitment | Independent JAP with `ce_usm_cw_ally_with_mng` is added to the initiator side. Opposition JAP already passes the opposition loop. [JAP opening join](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_crisis_effects.txt:352>); [JAP pre-war choice](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/usm_civilwar_events.txt:2528>) | Append countdown after this block, rather than inside `create_diplomatic_play`. |
| Retry | The retry button calls the same opener; successful creation sets global `usm_civilwar_occured`, and the opener rejects subsequent calls. [retry button](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/nesnd_south_accords.txt:63>); [opening guard](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_crisis_effects.txt:181>) | No second creator or double-escalation path needs a patch. |
| Monthly CNE retry | The existing monthly action retries only while committed and unsettled. [monthly retry](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/on_actions/nesnd_crisis_on_actions.txt:1>) | Leave its scripted policy intact; ordinary joining is a separate interface. |

## CNE versus GBR/FRA: what is and is not established

The present `additional_involvement_trigger` permits opposition flags, north-intervention flags, JAP's pledge flag, **or any non-CNE country allowed aggressive plays**. It does not itself bar GBR/FRA. [current involvement condition](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/diplomatic_plays/ce_diplomatic_plays.txt:16>) The earlier original also had additional geographic/home-country/subject/alliance conditions, so the modern predicate is broader; however, restoring the final 90 is the smallest direct fix to the reported lost countdown. Changing both mechanisms is unnecessary to establish this correction and could alter unrelated scripted admission semantics.

CNE **without** the three eligible flags is already excluded by the current predicate. CNE **with** `nesnd_north_intervention` is intended to be added by script; the opener exposes a separate caller-scope error detailed below. The screenshot alone therefore cannot prove that CNE itself joined illicitly through the ordinary UI. GBR/FRA's external-policy event merely starts their policy JE; it does not add combat backers, and searches of every current `add_target_backers`/`add_initiator_backers` occurrence found no GBR/FRA scripted combat join in that external system. [external entry](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_external_events.txt:3>)

The missing countdown plus broad ordinary involvement gate is sufficient source evidence for the **opportunity** for noncommitted foreign joining. It is not a reconstructed record of each flag shown in the user's specific war. Some flags may be subjects attached by native obligations; this report does not recommend removing subject relationships or all foreign participants indiscriminately.

## Native complete-chain reference and applicable differences

1. Native `on_secession_start`, root country/target uprising country, conditionally queues `italian_unification.7`. [native caller and scopes](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:5521>)
2. Native `.7 immediate` finds/tags San Marco, selects its diplomatic play, and runs `add_escalation = 25`; its options queue `.8`. [native escalation effect instance](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/italian_unification.txt:546>)
3. Native `.8 immediate` captures that play, then a player choice adds `root` with `add_target_backers`. [native backer lifecycle](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/italian_unification.txt:643>)
4. Engine-generated 1.13.11 docs identify `add_escalation`, `add_initiator_backers`, and `add_target_backers` as effects on `diplomatic_play`; creation also supports an escalation integer 0–100. [effect docs](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:178>), [initiator backers docs](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:226>), [target backers docs](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:431>), [creation docs](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:909>).
5. The similar native Chinese bespoke civil conflict is `heavenly_kingdom_events` creating `dp_taiping_rebellion`, whose database uses mirrored annexation, hidden lens access, and an additional involvement trigger; its image is the existing native annex-country icon. [native custom play creator](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/heavenly_kingdom_events.txt:505>), [native play database and resource](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_plays/00_diplomatic_plays.txt:664>). Native Taiping intentionally allows ordinary interested countries, so its involvement policy is **not** copied as NESND's intended rule.
6. Native thresholds and the join-restriction UI above supply the observable phase contract. This proposal changes no icon, UI file, localization, war goal, or settlement database. The native 25 escalation is API/scope evidence only; NESND's original 90 supplies the design value.

## Required caller-scope correction for committed CNE

`nesnd_join_opposition_play` currently performs `add_target_backers = { root }` at line 164 and unconditionally sets `nesnd_joined_south_play` after the attempt. There are three callers:

| Caller | Current country at helper entry | Event/on-action root | What `{ root }` supplies |
| --- | --- | --- | --- |
| `nesnd_crisis.20.c` | CNE | CNE | CNE, as intended |
| monthly country pulse | CNE | CNE | CNE, as intended |
| `nesnd_open_southern_war` → `c:CNE` | CNE | USM | **USM**, the opposite side's initiator |

The generated engine scope docs define `root` as the head of the current top scope (e.g. event recipient) and `prev` as the previous scope: [root contract](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/event_targets.log:747>), [prev contract](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/event_targets.log:715>). A scripted effect call and `if` do not create a new country-event root. Entering `random_diplomatic_play` changes current scope from the joining country to the play; its `prev` is therefore CNE for **all three** callers. This matches the already used opposition join pattern at current line 324.

The two-line scoped operation should be:

```text
random_diplomatic_play = {
    limit = { has_variable = this_is_nanming_civilwar_var is_war = no }
    add_target_backers = { prev }
}
```

Change only `root` → `prev` at line 164. Without this correction, the opening path can attempt to add USM to the opposition side and nevertheless mark CNE as joined; a countdown-only fix could close the ordinary window without correctly honoring CNE's scripted commitment. The source mistake is established by the callers and scope contracts; its exact current engine response (rejecting the initiator, logging, etc.) has not been observed and is not claimed here.

## Exact minimal proposed patch

First change `add_target_backers = { root }` to `{ prev }` in the helper as above. Then apply the countdown insertion.

Append the following inside the successful creation branch, immediately after the existing `c:JAP` block (current line 365), before that branch closes:

```text
random_diplomatic_play = {
    limit = {
        has_variable = this_is_nanming_civilwar_var
        initiator = root
        target = scope:nesnd_opposition_leader
        is_war = no
    }
    add_escalation = 90
}
```

The marker plus exact initiator/target avoids touching another diplomatic play. At this point creation and all scripted add-backers calls happen in the same effect execution, so adding 90 does not consume a normal daily tick or require an intervening join window. Keeping this after additions also avoids relying on undocumented script admission after closing.

Prepared artifact: [unapplied unified diff](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/persia-journal-ui-20261103/south-war-countdown-proposal.patch>). The source file expected by this proposal has SHA-256 `c44177a411384595a209a92d27b96735f131407c0f5ff24e123dcf406500ee45`. The proposal adds nine countdown lines and changes one helper argument (`root` → `prev`) in the same effect file. It makes no other changes.

Do not use `war = yes` or escalation 100: that would remove the countdown and retreat opportunity. Do not replace the active custom annex goal `wg_nesnd_usm_annex`, disable collapse callbacks, or alter player loss/Japan partition effects. This patch does not touch them. See [current war goal reference](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/diplomatic_plays/ce_diplomatic_plays.txt:1>) and [retained defeat/partition callbacks](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/on_actions/nesnd_war_collapse.txt:14>).

## Validation and existing-save limits

- Completed: original/current source comparison; only one creator of `dp_usm_civil_war`; both live callers traced; synchronous/queued backer and caller-scope audit; native defines, UI, actual effect examples, and generated docs checked; proposed unique insertion anchor checked; source hashes recorded.
- Not performed: source patch, Tiger/parser/MCP post-change checks, game launch, user-save rewrite, or reproduction of the user's exact live war. `error.log` currently contains no matching `usm_civilwar`/`nesnd_open_southern_war`/`add_escalation` error, which neither validates nor disproves the design regression.
- Applying this fixes **future executions** of the opener, including an old save that has not created the war yet. It does not rewind a play already created below 80, eject participants already admitted, or alter a war already in progress. A live-war repair would require separate state evidence and scope; none is proposed here.
- If an engine check is later needed, use one preserved pre-opening scenario: verify chosen scripted backers, escalation 90/countdown immediately after creation, ordinary join/sway unavailable, and unchanged retreat/capitulation settlement. No repeated launch/reload is necessary to establish the source regression.

[Source hashes and original comparison](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/persia-journal-ui-20261103/south-war-countdown-research-provenance.json>)
