from journal_war_context import *
import re,datetime
data=json.loads(read(R/'writing-keys.json'));src=Path(data['source']);assert sha(src)==data['source_sha256']
# The emperor may now be a guest in a different loyalist country.
data['candidate']['nesnd_south_holdouts_surrender_tt']=['本国将被大吴吞并。若明帝仍在本国，先安排其逃亡。','Our country will be annexed by Wu. A Ming emperor still sheltered here will be sent to safety first.']
for i,lang in enumerate(['simp_chinese','english']):
    p=C/f'localization/{lang}/replace/zzzzzzzzzzzzzzzz_nesnd_journal_feedback_l_{lang}.yml'
    text='l_'+lang+':\n'+''.join(' '+k+':0 "'+v[i].replace('"','\\"')+'"\n' for k,v in data['candidate'].items());write(p,text)
dump(R/'writing-keys.json',data)
samples={}
for no,line in enumerate(read(src).splitlines(),1):
    for key in data['source_keys']:
        if re.match(r'\s*'+re.escape(key)+r':',line):samples[key]=(no,line.strip())
lines=['# 玩家文本逐项对读','',f'作者原文：{src}；SHA256 {sha(src)}。候选中文及英文分别核过主语、断句、重复、世界设定与效果对应；这不是游戏显示验收。','',
'作者在 usm_civilwar.9.d 先叙战争消耗、再说脆弱和平，允许长句与明确政治判断；.11.d 从战后处境导出抉择；两条选项直接表态。新文沿用这条因果线，不另造国家宪法/议会，不把停战称作政治争端已解决。外交使节可以用所属国家指代；本轮没有颁诏动作，不强塞君主称号。','',
'返工记录：归降提示原稿“若明帝尚在行在”遗漏寄居其它国家的情况，现改“若明帝仍在本国”。英文同步改为 still sheltered here。其余正文不把代码轮次、重试、变量或后台队列写给玩家。','',
'短标签/统计取原生JE界面职责：显示名称与当前数值；不模仿事件叙事语气。两条印度完成条件各对应一个实际成果，不能合并成一个叉。', '']
for key,(no,line) in samples.items():lines += [f'原样本 {key}，第{no}行：', '', '> '+line,'']
lines+=['|键|最终中文|最终英文|对读与脚本核对|判定|','|---|---|---|---|---|']
for key,pair in data['candidate'].items():
    if key.endswith('.d') or key.endswith('_reason'):
        note='对照.9.d/.11.d：处境→行动；叙事主体明确，段内独立后果用句号。未新增机构或未来必然结局。'
    elif key.endswith('_tt'):
        note='对照.11.1/.11.2的明确表态；补原生不能表达的完成标记/等待/吞并或保护国后果，与实际分支对应。'
    elif '_bar_desc' in key:
        note='原生GetCurrentBarValue调用，绝对计数与max=3/7一致；不再使用相对baseline。'
    elif 'status' in key or key.endswith(('_working','_paused')):
        note='只报当前状态；不重复门槛。印度working与available、paused与visible对应。'
    elif key.endswith(('.t','.a')) or key.startswith('nesnd_south_holdouts.'):
        note='对照.11的短促选择；标题指当前事件，选项是行动，没有开发术语与无对应奖励。'
    else:note='短名称/来源标签与条目职责对应，不加入第二遍机制说明。'
    lines.append('|'+key+'|'+pair[0].replace('|','\\|')+'|'+pair[1].replace('|','\\|')+'|'+note+'|通过|')
lines+=['','共核39组中英文键。未改动原作者长篇事件文案；既有日本、印度正文与建筑门槛保持。英文按英语语序写，未逐逗号照译。新文没有把臣属市场误写成采购库存，没有将两院、礼法或地方行政改写为其它制度。']
assert len(data['candidate'])==39
write(R/'writing-comparison.md','\n'.join(lines)+'\n')

