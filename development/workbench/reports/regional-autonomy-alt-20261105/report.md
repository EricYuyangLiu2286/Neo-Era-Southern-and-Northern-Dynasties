# ALT / Soconusco completion — corrected and applied

**STATIC_PASS; ENGINE_NOT_RUN.** The corrected supplement is installed in the main MOD. It changes nine files: seven existing script/data/localization files and two new flag/coat-of-arms files. No population, religion, opening ownership, map pixels, capital locators, shared wars or diaspora changes. No game or Git operation was performed.

## Result

ALT now has an assigned local independence candidate: **SO1 Soconusco**, using native **Mayan culture and Catholic religion**. The existing9,251 Maya in the UCA/ALT portion of Chiapas provide the local population; no new culture, demographic estimate or conversion was added.

The founding territory is the existing **Tapachula wood-hub province `x1030C0`**. ALT retains **Mapastepec farm-hub province `x4DBDE9`** and its two northern provinces. Both the released territory and the remaining three provinces are connected. Mexican-owned Tuxtla is not selected or falsely described as a retained host city. Mapastepec is an existing named hub, not an invented city asset.

At the native16,667 population, ALT stays below the existing viability thresholds and sees a specific future Soconusco candidate. Growth on the same four provinces to49,999 remains blocked;50,000 enables release. The ordinary20,000 owner-state/50,000 host thresholds remain unchanged. Loss or occupation of Tapachula or Mapastepec, release of the last owned territory, a living SO1, or its previous creation receipt blocks the route. A living native MAY does not block this distinct local government.

All eleven kinds now resolve their founding region, country, culture, religion, dispatch, polity registry, partner and localized territory. Independent review verifies the original ten cases remain intact; kind10 Guayana remains a whole-state route, while kind11 Soconusco uses the province route.

## Tag collision and flag correction

The initial proposed ID **SC1 was wrong**: native SC1 is New Spain. The first symbol check collapsed declarations into a keyed dictionary and masked that collision. The initial seven-file supplement was reverted to its exact prior preimages, and the rejected checkpoint and review were archived. The actual Soconusco ID is now **SO1**. Native SC1's country, flag, coat of arms and English/Chinese values remain intact. The earlier SC1 approval is explicitly rejected, not retained as evidence for the final release.

The expanded source check also found missing flag closure in all seven new regional tags: HM1, NM1, NP1, BT1, GY1, OR1 and SO1. Native DEFAULT rules do not provide an unconditional generic flag; the fallback is the country's tag as a coat-of-arms key. Two narrow files now explicitly bind each tag to a unique prefixed coat of arms and the existing native horizontal-split pattern. These are simple fictional banners using each country's map colour and white, with no political emblem or historical-flag claim. No external or raster artwork was added. `flag-design-manifest.json` records the palettes.

## Sources and validation

The Mexican Culture Ministry's [Mam profile](https://sic.cultura.gob.mx/ficha.php?disciplina=&table=grupo_etnico&table_id=64) places this Indigenous community in the Chiapas/Soconusco context and describes Catholic local observances. The game's broad Mayan bucket is retained rather than reclassifying all9,251 people specifically as Mam. [INAFED's official article](https://www.gob.mx/inafed/articulos/municipios-del-soconusco-chiapas-175-anos-de-pertenecer-formalmente-a-mexico?idiom=es) describes Soconusco's autonomous period through1842; its direct page returned403, so only its official indexed excerpt was used. The new polity is an alternate local outcome, not a claim of uniform historical ethnic sovereignty.

Native1.15 map data, English/Chinese hub localization and actual history identify the two exact owned hubs. `provinces.json` and `chiapas.png` retain the geographical evidence. Current native flag-definition documentation, native pattern use and HSV360 examples support the explicit flag implementation.

- **310 source-AST cases against installed main files**, covering same-land growth, retained Mapastepec, ownership/occupation, existing MAY, duplicate SO1 and all previous hosts: `main-seed-tests.json`.
- **96 independent script/data/localization checks**, plus **112 raw multi-definition, flag, pattern, palette and localization checks**: `sol-so1-review.md`, `sol-validation.json`, `sol-symbol-validation.json`.
- Original pre-change ALT still has no seed at50,000 on the same four provinces, while the GUA positive control remains valid: `original-alt-growth-counterexample.json`.
- Removing the two flag files reproduces seven unresolved flag cases: `sol-symbol-before-flag-counterexample.json`.
- Five Astra-authored bilingual values are unchanged; only SC1 identifiers were mechanically rekeyed to SO1. All five new keys are unique across actual main localization. The community files contain36 pairs each:31 previous plus five new. The other two original regional replacements remain in their original files.

## Exact installed state

`applied-manifest.json` binds the corrected nine files to reviewed preimages and post-write hashes. The final set digest is `d2f5dc7e079859143d981a4652401b72599521604478deb34cba97c1a0fa3c86`.

`combined-regional-main-manifest.json` binds all **16 current regional release files**. `post-apply-verification.json` confirms their hashes. Use these current manifests; files ending`-superseded-sc1` and`rejected-sc1-checkpoint/` preserve the rejected checkpoint for audit only.

No engine run was performed. Static checks do not establish runtime population/building allocation, budgets, recruitment, tooltip rendering or war acceptance. This implementation agent's inherited model metadata is not exposed; independent review was configuredgpt-6.1-sol/medium and the writing agent reportsgpt-6-astra/high.
