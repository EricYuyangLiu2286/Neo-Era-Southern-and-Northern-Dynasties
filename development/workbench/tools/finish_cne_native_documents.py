from cne_native_context import *
import difflib,re

# Only trailing whitespace in the newly copied native files; preserve ordered AST.
sources=json.loads(read(R/'native-source-hashes.json'))
for rel in sources:
    p=C/rel;s=read(p);clean=re.sub(r'[\t ]+(?=\n|$)','',s)
    assert shape(parse(s))==shape(parse(clean))
    write(p,clean)
builder=W/'tools/build_cne_time_native_ban.py';s=read(builder)
s=s.replace('# Preserve all other native definitions and namespace declarations byte-for-byte.', '# Preserve all other native definitions and namespace declarations in order.')
needle="dump(R/'native-source-hashes.json',sources)"
assert s.count(needle)==1
s=s.replace(needle,"for rel in sources:\n    write(C/rel,re.sub(r'[\\t ]+(?=\\n|$)','',read(C/rel)))\n"+needle)
write(builder,s)
bm=man(B);patch={r:h for r,h in man(C).items() if bm.get(r)!=h}
assert len(patch)==12
dump(R/'patch-files.json',patch)
diff=''
for rel in patch:
    old=B/rel if (B/rel).exists() else G/rel
    diff+=''.join(difflib.unified_diff(read(old).splitlines(True) if old.exists() else [],read(C/rel).splitlines(True),fromfile=str(old),tofile=str(C/rel)))
(R/'gameplay.diff').write_text(diff,'utf-8')
p=R/'native-ban-contract.md';s=read(p)
s=s.replace('weight、max_hull_damage、max_crew_damage、period、intensity 全部为 `{ value=0 }`，modifier为空（显式零值或删除该可选块均保持无修正）','weight、period、intensity 设为 `{ value=0 }`，删除可选的 max_hull_damage、max_crew_damage 和 modifier 块')
s=s.replace('使用[官方按钮文档:19](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/scripted_buttons.md:19>)','采用[当前原版按钮实例:40](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/00_colonial_administration_buttons.txt:40>)；旧Markdown的base写法与当前实例不符')
write(p,s)

# User's DLC assumption is a design boundary, not a command to strip all native gates.
p=R/'italy-research-plan.md';s=read(p)
s=s.replace('本轮唯一新增产物为本文。','本研究分支的新增产物为本文。')
s=s.replace('新内容优先复用本机可用资源，缺DLC场景单列；','按本机完整DLC环境设计并复用已核资源；')
s=s.replace('|人物死亡/被放逐/未满足DLC|以同利益组织或通用角色接议程，不越权复活；缺DLC的资源/人物机制提供已核原生替代或收窄功能|','|人物死亡/被放逐|以同利益组织或通用角色接议程，不越权复活；按当前完整DLC环境核角色入口及唯一性|')
anchor='## 一、结论：主体应是既存的北方共和国及法国体系'
s=s.replace(anchor,'## 设计环境\n\n2026-11-03用户补充：通常不考虑DLC缺失。方案默认当前完整DLC环境，不建立缺DLC的替代人物、简化公司或旁路剧情，也不将缺DLC用例列为交付阻断。资料表中的DLC条件仍保留为源码事实；这不授权批量删除原生has_dlc条件，亦不豁免当前环境的引用、触发和退出检查。\n\n'+anchor)
write(p,s)
p=R/'spec.md';s=read(p);write(p,s+'\n9. 用户新增环境约定：本MOD通常按完整DLC环境设计，不新增无DLC兼容分支；意大利方案据此调整。现有原生门槛不因这一约定批量移除。\n')

for rel in ['references/active-work.md','references/system-design-and-plans.md','references/syntax-and-routing.md']:
    dst=R/'skill-before'/rel
    assert not dst.exists();dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/rel,dst)
p=S/'references/system-design-and-plans.md';s=read(p)
anchor='## 先恢复工作对象'
s=s.replace(anchor,'## DLC环境（2026-11-03用户约定）\n\n本MOD通常按当前完整DLC环境设计，引用本机已核资源和机制；无需另做缺DLC的替代人物、素材或剧情路线，也不将缺DLC兼容用例作为交付阻断。资料中的原生DLC条件如实记录。除非本次功能确有需要并已查证，不批量移除现有has_dlc门槛。完整环境下的引用、触发、关闭及存档边界仍须验证。\n\n'+anchor)
write(p,s)
p=S/'references/syntax-and-routing.md';s=read(p)
s+='''
## 定点停用原版故障链

用户允许从本MOD侧停用已定位的原版故障内容，其他作者MOD只读。先从error.log定位ID和完整入口链，按数据库支持选择覆盖：本项目已证JE和scripted_button可用`REPLACE:ID`，关闭visible/possible等对应trigger；事件REPLACE支持未核实时沿用同路径覆盖，只把目标事件改为hidden惰性壳（trigger always=no、cancellation_trigger always=yes、空immediate），其余定义和namespace保序保留。只关闭UI入口不能替代清除旧队列和effect中的坏引用。

同路径覆盖须记录当前GAME版本/源SHA，并用保序AST比较所有非目标对象；升级时重新对照，避免冻结整文件后漏掉更新。局部坏权重只停该limit，勿关闭仍被本MOD引用的整个意识形态。scripted_button的ai_chance采用当前实例的`value=0`（00_colonial_administration_buttons.txt:40），旧Markdown的`base`不能直接当作有效语法。2026-11-03具体证据：WORK/reports/cne-time-native-ban-20261103/native-ban-contract.md。
'''
write(p,s)
print('Final source formatting, DLC design assumption and source rules recorded; gameplay patch:',len(patch))
