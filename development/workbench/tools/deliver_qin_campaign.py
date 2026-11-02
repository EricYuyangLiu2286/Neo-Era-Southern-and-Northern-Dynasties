from qin_persia_context import *
import subprocess,zipfile
from datetime import datetime,timezone

repo=W/'projects/nesnd-repository';before=man(B);after=man(C)
parent='c0e11fe9812fc6a27d47bfefcd668679b9055c38'
candidate_backup=W/'backups/candidate-qin-persia-campaign-final-20261102T045423Z/mod'
premerge=W/'backups/pre-change-qin-persia-premerge-20261102T045443Z/mod'
assert man(M)==before==man(premerge),'Main changed since baseline; three-way reconciliation required'
assert man(candidate_backup)==after
assert subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()==b''
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip()==parent
assert subprocess.check_output(['git','branch','--show-current'],cwd=repo).strip()==b'main'
checks=json.loads(read(R/'checks.json'));assert checks['status']=='STATIC_PASS'
assert not json.loads(read(R/'tiger-delta.json'))['added']
assert json.loads(read(R/'mcp-queries.json'))['status']=='PASS'
assert not set(before)-set(after)
changes=sorted(r for r in after if before.get(r)!=after[r])
assert len(changes)==53
for rel in changes:
    q=repo/rel
    if rel in before:assert q.exists() and sha(q)==before[rel],('Git conflict',rel)
    else:assert not q.exists(),('Git add conflict',rel)

# Earlier review bound the gameplay snapshot. Since then only the documented
# landowner wording changed; preserve a verifiable final manifest and narrow delta.
review=json.loads(read(R/'standards-review-final-manifest.json'))
for row in review['changed_files']:
    if row['path'].endswith('.txt'):
        assert sha(C/row['path'])==row['sha256'],('Unreviewed script change',row['path'])
dump(R/'delivery-final-manifest.json',{'baseline_commit':parent,'files':after,
    'changes':[{'file':r,'before':before.get(r),'after':after[r]} for r in changes],
    'post_review_delta':'Two matching localization slots: 军府与军士 -> 军府与地主; new issue and appended task index. Gameplay script bytes unchanged since final review.',
    'checks':len(checks['checks']),'engine_verified':False})

