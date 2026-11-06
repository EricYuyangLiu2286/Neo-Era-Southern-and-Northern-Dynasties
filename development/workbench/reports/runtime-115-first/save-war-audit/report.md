# Frozen save war audit — 2026-11-05

Read-only source inspection. No game/UI, live monitoring, source edits, Git, or save rewriting. Runtime model/reasoning metadata was not exposed to this inherited agent.

## Provenance and limits

The snapshots in `snapshots/` were copied once and checked for unchanged source size/mtime before and after copying. `snapshot-manifest.json` records paths, source timestamps, byte counts and SHA256. Five plaintext snapshots are the same 1.15.0 playthrough (`8c986e5e-59ce-48f3-808a-d25b64f58c1d`): 1837.6.18.18, 1849.7.1, 1850.1.1, 1850.7.1, and latest 1851.7.1. The intervening autosave_1.v3 is ZIP/binary; local rakaly0.8.22 fails on token0xd04, including the stringify fallback. No partial melt is used as evidence.

The ordered parser reads individual database records; unindented numeric record boundaries are used, preserving nested records. Full state parsing is unsupported because of proprietary statistics syntax, so state evidence uses only anchored top-level owner/previous-owner/date fields. Missing variable identities remain missing, not zero. Value identities use signed64 fixedpoint /100000. Each plaintext snapshot has its complete extracted `*-audit.json`; active wars/plays and JE records retain raw blocks.

## Confirmed timeline

| Date | Live relevant tags | Anti-Wu and JE evidence |
|---|---|---|
|1837.6.18.18|USM735, HNA310, GNG315, SIH316, PHI171, SHA317; no WUU definition|No saved opposition flags yet. USM active conflicts_within/ruling_of_nanfu. Relations USM–SIH+50, USM–HNA+20, USM–GNG+50; no serialized truces for those pairs.|
|1849.7.1 /1850.1.1 /1850.7.1|USM735, GNG315, PHI171, SHA317; HNA/SIH/WUU absent|GNG and PHI each have usm_opposition_country=1 and active ce_usm_restoration_of_ming added1839.4.4. USM has active ce_usm_suppress_rebellion added1839.4.4. USM and GNG are not in a mutual active war.|
|1851.7.1|USM735 and SHA317 alive; GNG/PHI/HNA/SIH/WUU absent from entire live country definition map|USM has usm_government_winner_civilwar=1; suppress_rebellion is no longer active. New active USM nesnd_wu_eastern_question and nesnd_c2_usm_agenda both added1851.5.27.|

USM retains `tag_WUU_var=1` and `ce_country_is_daming=1` in all1849+ snapshots. A live WUU definition is not required for the saved USM Wu-identity marker. Opposition country count stays4, including latest when no live opposition-tagged country is present. The count is a persisted counter; these snapshots alone cannot establish its intended counting semantics. `usm_subject_country_count` is−2 in every1849+ snapshot (raw18446744073709351616 = 2^64−200000). The choice and choice_tt variables have type=value but no identity; no numerical value is invented.

Globals retain `usm_civilwar_occured`, `sih_anti_wuu_choice_1`, `sih_anti_wuu_choice_2`, and `sih_anti_gng_choice` as boolean1 in1849+. Latest also has `nesnd_south_settled=1`. The presence of a flag establishes saved state, not that current script logic ran in the observed interval.

## Standstill and truces

USM–GNG relation is+33 in all three1849.7–1850.7 priors; both first_truce/second_truce are absent and there is no mutual active war. This proves observed peace across the snapshots; it does not by itself prove a specific AI cause or uninterrupted peace between snapshots. USM–PHI relation value is omitted and no truce is serialized; omitted relation value is not reported as zero. PHI–GNG is−33 without serialized truce.

USM–CNE has relation−42 and both truce dates1852.5.15.18 in all1849+ snapshots. That date is still future at latest1851.7.1. USM–HUS truce1837.1.1 is expired. USM–SHA+50 has no serialized truce. Full-save scans of quoted and unquoted flag names in all five plaintexts found no `standstill`, `faction_leader`, `anti_wuu_lead`, or `opposition_lead` marker. This is a bounded name search, not proof that no other marker implements leadership or standstill.

## State and character evidence

Six latest state records (805,806,807,822,1035,1039) preserve previous_country_definition=SIH, current ownerUSM735 and last_owner_change1840.7.2. HNA is already absent by1849.7, but no surviving previous-HNA state record establishes its exact end date. Two latest records811/1042 preserve previousGNG, ownerUSM and last_owner_change1851.5.4. These establish those transfers, not an independently reconstructed whole annexation or war identity. One record827 preserves previousUSM, currentCNE and last_owner_change1847.5.2.

Latest USM ruler16780636 has first_name=name_Ju and last_name=ce_Zheng. Saved `nesnd_ming_claimant_ref`=com3145 and `nesnd_ming_heir_ref`=com3146 remain present, but character_manager contains exact tombstones `3145=none` and `3146=none`. The references no longer resolve to live character records. `nesnd_ming_refuge_resolved` and `nesnd_ming_retained_notice` are still1. No restoration source edit was made.

The inactive `nesnd_ming_after_truce` JE is saved forUSM with active=no/date_added1836.1.1 in all examined snapshots. This default inactive record cannot prove it previously activated or completed.

## Other wars

In all three1849.7–1850.7 priors USM participates in war61, the broad RUS–QE1 war started1849.2.26; GNG/PHI do not participate in it. Latest war61 is dead with peace_date1850.12.30.18. Latest USM is in no active war.

Latest has five active wars:65 (CMB,FRA,NET,SAR,PLY; began1850.4.19),70 (RUS,GRE,FIN,UBD;1851.3.24),71 (SER,TUR,GRE,MOL,WAL,TRI,TUN,SIC;1851.4.25),72 (SWE and Swedish revolt;1851.6.16),73 (USA,LKT,LIB;1851.6.29). Six active plays include an ALT revolution not yet at war (warID4294967295). Raw records and ID-to-tag maps are in latest auditJSON.

Deleted war records can lose participant/play references. Two latest dead wars68/69 started1851.1.23/1851.2.24 but have invalid play refs and peace_date1.1.1; this evidence does not identify either as the final PHI/GNG war. Do not infer exact victory dates from these orphan records. The1851.5.4 transfers and1851.5.27 newJE activation show post-standstill progress, while the exact initiating mechanic remains source/war-agent analysis.

## Reproduction

`extract.py` processes only frozen plaintext snapshots and emits complete auditJSONs. `latest-character-16780636.txt` preserves the ruler block. `latest-war_manager.txt`, `latest-diplomatic_plays.txt`, `latest-relations.txt`, `latest-pacts.txt`, and selected country text blocks permit raw-record review. The report's claims were checked directly against those records and snapshotJSONs; this is saved-state evidence, not new engine verification.
