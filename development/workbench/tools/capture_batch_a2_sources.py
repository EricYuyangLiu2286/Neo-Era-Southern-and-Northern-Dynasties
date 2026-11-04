"""Read-only source capture for A2 planning; no gameplay edits or validation."""
from pathlib import Path
import hashlib
import json

W = Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
C = W / 'exports/canon-route-execution-20261104-a'
R = W / 'reports/canon-route-execution-20261104'
G = Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
E = W / 'references/engine-docs-1.13.11-20261031'
sources = []

def add(sid, path, line, purpose):
    p = Path(path)
    data = p.read_bytes()
    sources.append(dict(id=sid, path=p.as_posix(), line=line,
                        sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), purpose=purpose))

add('P01', 'D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世/北明ppet.pptx', None,
    '作者原件；slide18 ¶8/18/21–23，slide19 ¶12/17–19/24/28。PPT只读。')
add('P02', R/'americas-acceptance-native.md', 1, '旧原住民复国/人口研究；其中HUS公民法变体建议已被A1取代。')
add('P03', R/'hus-khanate-native-contract.md', 1, '70:30、50%、四州、两战、TIS/Cherokee原生接口；其无限等待建议被当前授权要求取代。')
add('P04', R/'batch-a2-current-population-source-census.json', 1, '本次只读当前历史人口/文化源加总，非运行时或测试结果。')
add('P05', R/'remaining-batch-contracts.md', 5, 'root分派的A2完整范围。')

add('G01', G/'common/country_definitions/00_countries.txt', 2786, 'NAH:2786；TWT:3109；原色/主流/首都/tier。')
add('G02', G/'common/cultures/00_cultures.txt', 11155, 'zapotec11155/nahua11346/tarascan11444/quechua11537/aimara11734/siouan12784/mixtec13230。')
add('G03', G/'common/ideologies/01_character_ideologies.txt', 1692, 'reformer1692/jingoist_leader2810/royalist3081均character_ideology=yes。')
add('G04', G/'common/scripted_buttons/turtle_island_buttons.txt', 1, '真实country按钮visible/possible/effect与旧窗口副作用入口。')
add('G05', G/'common/journal_entries/04_sepoy_mutiny.txt', 1, '原生JE→压力/事件→建国与战争caller链。')
add('G06', G/'common/script_values/script_values.md', 119, 'script values支持所有list、加和与正常scope切换。')
add('G07a', E/'effects.log', 878, 'create_country878/create_DP909/move_partial9830/move_pop9844/while37383；country/DP/character/pop/state scope合同。')
add('G07b', E/'triggers.log', 2023, 'any_neighbouring_state2023；culture_percent_state9558；state_population14458；total_size14659。')
add('G07c', E/'event_targets.log', 1, '原生作用域链目标。')
add('G08', G/'common/character_templates/historical_leaders_americas.txt', 20, 'Juarez模板文化/出生/角色/思想。')
add('G09a', G/'common/character_templates/country_peu.txt', 43, 'Huachaca是Quechua ruler/general；Orbegoso/Pierola/Gamarra非任意native替身。')
add('G09b', G/'common/history/characters/peu - peru.txt', 1, 'NPU/SPU/IQU实际初始人物归属与Gamarra流亡。')
add('G10a', G/'common/character_templates/country_mex.txt', 62, 'Alvarez culture=primary，不能按姓名推定native。')
add('G10b', G/'common/history/characters/mex - mexico.txt', 1, 'MEX实际已有角色；Juarez不是无条件初始角色。')
add('G11', G/'common/scripted_effects/00_scripted_effects.txt', 720, 'exile_character_with_role_cleanup：exile、unassign、replace roles。')
add('G12a', G/'common/character_interactions/00_character_interactions.txt', 997, 'invite_exile完整possible/effect；acceptance_status_3、slot、can_agitate、religion、closed_borders。')
add('G12b', G/'events/agitators_events/exiles_events.txt', 231, '实际transfer_character + free_from_exile_effect调用。')
add('G13', G/'common/war_goal_types/war_goal_types.md', 47, 'on_enforced ROOT holder、target/play scopes；custom无预置效果；冲突验证由脚本配置。')
add('G14', G/'common/war_goal_types/29_restore_union.txt', 152, '原生kind=custom实际on_enforced改法与建宗属。')
add('G15a', G/'common/war_goal_types/00_annex_country.txt', 1, 'annexes_entire_country、conflict设置、control_half_target_country_states、target_typecountry。')
add('G15b', G/'common/war_goal_types/08_humiliation.txt', 1, 'kindhumiliation原生效果、contestion与on_enforced扩展。')
add('G16a', G/'common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt', 461, '原生create_DP以及以type/target/initiator重新定位真实DP后加goal。')
add('G16b', G/'common/diplomatic_plays/diplomatic_plays.md', 1, 'DP字段、mirror、allow_negotiated_peace、on_demand/war回调。')
add('G17', G/'common/on_actions/00_code_on_actions.txt', 6991, 'on_war_end ROOT DP、actorinitiator/targettarget；character_creation2566/death2604；Cherokee池479。')
add('G18', G/'events/red_scare_events.txt', 1276, '实际move_partial_pop国家→州→pop调用和population_ratio。')
add('G19', G/'common/strategic_regions/north_america_strategic_regions.txt', 15, '原版大平原15州；central_america含加勒比。有效候选覆盖另见C07b。')
add('G20', G/'common/combat_unit_types/00_land_combat_unit_types.txt', 83, 'line_infantry与cannon_artillery真实unitkeys、1000 manpower与technology。')
add('G21', G/'common/technology/technologies/20_military.txt', 84, 'artillery84/napoleonic118/line_infantry177的era1与前置。')
add('G22a', G/'common/geographic_regions/02_geographic_regions_america.txt', 23, 'Americas包含North/Central/South；Peru六州。')
add('G22b', G/'common/strategic_regions/europe_strategic_regions.txt', 80, 'Greenland在Scandinavia，计划显式补入Americas；Iceland不补。')
add('G23', G/'common/scripted_effects/00_political_setup.txt', 3, 'effect_starting_politics_liberal，HUS间接no_workers_rights/anti_strike_laws。')
for suffix, fn in [('a','00_navy_model'),('b','00_internal_security'),('c','01_policing'),('d','01_health_system'),('e','02_childrens_rights'),('f','02_welfare')]:
    add('G24'+suffix, G/f'common/laws/{fn}.txt', 1, '六个未由HUS历史显式设置的普通法组基础法；本批明确补全政策。')
