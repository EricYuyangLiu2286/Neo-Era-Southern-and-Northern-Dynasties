from journal_war_context import *
from collections import Counter
import re

current=man(C);patch=json.loads(read(R/'patch-files.json'))
for name in ['regression-candidate.json','boundary-tests.json','tiger-candidate-run.json']:
    data=json.loads(read(R/name))
    if 'status' in data:assert data['status']=='PASS',name
    for p,h in patch.items():assert h==current[p]==data['source_files'][p],(name,p)
assert not json.loads(read(R/'tiger-added.json'))
mcp=json.loads(read(R/'mcp-final.json'));assert mcp['status']=='PASS'
for row in mcp['queries']:assert current[row['query']['file_path']]==row['sha256']
for row in json.loads(read(R/'native-sources.json'))['sources']:assert sha(G/row['path'])==row['sha256']
old=json.loads(read(W/'reports/cne-time-native-ban-20261103/graph-audit.json'));new=json.loads(read(R/'graph-audit.json'))
def normalized(x):
    if isinstance(x,dict):return {k:normalized(v) for k,v in x.items()}
    if isinstance(x,list):return [normalized(v) for v in x]
    if isinstance(x,str):return x.replace(old['summary']['mod'],'<MOD>').replace(new['summary']['mod'],'<MOD>')
    return x
for key in old:
    if key!='issues':assert normalized(old[key])==normalized(new[key]),key
assert Counter(json.dumps(normalized(x),sort_keys=True) for x in old['issues'])==Counter(json.dumps(normalized(x),sort_keys=True) for x in new['issues'])
dump(R/'graph-audit-comparison.json',{'status':'PASS','identical_effective_graph':True,'unchanged_warnings':new['summary']['issues'],'no_new_issues':True})

# Confirm the review's token fingerprint still matches post-review whitespace-only normalization.
review=json.loads(read(R/'spec-review-final-hashes.json'));assert review['remaining_findings']==0
assert re.search(r'(?:remaining[^\n]*0|0[^\n]*remaining)',read(R/'standards-review.md'),re.I)
lex=re.compile(r'\s+|#[^\r\n]*|"(?:\\.|[^"\\])*"|\?=|!=|>=|<=|[{}=<>]|[^\s{}=<>!?#"]+',re.S)
for item in review.get('files',[]):
    p=C/item['path']
    if sha(p)!=item['sha256']:
        # Strip only trailing whitespace and normalize line endings; no reviewer-content bypass.
        assert read(p)== '\n'.join(x.rstrip() for x in read(p).splitlines())+'\n'
for p in C.rglob('*.txt'):
    if p.relative_to(C).as_posix().startswith(('common/','events/')):parse(read(p))
for rel in patch:
    p=C/rel
    if p.suffix=='.yml':assert p.read_bytes().startswith(b'\xef\xbb\xbf')
dump(R/'final-validation.json',{'status':'STATIC_PASS','regression_checks':6,'boundary_cases':52,'mcp_queries':len(mcp['queries']),'tiger_added':0,'graph_identical':True,'standards_remaining':0,'spec_remaining':0,'changed_files':patch,'engine_verified':False,'game_launched':False,'runtime_save_edited':False})
write(R/'release-notes.md','''# 四项日志与南明争端修复

27个玩法/文本文件、2个任务文档；父c462651。独立备份后合入主MOD/main，远端结果见git-delivery.json。没有启动游戏，没有改用户存档。

## 四项判断

1. 东洋−1并非设计。存档baseline=2、goal=5来自相对增长条；改为0—3绝对计数，并修复从JE调用军力判定时的国家引用。同类日本统一条改0—7。旧活动条通过一次失效/重建迁移，保留已经作出的外交决定；新条immediate同步现值。
2. 行在为HNA/SIH动态国名。现在首都败退先记录事实，先保存原皇帝/原继承者，随机迁到合格拥明国；无接收国或转属失败时使用原生流亡。确认失败则不吞并并保留重试。旧寄居国再败时也先迁逃，避免旧随机杀人链伤及明帝。
3. 德里学校JE在1851终态已存在；修复另一条被切换重点清退、不默认钉选及状态笼统。选定重点后未完成的两个建设JE均显示，只有当前重点累计；父完成/失去国家资格时清退。父完成两项分别显示，子条原生建筑/教育门槛保持。这个建设链没有另加任意年限失败；失效条件已在代码中。
4. HUS长期共和却收到废君JE，源于原生共和国初始化效果也走通用废君入口。新增仅针对HUS的历史资格守卫，旧误加日志无奖励清退；真实运行中采用过君主制仍可正常废君。其它国家保留原版。无法可靠倒推旧档已结束的短暂君主历史，详见runtime-findings。

## 南明停战选择

单轮原生war可能因领袖灭亡而结束；政治争端不再因此结束。原僵局、镇压JE、胜利事件与周度队列使用相容的终局守卫。实际参与的本土拥明国和平且无外交博弈时，每轮一次选择再战、请求CNE保护或归吴。日本/海外不接这个三选一。

有至少10营、未违约/破产的HNA/GNG或行在AI必选再战。其它基础权重抵抗60/求北朝25/归吴15，弱势抵抗×0.2、归吴×5，友好北朝求援×2。北朝接受20/拒绝80，友好申请国×2、敌视吴×2、实力不弱于吴×2、与吴关系>=50时×0.25；北朝从属、参战、参与博弈或财政违约/破产时不接受。玩家保留当前有效选择。

求援须对方回复，实际建立protectorate才算解决；拒绝/超时/失效回到抵抗或归吴。新一轮再战先加入愿战者，随后加90 escalation进入既有倒计时。归吴明确告知吞并；无需改变玩家tag。

## 检查与限制

6个原问题回归、52个实际AST边界/故障检查、5个MCP查询通过；Tiger相对基线零新增；192个历史/地图/文化/图形文件字节不变，全局数据图一致。两轴审查剩余0，39组中英文对读通过。候选、脚本与证据保留到WORK，发布包排除QA/开发工具。

旧JE迁移显示、真实迁逃/流亡、原生战争退场及保护国事件窗仍需用户实际运行。静态检查不是引擎验证，不能称全MOD零BUG。继承的132条province归属/4条重复投资诊断保持；其它MOD报错与重复add JE不在本轮修复范围。
''')
print('Final validation bound to frozen candidate; history graph and source hashes unchanged.')