release='''# 西秦与唐衣大食：交付说明

本轮按最新九项规格完成西秦和波斯的12个新日志及配套脚本，交付主MOD并保存私有仓库main。当前状态是 **STATIC_PASS / ENGINE_NOT_RUN**；未启动游戏。实际提交、远端验证及压缩包指纹见同目录 git-delivery.json、package.json；合入逐文件清单见main-merge.json。

## 已实现

|日志|入口及进展|关闭或重入保护|
|---|---|---|
|西部帝国的自救|开局/旧档维护初始化，−50..50，秦王60/40倾向，首王安国|端点29天计时且周度确认；十年时钟持久；胜负与<4州各有终局锁|
|安国之策|实际父日志存在，法律与全国建筑各自判断；月−1|父日志结束即失效，临时议法/裁军修正清理|
|军府之议|实际父日志存在，开局实际营房+25、印度/波斯/俄境条件；月+2|父日志结束即失效；军费按钮、一次性实测基线及AI资金条件|
|帝国的稳定|70开局，经济、主流人口、传承、法律、战争、士兵等原生明细|解体锁；归化不改宗教，复归按地区原版文化/宗教成对选择|
|羌种暴动|团结首次<25才添加，0..100；恢复时下降|主JE唯一结算country数值；子JE镜像同步；100只分国一次|
|恢复故土|秦国存在且未完成；河西、甘肃、西安、陕北自有或附属控制|一次选择军事或民政奖励；两个选项均给大陆和实际东北亚地区宣称|
|伊犁的朝议|皇权/士人/军队三条；单一赞助与科技门槛改法按钮|普选、委员会共和或<5州永久封存，赞助失去资格自动清除|
|唐衣之下|波斯存在，官僚/教育/大学建设|常驻；条件失去清修正，身份不符失效|
|波斯的市镇|波斯存在，棉田/织造/铁路建设|常驻；短修正刷新不叠加，身份不符失效|
|近西帝国的未来|一次选路，AI75%求援/25%秘密运动，每月+2|100完成仅结算一次；不依赖自身仍在活动日志列表|
|重启远西战争|求援路线完成后显式添加，兼有自动入口|常驻西向宣称；一次每月；第三国宗属不强行夺走|
|近西战争重启|秘密路线完成后显式添加，兼有自动入口|常驻东向宣称，与西向互斥；同一月不能反复索取|

政治失败可引发普通战争；文化崩溃恢复中亚国家，并形成共同反秦战争。新国兵力有限、无新增海军；现存TAG不重建，不改现存国家身份，不夺第三国领土。秦国保留伊犁、准噶尔、西益的现有土地；后期新征服地有联邦接收分支。波斯秘密运动由秦团结公式统一扣1/月，避免两端重复扣除。

## 验证与保留

- 5,344项源码检查、720组有界算术样本、8项真实MCP源码协议查询通过。12项生命周期矩阵、按钮引用/有效scope/一次性锁及两个回调顺序均有记录。
- 全MOD75个JE入口扫描未发现正向依赖自身已存在的激活死锁；10个既有停用条目保持。该扫描不是完整引擎逻辑模拟。
- Tiger差分新增0；基线仍有6 error、966 warning、2 tips，不能表述为全MOD零诊断。工具1.19的规则目标1.13.5，本机源码1.13.11/build24799966，接口另以本机原版与导出script_docs交叉核查。
- Matt Pocock两轴审查分别完成，最终无剩余可行动问题；因代理名额限制复用既有代理，研究与审查均为只读。审查后仅修正一句按钮文案的代价集团名称，并加交接，玩法脚本未变。最终新增205条文本逐项对读作者原始replace；英文槽使用中文回退。
- 51个玩法/本地化文件＋2个任务文档变更，零删除；两个country history只追加初始化。现有地图、人口、建筑、人物、肖像、日本机制和用户配置逐字保留。工具、QA、文档不进入游戏压缩包。

## 明确边界

原生专制和技官制属于同一法律组，因此皇权改法采用君主制＋技官制；比例代表制是带显式投票参数与原生启用钩子的census_voting变体。生活水平造成的额外15%效忠/10%激进变化为州×职业月度采样，参考原版基础系数、农民及高生活水平折减，不能精确重现月内每次涨跌。

地区复归有677个原版地区、3001个文化/宗教配对；原始36个秦地区174配对保留。这是地区身份参考，不是当前人口真实祖源。三遍人口转换、动态国家创建、战争联盟、日志同日回调及存读档仍无本轮引擎证据。

新开局读取追加入口；旧档在首次月度维护补齐未初始化日志，已有变量、结束标志和基线不重置。原始世界历史数据不迁移。不要重跑一次性构建脚本覆盖手工修订。南朝概率/密使待办仍按原任务图保留，本次未扩展到该范围。

## 证据入口

实施规格：WORK/plans/two-empires/20261102-qin-persia-implementation.md。研究：native-political-contracts.md、native-identity-breakup.md、native-persia-canon.md。审查：standards-review-final.md、spec-review-final.md。外部结果：checks.json、arithmetic-cases.json、mcp-queries.json、tiger-delta.json。文案：writing-comparison.md、writing-items.json。备份、差异与远端归档：main-merge.json、delivery-final-manifest.json、git-delivery.json。
'''
write(R/'release-notes.md',release)

