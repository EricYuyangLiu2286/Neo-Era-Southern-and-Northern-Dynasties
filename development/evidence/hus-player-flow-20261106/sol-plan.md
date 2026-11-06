# Narrow journal repair plan

Delegation: /root -> /root/sol_hus_supply_diagnosis; actual configured model gpt-6.1-sol, reasoning medium.
Scope: only common/journal_entries/nesnd_supply_journals.txt and common/journal_entries/nesnd_small_states.txt. Existing pre-change source snapshot supplied under before/. No game, Git, localization, monthly writer or reward changes.

Native basis: catalog status CURRENT, Victoria 3 1.15.0 build 26453692. GAME/common/scripted_buttons/scripted_buttons.md defines manual buttons unless autocomplete=yes; GAME/common/scripted_buttons/china_buttons.txt:49-58 uses market.owner=root; GAME/common/journal_entries/journal_entries.md defines triggered outcomes and hidden invalid_outcome, but only promises declaration order for presentation. GAME/common/journal_entries/00_alaska.txt:26,89-105 -> common/scripted_buttons/00_scripted_buttons.txt:310-407 -> events/alaska_events.txt:171 shows button/event writing success variable before outcome.

1. HUS supply: prepend two ready-for-review statuses gated by live all_ready and weeks>=12, partitioned by existing market ownership. Wrap done completion in player-facing custom tooltip. Preserve manual confirmation and all effects.
2. Four small-state economy/governance journals: hidden success gate on permanent done, visible goals only before done, explicit months tooltip at all times. Invalid outcomes require not done, with original invalid reasons otherwise unchanged. Monthly writer remains sole reward authority.
3. Small-state order journal: same completion contract because monthly completion writes done and removes active, otherwise making invalid true. No other journals changed.
4. Freeze edits and inspect structural diff, braces, names and hashes. This is static source verification, not engine validation. Independent main review follows.
