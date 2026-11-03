# Standards: Ming generation follow-up

Snapshot review: `backups/pre-change-persia-journal-ui-20261103T005805Z/mod` → `exports/persia-journal-ui-20261103-a`, using per-file `git diff --no-index` and full new files. This supplements `standards-final.md`; it does not create a synthetic Git merge-base.

**No new documented-standard breach or actionable Fowler smell found.**

Reviewed the new `common/{scripted_effects,scripted_triggers,on_actions}/nesnd_ming_generation.txt`, restoration integration, event options, character-role dependency, and effective Chinese/English tooltips. Scope and variable guards follow NESND `references/syntax-and-routing.md` §§引用安全、人物及创建回调. Existing-character search and generation guards share the same qualification predicates; creation uses a new nonhistorical character rather than reusing a historical template. Generated scope reads have explicit existence branches, and settlement checks actual accession before committing.

The previously identified global scan on every newborn has been removed: `scripted_effects/nesnd_ming_generation.txt:264` now identifies only the guarded `owner.ruler`. Global identity repair remains in the exceptional restoration path. This follows the affected-character maintenance rule in `references/journal-text-contract.md`.

Native checks: GAME `00_code_on_actions.txt:6751` documents character ROOT for heir birth; `00_victoria_heir_generation.txt:17` and `00_victoria_ip4_scripted_effects.txt:2028` establish creation/recruitment patterns; `events/brazil/pedro_brazil_events.txt:937` confirms character variables and saved scopes inside `on_created`. Engine `effects.log` verifies creation, transfer, naming, and ruler interfaces. The full primary-source chain is recorded in `ming-successor-generation.md`.

Both prior tooltip findings are corrected: restoration describes availability and foreign-ruler protection; Persian claims say “foreign power.” No broad tooltip regression was found in this follow-up. Terminal-generation name reuse remains a Spec-axis matter. Jomini repeated branches and scope traversals are retained under `docs/agents/engineering-skills.md`; no OO-style refactoring is warranted.

Reviewed SHA-256: generation effects `e84c671757bc3936862305fe3de0c9620d884a2d59529a0ead11b69bf1b43dd5`; generation trigger `29f99a0569f12951953051a8ff269150161cbc85a07daf1246b5fc943dbd0587`; generation on-action `cdf3628c4de439038eb1c5f3e70ef219fcd1714713fe565aa288a1a66ca6a52b`; restoration effects `04c8647c38b163c79f9fde75cfc3666104531fabe028e475b02f92577e13d8ad`; event `7e765a85c2e4464c33931006e7e08ebc8a8b4373eab0fa1cdfe6ea6a0eb558b1`.

Catalog CURRENT: 1.13.11 / build 24799966. Source review only; no game launched, no gameplay files edited, no engine-pass claim.
