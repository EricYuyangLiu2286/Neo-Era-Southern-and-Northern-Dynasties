# France–Gujarat source inventory (2026-11-06)

## Scope and baseline

Read-only inventory of the current primary MOD and installed Victoria 3 game. No MOD or game files were changed and the game was not started. `catalog.py status` reports installed source baseline **1.15.0 / build 26453692**, indexed version 1.15.0, `CURRENT`, 0 changed source files.

Authorized geographic scope interpreted literally: transfer the current **USM-owned Gujarat substate**, **Baroda (BER)** and **Nawanagar (NAW)** to France. Gujarat is one `state_region` with nine owner slices. Only the three specified slices are in scope; leave Kutch (KUT), Dhar (DHA), Idar (IDA), Porbandar (PLP), Junagadh (JUN), and Bhavnagar (BHV) untouched.

## Ownership and province split

Primary source: MOD `common/history/states/00_states.txt:4254-4298`; current game state region and port locator: GAME `map_data/state_regions/10_india.txt:153-167`.

| Slice | Current owner | Provinces (map color IDs) | Count | Authorized transfer |
|---|---:|---|---:|---|
| USM | USM | `x31D0E0 x9C8D06 xCC1D23 xF87E91 xC7C3FD xB0D060 xF01160 x0C6CB1` | 8 | France |
| Baroda | BER | `x3151E0 x73656F xEB1229 xD8CEF7 xECB4F5 x90B589 x03C674 x30E365` | 8 | France |
| Nawanagar | NAW | `xFC0FC1 x164DBB xD77765 xB9D851 x49DDB8 x0A4C7A` | 6 | France |
| Kutch | KUT | `xC0310F xF64FA2 xB05060 xEB6009 x5B6745 x8F568D xB89EF0` | 7 | Preserve |
| Dhar | DHA | `x4EB354 x7E0401` | 2 | Preserve |
| Idar | IDA | `x3FFA53 x128888 x90052D x4133D4 xADD2A3` | 5 | Preserve |
| Porbandar | PLP | `xD31590` | 1 | Preserve |
| Junagadh | JUN | `x30D060 x075A8E xB3D1CD` | 3 | Preserve |
| Bhavnagar | BHV | `x697511 xB11F7B xBBB2BD` | 3 | Preserve |

The three authorized slices are 22/43 Gujarat provinces. The port locator is `x31D0E0`, inside the USM slice (`10_india.txt:166-167`). The two USM-owned colors `xF01160` and `x0C6CB1` occur in an old commented-out Portugal slice at `00_states.txt:4263-4267`; current active ownership is USM at lines 4284-4288, so they belong to the authorized USM portion.

## Population baseline

Source: MOD `common/history/pops/10_india.txt:395-703`. All pop groups are individual repeated `create_pop` blocks; preserve each block's culture, religion, pop type, size and order. Sums below are arithmetic over the listed `size` values, not live game UI measurements.

| Slice | Population |
|---|---:|
| USM | 2,643,330 |
| Baroda / BER | 1,118,767 |
| Nawanagar / NAW | 233,775 |
| **Authorized transfer total** | **3,995,872** |
| Other six minors, to preserve | 1,394,791 |
| Gujarat total | 5,390,663 |

USM contains mostly Gujarati Hindu/Sunni groups, a Gujarati Jain-commented Hindu group, small Parsi, British/Scottish bureaucrat/capitalist/officer, Armenian, Portuguese, and other Gujarati/Pathan groups (`621-702`). Baroda's group list includes Gujarati Hindu/Sunni/Protestant/Catholic, Marathi, Rajput, and Pathan (`396-435`). Nawanagar includes Gujarati Hindu/Sunni/Jain-commented Hindu plus Marathi and Sindi (`553-577`). Keep the three slices' existing identities and counts; don't move any other minor's populations.

When those country slices become French-owned, history/population selectors keyed to `region_state:USM`, `region_state:BER`, and `region_state:NAW` need to be reconciled with the resulting French `region_state` ownership. A merged French slice cannot retain ownership history under dead regional tags. Preserve all repeated pop records; do not collapse them by parsing into a map or replacing the full Gujarat history with one aggregate pop.

## Buildings, owners, levels, and production methods

Source: MOD `common/history/buildings/10_india.txt:933-1243`. `reserves = 1` is set on each listed building. The `add_ownership` type is shown as written; it is not inferred from the building type.

