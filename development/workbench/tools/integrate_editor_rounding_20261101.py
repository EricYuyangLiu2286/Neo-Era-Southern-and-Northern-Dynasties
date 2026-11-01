"""Promote the checked editor-only fix; preserve all deployed game data."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,shutil,subprocess,zipfile
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
M=W.parent/'mod/Neo-Era Southern and Northern Dynasties';G=W/'projects/nesnd-repository';E=W/'editor';S=Path('C:/Users/Eric Liu/.codex/skills/nesnd-victoria3')
R=W/'reports/editor-rounding-integration-20261101';A=W/'reports/editor-rounding-20261101'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(p):return {f.relative_to(p).as_posix():sha(f) for f in p.rglob('*') if f.is_file() and '__pycache__' not in f.parts}
def put(p,s):
 old=p.read_bytes() if p.exists() else b'';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_bytes((b'\xef\xbb\xbf' if old.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\r\n','\n').replace('\n','\r\n' if b'\r\n' in old else '\n').encode('utf-8'))
def dump(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2))
def copy(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
proof=Path(sys.argv[1]);result=json.loads(proof.read_text('utf-8'));C=Path(result['editor'])
assert result['tests_run']>=7 and result['failures']==result['errors']==result['skipped']==0,result
assert result['source_unchanged'] and result['game_launched'] is False
assert Path(result['source']).resolve()==M.resolve()
assert manifest(M)==json.loads((R/'main-before.json').read_text('utf-8'))
assert result['source_manifest']==manifest(M)
assert manifest(C)==result['editor_manifest'],'Candidate changed after tests'
pre=json.loads((A/'pre-change.json').read_text('utf-8'));old=manifest(E)
for p,h in old.items():assert h==pre['files'][p],('Editor changed',p)
new=manifest(C);changed=[p for p,h in new.items() if old.get(p)!=h]
assert changed==['model.py'],changed
assert sha(G/'development/workbench/editor/model.py')==old['model.py']
assert sha(G/'development/workbench/editor/province_move.py')==old['province_move.py']
assert not subprocess.check_output(['git','status','--porcelain'],cwd=G).strip()
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
backup=W/'backups'/('pre-change-editor-rounding-integration-'+stamp)
shutil.copytree(E,backup/'editor');assert manifest(backup/'editor')==old
dump(backup/'manifest.json',{'source':str(E),'status':'pre-change','files':old})
copy(C/'model.py',E/'model.py');assert manifest(E)==new
checkpoint=W/'backups'/('checkpoint-editor-rounding-'+stamp);shutil.copytree(E,checkpoint/'editor');assert manifest(checkpoint/'editor')==new
dump(checkpoint/'manifest.json',{'source':str(E),'status':'checkpoint','files':new,'tests':str(proof),'engine_verified':False})

note=f'''# Editor rounding 修复已整合

2026-11-01，用户明确授权恢复该子任务、外部测试并整合；未打开游戏或UI。

该任务修复离线地图编辑器Project.split的建筑等级分配。旧算法逐股份向下取整，使两笔1级股份的2级伐木场在50%拆分后成为旧2/新0；世界总量不变，旧守恒检查无法发现。修复仅修改model.py的import和分配调用，复用现有divide_building_ownership：先确定建筑迁出总等级，再按最大余数分配股份，50%明确得到旧1/新1。

现有主MOD无需重生成地图：独立核对12州148个国家/建筑组合，与原明确设计分配表完全一致（current-map-impact.json）。编辑器Python不被游戏加载，修复正式入口是WORK/editor，源码保存到Git main的development/workbench/editor；没有把工具、测试地图或数据夹具放进游戏目录。

验证：{result['tests_run']}项真实Project接口测试全部通过，0失败/0错误/0跳过。覆盖2→1/1、奇数和非50%比例、重复/外国/外州所有权、零级过滤、整个国别分州迁移、修正后的split保存/重开和不完整几何导出拒绝、当前主MOD无动作保存/重开/独立导出。测试源SHA保持不变；完整明细见{proof.as_posix()}。

已部署编辑器SHA：{new['model.py']}。
工具修改前完整备份：{backup.as_posix()}/editor。
工具交付checkpoint：{checkpoint.as_posix()}/editor。
主MOD修改前备份：WORK/backups/pre-change-editor-rounding-main-entry-20261101T094538Z/mod。

本次主MOD只更新任务记录；玩法文件与按钮修复版本629281f保持逐字节相同。沿用nesnd-20261101-button-guards.zip，游戏无需增加工具或QA加载项。游戏运行和编辑器UI验收没有在本轮执行；编辑器其它已列明的能力限制仍保留。
'''
put(R/'release-notes.md',note)
issue=M/'.scratch/debug-release/issues/10-editor-rounding.md'
put(issue,f'''# 10 编辑器建筑拆分取整

Record: implementation
Category: bug
Status: ready-for-agent
Execution: completed
Assignee: root/editor_rounding; root integration
Blocked by: none
Validation: STATIC_PASS
Evidence: [交付记录](<{(R/'release-notes.md').as_posix()}>)

## Result

正式WORK/editor已修复2级碎片持股均分2/0问题；{result['tests_run']}项真实工具接口测试通过，未开游戏。Git主分支保存工具修复；12州148个建筑组与既有设计一致，因此正式游戏数据保持不变。本任务只关闭舍入缺陷，不关闭08中其他改革、多结局或编辑器UI/通用交通能力欠账。
''')
for path,extra in [
 (M/'.scratch/debug-release/map.md','\n## Editor rounding 已完成\n\n[10 编辑器舍入修复](issues/10-editor-rounding.md)：正式工具已部署，真实接口外部测试通过；现有12州148建筑组分配正确，主MOD玩法数据未改。未开游戏。\n'),
 (M/'.scratch/debug-release/issues/08-original-backlog.md','\n## 已关闭的子项\n\n2026-11-01编辑器拆州建筑舍入缺陷已由[10](10-editor-rounding.md)完成，实际工具测试通过并合入主仓库。其余功能欠账及编辑器UI/通用地图能力边界继续保留。\n'),
 (S/'references/active-work.md','\n## Editor rounding 子项完成\n\n2026-11-01按用户要求恢复并完成编辑器拆州舍入任务，正式WORK/editor已更新，Git保存development/workbench/editor。真实Project接口回归通过，未打开游戏。现有主MOD12州148个建筑组与设计一致，玩法不变；旧“编辑器舍入修复待办”由此关闭，其他功能与UI能力欠账保留。详见[交付记录](<'+(R/'release-notes.md').as_posix()+'>)。规则见map-economy-design.md的建筑总等级/投资股份两步取整。\n')]:put(path,path.read_text('utf-8-sig')+extra)

before=json.loads((R/'main-before.json').read_text('utf-8'));after=manifest(M)
assert not(set(before)-set(after))
main_changes=[p for p,h in after.items() if before.get(p)!=h];assert len(main_changes)==3 and all(p.startswith('.scratch/') for p in main_changes)
z=W/'releases/nesnd-20261101-button-guards.zip'
with zipfile.ZipFile(z) as pack:
 for p in pack.namelist():assert pack.read(p)==(M/p).read_bytes(),p
dump(R/'integration.json',{'changed_editor':changed,'old_model_sha256':old['model.py'],'new_model_sha256':new['model.py'],'tests':str(proof),'backup':str(backup),'checkpoint':str(checkpoint),'main_changes':main_changes,'gameplay_changes':[],'existing_release_payload_identical':True,'game_launched':False})
copy(E/'model.py',G/'development/workbench/editor/model.py')
for p in main_changes:copy(M/p,G/p)
for name in ['map-economy-design.md','active-work.md']:copy(S/'references'/name,G/'development/nesnd-skill/references'/name)
for name in ['test_editor_split_rounding_20261101.py','integrate_editor_rounding_20261101.py']:copy(W/'tools'/name,G/'development/workbench/tools'/name)
for folder in [R,A]:
 for p in folder.iterdir():
  if p.is_file() and p.suffix in ['.md','.json','.txt','.diff'] and p.name!='main-before.json':copy(p,G/'development/workbench/reports'/folder.name/p.name)
subprocess.run(['git','add','--all'],cwd=G,check=True)
cmd=['git','-c','core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol','diff','--cached','--check','--','.',':(exclude)**/*.diff']
check=subprocess.run(cmd,cwd=G,capture_output=True,text=True,encoding='utf-8');dump(R/'git-whitespace-check.json',{'exit_code':check.returncode,'output':check.stdout+check.stderr});assert check.returncode==0,'See git-whitespace-check.json'
print(json.dumps({'editor_integrated':changed,'main_gameplay_changes':0,'tests_passed':result['tests_run'],'staged':True},ensure_ascii=False))
