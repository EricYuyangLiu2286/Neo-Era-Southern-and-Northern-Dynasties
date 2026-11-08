# 主 MOD 修改的原版文件

对照 Victoria 3 1.15.0，Steam build 26453692。文件夹从 MOD 根目录或原版 `game/` 起算，拼上文件名即可定位双方文件。

本表用于复查整文件覆盖。新增、撤回同路径覆盖，或完成版本迁移时，按主 MOD 实际加载目录与本机原版重新比对，并同步技能副本。独立文件中的 `REPLACE:` 按覆盖的定义另行比对；例如秀全的通用选人条件对应 `common/scripted_triggers/00_ep2_victoria_scripted_triggers.txt` 中的 `character_is_valid_for_events`。

## 内容有改动（185 个）

| 文件夹 | 文件名 |
| --- | --- |
| `common/achievements` | `base_achievements.txt` |
| `common/ai_strategies` | `00_default_strategy.txt` |
| `common/buildings` | `11_private_infrastructure.txt` |
| `common/character_interactions` | `00_character_interactions.txt`、`01_additional_interactions.txt` |
| `common/country_creation` | `00_releasable_countries.txt` |
| `common/country_formation` | `00_formable_countries.txt` |
| `common/customizable_localization` | `01_decisions.txt`、`99_ru_custom_loc_V3.txt` |
| `common/decisions` | `manifest_destiny.txt` |
| `common/diplomatic_actions` | `43_subjects_handle_states.txt` |
| `common/dynamic_country_names` | `00_dynamic_country_names.txt` |
| `common/flag_definitions` | `00_flag_definitions.txt` |
| `common/geographic_regions` | `01_geographic_regions_europe.txt`、`02_geographic_regions_america.txt`、`04_geographic_regions_asia.txt`、`05_geographic_regions_content.txt`、`05_geographic_regions_seismic.txt` |
| `common/geographic_regions` | `06_old_strategic_regions.txt` |
| `common/history/buildings` | `00_west_europe.txt`、`01_south_europe.txt`、`02_east_europe.txt`、`04_subsaharan_africa.txt`、`05_north_america.txt` |
| `common/history/buildings` | `08_middle_east.txt`、`09_central_asia.txt`、`10_india.txt`、`11_east_asia.txt`、`12_indonesia.txt` |
| `common/history/buildings` | `13_australasia.txt`、`14_siberia.txt`、`15_russia.txt` |
| `common/history/characters` | `dei - dutch east indies.txt`、`fra - france.txt`、`jap - japan.txt`、`mug - hindustan.txt`、`per - persia.txt` |
| `common/history/characters` | `phi - philippines.txt`、`rus - russia.txt` |
| `common/history/countries` | `aus - austria.txt`、`dei - dutch east indies company.txt`、`ezo - ezochi.txt`、`fra - france.txt`、`frm - frankfurt am main.txt` |
| `common/history/countries` | `gbr - great britain.txt`、`jap - japan.txt`、`kra - krakow.txt`、`lkt - lakota.txt`、`mug - mughals.txt` |
| `common/history/countries` | `net - netherlands.txt`、`per - persia.txt`、`phi - philippines.txt`、`pru - prussia.txt`、`rus - russia.txt` |
| `common/history/countries` | `spa - spain.txt`、`spc - carlist spain.txt`、`swe - sweden.txt`、`tas - tasmania.txt`、`tib - tibet.txt` |
| `common/history/diplomacy` | `00_relations.txt`、`00_rivalries.txt`、`00_subject_relationships.txt`、`00_truces.txt` |
| `common/history/diplomatic_plays` | `00_carlist_war.txt` |
| `common/history/lobbies` | `00_lobbies.txt` |
| `common/history/military_formations` | `00_military_formations_europe.txt`、`04_military_formations_middle_east.txt` |
| `common/history/pops` | `00_west_europe.txt`、`01_south_europe.txt`、`02_east_europe.txt`、`04_subsaharan_africa.txt`、`05_north_america.txt` |
| `common/history/pops` | `06_central_america.txt`、`07_south_america.txt`、`08_middle_east.txt`、`09_central_asia.txt`、`10_india.txt` |
| `common/history/pops` | `11_east_asia.txt`、`12_indonesia.txt`、`13_australasia.txt`、`14_siberia.txt`、`15_russia.txt` |
| `common/history/population` | `jap - japan.txt`、`phi - philippines.txt`、`tib - tibet.txt` |
| `common/history/power_blocs` | `00_power_blocs.txt` |
| `common/history/production_methods` | `00_urban_center.txt` |
| `common/history/states` | `00_states.txt` |
| `common/history/trade` | `00_historical_trade.txt` |
| `common/history/treaties` | `00_historical_treaties.txt` |
| `common/ideologies` | `00_ig_ideologies.txt`、`00_ig_ideologies_event.txt`、`00_ig_ideologies_flavored.txt`、`01_character_ideologies.txt`、`03_ig_ideologies_movement.txt` |
| `common/journal_entries` | `00_alaska.txt`、`00_belle_epoque.txt`、`00_east_indies.txt`、`00_hawaii.txt`、`00_indian_removal.txt` |
| `common/journal_entries` | `00_major_railroads.txt`、`00_manifest_destiny.txt`、`00_meiji_restoration.txt`、`00_seminole_wars.txt`、`00_veiled_protectorate.txt` |
| `common/naval_battle_conditions` | `00_naval_battle_conditions.txt` |
| `common/objectives` | `00_objective_tutorial.txt`、`01_player_objectives.txt` |
| `common/on_actions` | `00_code_on_actions.txt` |
| `common/power_bloc_names` | `00_power_bloc_names.txt` |
| `common/scripted_buttons` | `00_christ_of_europe_buttons.txt`、`07_meiji_buttons.txt` |
| `common/scripted_effects` | `00_dynamic_state_names_europe.txt`、`00_victoria_ep2_scripted_effects.txt` |
| `common/scripted_triggers` | `00_ai_triggers.txt`、`00_geography_triggers.txt`、`00_scripted_triggers.txt` |
| `common/strategic_regions` | `east_asia_strategic_regions.txt`、`europe_strategic_regions.txt`、`north_america_strategic_regions.txt`、`west_south_asia_strategic_regions.txt` |
| `events` | `1848.txt`、`alaska_events.txt`、`character_events.txt`、`colonial_administration_events.txt`、`commander_events.txt` |
| `events` | `crime_events.txt`、`dei_breakup.txt`、`fascism_events.txt`、`ig_leaders.txt`、`ig_suppression_events.txt` |
| `events` | `italian_unification.txt`、`manifest_destiny_events.txt`、`meiji_restoration.txt`、`movement_events.txt`、`native_resettlement.txt` |
| `events` | `nihilism.txt`、`poland_events.txt`、`prostitution_events.txt`、`psychology_events.txt`、`resignation.txt` |
| `events` | `russo_chinese_events.txt`、`secession_situations.txt`、`veiled_protectorate_events.txt`、`warlord_china_events.txt`、`zanzibar_events.txt` |
| `events/agitators_events` | `agitator_law_events_2.txt`、`agitators_election_events.txt`、`agitators_law_events.txt`、`coup_events.txt`、`exiles_events.txt` |
| `events/agitators_events` | `exiles_events_02.txt`、`garibaldi_events.txt`、`revolution_events_01.txt`、`revolution_events_02.txt`、`yeet_agitator_events.txt` |
| `events/iberia_events` | `ip4_anarchism_events.txt` |
| `events/japan_events` | `ep2_meiji_restoration.txt` |
| `events/law_events` | `anarchy_law.txt`、`distribution_of_power_laws.txt`、`internal_security_events.txt`、`technocracy_law.txt` |
| `events/russia_events` | `ip5_communism_events.txt` |
| `events/soi_events` | `00_ep1_caucasus_events.txt`、`00_ep1_kazakh_events.txt`、`00_lobbies_events_03.txt`、`00_lobbies_events_04.txt` |
| `events/tech_events` | `war_crimes_events.txt` |
| `gfx/map/map_object_data` | `generated_map_object_locators_city.txt`、`generated_map_object_locators_farm.txt`、`generated_map_object_locators_mine.txt`、`generated_map_object_locators_port.txt`、`generated_map_object_locators_wood.txt` |
| `gfx/map/spline_network` | `spline_network.splnet` |
| `gfx/map/spline_network/military_route_graphics` | `02_railroad_vehicles.txt` |
| `gui` | `culture_panel.gui` |
| `map_data/state_regions` | `00_west_europe.txt`、`05_north_america.txt`、`08_middle_east.txt`、`09_central_asia.txt`、`11_east_asia.txt` |
| `map_data/state_regions` | `12_indonesia.txt`、`13_australasia.txt`、`14_siberia.txt`、`15_russia.txt` |

## 仅编码标记或换行有差异（2 个）

| 文件夹 | 文件名 |
| --- | --- |
| `common/journal_entries` | `journal_entries.md` |
| `common/scripted_progress_bars` | `scripted_progress_bars.md` |

## 与原版逐字节相同的同路径副本（3 个）

| 文件夹 | 文件名 |
| --- | --- |
| `common/discrimination_traits` | `discrimination_traits.md` |
| `common/history/characters` | `net - netherlands.txt` |
| `common/scripted_buttons` | `scripted_buttons.md` |
