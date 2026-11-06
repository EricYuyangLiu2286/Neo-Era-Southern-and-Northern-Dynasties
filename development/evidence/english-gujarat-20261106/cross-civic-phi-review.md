# Independent cross-review: civic characters and Luzon

Reviewer: `/root/astra_english_small_native`, explicitly configured **gpt-6-astra / high**, as confirmed by root. Read-only review of the two frozen English files and their Chinese counterparts. This review did not edit localization or gameplay. The only output written for this cross-review is this report.

## Result

All **281 entries** independently read and compared: **201 civic-character entries**, **80 Luzon entries**. The English retains the Chinese arguments, individual interests, options and relevant numerical details. One definite minor language correction remains before editorial sign-off. A separate renewal sentence would benefit from a small clarification. No blocking numerical, dynamic-reference or gameplay-contract error was found in the inspected scope. **ENGINE_NOT_RUN**; this is an editorial/source review.

The other writer's report and comparison JSON were used as navigation, not as evidence of correctness. I read the live bilingual files and actual event/trigger/effect chains myself. A fresh comparison against the independent pre-change backup confirms **135 civic + 45 PHI changed entries**. My independent structural checks confirm identical key order, unchanged dynamic expressions/localization references/format tags and numerical-token multisets, no duplicate keys, matching Chinese/English key order, UTF-8 BOM and no CJK in English.

Backup-path detail: the pre-change PHI English file is at `localization/english/nesnd_phi_finance_l_english.yml`, while the frozen current file is in `localization/english/replace/`. Its actual backup SHA-256 is `15aa1fe099258dfafc4923045029f616a72441d90c75a88abc8c37d497254c36`. After locating that moved source, the independent comparison covered all 80 PHI entries successfully.

## Required correction

**P3 — Bellandi introduction: unnatural tense combination.**

File: `localization/english/replace/nesnd_civic_characters_l_english.yml:15`, key `nesnd_civic_characters.2.d`.

Current: “She has soon found that many of their arguments can be put to the very people who run the school.”

Chinese: “她很快发现，文章中的许多道理恰好可以用来追问办学的人。”

Replace **“She has soon found”** with **“She soon discovers”**. The surrounding narrative is in the present (“Bellandi teaches”), and this retains both the timing and the discovery without the awkward present-perfect construction. No mechanical token is involved.

## Recommended clarification

**P3 — Cash naval proposal: prefer standing-allocation wording on renewals.**

File: `localization/english/replace/nesnd_phi_finance_l_english.yml`, key `nesnd_phi_finance.13.d`.

Current: “Twenty ships of the line would come under the central navy, with their bases, crews and supplies arranged by the centre.”

This can be read as a new handover whenever the event appears. The same event is used for renewed cash-route proposals (`common/scripted_effects/nesnd_phi_finance.txt:652-704`; `events/nesnd_phi_finance.txt:712`), whereas actual ownership transfer occurs only when `nesnd_phi_b_transferred` is absent (`common/scripted_effects/nesnd_phi_finance.txt:415-437`). The terms tooltip explicitly says renewals do not transfer more ships, so this is an avoidable narrative ambiguity rather than a missing rule or unequivocal false promise.

Suggested replacement sentence: **“The proposed division places twenty ships of the line under central naval command, which provides their bases, crews and supplies.”** This states the proposal's standing division and works for both first agreements and renewal. Keep the rest of the paragraph and the separate £3,700/one-year funding sentence.

The other naval prose was checked with this branch in mind. Event .2 describes where the ships “would belong” under a proposed division. Events .4 and .14 explicitly frame command as the arrangement's terms and still await signature. The tooltips clearly restrict actual transfer to the first agreement. I do not classify these as further defects.

## Whole-series editorial review

The repeated support/neutral option structure follows the actual events. It does not say that supporting a character immediately enacts the reform: the options add a support modifier and backing variable for twelve months, while the alternative is a political response. Follow-up events choose the character description only when a living relevant character remains in the country; the eighteen organisational descriptions do not invent death, retirement or exile.

| Civic pair | Independently checked argument and result |
|---|---|
| 1 / 101, Valdieri | Contractor advances, treasury arrears, guarantees, repayment and taxpayer exposure all survive the translation. |
| 2 / 102, Bellandi | Girls' education, poor pupils' fees, citizenship and the reluctance of respectable supporters are distinct. Only the tense correction above is required. |
| 3 / 103, Rusciani | Common government funding competes with southern roads and schools; mining revenues and local shares remain explicit. |
| 4 / 104, Sereni | Soldiers' pay, families, engineering education and life after service remain linked. Republican claims belong to Sereni and his volunteers, without declaring the host state a republic. |
| 5 / 105, Vitali | Church control, public grants, families' fees and teachers' wages remain the grounds of dispute; the parties retain different interests. |
| 6 / 106, Martelli | Injured miners' households, compensation, education and mining revenues remain explicit. The pointed final option retains the Chinese political voice. |
| 7 / 107, Tong | Immediate public savings are weighed against long concessions, route choice, freight charges and future local costs. |
| 8 / 108, Shen | Debt dependence, freedom, literacy and association remain a connected argument; the organisational branch concerns intergenerational dependence. |
| 9 / 109, Bayantu | Seasonal routes, water and pasture are distinguished from the occupied plot's market value. Compensation is proposed, not asserted as a completed effect. |
| 10 / 110, Lin | Evening lessons support workers' reading of wages and debt bonds, then collective self-advocacy. No immediate change in employment law is claimed. |
| 11 / 111, Lu | Public accounts, work actually done, employment and engineering credibility remain separate from contractors' reputations. |
| 12 / 112, Guan | Oil taxes, reinvestment, schools, roads and a fixed producing-district share retain both material and political dimensions. |
| 13 / 113, Ji | Practical learning, access to office, pedigree and property qualifications remain distinct. The Assembly of Rites retains its examination role. |
| 14 / 114, Duan | Sichuan curriculum and student places are tied to recognised qualifications and students' political prospects. |
| 15 / 115, Xu | Existing qualifications and property face post-war fiscal demands; the gentry's responsibility to fund public affairs is not removed. |
| 16 / 116, Luo | Women workers' literacy starts with wages and invoices and develops into access to other positions; the Chinese challenges remain intact. |
| 17 / 117, Han | Skills, fees, pay and injury protection remain connected. Employer and worker interests are not collapsed into generic educational benefit. |
| 18 / 118, Jiang | Coastal profits, inland tax burdens and provincial educational places remain differentiated. Delegates debate and explain budgets; they are not made provincial administrators. |
| 200, Duan's qualification | Text follows actual qualification, rather than merely permission to sit an examination. `nesnd_c2_duan_qualification` sets the qualified flag after constitutional choice 2/3 and triggers the event; the event requires a living qualified politician. |

