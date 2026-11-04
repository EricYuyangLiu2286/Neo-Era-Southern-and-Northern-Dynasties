from pathlib import Path
import hashlib

W = Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
C = W / 'exports/canon-route-execution-20261104-a'
R = W / 'reports/canon-route-execution-20261104'
B = W / 'backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace'
entries = []


def add(key, zh, en, category):
    entries.append((key, zh, en, category))


add('lawgroup_nesnd_hus_social_hierarchy', '东洲等级制度', 'Dongzhou Social Hierarchy', '名称')
add('lawgroup_nesnd_hus_social_hierarchy_desc', '以族籍划定共和国各族居民的社会地位。', 'A system that assigns social standing within the republic by cultural registration.', '制度说明')
add('nesnd_hus_social_hierarchy', '东洲等级制度', 'Dongzhou Social Hierarchy', '名称')
add('nesnd_hus_social_hierarchy_desc', '汉人、满蒙、美洲原住民与白人的族籍，决定了他们在共和国中获得的接纳与待遇。', 'Han, Manchu and Mongol, Indigenous American, and European registrations determine acceptance and treatment within the republic.', '制度说明')
add('law_nesnd_hus_four_tier_system', '四等户籍', 'Four-Tier Registration', '名称')
add('law_nesnd_hus_four_tier_system_desc', '汉人居于一等，满蒙居于二等，美洲原住民居于三等，白人居于四等。族籍限定各族居民的社会地位；财富与职业不能使人越过这一界限。', 'Han people occupy the first tier, Manchu and Mongol peoples the second, Indigenous Americans the third, and Europeans the fourth. Cultural registration limits social standing regardless of wealth or profession.', '制度说明')
add('law_nesnd_hus_manchu_registration', '满蒙编户', 'Manchu and Mongol Registration', '名称')
add('law_nesnd_hus_manchu_registration_desc', '满蒙居民取得与汉人相同的一等户籍，美洲原住民与白人仍分别列为三等、四等。共和国借此扩大享有最高待遇的公民之列。', 'Manchu and Mongol residents receive the same first-tier registration as Han residents. Indigenous Americans remain in the third tier and Europeans in the fourth, as the republic enlarges the body entitled to its highest standing.', '制度说明')
add('law_nesnd_hus_native_registration', '原住民编户', 'Indigenous Registration', '名称')
add('law_nesnd_hus_native_registration_desc', '美洲原住民取得与汉人相同的一等户籍，满蒙与白人仍分别列为二等、四等。共和国以共同的公民地位，重新安排殖居者与原住民的关系。', 'Indigenous Americans receive the same first-tier registration as Han residents. Manchu and Mongol residents remain in the second tier and Europeans in the fourth. Equal civic standing reshapes the relationship between settlers and Indigenous peoples.', '制度说明')
for old, new in [('hierarchy', 'four_tier_system'), ('registry_manchu', 'manchu_registration'), ('registry_native', 'native_registration')]:
    add('law_nesnd_hus_' + old, '$law_nesnd_hus_' + new + '$', '$law_nesnd_hus_' + new + '$', '兼容名称')
    add('law_nesnd_hus_' + old + '_desc', '$law_nesnd_hus_' + new + '_desc$', '$law_nesnd_hus_' + new + '_desc$', '兼容名称')