| Slice | Buildings / levels | Historic ownership | Production methods |
|---|---|---|---|
| USM | Government administration 1; port 1; textile mill 1; paper mill 2; furniture manufactory 1; cotton plantation 2; tobacco plantation 1; silk plantation 1; fishing wharf 1 (11 total levels) | Administration and port public to USM. Textile 1, paper 2, furniture 1, fishing wharf 1 privately owned by USM. Cotton 2, tobacco 1, silk 1 have `building_manor_house` ownership by USM. | Administration: `pm_simple_organization`, `pm_hereditary_bureaucrats`, `pm_religious_bureaucrats`; port `pm_anchorage`; textile `pm_handsewn_clothes`, `pm_no_luxury_clothes`, `pm_traditional_looms`; paper `pm_pulp_pressing`, `pm_automation_disabled`; furniture `pm_handcrafted_furniture`, `pm_automation_disabled`, `pm_luxury_furniture`; plantations default crop PM + `pm_road_carts`; fishing `pm_simple_fishing`, `pm_unrefrigerated`. |
| Baroda / BER | Government administration 1; shipyard 1; furniture manufactory 1; textile mill 1; fishing wharf 1; tobacco plantation 1; naval administration 1 (7 total levels) | Administration and naval administration public to BER. Furniture, textile, fishing wharf privately owned by BER. Tobacco 1 has `building_manor_house` ownership by BER. Shipyard has one level held by BER through `building_financial_district` ownership (`1071-1075`), a normal private investment ownership pattern also used by vanilla shipyards. | Administration as above; shipyard `pm_basic_shipbuilding`; furniture/textile/fishing as above; tobacco default crop PM + `pm_road_carts`; naval administration `pm_simple_sailor_recruitment`. |
| Nawanagar / NAW | Livestock ranch 1 (1 level) | `building_manor_house`, country NAW | `pm_open_air_stockyards`, `pm_simple_ranch`, `pm_standard_fences`, `pm_unrefrigerated` |
| KUT (preserve) | Fishing wharf 1; livestock ranch 1 | Fishing private KUT; ranch `building_manor_house`, KUT | Fishing as above; ranch same as NAW |
| BHV (preserve) | Fishing wharf 1; cotton plantation 1 | Fishing private BHV; cotton `building_manor_house`, BHV | Fishing as above; cotton default crop PM + `pm_road_carts` |
| JUN (preserve) | Fishing wharf 1 | Private JUN | `pm_simple_fishing`, `pm_unrefrigerated` |
| DHA, IDA, PLP (preserve) | No Gujarat history buildings found | — | — |

The authorized inventory is **19 listed building levels**. Existing foreign/private ownership should remain private when owners change: convert owner tags BER/NAW/USM to FRA only where ownership is explicitly those owners. Retain building types, levels, production methods, reserves, and repeated building blocks. Gujarat has one designated port province, but the listed shipyard is Baroda's slice; do not assume `building_naval_administration` is itself a fleet.

## Tag, treaty, and military references

- BER and NAW are existing base-game country tags, not new tags: GAME `common/country_creation/00_releasable_countries.txt:3040-3043` and `3065-3068` define their exact Gujarat province sets. Their active MOD geography is the state-history assignment above. Their active MOD references outside geography/building/pop histories are India/princely-country predicates (`common/scripted_triggers/nesnd_commission_expansion.txt:34`, `nesnd_india_core.txt:4`), localization existence checks, and flags. No active Gujarat treaty or military formation target to BER or NAW was found in the scanned MOD history files.
- Those reusable/releasable country definitions remain available in the base game. If BER/NAW no longer own territory after transfer, release/formation predicates and any future release can still refer to them. They are not missing tags or startup-invalid merely because the historical start no longer assigns them land; decide separately whether they should remain releasable.
- MOD `common/history/treaties/ce_historical_treaties.txt:30-61` has the historic USM–QE1 pact; `:64+` continues unrelated treaties. No BER/NAW treaty entries occur in MOD treaty history. `common/history/treaties/00_historical_treaties.txt` contains no active BER/NAW entry. USM–QE1 is unrelated to a France/Gujarat transfer and should not be edited on this evidence.
- No BER/NAW army or formation target occurs in MOD `common/history/military_formations/`. MOD's only active USM state ownership slices elsewhere are separate geography and are out of scope.
- France currently has four Europe-based army entries in the base-game `common/history/military_formations/00_military_formations_europe.txt:746-861` (three corps plus `troupes_de_la_marine`, all `type = army`; a later North Africa army begins at `:874`). These are not local Gujarat naval forces. MOD France initialization is `common/history/countries/fra - france.txt`, but does not provide a Gujarat fleet setup.

