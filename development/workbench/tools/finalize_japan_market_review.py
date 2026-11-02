from japan_dev_context import *
from collections import Counter

plan=W/'plans/two-empires/20261102-japan-development-design.md'
s=read(plan)
s=s.replace('建立征募/训练和后勤、军需采购、行政控制的议程','建立征募、训练、军工生产与行政控制的议程')
s=s.replace('建设可衔接南朝市场、海防与采购','建设衔接南朝市场的产业与海防')
s=s.replace('军工船业可提供实际供给合作，获得对应报偿并承担明确负担','军工船业的产出与投入需求加入实际所属市场')
s=s.replace('保留已建产业，可自愿续订采购和贸易','保留已建产业，由原生跨市场贸易承接供需')
s=s.replace('终止不兼容的未来资助/采购任务','终止不兼容的待答资助请求')
start=s.index('### 3. 实际供给与援助接口')
end=s.index('### 4. 关系对团结与人物的作用',start)
s=s[:start]+'''### 3. 共同市场、跨市场贸易与财政援助

同一市场内，成员国建筑和人口的买卖订单由原生市场汇合；日本的矿业、军工、船业和消费品产业因此参与整个市场的供需。产业日志检查实际建筑、就业、生产方式和价格，完成不需要宗主批准或支付采购款。实际市场归属与宗属分别查询。

独立、换宗主或退出共同市场时保留产业及完成记录，由原生市场、接入与跨市场贸易决定新的供需和价格。财政资助单独处理国库资金与双方答复，不代表购买或储存商品。现有跨市场条约只在权限成立时使用，原生 good / goods 参数按各自接口核验。

旧采购、预付款、折价、履约与合同日志提案已被作者明确撤回；旧文保存在 plan-before-market-correction.md，仅供溯源，不是实施要求。

'''+s[end:]
write(plan,s)

def signature(d):
    return (d['severity'],d['key'],d['message'],tuple((x['path'],(x.get('line') or '').strip()) for x in d.get('locations',[])))
b=json.loads(read(W/'reports/canon-prose-20261102/tiger-candidate.json'))
a=json.loads(read(R/'tiger-candidate.json'))
bc,ac=Counter(map(signature,b)),Counter(map(signature,a))
added=list((ac-bc).elements());removed=list((bc-ac).elements())
dump(R/'tiger-final-delta.json',{'baseline':len(b),'candidate':len(a),'added':added,'removed':removed,'baseline_commit':'38cf3ea6bacdd5bcc43f3041a39bcde6d96982d9','engine_verified':False,'note':'Inherited diagnostics remain; this is an incremental source comparison, not proof of zero game errors.'})
assert not added,added
check=json.loads(read(R/'external-final-checks.json'))
probe=json.loads(read(R/'mcp-final-queries.json'))
assert check['status']=='STATIC_PASS'
assert probe['status']=='PASS'
assert man(C)==check['files'],'Game source changed after checks.'

write(R/'review-aggregate.md','''# 日本候选最终外部复核

当前依据为作者最新共同市场纠正。采购功能曾进入独立候选，已完整撤回，未进入主 MOD；七个模块文件和所有 kind 8 引用删除，旧草稿单独留档。不得从旧方案恢复。

- 外部检查：866 项通过；25 个新日志；196 个日本本地化键。
- 实际 MCP 查询：10 项通过。
- Tiger：553 条继承诊断，新增 0；遗留工具规则差异和原有诊断不伪称已消灭。
- Spec 与 Standards：最新市场修正各剩余 0 项，报告及源码 SHA 分别见 spec-final.md、standards-final.md。
- 官方网络研究见 market-web-sources.md；本机 1.13.11 链条见 market-model-native-review.md；既有供给、财政、舰船与条约复核见 market-model-existing-systems.md。

游戏尚未启动。上述结论仅为 STATIC_PASS，不证明所有分支已在引擎中运行。
''')
print(json.dumps({'tiger_baseline':len(b),'tiger_candidate':len(a),'new_diagnostics':len(added),'checks':len(check['checks']),'candidate_game_source_unchanged':True}))