sources={
'common/journal_entries/00_abolish_monarchy.txt':['je_abolish_monarchy'],
'common/scripted_effects/00_victoria_ep2_scripted_effects.txt':['transition_off_of_monarchy_effects'],
'common/scripted_effects/00_scripted_effects.txt':['exile_character_with_role_cleanup'],
'common/on_actions/00_code_on_actions.txt':['on_law_activated','on_law_enactment_started','on_battle_ended','on_enemy_capitulated_notification'],
'common/journal_entries/05_bulgaria_je.txt':['set_bar_progress'],
'common/script_values/ip4_je_values.txt':['scripted_bar_progress'],
'events/balkans_events/balkan_wars_events.txt':['ai_chance'],
'common/alert_types/00_alert_types.txt':['country_has_local_shortage'],
}
found=[]
for rel,keys in sources.items():
    p=G/rel;assert p.exists()
    text=read(p);hits={key:[i for i,line in enumerate(text.splitlines(),1) if key in line][:10] for key in keys}
    assert all(hits.values()),(rel,hits)
    found.append({'path':rel,'sha256':sha(p),'lines':hits})
dump(R/'native-sources.json',{'game_version':'1.13.11','steam_build':'24799966','sources':found,'detail_reports':['hus-monarchy-source.md','india-children-source.md','ming-war-source.md']})
write(R/'runtime-findings.md','''# 当前测试存档与源码诊断

归档的是本轮读取时最新的autosave.v3（1851.1.1），并保留1850.9.3手动存档与error.log副本。原件未改。runtime-capture.json记录逐文件SHA。官方rakaly v0.8.22仅在本地对副本执行melt --format vic3 --unknown-key error，解码成功；没有上传存档，也没有打开游戏。

- USM东洋JE加入1840.2.14，保存baseline_value=2、goal_value=5。分数为1时相对进度1−2=−1、目标增量3，解释截图。原计分函数本身仅加三项0/1，没有负贡献。
- MUG priority=1，学校JE在1836.5.1加入并处于active，工业JE不活跃。说明当前存档不是“从未有学校JE”；原available共用于invalid使切换重点会移走另一条，未默认钉选进一步掩盖了入口。不能从1851终态断言点击当刻UI是否显示。
- HUS原生废君JE加入日1836.1.1。原生总统制activate→transition_off_of_monarchy_effects会添加JE，未要求实际经历过君主制。新增HUS资格限制与旧JE无奖励清退，其他国家保留原版。旧档若曾短暂实行君主制、如今共和、又没有新标记，不能可靠恢复这段历史；当前截图档的开局JE可以确定清退。
- HNA拥有行在标记和明帝引用，停战JE加入1840.2.16；SIH/GNG已不在该局活跃主权国家集合。行在不是另一个MNG tag。旧停战入口把global settled设真，部分后续流程因此已封存。
- 最新error.log没有本批四模块的明确新定位报错，存在依赖/资源等其它日志；诊断主要依据存档值、截图和完整调用链，不能宣称全MOD没有报错。

原生战争领袖消灭可能终止当前war对象；未找到经证实的战争领袖替换effect。修复保存争端与参与国，幸存者和平后作抉择，愿战者由新一轮既有内战博弈接续。新博弈先加backer再加90 escalation，沿用已验证的倒计时路径。
''')

# Snapshot only the skill pages actually being edited; historical instructions remain linked.
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ');sb=W/'backups'/('skill-before-journal-war-'+stamp)
for rel in ['references/journal-text-contract.md','references/syntax-and-routing.md','references/active-work.md']:
    p=sb/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/rel,p)