## Native 1.15 naval and formation evidence / implementation cautions

- Current game effect example `common/scripted_effects/00_victoria_scripted_effects.txt:1-19` creates an army with `create_military_formation`, `type = army`, `combat_unit` entries (`type`, `state_region`, `count`). Current game history also directly defines fleet formations.
- France's native setup at `common/history/military_formations/00_military_formations_europe.txt:923-992` has four `type = fleet` formations: Mediterranean (`hq_region = sr:region_southern_europe`, ship counts 13 line ships, 19 frigates, 10 troop ships), North (`region_western_europe`, 12/23/8), Antilles (`region_central_america`, 2 line ships and 2 frigates), and South Atlantic (`region_west_africa`, 3 frigates). This is a directly applicable native fleet format: `create_military_formation` + `type = fleet` + `hq_region` + repeated `ship = { type = ship_type:... count = ... }`. The base game's India setup also creates `Indian_Navy` at `sr:region_south_india` with 1 frigate and 6 troop ships (`common/history/military_formations/05_military_formations_india.txt:319-333`), confirming the same formation structure in the Indian theater.
- Other native fleet forms also use `create_ship` with `fleet = scope:...` (same file `:350-361`), though that sample is a Prussian singleton ship. No literal `home_port` field occurs in the installed game's `.txt` source; the fleet formation examples use `hq_region`. For Gujarat's strategic locality, `region_north_india` includes `STATE_GUJARAT` (GAME `common/strategic_regions/west_south_asia_strategic_regions.txt:43-48`), while Gujarat's port locator is the USM province `x31D0E0` (GAME `map_data/state_regions/10_india.txt:163-167`). These data support an India-local fleet HQ; they do not prove a per-province home-port selector.
- `building_naval_administration` is the naval building with sailor-recruitment PM at GAME `common/buildings/05_military.txt:109-129`. It is distinct from `building_port`, defined at `common/buildings/11_private_infrastructure.txt:3-35`; preserve both existing Gujarat facilities where their owner slice is transferred.
- No runtime effect example for `create_military_formation` with `type = fleet` was found in the installed `common/scripted_effects` files; the verified fleet syntax is in start-history `common/history/military_formations`. This is enough to support a starting local French fleet. If a later design needs to spawn it dynamically, confirm that separate runtime path against script docs or a minimal native test. Fleet size remains a root design choice.
- A direct history transfer means the USM/BER/NAW `create_state` slices in the Gujarat state source are assigned to FRA. Preserve the six other slices and the shared Gujarati/Sindi homelands at `00_states.txt:4298-4299`. Reconcile pop/building selectors, ownership records and target-country references as one closure. Do not rewrite the entire `STATE_GUJARAT` as FRA or substitute the full state: that would transfer the six explicitly unauthorized minors.

## Correction record

This record explicitly supersedes errors in the first version of this inventory:

1. The statement that no native fleet formation/ship syntax existed was materially wrong. The missed France history block at GAME `common/history/military_formations/00_military_formations_europe.txt:923-992` is now documented above. It defines four French fleets with ship entries and `hq_region`; the installed game does not use a literal `home_port` key in these definitions.
2. The Baroda shipyard's `building_financial_district` ownership is not a type mismatch. GAME `common/history/buildings/10_india.txt:283-286` uses the same shipyard/private-financial-district pattern. The report now records it as normal private ownership.
3. The USM cotton plantation has **2** levels, not 1 (MOD `common/history/buildings/10_india.txt:1001-1012`). The USM total remains 11 listed levels and the authorized total remains 19 because the earlier total counted those two levels; only the per-building entry was wrong.
4. Population arithmetic was independently recomputed using separate region-block ranges and all 60 `size` entries at MOD `common/history/pops/10_india.txt:395-703`: Gujarat 5,390,663; USM 2,643,330; BER 1,118,767; NAW 233,775; authorized total 3,995,872; six untransferred minors 1,394,791. Those figures match the first report.
