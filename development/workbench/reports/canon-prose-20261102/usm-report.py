from pathlib import Path
import json,re,collections,hashlib
R=Path(__file__).parent
M=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties')
G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
B=M.parent.parent/'nesnd-workbench/backups/pre-update-20261030T233944Z/mod'
I=json.loads((R/'usm-inventory.json').read_text(encoding='utf-8'))
P=json.loads((R/'usm-proposals.json').read_text(encoding='utf-8'))
def link(root,f,line=None):
    return f'[{f}{":"+str(line) if line else ""}](<{(root/f).as_posix()}{":"+str(line) if line else ""}>)'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report='''# 南朝／吴明／湖广文案审查与双语修订提案

状态：EDITORIAL_PROPOSAL；未改主 MOD、未改候选、未改技能、未开游戏。源码核对不能称为引擎验收。版本为 1.13.11 / Steam build 24799966；本轮 `catalog.py status` 返回 CURRENT、changed_count=0。

本审查按当前主 MOD 的本地化覆盖顺序整理 683 个相关键，其中包含成熟作者原文、AI后覆盖、隐式日志字段和旧兼容键。有效层按普通本地化后 replace、文件名顺序归并；每层原文和SHA均留在 usm-inventory.json，未将此静态归并冒充引擎观测。作者本轮附件与主MOD英文文件中的中文修订均作为作者证据；不能把错放在英文槽中的中文当作已经完成的英译。

修订 JSON 为 `usm-proposals.json`，300键，逐键含 zh/en/reason/source/mechanic/current_zh/current_en/status。主键文本应写回实际覆盖它的各层，或移除冲突的旧覆盖；不要只修改 ce_usm 基础文件。本审查没有把所有“盟约”替换成“礼法”：中央国制是礼法，反吴军阀可结盟，外交通商和援助仍使用条约。

## 关键结论与作者原稿的机制差异

1. **作者修改的 federal_compact_button 不是现行按钮显示源。**旧同名按钮已指向 south_offer 名称与描述，且没有当前JE调用；真正被“南朝诸国”调用的是 `nesnd_south_offer_accord`。该动作发送改制提议，不能写成点击即召开大会、立即通过宪法或改变领土。
2. **事件10无当前调用者。**`nesnd_crisis.10`保留了旧清理与招抚效果，但当前和平结局走明20→22、吴21→23。因此将作者关于“礼法通过”的历史论说接入真实结局，保留旧10稿作为兼容文本，不复活其奖励。两路线已分别写；不共享一个拥明胜利段落。
3. **湖广旧三按钮已退役。**`nesnd_huguang_preparations` possible=no、shown=no、invalid=yes，清理旧存档。书院、粮运、老兵按钮当前无JE调用。作者稿精修为可追溯的闲置提案，不能宣称三项教育、政治动员或荆蜀协定已经上线。现行湖广内容为“脆弱的贸易”，只核大学、军营等建筑就业与供应、民生和联络条件。报告与JSON分别覆盖了现行条目。
4. **警卫旧事件11已隐藏。**作者拟定的大理寺公开调查／锦衣卫秘密调查没有现行选择效果。真实首辅按钮被 chen_security 最终层覆盖，走六个月护卫、留署、内应清查及死亡／负伤／脱险概率。已将作者保护改革领袖的动机移至这个真实面板；旧11稿保留，不宣称旧两选项可玩。
5. **明和平不吞并诸省，不调整其经济法律。**它保留实际朱氏君主和各成员政府，中央获得120个月 authority−15%、government_wages+10%的礼法约束。作者“统一完成、万世难改”的表述改为共同认可权责；不得据此虚构统一省法或新增立法机制。
6. **吴和平有实际整合与日本割地。**在全部既有门槛连续满足12个月后，设置吴统治者／旗标，将明确同意且安全控制的中国范围辖地并入；日本只转让自己持有的四国、九州。海外保留条件按现有代码，不写成全体海外已经同意或全部吞并。二元君主立宪是作者本轮设定在叙事中的表达；现有effect没有另行 enact_law，不能声称某一法律组因此自动改变。
7. **首辅去位旧AI后覆盖与实际触发冲突。**flavorUSM.6要求陈东阳已无在世人物，是死亡后续。改为“首辅身后”，不强断言遇刺，兼容自然死亡。其d1在当前≤1862事件触发与>1870描述条件下不由正常调用可达，保留成熟原稿，不扩大机制修复。
8. **crisis20可能发生在土改结束后。**作者稿无条件“地权改革仍在继续”改为“若尚未完成”。A旁观，B湖南援助36个月、仅改革活跃时失序+8，C干预60个月、仅改革活跃时+15并加入可用反吴对峙。保留北朝“伪朝禅代”的阵营立场；选项C为“联络襄樊大营，准备南下”。
9. **外国主体不固定为皇帝。**法国事件没有君主制守卫，改“政府”，不为显示标题额外引用可能不存在的君主。真正新礼法颁诏的明20、22和吴23有君主来源，使用动态title＋name。
10. **英文回退与异步旧文已完整扫清提案范围。**683键中原有161个尚未进入首批提案的英文槽含中文；300键修订合并后，范围内英文中文回退为0。供应规则EN补齐当前CN的50%商品价格、各国建筑类型，删Latest refresh、每次核验等更新说明。external全部67键完成英译／审查；供应全部相关字段完成双语对照。

## 原版完整链条及适用边界

### 脚本按钮动态描述

'''
report+=f"- 调用者：{link(G,'common/journal_entries/06_cuba.txt',324)} 的 `je_cuba_independencia`，343行 `scripted_button = je_cuba_promise_freedom`；同JE有icon/group/progress_bar。\n"
report+=f"- 实例：{link(G,'common/scripted_buttons/00_cuba_scripted_buttons.txt',2)}；name在3–20行、desc在21–36行均直接用`first_valid/triggered_desc`，同一country上下文以 `has_law_or_variant` 分支；visible/possible/selected/effect全部在同对象内。effect从82行起设置承诺变量并作用于奴隶起义运动，说明这里是有效行为入口而非纯示意。\n"
report+=f"- 本地化：{link(G,'localization/english/ip4_cuba_l_english.yml',98)}，99/105行对应两个desc，后者已使用ROOT.GetCountry；无需新增GUI或customizable_localization。\n"
report+='- 适用差异：NESND按当前阵营脚本值1/2选择文字，效果和条件仍沿用原发送函数。`tag_WUU_var`只在登基后设置，不能用于判断登基前已选择的拥吴路线。无立场时回退中性描述。\n'
report+=f"- 原版按钮SHA256：`{sha(G/'common/scripted_buttons/00_cuba_scripted_buttons.txt')}`。\n"
report+='\n### 君主标题与姓名\n\n'
report+=f"- 原版{link(G,'events/law_events/republic_laws.txt',174)} 的 `republic_laws.3` 为country_event/placement ROOT，以君主制和正在立法为触发，description引用republic_laws.3.d；icon与event_image都由本体定义。\n"
report+=f"- 实际文案{link(G,'localization/english/content_4_l_english.yml',272)}同时使用 `[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle] [ROOT.GetCountry.GetRuler.GetFullName]`。{link(G,'localization/english/agitators_2_l_english.yml',8)}还存在同一GetFullName/GetPrimaryRoleTitle组合。\n"
report+='- NESND明20触发须有在世合法朱氏君主，明22紧接commit_ming；吴23紧接install_wu_peacefully，该函数先转入/生成实际君主再通知。其余无君主保证的country主体仍可执行外交，但不强接ruler动态引用。没有把旧历史回忆中的郑昭改为现任君主。\n'
report+='\n### 当前项目调用与机制来源\n\n'
sources=[('common/journal_entries/nesnd_succession_board.txt',26),('common/scripted_buttons/nesnd_south_accords.txt',1),('common/scripted_buttons/nesnd_crisis_buttons.txt',53),('common/scripted_effects/nesnd_south_accords.txt',9),('common/scripted_triggers/nesnd_south_politics.txt',179),('events/nesnd_south_accords.txt',3),('events/nesnd_south_accords.txt',221),('events/nesnd_south_accords.txt',262),('common/scripted_effects/nesnd_south_peace.txt',403),('common/scripted_effects/nesnd_south_peace.txt',439),('common/journal_entries/nesnd_regional_preparations.txt',2),('events/nesnd_crisis_events.txt',126),('events/nesnd_chen_security.txt',2),('events/flavorUSM_ce.txt',806),('common/scripted_effects/nesnd_chen_security.txt',147),('common/scripted_effects/nesnd_south_reconciliation.txt',26),('events/nesnd_external_events.txt',1),('common/scripted_buttons/nesnd_external_buttons.txt',1),('common/scripted_triggers/nesnd_supply_triggers.txt',1),('common/static_modifiers/nesnd_crisis_modifiers.txt',1)]
for f,ln in sources:report+=f'- {link(M,f,ln)}；SHA256 `{sha(M/f)}`。\n'
report+='''
## 最小代码改动

只更改显示分支；不新增权重、不恢复退役日志、不增加任何货物／金钱／政体效果。

1. `common/scripted_buttons/nesnd_south_accords.txt` 的现行按钮中，将单行 `desc = nesnd_south_offer_accord_desc` 替换为：

```text
desc = {
    first_valid = {
        triggered_desc = {
            trigger = { nesnd_board_stance_value = 1 }
            desc = nesnd_federal_compact_button_desc
        }
        triggered_desc = {
            trigger = { nesnd_board_stance_value = 2 }
            desc = nesnd_federal_compact_button_alt_desc
        }
        desc = nesnd_south_offer_accord_desc
    }
}
```

2. `common/scripted_buttons/nesnd_crisis_buttons.txt` 中旧 `nesnd_federal_compact_button` 若保留兼容定义，可同步使用相同desc块；它当前无JE调用，不必重新挂回JE。name保持现有 `nesnd_south_offer_accord`。新alt键原为注释，需在两种语言中成为真实键。
3. `nesnd_south_accords.20`、`.21` 的 `name = nesnd_south_accords.reconsider` 选项中，各添加 `custom_tooltip = nesnd_south_reconsider_tt`。实际重新开始12个月的效果不变；原选项里的开发式“重新计算”移至具体操作提示。
4. 明20/22、吴21/23本来就是四个独立事件，按JSON分别修订正文即可，无须为它们另造动态分支。`nesnd_crisis.10`无caller，保留旧兼容稿；不能仅替换它后宣称用户现在能看到礼法结果。
5. 每个改动键的所有定义路径见inventory附表与JSON all_zh/all_en。同键多层须统一或由应用者明确保留单一最终定义，不新增一个更深zz文件来继续堆旧解释。主MOD英文中用户中文修改的事实／立场已人工继承到提案，不能用旧候选覆盖其本意。

## 作者语体对读与本轮返工

作者基线只来自 pre-update-20261030T233944Z/mod；本轮作者附件为事实和修订意图来源，旧AI句不当作作者样本。已对读原版 ce_usm_events 的 flavorUSM.1.d／4.d／5.d／7.d／8.d／10.d、ce_usm_conflicts_within_reason、usm_civilwar.8.d／10.d、相关选项和引文。原稿允许政治论说、历史铺陈和有立场的选项；判断重点是具体人物、制度与行动的因果，不靠每段短句或装饰文言。

'''
style=[('flavorUSM.4.d','nesnd_south_accords.23.d','郑昭的军事实绩、移民与集权变法相接；候选沿这种因果写郑氏权势如何成为国制，去交接印信簿册。'),('ce_usm_conflicts_within_reason','nesnd_south_succession_board_reason','原文把论争放在乡校与议会；候选明确监生、学政、内阁及营伍，而不把全天下压成同一张案。'),('flavorUSM.7.d','nesnd_huguang_preparations_reason','原文从朱班博与郑雕锦关系讲西府政治；候选保留作者岳麓、共和派和南府排挤的具体链条。'),('flavorUSM.5.d','nesnd_protect_chen_button_desc','原文写政治盟友转为相忌；现行按钮叙述改革触动谁、为什么应保护陈，不承诺护卫必然救活。'),('usm_civilwar.10.d','usm_civilwar.10.d','作者胜利不等于无争论；候选说明宗室、地方领袖与共和派各有主张，真实战争联盟仍称联盟。'),('flavorUSM.4.1','nesnd_south_accords.21.a','作者选项是政治行动/立场；新选项用受禅与依礼法施政，不写代码进度。'),('flavorUSM.4.f','flavorUSM.4.f','成熟作者引文原样保留中文并英译；crisis10/11等无出处新引文单独标为剧情拟写，不冒署古人。')]
for orig,new,why in style:
    base=I.get(orig,{}).get('baseline_zh')
    if base:report+=f"- 原文{link(B,base['file'],base['line'])}，SHA `{base['sha256']}`：{base['text'][:110]}……\n"
    report+=f"  - 对读键 `{new}`；决定：{why} 改后为编辑提案通过，未接入游戏。\n"