master=W/'plans/two-empires/00-master-plan.md'
old=R/'documentation-before/00-master-plan.md'
if not old.exists():shutil.copy2(master,old)
write(master,read(master).rstrip()+'''\n\n## 西秦与唐衣大食实施（2026-11-02）

新规格与完整状态见 `20261102-qin-persia-implementation.md`、WORK/reports/qin-persia-20261102/release-notes.md及主MOD任务16。12个JE及事件/按钮/文化/战争闭包已完成外部检查；ENGINE_NOT_RUN。旧国家体验矩阵保留作总体计划，不将本次范围外南朝新概率/密使标作完成。
''')

def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
for rel in changes:cp(C/rel,M/rel);cp(C/rel,repo/rel)
assert man(M)==after
dump(R/'main-merge.json',{'candidate':str(C),'main':str(M),'parent_commit':parent,
    'changed':[{'file':r,'before':before.get(r),'after':after[r]} for r in changes],
    'deletions':[],'conflicts':[],'main_files_equal_candidate':len(after),
    'premerge_backup':str(premerge),'candidate_backup':str(candidate_backup),
    'engine_verified':False,'game_launched':False})
archive=W/'releases/nesnd-20261102-qin-persia-campaign.zip';assert not archive.exists();excluded=[]
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for rel in sorted(after):
        if rel.startswith(('docs/','.scratch/','development/','tools/')) or rel.endswith(('.md','.bak','.py','.pyc')):excluded.append(rel);continue
        assert not any(x in rel for x in ['nesnd_qa','nesnd_f2_qa','nesnd_batch_probe','nesnd_sequence_qa'])
        z.write(M/rel,rel)
with zipfile.ZipFile(archive) as z:
    for rel in z.namelist():assert z.read(rel)==(M/rel).read_bytes()
dump(R/'package.json',{'path':str(archive),'sha256':sha(archive),'excluded':excluded,'files':len(after)-len(excluded),'QA_included':False,'engine_verified':False})

support={}
for rel in ['SKILL.md','references/active-work.md','references/content-development.md','references/journal-text-contract.md','references/numeric-scale-contract.md','references/syntax-and-routing.md']:
    support['nesnd-skill/'+rel]=S/rel
for p in (S.parent/'nesnd-player-writing').rglob('*'):
    if p.is_file():support['nesnd-player-writing/'+p.relative_to(S.parent/'nesnd-player-writing').as_posix()]=p
for p in R.iterdir():
    if p.is_file() and p.suffix in {'.md','.json','.diff','.py'} and p.name not in {'baseline.json','tiger-first.json','tiger-second.json','tiger-third.json','tiger-heritage.json','tiger-final.json'}:
        support['workbench/reports/'+R.name+'/'+p.name]=p
for p in (R/'documentation-before').rglob('*'):
    if p.is_file():support['workbench/reports/'+R.name+'/documentation-before/'+p.relative_to(R/'documentation-before').as_posix()]=p
for p in (W/'tools').glob('*.py'):
    if 'qin' in p.name or 'persia' in p.name or p.name=='audit_journal_entry_gates.py':support['workbench/tools/'+p.name]=p
for name in ['00-master-plan.md','20261102-western-qin-design.md','20261102-qin-persia-implementation.md']:
    support['workbench/plans/two-empires/'+name]=W/'plans/two-empires'/name
for rel,p in support.items():cp(p,repo/'development'/rel)
mf=repo/'development/snapshot-manifest.json';data=json.loads(read(mf));records={x['path']:x for x in data['files']}
for rel,p in support.items():records[rel]={'path':rel,'source':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
data['files']=[records[k] for k in sorted(records)];data['updated_utc']=datetime.now(timezone.utc).isoformat()
data['refresh_scope']='Qin/Persia 12-journal campaign; native source, lifecycle and culture checks; external-only delivery; tool scripts are retained historical construction evidence, not idempotent migrations.'
dump(mf,data)
print(json.dumps({'main_changed_files':len(changes),'main_verified_files':len(after),'package':str(archive),'support_files':len(support),'game_launched':False}))
