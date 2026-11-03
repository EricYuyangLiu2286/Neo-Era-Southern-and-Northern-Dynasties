from qin_persia_context import W,M,S,read,write,sha,dump
from collections import Counter
import json
R=W/'reports/qe1-variable-20261103';C=W/'exports/qe1-variable-20261103-a'
def sig(x):return (x['severity'],x['key'],x['message'],tuple((a['path'],(a.get('line') or '').strip()) for a in x.get('locations',[])))
b=json.loads(read(W/'reports/japan-development-20261102/tiger-candidate.json'));a=json.loads(read(R/'tiger-candidate.json'))
added=list((Counter(map(sig,a))-Counter(map(sig,b))).elements())
dump(R/'tiger-delta.json',{'baseline':len(b),'candidate':len(a),'added':added,'engine_verified':False})
assert not added,added

write(R/'diagnosis.md','''# QE1 数值变量缺失报错

读取 20261102T234900Z 隔离运行的 error.log 与 error.1.log，保存原日志；主用户目录旧 error.log 时间较早，没有冒用为本次运行。两份保留日志共4827条脚本错误，其中4824条对应本次修复：unity三处读取各产生524组错误，war_months两处读取合计36组；其余3条是原版秘鲁/玻利维亚重复加入日志参与国，另列但不混入本次变量修复。

## 原因与证据

按顺序检查了：未激活日志的求值、初始化遗漏/旧档缺值、变量所属scope不符。

实际1836.3.1 autosave中，唯一存活QE1有campaign_v1，unity为70.50745，war_months/uprising为0；只有QE1团结日志active=yes。与此同时保存了526个团结/暴动JE实例，其余525个未激活，其中包括英、俄、法。结合重复报错和实际源码，问题是进度条script_value直接访问不具备西秦变量的上下文。JE的possible/is_shown_when_inactive不能充当数值读取保护；给所有国家初始化西秦变量会掩盖错误并污染状态。

未改初始化、数值、历史、人口、文化转换或进度推进顺序。四个script_value在独立has_variable分支内执行原计算，缺值时只返回0；不会set_variable为0。两条状态文字及暴动完成条件同样用trigger_if/trigger_else保护，缺值明确false。

## 原版链条

1.13.11 / build24799966：05_danubian_federation JE immediate设置count_integrated_cultures；00_victoria_ip3_scripted_effects变更计数；je_values的danubian_federation_remaining_cultures_to_integrate先查has_variable再读取；JE完成条件使用trigger_if。另对照ep2_japan_values的cached_daimyo_loyalty缺值分支。路径/行号/SHA见native-sources.json。进度条文档明确更新先于JE pulse。

## 验证

- check_qe1_variable_guards.py 修前FAIL：5处未保护；修后STATIC_PASS：8次变量读取均有分支保护。
- 46项结构/不变性检查通过：变量存在时原计算AST完全保留，只改变缺值路径；全common/events可解析，游戏内容只改2文件。
- 5项实际MCP结构查询通过。
- Tiger相对已交付版本553→553，新增0；不代表全MOD无遗留诊断。
- 没有启动或操作游戏、没有改存档或冻结运行副本。修后引擎结果待用户运行确认。

来源：runtime-save-evidence.json、error-inventory.json、guards-before/after.json、validation.json、mcp.json。保存的真实存档只读，报告仅存相关字段和SHA。
''')
write(C/'.scratch/debug-release/issues/23-qe1-variable-guards.md','''# 23 西秦进度条变量缺失

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: STATIC_PASS
Evidence: WORK/reports/qe1-variable-20261103/diagnosis.md

## Result

用户本次error.log显示nesnd_qe1_unity和nesnd_qe1_war_months未设置。实际存档西秦已初始化，其他国家的未激活日志数值被求值时缺少读取保护。修复四个script_value和同一日志三处条件；不改已有团结度、战争月份、阈值或奖励。

修前5处未保护读取，修后0；46项外部检查、MCP5和Tiger零新增通过。修改前和最终候选均独立备份。主MOD/Git实际交付见报告main-merge.json/git-delivery.json。

## Runtime boundary

用户已接手游戏。此次只读日志/存档并修代码，没有开游戏。20261102T234900Z冻结运行副本保持原样；下次验证需加载更新后的主MOD。用户旧存档不会被覆盖，现有数值不重置。
''')
p=C/'.scratch/debug-release/map.md'
write(p,read(p)+'''
## 最新：西秦变量报错（2026-11-03）

[23 西秦进度条变量保护](issues/23-qe1-variable-guards.md)根据用户实际error.log及1836.3.1存档修复。四个script_value、两条状态文字与完成条件增加缺值分支；原有数值不变。46检查/MCP5/Tiger零新增，未开游戏；用户接手运行，旧隔离副本不改。
''')
p=S/'references/syntax-and-routing.md';s=read(p)
anchor='4. **延迟回复核整个生命周期。**'
insert='''进度条的数值函数也须独立处理未初始化上下文，不能把JE的possible、is_shown_when_inactive或immediate当作读取保护。2026-11-03真实QE1日志和存档显示：其他国家持有未激活JE，数值函数仍触发缺变量报错。用script_value的has_variable分支返回无变化值；状态文字/完成条件用trigger_if并明确缺值false。不要为消除错误向所有国家写入西秦变量，也不要重置已有进度。回归证据：WORK/reports/qe1-variable-20261103/diagnosis.md。

'''
assert anchor in s;s=s.replace(anchor,insert+anchor);write(p,s)
p=S/'references/active-work.md';s=read(p)
s=s.replace('游戏尚未启动。用户已授权完成更新/测试后仅启动一次，选择任意国家后切观察者并五速运行留待用户；失败/崩溃按当次error.log定向修复。运行后读取 runtime-observation.md，不能把此处旧的“尚未启动”当作新开局授权。正式包排除QA，运行仅使用独立最小观察者按钮，不加载历史夹具。','2026-11-02已启动隔离profile 20261102T234900Z，随后用户明确接手测试，停止AI游戏操作。日本main已交付c1463da。2026-11-03用户要求读取error.log并修QE1变量；已读取实际1836.3.1存档，完成任务23源码修复/外部检查，未再次开游戏。冻结运行副本不改，后续测试加载更新后的主MOD。实际修复交付见WORK/reports/qe1-variable-20261103/main-merge.json与git-delivery.json；没有新的开启或控制游戏要求时不操作游戏。')
s=s.replace('Updated: 2026-11-02。当前任务为主MOD .scratch/debug-release/issues/21-japan-implementation.md；证据 WORK/reports/japan-development-20261102/。','Updated: 2026-11-03。当前任务为主MOD .scratch/debug-release/issues/23-qe1-variable-guards.md；证据 WORK/reports/qe1-variable-20261103/。日本任务21证据在WORK/reports/japan-development-20261102/。')
write(p,s)
print('Tiger delta',len(b),len(a),'new',len(added),'; diagnosis, issue and scope-safety lesson recorded.')