add('nesnd_hus_registration', '共和国的族籍', 'Registration in the Republic', '名称')
add('nesnd_hus_registration_reason', '$HUS$的公民之名，向来有不同的分量。汉人居于等级之首，满蒙、美洲原住民与白人依次列后；同在共和国生活，并不意味着得到相同的待遇。如今，扩大公民之列的争论已经进入政府。满蒙希望凭借与汉人的联系取得平等地位，原住民则要求共和国承认他们对这片土地与国家的权利。\n\n政府将选择一方编入一等户籍，经过一年的登记后施行新法。这一决定也将改变共和国与被留在旧等级中的人们的关系。', 'Citizenship has never carried equal weight in the $HUS$. Han residents stand first, followed by Manchu and Mongol peoples, Indigenous Americans, and Europeans. Living in the same republic does not bring the same treatment. The question of widening the civic body has now reached the government. Manchu and Mongol residents seek equality through their ties with the Han; Indigenous peoples demand recognition of their claims upon this land and its republic.\n\nThe government will grant first-tier registration to one of these groups after a year of registration. Its decision will also reshape relations with those left under the old distinctions.', '日志正文')
add('nesnd_hus_registration_goal', '决定扩大一等户籍的范围，并完成一年的登记。', 'Choose whom to admit to the first tier and complete a year of registration.', '条件状态')
add('nesnd_hus_registration_lock_tt', '东洲等级制度存续期间，不能更改$lawgroup_citizenship$法律', '$lawgroup_citizenship$ laws cannot be changed while the Dongzhou social hierarchy remains in force', '条件状态')
add('nesnd_hus_registration_uncommitted_tt', '尚未决定编户对象', 'No registration has been chosen', '条件状态')
add('nesnd_hus_registration_enacted', '编户已完成，相应法律已施行', 'Registration is complete and its law is in force', '条件状态')
add('nesnd_hus_registration_choose', '政府尚未决定将哪一方编入一等户籍。', 'The government has yet to decide whom to admit to the first tier.', '条件状态')
add('nesnd_hus_registration_pending_manchu', '满蒙编户正在进行。', 'Manchu and Mongol registration is underway.', '条件状态')
add('nesnd_hus_registration_pending_native', '原住民编户正在进行。', 'Indigenous registration is underway.', '条件状态')
add('nesnd_hus_registration_pending', '编户正在进行。', 'Registration is underway.', '兼容名称')
add('nesnd_hus_registration_completed', '编户完成，新法已经施行。', 'Registration is complete and the new law is in force.', '条件状态')
add('nesnd_hus_registration_conflict', '既有编户决议相互抵牾，现行等级安排暂且维持。', 'Conflicting registration decisions have left the existing hierarchy in place.', '条件状态')
add('nesnd_hus_register_manchu', '将满蒙编入一等户籍', 'Admit Manchu and Mongol Residents', '按钮')
add('nesnd_hus_register_manchu_desc', '满蒙居民与汉人之间的联系，为扩大共和国的公民之列提供了一条道路。政府将承认他们与汉人相同的社会地位。', 'Ties between Manchu, Mongol, and Han residents offer one path to a broader civic body. The government will recognize their equal social standing.', '按钮')
add('nesnd_hus_register_manchu_tt', '经过#bold 12个月#!施行$law_nesnd_hus_manchu_registration$。美洲原住民仍列三等，白人仍列四等。选择后不能改换编户对象。', '$law_nesnd_hus_manchu_registration$ takes effect after #bold 12 months#!. Indigenous Americans remain in the third tier and Europeans in the fourth. This choice cannot be changed.', '操作效果')
add('nesnd_hus_register_native', '将原住民编入一等户籍', 'Admit Indigenous Residents', '按钮')
add('nesnd_hus_register_native_desc', '原住民同样生活于共和国的土地之上，政府将承认他们与汉人相同的社会地位。这一决定也会使仍居二等的满蒙居民寻求别处的生活。', 'Indigenous peoples share the republic’s land. The government will recognize their equal standing with Han residents, prompting Manchu and Mongol residents left in the second tier to seek a life elsewhere.', '按钮')
add('nesnd_hus_register_native_tt', '经过#bold 12个月#!施行$law_nesnd_hus_native_registration$。满蒙仍列二等，白人仍列四等；此后满蒙居民将迁往$CNE$或美国西部。选择后不能改换编户对象。', '$law_nesnd_hus_native_registration$ takes effect after #bold 12 months#!. Manchu and Mongol residents remain in the second tier and Europeans in the fourth; Manchu and Mongol communities will subsequently leave for $CNE$ or the American West. This choice cannot be changed.', '操作效果')
add('nesnd_hus_registration.1.t', '草原上的新汗国', 'A New Khanate on the Plains', '事件')
add('nesnd_hus_registration.1.d', '美国内战打乱了西部的秩序，一个由美洲原住民建立的汗国已经出现。来自共和国与美国的原住民正在迁往那里，新的国境与他们对土地的要求，也将把两个共和国卷入冲突。', 'The American civil war has unsettled the West, where Indigenous Americans have established a new khanate. Indigenous communities from both republics are moving there. Its new borders and claims to the land threaten to draw both republics into conflict.', '事件')
add('nesnd_hus_registration.1.a', '东洲又添一处纷争。', 'Another conflict takes shape in Dongzhou.', '选项')
add('nesnd_hus_registration.2.t', '离开共和国', 'Leaving the Republic', '事件')
add('nesnd_hus_registration.2.d', '原住民编户完成之后，满蒙居民仍被留在二等户籍之中。如今，他们已经离开共和国：有人投向$CNE$，也有人前往美国西部，在新的土地上寻找生活。', 'After Indigenous registration was completed, Manchu and Mongol residents remained in the second tier. They have now left the republic: some for $CNE$, others for the American West, seeking a life on new ground.', '事件')
add('nesnd_hus_registration.2.a', '他们已作出自己的选择。', 'They have made their choice.', '选项')

for culture, zh_c, en_c in [('han', '汉人', 'Han'), ('manchu', '满蒙', 'Manchu and Mongol'), ('native', '原住民', 'Indigenous'), ('white', '白人', 'European')]:
    for strata, zh_s, en_s in [('upper', '上层', 'Upper Strata'), ('middle', '中层', 'Middle Strata'), ('lower', '下层', 'Lower Strata')]:
        key = f'nesnd_hus_{culture}_{strata}'
        add(key, zh_c + zh_s, en_c + ' ' + en_s, '阶层名称')
        add(key + '_desc', f'属于{zh_s}职业的{zh_c}居民。', f'{en_c} residents in {en_s.lower()} professions.', '制度说明')
        for bound, zh_b, en_b in [('min', '最低', 'Minimum'), ('max', '最高', 'Maximum')]:
            mod = f'country_{key}_acceptance_{bound}_add'
            add(mod, f'${key}$[concept_social_class]的{zh_b}[concept_acceptance]', f'{en_b} [concept_acceptance] for the ${key}$ [concept_social_class]', '原生修正')
            zh_end = '低于' if bound == 'min' else '高于'
            en_end = 'fall below' if bound == 'min' else 'rise above'
            add(mod + '_desc', f'${key}$[concept_social_class][Concept(\'concept_pop\', \'$concept_pops$\')]的[concept_acceptance]不会{zh_end}该数值', f'The [concept_acceptance] of [Concept(\'concept_pop\', \'$concept_pops$\')] in the ${key}$ [concept_social_class] cannot {en_end} this value.', '原生修正')