add('G25', G/'common/journal_entries/00_turtle_island.txt', 1, 'JE三按钮、原生形成/吞并链。')
add('G26', G/'common/government_types/01_monarchies.txt', 2350, 'gov_khanate真实TAG白名单、hereditary/摄政/宗属门槛与原生回调。')

for i, sub in enumerate(['journal_entries','scripted_triggers','script_values','scripted_progress_bars','scripted_buttons','scripted_effects','on_actions','diplomatic_plays','static_modifiers'],1):
    add(f'C01.{i}', C/f'common/{sub}/nesnd_american_restoration.txt', 1, '当前未验证复国草稿；本计划重写范围。')
add('C01.10', C/'events/nesnd_american_restoration.txt', 1, '当前复国事件骨架。')
add('C02a', C/'common/scripted_effects/nesnd_hus_registration.txt', 355, 'A1冻结exodus/maintenance；仅迁徙body可局部改。')
add('C02b', C/'common/scripted_triggers/nesnd_hus_registration.txt', 68, 'A1 native/MM分类及USA西部82–85；不编辑classifier。')
add('C02c', C/'common/history/countries/HUS.txt', 84, 'HUS开局明确法律＋liberal effect；本批只读。')
add('C02d', R/'batch-a-owned-files-sha256.json', 1, 'A1原24文件指纹，A2局部改动必须独立diff与回归。')
for i, sub in enumerate(['country_definitions','scripted_effects','scripted_triggers','on_actions','diplomatic_plays','journal_entries','decisions'],1):
    add(f'C03.{i}', C/f'common/{sub}/nesnd_native_khanate.txt', 1, '当前NKH草稿；其中A1法律辅助接口已冻结。')
add('C04', C/'common/journal_entries/zzzz_nesnd_turtle_island.txt', 1, '当前仅JE禁用；未覆盖3按钮effect。')
add('C05a', C/'events/native_resettlement.txt', 1, '当前Cherokee七事件cancelled/inert旧窗口闭包。')
add('C05b', C/'common/journal_entries/nesnd_hus_registration.txt', 25, 'je_indian_removal inert REPLACE；A1其它内容不动。')
add('C06', C/'common/religions/CE_religion.txt', 8, '实际old_confucianism与kaimeng_confucianism定义。')
add('C07a', C/'common/geographic_regions/02_geographic_regions_america.txt', 23, '有效Americas geographic region覆盖。')
add('C07b', C/'common/strategic_regions/north_america_strategic_regions.txt', 9, '有效Pacific含南北大原、大平原仍15region。')
add('C07c', C/'map_data/state_regions/05_north_america.txt', 1660, '作者南北大原state_region，北美完整范围不可漏。')
add('C08a', C/'common/history/pops/05_north_america.txt', 1, '已重配北美人口；只读冻结，不重跑人口工具。')
add('C08b', C/'common/history/pops/07_south_america.txt', 1, '已重配南美人口；只读冻结。')
add('C09', C/'common/country_definitions/ce_countries.txt', 63, '本候选国家定义数据库已有REPLACE实际用法。')

payload = {'kind':'read-only source manifest for A2 plan; not validation or whole-C freeze',
           'game_version':'1.13.11 / Steam build 24799966', 'sources':sources}
(R/'batch-a2-source-manifest.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
plan=R/'batch-a2-native-americas-plan.md'
body=plan.read_text(encoding='utf-8').split('\n<!-- SOURCE_CAPTURE_START -->')[0]
lines=['','<!-- SOURCE_CAPTURE_START -->','',
       '编号字母/数字后缀属于同一来源组；正文 `[G07]` 例如指 G07a–c。路径均为实际读到的文件。','',
       '|ID|来源（定位）|SHA-256|证据用途|','|---|---|---|---|']
for x in sources:
    p=x['path']; loc=p+(f":{x['line']}" if x['line'] else '')
    label=Path(p).name+(f":{x['line']}" if x['line'] else '（slides18/19）')
    lines.append(f"|{x['id']}|[{label}](<{loc}>)|`{x['sha256']}`|{x['purpose']}|")
plan.write_text(body+'\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'sources':len(sources),'report':str(plan),'manifest':str(R/'batch-a2-source-manifest.json')},ensure_ascii=False))
