"""Prepare handoff, then merge only reviewed files with before-hash conflict checks."""
from pathlib import Path
import json,sys,hashlib,shutil,subprocess,zipfile
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');M=W.parent/'mod/Neo-Era Southern and Northern Dynasties'
C=W/'exports/button-guards-20261101-a';B=W/'backups/pre-change-button-guard-fix-20261101T093152Z/mod';R=W/'reports/button-guards-20261101'
S=Path('C:/Users/Eric Liu/.codex/skills/nesnd-victoria3');G=W/'projects/nesnd-repository'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(p):return {x.relative_to(p).as_posix():sha(x) for x in p.rglob('*') if x.is_file()}
def put(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def dump(p,v):put(p,json.dumps(v,ensure_ascii=False,indent=2))
def copy(src,dst):dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
assert json.loads((R/'source-checks.json').read_text('utf-8'))['status']=='STATIC_PASS'
assert not json.loads((R/'tiger-delta.json').read_text('utf-8'))['added']
assert json.loads((R/'mcp-queries.json').read_text('utf-8'))['status']=='PASS'
changes=json.loads((R/'source-changes.json').read_text('utf-8'))
for p in changes['changed']:assert sha(C/p)==changes['after'][p]
issue='.scratch/debug-release/issues/09-button-reference-guards.md'
if sys.argv[1]=='prepare':
 notes='''# 按钮引用修复：供用户测试的主 MOD 交付

2026-11-01。用户授权修复上一轮代码审计发现的问题，备份后合入主项目，由用户自行测试。本轮没有启动游戏或修改游戏加载配置。

## 修复范围

- 外部援助：目标选择、援款/军火的供给与请求、AI周检查的缺目标保护；pending/双方sponsor与发起国安全校验；接受执行重新检查资格，取消/超时撤销事件，拒绝仅清理匹配请求。保留30天pending、6个月冷却、7天投递及原金额/货量。
- 土改、南明/吴、丹那沙林进度刷新：临时scope和数值存在后再读取；同形PHI helper也保护。按钮预览不会假定前面保存作用域已经执行。
- 丹那沙林的建设、培训、健康条件与地主协商：对象失效时安全返回false。
- 日本发送条件及实际执行：JAP不存在时不读取停战关系、不设置“已送达”标记或发送空目标事件；原吞并/恢复/Lin链保持原样。
- 法国打击共和派团结按钮：实际随机目标采用与可用条件相同的排除规则。
- 新的AI闲置周数安全getter；既有接口字段good/goods写法按各自引擎文档保留，没有机械替换。

## 检查与边界

53项针对真实源代码的守卫/选择一致性检查，旧版53项失败→候选0项失败；条约实际payload、保存的金额/期限、地图/历史/人口/图像/本地化和发布metadata的SHA一致。全common/events文本通过有序解析。Tiger零新增诊断，最终6 error、975 warning、2 tips；6条旧error沿用上次已有原版/工具差异分类，并非本次新增。4次实际stdio MCP嵌套查询通过。

这些检查不执行引擎。本批为STATIC_PASS / ENGINE_NOT_RUN，用户测试结果尚未产生，不声称error.log已经在实机清零。

Skill的核心入口和syntax-and-routing引用安全章节已更新，log-first-delivery链接该单一规则来源。记录对象/数值、嵌套guard、预览、过期请求、随机候选一致性、接口字段差异及保留引号的局部编辑方法。

## 保存与测试入口

主MOD原路径不变，正常加载组合不变；无需QA覆盖层。可以直接使用主项目测试上述按钮。旧存档里已经出现的错误不会被本轮倒推消除；新交互受修复代码保护，不修改已有存档。

完整修改前备份：WORK/backups/pre-change-button-guard-fix-20261101T093152Z/mod。
候选：WORK/exports/button-guards-20261101-a；独立候选/合入后checkpoint备份由backup.py生成。
正式包：WORK/releases/nesnd-20261101-button-guards.zip，工具/报告/任务文档/QA均排除。
逐文件合并和SHA：本目录main-merge.json；Git与远端结果：git-delivery.json。

## 原版与工具依据

GAME为本机Victoria 3 1.13.11 / build24799966，catalog CURRENT、changed0。原版events/commander_events.txt:57–61提供saved scope失效时cancellation_trigger；common/scripted_triggers/00_scripted_triggers.txt:44起为条件分支实例。已有供给预览原生日志与已修的supply helper提供本项目错误模式；本轮只修同类闭包。

WORK/references/engine-docs-1.13.11-20261031/triggers.log:8955与effects.log:1056分别约定good/goods；GAME/common/treaty_articles/13_goods_transfer.txt及history/treaties实例用于实际条约payload交叉核查。

旧审计：WORK/reports/button-code-audit-20261101/report.md。检查脚本：WORK/tools/check_button_guards_20261101.py。MCP浅层返回[block]必须继续展开key_path；本轮修正的是查询路径，不是为迎合工具改变脚本。
'''
 put(R/'release-notes.md',notes)
 put(C/issue,f'''# 09 按钮引用、预览与延迟回复保护

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: STATIC_PASS
Evidence: [{R.as_posix()}/release-notes.md](<{R.as_posix()}/release-notes.md>)

## Result

按2026-11-01用户授权修复审计问题并交付主项目。12个玩法脚本文件变化，53项源检查通过、Tiger零新增、MCP四查询通过。完整独立备份、无玩法删除，未启动游戏；实机由用户测试，未标ENGINE_PASS。

## Comments

引用规则维护在NESND技能syntax-and-routing.md，核心SKILL与log-first-delivery均路由到该节。之前已验证地图/发型/恢复/进港机制的代码保持不变。
''')
 p=C/'.scratch/debug-release/map.md';s=p.read_text('utf-8-sig');s+='\n## 最新交付：按钮引用保护\n\n[09 按钮修复与用户测试](issues/09-button-reference-guards.md)：完成源码修复和主项目交付，STATIC_PASS，用户自行实机测试；不打开游戏。12个玩法脚本文件修改，53项检查通过，Tiger零新增，MCP四查询通过。该节为当前入口；上方历史进度保留。引用规则集中在技能syntax-and-routing.md。\n';put(p,s)
 p=S/'references/active-work.md';s=p.read_text('utf-8');s+='\n## 当前：按钮同类问题已修复并交付用户测试\n\n2026-11-01用户进一步授权修复全部已发现按钮问题、合入主项目，并亲自测试。本轮禁止启动游戏。`button-guards-20261101-a`修复外部援助引用与过期回复、四组display helper、丹那沙林/JAP对象边界、法国目标筛选，主MOD与main为交付目标。53项源码检查通过，Tiger零新增、MCP四查询通过；STATIC_PASS / ENGINE_NOT_RUN。详细交付见[记录](<'+(R/'release-notes.md').as_posix()+'>)，Git结果见同目录git-delivery.json。旧交接逐字保存于本次报告skill-before/references/active-work.md。引用规则集中在[语法与引用安全](syntax-and-routing.md#引用安全按钮延迟回复与预览)。原始功能欠账保持原列表。\n';put(p,s)
 dump(R/'skill-review.json',{'date':'2026-11-01','source':'User explicit request plus audited button call chains and existing native preview failures','files':{p:sha(S/p) for p in ['SKILL.md','references/syntax-and-routing.md','references/log-first-delivery.md','references/active-work.md']},'validation':'quick_validate PASS; references and code examples reviewed against repaired sources','engine_run':False})
 print('Handoff, issue and skill evidence prepared.')
elif sys.argv[1]=='merge':
 assert manifest(M)==manifest(B),'Main changed since independent backup; stop for three-way review'
 assert subprocess.check_output(['git','status','--porcelain'],cwd=G).strip()==b''
 assert subprocess.check_output(['git','branch','--show-current'],cwd=G).strip()==b'main'
 bm,cm=manifest(B),manifest(C);plan=[p for p,h in cm.items() if bm.get(p)!=h]
 for p in plan:
  if p in bm:assert (G/p).exists() and sha(G/p)==bm[p],('Git conflict',p)
  else:assert not (G/p).exists(),('Git add conflict',p)
 for p in plan:copy(C/p,M/p)
 assert manifest(M)==cm
 assert sha(M/'.metadata/metadata.json')==bm['.metadata/metadata.json']
 dump(R/'main-merge.json',{'source':str(C),'target':str(M),'before_backup':str(B),'files':[{'path':p,'before':bm.get(p),'after':cm[p]} for p in plan],'deletions':[],'conflicts':[],'main_equals_candidate':True,'engine_run':False})
 z=W/'releases/nesnd-20261101-button-guards.zip';assert not z.exists();excluded=[]
 with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as pack:
  for p in sorted(cm):
   if p.startswith(('docs/','.scratch/','development/','tools/')) or p.endswith(('.md','.bak','.py','.pyc')):excluded.append(p);continue
   assert not p.startswith('EDITOR-');pack.write(M/p,p)
 with zipfile.ZipFile(z) as pack:
  for p in pack.namelist():assert pack.read(p)==(M/p).read_bytes()
 dump(R/'package.json',{'path':str(z),'sha256':sha(z),'excluded':excluded,'QA_included':False})
 load=W.parent/'content_load.json'
 if load.exists():
  data=json.loads(load.read_text('utf-8-sig'));enabled=data.get('enabledMods',[])
  dump(R/'normal-load-check.json',{'path':str(load),'sha256':sha(load),'modified':False,'QA_enabled':any('qa-overlay' in x.get('path','').lower() for x in enabled),'main_MOD_present':any(Path(x.get('path','')).resolve()==M.resolve() for x in enabled)})
 for p in plan:copy(M/p,G/p)
 for p in ['SKILL.md','references/syntax-and-routing.md','references/log-first-delivery.md','references/active-work.md']:copy(S/p,G/'development/nesnd-skill'/p)
 for p in R.iterdir():
  if p.is_file() and p.name not in ['tiger-raw.json','tiger-stderr.txt']:copy(p,G/'development/workbench/reports/button-guards-20261101'/p.name)
 for name in ['fix_button_guards_20261101.py','format_button_guard_spans_20261101.py','check_button_guards_20261101.py','deliver_button_guards_20261101.py']:copy(W/'tools'/name,G/'development/workbench/tools'/name)
 for p in plan:assert sha(G/p)==cm[p]
 subprocess.run(['git','add','--all'],cwd=G,check=True)
 # Preserve Windows CRLF; the saved .diff is evidence, not code to lint as new source.
 command=['git','-c','core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol','diff','--cached','--check','--','.',':(exclude)development/workbench/reports/button-guards-20261101/changes.diff']
 result=subprocess.run(command,cwd=G,capture_output=True,text=True,encoding='utf-8');dump(R/'git-whitespace-check.json',{'command':command,'exit_code':result.returncode,'output':result.stdout+result.stderr});assert result.returncode==0,'See git-whitespace-check.json'
 print(json.dumps({'merged_files':len(plan),'gameplay_files':len(changes['changed']),'deletions':0,'zip':str(z),'git_staged':True},ensure_ascii=False))
else:raise ValueError(sys.argv[1])