All names, titles, options and eighteen support-modifier names were included in the read-through. Longer paragraphs and rhetorical questions largely reproduce the current Chinese's deliberate arguments. I found no new repeated generic ending that substitutes a summary for those arguments. Organisation paragraphs focus on what contractors, teachers, soldiers, workers, herders or delegates are doing, rather than on an absent actor's unexplained fate.

## Luzon phase and numeric review

Read `events/nesnd_phi_finance.txt`, the relevant callers in `common/scripted_effects/nesnd_phi_finance.txt`, actual eligibility/readiness triggers and `common/journal_entries/nesnd_phi_finance.txt`.

- The JE reason retains the Chu/Huguang migration, Lin Zexu, the overseas garrison and the clash between central naval service and local livelihoods. The northern-threat claim in event .1 is attributed to the Commission's argument, not asserted as a universal current trigger result.
- Central proposal events .1/.2/.11/.13 remain proposals. Approval advances to final Luzon signature, and .3/.4/.12/.14 explicitly await that signature. No subsidy is described as already paid at approval.
- Actual treaty creation precedes `.5`. A twelve-month term is recorded, and .5 accurately describes assistance beginning. The English does not turn the year into a permanent grant.
- .6 is expiry, .7 is interruption, and .10 is an amended agreement. The broader word “arrangements” in .7 correctly covers lost treaty or concessions as well as altered subject/market/peace eligibility. It does not invent a particular war or diplomatic break.
- Native routes preserve £8,000/£3,000, twelve months, the 10-percentage-point tribute reduction, £10,000/£5,000 surplus and £100,000/£60,000 reserves. Cash routes preserve £8,700/£3,700 and their distinct tribute treatment.
- First naval transfer is twenty owned, surviving ships of the line not in battle; the frigate/garrison division and no further transfer on renewal remain in the operation tooltips. “Not in battle” matches `is_in_battle = no` more precisely than “not at war”.
- Withdrawal preserves other agreements' separate terms and transferred ships' ownership. Expiry removes the relevant subsidy while leaving tribute/exemption arrangements governed separately. Amendment is not called cancellation.
- The four requirements retain 35 battalions, 40/20 surviving ships, 75% crew per qualifying ship, 80% maintenance fulfilment, 12% unemployment and 15% starving workforce, together with fiscal/default/bankruptcy conditions. Both workforce denominators are national workforce.
- The completion prose follows three qualifying peaceful months after subsidy cessation, matching the JE's ever-received, inactive and good-months conditions. Ending the subsidy resets the counter through `nesnd_phi_clear_active`, so this is not a premature completion claim.
- The status links, aliases, concept references and currency/colour formatting remain unchanged.

## Fleet-name location recommendation

Use the existing pair:

- `localization/english/replace/ce_country_flavor_l_english.yml`
- `localization/simp_chinese/replace/ce_country_flavor_l_simp_chinese.yml`

Append within **“Armies and other”**, next to the existing `Nanyang_fleet`, `Dongyang_fleet` and `HUS_fleet_of_dongyang` formation names. The English group is at lines 19-34; the Chinese equivalent begins at line 24. These files already hold short military formation names. `ce_anniversary_formations` concerns national formation events and is not an army/fleet-name catalogue; `ce_scripted_names` currently concerns IG/party names.

Exact proposed entries, for root to add:

```yaml
 nesnd_french_gujarat_squadron:0 "Gujarat Squadron"
```

```yaml
 nesnd_french_gujarat_squadron:0 "古吉拉特分舰队"
```

The country-history formation at `common/history/military_formations/nesnd_french_gujarat_fleet.txt:6` already references this key for France's fleet in `sr:region_north_india`, with two ships of the line and four frigates. The concise name fits that formation without adding unsupported rank or institutional history. I did not add the key.

## Reviewed fingerprints

| File | SHA-256 |
|---|---|
| English civic | `af68ee61ea2a4a88b93ce6395bb04888f2987337e1315fa8a453308815cc1eb4` |
| Chinese civic | `8d45c90975f7da7f6e89444d1dbcc22ee7a0af3f48a956937025818652c6e9de` |
| English PHI | `fbd3163d29d089a023d6cc5c35df72123c00830081898e2768fd69b9fb013077` |
| Chinese PHI | `96a12d38aa68e9628c2cfa8214f250286f2d6e6f86432b029aa1c2b95e3018ea` |

These are the actual bytes reviewed, independently hashed during this pass. A root correction changes the corresponding fingerprint and requires the affected entry to be read again. No game was launched, and no engine or visual-layout claim is made.
