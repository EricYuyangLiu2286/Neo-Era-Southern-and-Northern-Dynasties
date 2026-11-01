"""Authorized source-only delivery; conflict checks preserve current main and Git."""
from pathlib import Path
import sys,json,hashlib,shutil,subprocess,zipfile
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');M=W.parent/'mod/Neo-Era Southern and Northern Dynasties';G=W/'projects/nesnd-repository'
C=W/'exports/south-feedback-20261101-a';R=W/'reports/south-feedback-20261101';S=Path('C:/Users/Eric Liu/.codex/skills/nesnd-victoria3')
B=W/'backups/pre-change-south-politics-feedback-20261101T175047Z/mod'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def man(root):return {p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file()}
def put(p,s):
 raw=p.read_bytes() if p.exists() else b'';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\r\n','\n').replace('\n','\r\n' if b'\r\n' in raw else '\n').encode('utf-8'))
def dump(p,v):put(p,json.dumps(v,ensure_ascii=False,indent=2))
def copy(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
proof=json.loads((R/'source-checks.json').read_text('utf-8'));assert proof['status']=='STATIC_PASS'
assert not json.loads((R/'tiger-delta.json').read_text('utf-8'))['added']
assert json.loads((R/'mcp-queries.json').read_text('utf-8'))['status']=='PASS'
for rel in proof['changed']:assert sha(C/rel)==proof['after_manifest'][rel],rel
if sys.argv[1]=='prepare':
 text='''# 南朝立场、文案与四年危机节奏修正

2026-11-01用户七项反馈的交付记录。本轮未打开游戏、未切换加载组合、未操作存档；实机结果由用户后续测试。

## 对应修改

1. 襄樊大营（HNA）在朝争开局与战前固定拥明。初始化、旧档每周刷新、只读立场值、AI首次选择/复议、盟约邀请/接受及内战答复一起约束；旧的拥吴盟书会撤销。内战答复拥有HNA专用的有效默认拥明选项，其他国家原有效选项及效果保留。战后既有革命/结局不由每周刷新强制重写。
2. “通商与自筹”更名“脆弱的贸易”（Fragile Trade）。两类贸易日志正文、状态、动作和相关说明按作者旧replace文本重写。配员不足按湖广/四川/广西/东洲分别描述，完整数值条件移到“货源与生计”悬停说明。
3. 全局“南朝诸国”新增should_be_pinned_by_default_involved=yes；原uninvolved_or_context设置保留。默认钉选定义已修；没有声称已在当前存档界面验证。
4. 南朝诸国正文与状态不再用“每周更新、对应事件决定”等开发说明；主体改为南京/杭州、诸侯、使者、商人与兵财的政治矛盾。精确数量仍在表格与tooltip中保留；未隐藏玩家决策所需门槛。
5. 压力通常每月＋3，旧邦国契约修正期间＋2.5；有效和解原有每月−3另算。共用script_value确保实际增量与说明一致。首辅案自1837年7月且压力>24进入概率窗口；1838年初仍未结案且陈在本国，就通过现有nesnd_chen.2强制进入原分支。护卫、迁居、查谍仍影响死亡/受伤/脱险概率，未改其权重。
6. USM中央及带nesnd_ming_court身份的朝廷不提供中立/自主按钮；visible、possible和effect同时保护。旧存档的这两种无意义朝廷立场改回拥明；拥明/拥吴两条路线保留。
7. +25原本在nesnd_chen_after_death中，沿调用链已核对；保留started_with_chendongyang的一次性保护，没有重复加分。死亡/受伤/脱险结算后立即同步国家JE与全局JE的压力条。修复flavorUSM.1残留的无条件归零，已积累压力不再被开场事件覆盖。

## 时间与顺序

未解决的危机在1839年初达到100压力，沿既有提前易代入口推进，解除无限等待郑钦自然死亡的瓶颈；不新增强制死亡，不改变人物历史。已经达成和平结局的国家不被重新开启危机。每周也校正期限压力，避免和解/月脉冲先后顺序造成卡在97。

自动与主动易代都等首辅案结算；待执行的死亡事件先结束。随后沿flavorUSM.4→flavorUSM.400→各国答复→ce_usm_civilwar_journal→usm_civilwar.2→nesnd_open_southern_war进入现有内战链。诸国答复保留3个月缓冲、180天最长等待，1839年开始后给后续外交阶段留出时间。此为正常开局节奏设计及源码顺序证据，不是引擎四年模拟结果；已达成和解、外交退让、关键国家灭亡、玩家主动暂缓等仍是既有游戏结果。

## 实际检查

- 48项源码检查：修改前43项不满足→候选全部通过。其余5项原本就正确（含已有+25及一次性保护），未冒称原先缺失。
- 全common/events有序解析通过；受改YAML均UTF-8 BOM、头/引号/键唯一检查通过，新文本键中英齐全。原始历史、地图、人物模板、资源及metadata哈希完全不变。
- Tiger：6 error、973 warning、2 tips；相对按钮修复后的基线没有新增诊断。6条既有工具/原版差异沿用原记录，未声称所有日志错误已实机清零。
- 实际stdio MCP四次嵌套源码查询通过：首辅案期限、压力期限、HNA身份、全局进度条刷新。它不运行引擎。
- 原两widget布局逐字保留，仅加钉选字段，避免格式重排让已有工具提示被误分类为新增。

## 原始来源与写作对照

原版1.13.11/build24799966：common/journal_entries/00_peoples_springtime_je.txt:317–318的参与/未参与钉选字段；events/peoples_springtime.txt:776的country→global je可选跳转；journal_entries.md月/周on_action回调。现有项目的刺杀/继位/答复链原样复用。
作者样本取修改前备份pre-update-20261030T233944Z中的ce_usm_events_l_simp_chinese.yml：吴明论战日志与郑昭觐见正文。原文、SHA、候选与判断见prose-review.json。明确数值归tooltip，正文保留政治判断和具体行动者；新文本不冒充作者旧原稿。
规则补入技能journal-text-contract.md：全局钉选双字段、共享effect加分与bar同步、初始化不清零、期限与身份约束、按国家写状态。

## 保存

修改前备份：WORK/backups/pre-change-south-politics-feedback-20261101T175047Z/mod。
候选：WORK/exports/south-feedback-20261101-a；候选与合入后checkpoint另由backup.py独立保存。
主MOD仍为原路径；主分支与远端见git-delivery.json，逐文件合并见main-merge.json。
正式包：WORK/releases/nesnd-20261101-south-feedback.zip。没有QA面板、夹具、测试脚本、报告或开发文档。现有用户加载组合保持不变。
'''
 put(R/'release-notes.md',text)
 issue=C/'.scratch/debug-release/issues/11-south-feedback.md'
 put(issue,f'''# 11 南朝立场、文案与危机节奏

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: STATIC_PASS
Evidence: [交付记录](<{(R/'release-notes.md').as_posix()}>)

## Result

按用户七项反馈完成HNA固定拥明、朝廷选项约束、全局日志默认钉选、脆弱的贸易及文风修订、1837–1839危机窗口、陈事件即时进度同步和开场归零修复。48项源码检查、Tiger零新增、MCP四查询通过。历史地图/人物/资源不变；未启动游戏，等待用户实测。
''')
 p=C/'.scratch/debug-release/map.md';put(p,p.read_text('utf-8-sig')+'\n## 最新：南朝反馈修正\n\n[11 南朝立场、文案与危机节奏](issues/11-south-feedback.md)已交付主MOD：HNA战前固定拥明、朝廷无中立/自主、参与国默认钉选、“脆弱的贸易”与日志文风重写。1837下半年起首辅案、1838初保底进入分支、1839初未解决危机推进；陈各结局即时同步两处bar，intro不再清零。STATIC_PASS，未开游戏；完整限制与证据见对应交付记录。\n')
 p=S/'references/active-work.md';put(p,p.read_text('utf-8-sig')+'\n## 当前：南朝反馈修正已交付\n\n2026-11-01按最新七项反馈完成HNA默认固定拥明、朝廷身份选项约束、全局参与国默认钉选和日志文风修订。通商与自筹改为“脆弱的贸易”。首辅案1837下半年开始、1838年初保底，未解决危机1839年初沿既有易代/内战链推进。死亡原有+25保留且只加一次，两处压力bar立即刷新，intro归零移除。48项源码检查通过，Tiger零新增，MCP四查询通过；未开游戏、未修改存档，STATIC_PASS。候选south-feedback-20261101-a；[交付记录](<'+(R/'release-notes.md').as_posix()+'>)与主项目任务11为当前入口。旧交接保存于本轮报告skill-before/references/active-work.md。\n')
 dump(R/'skill-review.json',{'files':{p:sha(S/p) for p in ['references/journal-text-contract.md','references/active-work.md']},'source':'User 2026-11-01 southern-crisis feedback and current vanilla examples','validation':'quick_validate PASS; 48 source checks; no game launched'})
 print('Delivery notes, task 11 and skill handoff prepared.')
elif sys.argv[1]=='merge':
 assert man(M)==man(B),'Main files changed; review conflict instead of overwriting'
 assert subprocess.check_output(['git','status','--porcelain'],cwd=G).strip()==b''
 assert subprocess.check_output(['git','branch','--show-current'],cwd=G).strip()==b'main'
 before,after=man(B),man(C);changed=[p for p,h in after.items() if before.get(p)!=h]
 for rel in changed:
  if rel in before:assert (G/rel).exists() and sha(G/rel)==before[rel],('Git conflict',rel)
  else:assert not (G/rel).exists(),('Git add conflict',rel)
 for rel in changed:copy(C/rel,M/rel)
 assert man(M)==after
 dump(R/'main-merge.json',{'source':str(C),'target':str(M),'changes':[{'file':p,'before':before.get(p),'after':after[p]} for p in changed],'deletions':[],'conflicts':[],'main_equals_candidate':True,'game_launched':False})
 z=W/'releases/nesnd-20261101-south-feedback.zip';assert not z.exists();excluded=[]
 with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as pack:
  for rel in sorted(after):
   if rel.startswith(('docs/','.scratch/','development/','tools/')) or rel.endswith(('.md','.bak','.py','.pyc')):excluded.append(rel);continue
   assert not rel.startswith('EDITOR-') and not any(x in rel for x in ['nesnd_qa','nesnd_f2_qa','nesnd_batch_probe','nesnd_sequence_qa']);pack.write(M/rel,rel)
 with zipfile.ZipFile(z) as pack:
  for rel in pack.namelist():assert pack.read(rel)==(M/rel).read_bytes()
 dump(R/'package.json',{'path':str(z),'sha256':sha(z),'excluded':excluded,'QA_included':False})
 load=W.parent/'content_load.json'
 if load.exists():
  enabled=json.loads(load.read_text('utf-8-sig')).get('enabledMods',[]);dump(R/'normal-load-check.json',{'sha256':sha(load),'modified':False,'QA_enabled':any('qa-overlay' in x.get('path','').lower() for x in enabled),'main_present':any(Path(x.get('path','')).resolve()==M.resolve() for x in enabled)})
 for rel in changed:copy(M/rel,G/rel)
 for rel in ['references/journal-text-contract.md','references/active-work.md']:copy(S/rel,G/'development/nesnd-skill'/rel)
 for p in R.iterdir():
  if p.is_file() and p.suffix in ['.json','.md','.diff'] and p.name not in ['tiger-raw.json','logic-changes.json']:copy(p,G/'development/workbench/reports/south-feedback-20261101'/p.name)
 for name in ['fix_south_feedback_20261101.py','rewrite_south_feedback_loc_20261101.py','check_south_feedback_20261101.py','deliver_south_feedback_20261101.py']:copy(W/'tools'/name,G/'development/workbench/tools'/name)
 subprocess.run(['git','add','--all'],cwd=G,check=True)
 cmd=['git','-c','core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol','diff','--cached','--check','--','.',':(exclude)**/*.diff'];q=subprocess.run(cmd,cwd=G,capture_output=True,text=True,encoding='utf-8');dump(R/'git-whitespace-check.json',{'command':cmd,'exit_code':q.returncode,'output':q.stdout+q.stderr});assert q.returncode==0,'See git-whitespace-check.json'
 print(json.dumps({'main_merged':True,'files':len(changed),'gameplay_and_loc_files':len(proof['changed']),'deletions':0,'package':str(z)},ensure_ascii=False))
else:raise ValueError(sys.argv[1])