report+='''
局部纠正规则已实际应用：把“中央的盟书”按实际职责改成礼法；省际军事协议和国家间条约不改。把“军校—算粮饷”重建为书院监生—礼议院考试—未来省代表。把“国家颁诏”改为在有君主保证的事件中显示真正的title/name；无保证时改写行动主体。上述规则先回读最新north-south-institutions，再完成第二轮重写。第一版的 Liyi Assembly 已按本轮一致译名统一为 Assembly of Rites。

## 提案静态复核与局限

- 所有300键均有完整中文与英文；两语言动态方括号引用集合逐键相等；英文无中文回退；提案中文无“原生／本日志／本项目／按原规则／快照”。
- 数字只据现有脚本或原有效提示保留；没有调整政治权重、定向立场概率、经济成本或HNA三按钮可达性。12个月重置提示属于已有代价的展示。
- 已识别原稿与效果的差异并写明：HNA闲置；crisis10无caller；crisis11隐藏；明结局不吞并；crisis20土改条件；flavorUSM6死亡；法国可能共和。
- `nesnd_wu_eastern_question_reason` 为日本开发交接项：当前中文仅写天皇／德川两方，英文写丰臣／德川／天皇三方。已通知主代理，由日本候选所有者统一；不以本南朝审查覆盖其正在变更的日本剧情。
- 原作者成熟历史事件中不属于本次AI修订的长文与强烈立场保留。它们列在清单中，保留结论不等于认证所有原版剧情、角色生命周期、历史日期或引用归属均正确。
- 仅在报告目录生成文件；没有运行游戏、没有自称ENGINE_PASS。正式应用后的覆盖键检查、BOM、Jomini解析和候选检查由主代理进行。

## 逐文件／逐键清单

`重写`=JSON有双语提案；`保留作者原文`=中文与成熟基线逐字相同，本轮不改；`通过`=当前文案在本轮制度/玩家表达范围内保留；`日本交接`=交由日本正在修改的候选负责。是否有直接引用仅用于定位，JE自动字段、modifier名与二级本地化引用也可能有效，不能以未检出直接引用擅删文本。

'''
groups=collections.defaultdict(list)
for k,v in I.items():groups[v['zh']['file']].append(k)
counts=collections.Counter()
decisions={}
for f,keys in sorted(groups.items()):
    report+=f'### {f}\n\n共{len(keys)}键；主MOD SHA256 `{I[keys[0]]["zh"]["sha256"]}`。\n\n|键|行|判定|依据／机制来源|\n|---|---:|---|---|\n'
    for k in keys:
        v=I[k]
        if k=='nesnd_wu_eastern_question_reason':state='日本交接';reason='三日本政权叙述不一致，已通知主代理。'
        elif k in P:state='重写';reason=P[k]['reason']+('【闲置/兼容字段，未接入现行界面】' if P[k]['mechanic'].startswith(('DORMANT','LEGACY DISPLAY')) else '')
        elif k=='nesnd_federal_compact_button_outcome_tt':state='闲置旧机制';reason='旧+20/−8/18月循环无当前caller；现行遣使6月/36月承诺，不得把旧数值当上线效果。'
        elif v.get('baseline_zh') and v['baseline_zh']['text']==v['zh']['text']:state='保留作者原文';reason='成熟作者基线逐字一致；本轮无制度冲突改动。'
        else:state='通过';reason='名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。'
        counts[state]+=1
        refs='；'.join(v['refs'][:2]) or '自动字段／本地化引用；无直接脚本文字命中'
        decisions[k]={'decision':state,'reason':reason,'refs':v['refs'],'file':f,'line':v['zh']['line']}
        report+=f'|`{k}`|{v["zh"]["line"]}|{state}|{reason.replace("|","／")} 来源：{refs}|\n'