for locale, index in [('simp_chinese', 1), ('english', 2)]:
    dest = C / f'localization/{locale}/replace/zzzz_nesnd_hus_social_hierarchy_l_{locale}.yml'
    dest.parent.mkdir(parents=True, exist_ok=True)
    lines = ['l_' + locale + ':']
    for row in entries:
        # Localization entries stay on one physical line; paragraphs use literal \n.
        value = row[index].replace('\r\n', '\n').replace('\n', '\\n')
        value = value.replace(chr(34), chr(92) + chr(34))
        lines.append(f' {row[0]}:0 "{value}"')
    dest.write_text('\n'.join(lines) + '\n', encoding='utf-8-sig', newline='')

sources = [B/'ce_cne_events_l_simp_chinese.yml', B/'ce_french_empire_journals_l_simp_chinese.yml']
sample = {
    '名称': ('ce_cne_land_reform', '地权革命'),
    '制度说明': ('ce_cne_land_reform_reason', '以打破宗族对农村人口的束缚和垄断，说明改革改变谁的地位'),
    '日志正文': ('ce_cne_land_draft_failing_reason', '掌握权力的中华帝国统治集团是以牧氏家族为核心的武勋贵族集团，以及围绕着他们成长起来的一批新派士绅。'),
    '按钮': ('ce_french_support_dynasty_button_desc', '波拿巴的道路是[ROOT.GetCountry.GetAdjective]民族团结和繁荣的唯一办法。'),
    '操作效果': ('ce_orl_law_request_trade', "没有[GetLawType('law_free_trade').GetName]"),
    '条件状态': ('ce_cne_reform_limited_market_access_explain', '国内没有任何省份的[concept_market_access]小于#bold 80%#!'),
    '事件': ('flavorCNE.1.d', '由统治集团的利益、改革及其阻力叙述政治变化；本轮不借用其帝国/君主主体'),
    '选项': ('flavorCNE.1.1', '民众之利益构建帝国，无能维护者虽强亦亡。'),
    '阶层名称': ('GAME social-class localization', '按文化与原生职业strata直称，不把经济上层等同法律一等'),
    '原生修正': ('GAME modifiers_l_*.yml:country_brahmins_acceptance_min_add', '沿用原生社会阶层/接纳下限模板，不增写故事或重复数字'),
    '兼容名称': ('本轮已定名', '以本轮有效法律名引用，旧存档界面不显示开发迁移说明'),
}
report = '''# Batch A 玩家文本对读

状态：编辑完成，未运行游戏或行为测试。作者基线为pre-update-20261030T233944Z独立备份；当前候选原先没有nesnd_hus_*玩家文本，不能冒称本轮旧稿为作者原文。原版修正模板只用于类型/数值显示，不充当作者叙事样本。

采用的句法：作者先点明统治者、居民或社会阶层，再说明制度改变的利益关系；政治按钮明确支持对象，状态说明则直接给当前事实。本轮据此保留共和国主体、族籍与群体待遇，未改写为文书流程。法定四等级与经济upper/middle/lower分别命名，所有数字均来自法律上下限或实际12月选择。

返工记录：最初“同一身份分类提供层级上下限”是实现语言，改为“四等户籍”及具体族群次序；最初“迁移冲突待修复”泄漏开发过程，改为“既有编户决议相互抵牾”；原住民按钮补出满蒙外迁这一真实代价。全局epoch、回调及存档托管只写技术报告，未进入玩家文案。

| 作者/原生样本 | SHA-256 |
|---|---|
'''
for src in sources:
    report += f'| [{src.name}](<{src.as_posix()}>) | `{hashlib.sha256(src.read_bytes()).hexdigest()}` |\n'
report += '\n下表逐条记录落库候选及编辑结论；技术行为仍交后续冻结测试。\n\n| key | 类别/对照 | 中文候选 | English | 结论 |\n|---|---|---|---|---|\n'
for key, zh, en, category in entries:
    skey, observation = sample[category]
    zh_cell = zh.replace('|', '\\|').replace('\n', '<br>')
    en_cell = en.replace('|', '\\|').replace('\n', '<br>')
    report += f'| `{key}` | {category}；`{skey}`：{observation} | {zh_cell} | {en_cell} | 编辑通过：主体、等级/职业、条件与代价对应；无开发说明。 |\n'
(R/'batch-a-writing-comparison.md').write_text(report, encoding='utf-8', newline='')
print('Authored dedicated Chinese/English HUS text and per-key editorial comparison.')