dump(R/'skill-backup.json',{'path':str(sb),'files':man(sb)})
p=S/'references/journal-text-contract.md';s=read(p)
s+='''
## 绝对条件数与切换重点（1851测试档反例，2026-11-04）

现值条不是“从进入日志起再增加多少”。goal_add_value会保留进入时baseline；东洋JE存档baseline=2、goal=5，现值1显示−1/3。当前条件数/占领数改用有界scripted_progress_bar，immediate同步现值，周期明细算目标减当前条。旧活动JE必须迁移而不能只改定义留着旧baseline；迁移不得重置外交结果或重发奖励。

互斥建设重点若仅暂停推进，显示/存续条件与计分条件分开。取消重点不等于invalid；父日志结束/不再符合国家身份才清退。复核调用者根scope：country JE/tick与JE-root bar不是同一root，跨层shortage等国家参数显式传入，并核全部调用点。别用未经验证的prev.prev链掩盖根对象不明。

来源、39组文案对读、实际AST边界与局限：WORK/reports/journal-war-feedback-20261103/。静态检查不认证旧档JE重建的引擎显示时序。
''';write(p,s)
p=S/'references/syntax-and-routing.md';s=read(p)
s+='''
### 战后结算与寄居人物（2026-11-04）

一轮war结束不等于整个剧情争端结束。改停战/战败链时搜索所有settled写入者，包括旧JE complete、延迟事件immediate、僵局按钮；不能让新周度队列与旧终局互相改写。按实际参战轮次登记一次答复，延迟外国回复重验对象、轮次、期限和当前关系，实际建立附属关系后才提交结果。

先保存皇帝与原继承者，再转移皇帝；移动君主可能立刻触发继承。实际owner确认失败则走原生exile_character_with_role_cleanup；两者失败时阻止吞并且保留重试，不能先记录已答复把国家锁死。寄居别国的受保护人物也要避开旧随机处置链，不仅检查“行在”国名标记。不得据此自动改接收国君主、政体或玩家tag。

来源：GAME/common/scripted_effects/00_scripted_effects.txt的流亡清角色；WORK/reports/journal-war-feedback-20261103/ming-war-source.md及boundary-tests.json。故障注入检验脚本分支，不是引擎迁逃验收。
''';write(p,s)
p=S/'references/active-work.md';write(p,'''# 当前交接：四项日志与南明停战修复（2026-11-04）

任务30，报告WORK/reports/journal-war-feedback-20261103/，父提交c462651。候选exports/journal-war-feedback-20261103-a：东洋/统一日本绝对计数；德里建设双条可见、重点切换仅暂停；HUS真实废君资格；行在吞并前迁逃明帝、剩余本土拥明国逐轮抉择。具体主MOD/main/远端提交以main-merge.json及git-delivery.json为准。

最新读档证据是1851.1.1，区别于旧1866观察者终档。本轮只本地解码副本、做外部检查，没有开游戏，也不改存档。需要用户确认新旧JE迁移、实际战争领袖退场、人物流亡与保护国事件窗；不得声称ENGINE_PASS。下列France/Italy方案尚未实施且继续保留。

'''+read(p))

write(C/'.scratch/debug-release/issues/30-journal-war-feedback.md',f'''# 四项日志与南明停战修复

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS（引擎待用户测试）
Evidence: [{R.name}](<{R.as_posix()}/spec.md>)

## Result

东洋−1是相对基线错误；德里学校已在1851存档中活跃，修子条显示/暂停及市场国家引用；HUS开局废君源于原生政体初始化，定点限制入口与清退旧JE。南朝争端独立于单轮war，行在占领后先迁逃再吞并；本土参战国和平时每轮一次选择再战、求北朝保护、归吴。AI及例外详见spec与runtime-findings。两轴复审、定向回归、AST故障注入、MCP、Tiger差分与数据图保护结果见同目录final-validation.json。

未更改地图、人口、国家历史和已验证日本三分；未开游戏。候选独立备份及合入与远端结果分别见candidate-backup.json、main-merge.json、git-delivery.json。旧HUS短暂君主历史无法可靠倒推；旧war领袖不做未经证实的引擎替换。
''')
p=C/'.scratch/debug-release/map.md';write(p,read(p)+f'\n## 2026-11-04四项日志与停战反馈\n\n[任务30](issues/30-journal-war-feedback.md)：东洋绝对计数、德里双条显示、HUS废君入口、行在迁逃/吞并及逐轮停战处理。STATIC_PASS；未开游戏，交付指纹与剩余引擎场景见WORK/reports/journal-war-feedback-20261103/。\n')
print('Writing comparisons, source contracts, runtime findings, task and skill references recorded.')