report+='\n新增键：`nesnd_federal_compact_button_alt_desc`、`nesnd_south_reconsider_tt`；两语言均已在提案JSON中。\n\n'
report+='判定计数：'+json.dumps(dict(counts),ensure_ascii=False)+'。\n'
(R/'usm-audit.md').write_text(report,encoding='utf-8')
(R/'usm-decisions.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2),encoding='utf-8')
desc='''desc = {
    first_valid = {
        triggered_desc = {
            trigger = { nesnd_board_stance_value = 1 }
            desc = nesnd_federal_compact_button_desc
        }
        triggered_desc = {
            trigger = { nesnd_board_stance_value = 2 }
            desc = nesnd_federal_compact_button_alt_desc
        }
        desc = nesnd_south_offer_accord_desc
    }
}'''
changes=[
{'file':'common/scripted_buttons/nesnd_south_accords.txt','find':'desc = nesnd_south_offer_accord_desc','replace':desc,'count':1,'required':True},
{'file':'common/scripted_buttons/nesnd_crisis_buttons.txt','find':'name = nesnd_south_offer_accord desc = nesnd_south_offer_accord_desc','replace':'name = nesnd_south_offer_accord\n    '+desc,'count':1,'required':False,'reason':'Synchronise unused compatibility button only; do not add a caller.'},
{'file':'events/nesnd_south_accords.txt','find':'name = nesnd_south_accords.reconsider','replace':'name = nesnd_south_accords.reconsider\n        custom_tooltip = nesnd_south_reconsider_tt','count':2,'required':True}]
(R/'usm-code-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
checks={'scope_sets_equal':all(sorted(re.findall(r'\[[^]]+\]',v['zh']))==sorted(re.findall(r'\[[^]]+\]',v['en'])) for v in P.values()),'no_chinese_english':all(not re.search('[\u4e00-\u9fff]',v['en']) for v in P.values()),'no_programmer_terms_zh':all(not re.search('原生|本日志|本项目|按原规则|快照',v['zh']) for v in P.values()),'proposals':len(P),'inventory':len(I),'engine_run':False,'code_mutated':False,'main_mutated':False}
(R/'usm-proposal-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print('report',len(report),'characters;',dict(counts))
