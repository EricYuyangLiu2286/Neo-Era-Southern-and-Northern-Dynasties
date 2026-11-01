"""Authorized three-way integration; preserve current main metadata and all newer documents."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,zipfile,re
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
M=W.parent/'mod/Neo-Era Southern and Northern Dynasties';C=W/'exports/release-logfix-20261101-a'
P=W/'exports/resumed-integrated-20261101-a';B=W/'backups/pre-change-github-f2-entry-20261101T002814Z/mod'
S=Path('C:/Users/Eric Liu/.codex/skills/nesnd-victoria3');R=W/'reports/logfix-release-20261101'
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def re_debug(rel):return bool(re.search(r'(?:^|/)(?:qa|probe|fixture)[^/]*|nesnd_(?:qa|batch_probe|sequence_qa|f2_qa)',rel,re.I))
def manifest(p):return {f.relative_to(p).as_posix():sha(f) for f in sorted(p.rglob('*')) if f.is_file()}
def put(p,text):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
checks=json.loads((R/'final-source-checks.json').read_text('utf-8'))
assert not checks['tiger_new_errors'] and not checks['production_QA_leaks'] and not checks['source_regression']['after_failures']
assert json.loads((R/'mcp-supply-query.json').read_text('utf-8'))['status']=='PASS'
base,main,candidate,parent=manifest(B),manifest(M),manifest(C),manifest(P)
assert not set(base)-set(candidate),'Deletion requires separate review'
for rel,h in parent.items():
 if rel.startswith(('map_data/','common/history/','gfx/','localization/')):assert candidate[rel]==h,rel
keep=lambda rel:rel.endswith('.md') or rel=='.metadata/metadata.json'
conflicts=[rel for rel,h in candidate.items() if not keep(rel) and main.get(rel)!=base.get(rel) and main.get(rel)!=h]
assert not conflicts,conflicts
plan=[]
for rel,h in candidate.items():
 if keep(rel) and rel in main:continue
 if main.get(rel)!=h:plan.append({'file':rel,'action':'update' if rel in main else 'add','before':main.get(rel),'after':h})
planfile=R/'main-merge-plan.json';assert not planfile.exists()
put(planfile,json.dumps({'authorized_by':'User 2026-11-01: fix bugs, then integrate into main; log/external validation prioritized','source':str(C),'target':str(M),'base':str(B),'conflicts':conflicts,'deletions':[],'plan':plan,'preserved_metadata':main['.metadata/metadata.json'],'fresh_engine_rerun':False,'reused_engine_evidence':'run20261101T014437Z hair/new-map/Japan/Lin/Chen initialization; user accepted harbor test closure'},ensure_ascii=False,indent=2))
assert manifest(M)==main and manifest(C)==candidate
for row in plan:
 d=M/row['file'];d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(C/row['file'],d)
assert sha(M/'.metadata/metadata.json')==main['.metadata/metadata.json']
for row in plan:assert sha(M/row['file'])==row['after']
for rel,h in main.items():
 if keep(rel):assert sha(M/rel)==h
# Archive documents before reconciling the authoritative handoff.
archive=W/'plans/two-empires/archive'/('log-first-delivery-'+stamp);archive.mkdir(parents=True)
for f in [S/'references/active-work.md',M/'.scratch/debug-release/map.md',M/'.scratch/debug-release/issues/05-delivery-merge-review.md']:
 shutil.copy2(f,archive/(f.parent.name+'-'+f.name))
summary='''# 2026-11-01 日志优先修复交付

本轮已按最新授权备份并整合至主MOD；Git保存另记录实际提交和远端核验。

- 修复供给按钮预览缺失pending/partner/sponsor、双边回复与条约查询的对象守卫；缺对象的有效性谓词明确返回false。市场/宗主旧档缺字段走安全重新登记，保持实际合作逻辑。
- 清理不存在的修正先判has_modifier。除供给旧修正外，另修17处同类写法；不改变修正存在时的结果。
- 进度展示读取安全script_value，不假定预览执行了前面的set_variable；保留12周门槛和原经济条件。
- 一并合入已保存的F1/F2、女性发型兼容、六地区地图细化、Lin摄政及陈压力初始化保护；主MOD metadata、当前文档和原数据完整保留，零删除、零冲突。
- QA浮层、控制台按钮、测试事件/on_action与工具仅在WORK独立测试环境，正式MOD及发布ZIP没有这些文件。

验证：已捕获原生日志中的错误模式，源码回归23项失败→0；最终Tiger相对综合父版本零新增诊断；4次针对修复函数的实际stdio MCP查询通过。历史/人口/生产/几何/交通/本地化全量检查通过，相关源文件在最后修复中未改变。局部脚本修改后重新完成解析/Tiger/MCP检查。

Tiger保留6条已有error及977条warning，不将旧报告改成全绿：other角色与control_half_target_country_states有当前原版实例，total_crew_needed有先前原生证据，Foochow船体奖励与Russia空if有原版同形证据。细目和旧原始报告保留；本次零新增不宣称所有旧警告均无问题。

按用户指示，本轮不再启动游戏反复截图或读档；新按钮修复为外部源码验证，未伪称修复后新引擎日志已清零。复用已有发型、日本恢复/Lin、陈压力0→25→JE仍25、地图新局及三港入港证据。全游戏所有未来分支绝无BUG无法由这些检查证明。

完整改革后续连接、长期履约、编辑器舍入修复仍属原始欠账；中断中的独立工作未混入本次正式修复。
'''
put(R/'release-notes.md',summary)
handoff=f'''# 当前交接：日志优先修复已整合

更新：2026-11-01。先读[日志优先交付](log-first-delivery.md)与[项目任务索引](< {M.as_posix()}/.scratch/debug-release/map.md >)。旧交接完整保留于 `{archive.as_posix()}`。

当前主MOD已整合 `release-logfix-20261101-a` 的玩法差异，保留原metadata id3702225772、最新文档和已有数据。详见[交付记录](<{(R/'release-notes.md').as_posix()}>)及[逐文件合并清单](<{planfile.as_posix()}> )。Git提交/远端结果见同目录git-delivery.json。

优先按error.log去重查调用链，批量修复后用现有parser/Tiger/MCP复核。进港、死亡、分裂、任命等已成功一次即复用结论；本轮用户明确停止重复开局/读档/截图。只有新的未决引擎语义需要定向实测。正式加载不含QA覆盖层。

已完成：原版参考核心步骤；女性发型；六地区地图细化；日本吞并后三政权恢复及Lin摄政；陈死亡压力初始化保护；供给按钮nil scope与修正清理错误的源码修复。新按钮修复只完成外部检查，没有声称新引擎日志零错。

原始欠账继续保留：QE1/SHA改革连接、明吴战后重建/长期履约、编辑器舍入修复。中断代理可能有独立备份/候选，先检查现场再继续，主MOD已发布修复作为新基线。市场退出低优先级，允许游戏失败、稀缺与破产；不加保姆式补救。
'''
handoff=handoff.replace('< ', '<').replace(' >','>').replace('}> )','}>)')
put(S/'references/active-work.md',handoff)
p=S/'references/log-first-delivery.md';s=p.read_text('utf-8');s+='\n- 代码重写须保留函数式键的引号（如`"relations(scope:...)"`）。本地宽松parser可解析未加引号的错误写法，须由独立Tiger复核，不能让同一parser自证生成正确。MCP get_structure默认只给顶层键，核嵌套guard用key_path（如if.limit），返回占位符不是缺少guard。\n';put(p,s)
p=M/'.scratch/debug-release/map.md';s=p.read_text('utf-8');s+='\n## 已整合：日志修复正式包\n\n主MOD已按最新授权备份合入，零文件删除/零冲突，metadata和当前文档保留。供给按钮缺失对象及17处其他清理保护已修；源码23→0，Tiger零新增，MCP4查询通过。正式包无QA覆盖层。详细范围、未新跑引擎及后续功能欠账见WORK/reports/logfix-release-20261101/release-notes.md。此节取代上方旧“主MOD未合入/等待审批”状态；旧阶段记录保留。\n';put(p,s)
p=M/'.scratch/debug-release/issues/05-delivery-merge-review.md';put(p,f'''# 主MOD合并与版本保存

Record: implementation
Category: enhancement
Status: ready-for-agent
Execution: completed
Assignee: root
Blocked by: none
Validation: STATIC_PASS
Evidence: [交付记录](<{(R/'release-notes.md').as_posix()}>)
Approval: user-authorized 2026-11-01

## Result

最新用户指令取代此前再次审批门槛；已备份并按三方SHA比较整合主MOD，保留原发布标识及后续文档。QA工具未进入正式加载；Git提交及推送按实际报告核验。新按钮修复未冒称引擎复测通过；复用已验证的游戏机制与地图结果。

旧审批草稿及记录保留于 `{archive.as_posix()}`。
''')
for name in ['03-f2-minimal-debug.md','04-engine-validation.md','07-map-refinement.md']:
 p=M/'.scratch/debug-release/issues'/name;s=p.read_text('utf-8-sig');s+='\n## 2026-11-01 收口\n\n依用户最新指令复用已有机制、地图/进港证据，停止重复开局/读档。日志优先修复及主MOD整合已完成；具体范围与未新跑引擎边界见WORK/reports/logfix-release-20261101/release-notes.md。旧未测组合不扩写为全部通过。\n';put(p,s)
post=manifest(M);put(R/'main-merge-result.json',json.dumps({'main':str(M),'timestamp':stamp,'files':len(post),'added':sum(x['action']=='add' for x in plan),'updated':sum(x['action']=='update' for x in plan),'deletions':0,'metadata_preserved':True,'main_manifest':post,'source_candidate_manifest':candidate,'checked':checks,'fresh_engine_rerun':False},ensure_ascii=False,indent=2))
release=W/'releases/nesnd-20261101-logfix.zip';release.parent.mkdir(exist_ok=True);assert not release.exists()
excluded=[]
with zipfile.ZipFile(release,'w',zipfile.ZIP_DEFLATED) as z:
 for rel in post:
  if rel.startswith(('docs/','.scratch/','development/','tools/')) or rel.endswith(('.md','.bak','.py','.pyc')):excluded.append(rel);continue
  assert not re_debug(rel),rel
  z.write(M/rel,rel)
put(R/'package.json',json.dumps({'path':str(release),'sha256':sha(release),'excluded_documentation_and_legacy_backups':excluded,'QA_included':False},ensure_ascii=False,indent=2))
print(json.dumps({'main_files':len(post),'copied':len(plan),'deletions':0,'package':str(release)}))
