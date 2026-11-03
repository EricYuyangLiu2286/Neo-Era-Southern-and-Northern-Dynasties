from feedback_context import *
from datetime import datetime,timezone
import subprocess
notes='''# 断点总结与本轮交付

2026-11-03；父提交 f0463ff；候选 persia-journal-ui-20261103-a。STATIC_PASS，未启动游戏，未修改用户存档。合并与远端结果以本目录 main-merge.json、git-delivery.json 为准。

## 已完成源码

- 波斯前途完成条件用简短本地化包住原变量判定；纺织厂 bt 引用改为实际 building_textile_mill。原 error.log 已证明旧复数别名未能解析。保留全国棉花10、纺织10、铁路5三级独立勾叉；奥斯曼大学单建筑配员条件与本设计不同，未照搬。
- 秦、波斯、法国、波兰及外援相关按钮补必要的变量/路线提示；可原生显示的修正、法律和国库效果使用 show_as_tooltip。48个土改启停按钮隐藏执行内部的存在性与生命周期判定，保留实际守卫。
- 明吴战争脚本加入参与者后 add_escalation=90；原版 closing 阈值80。嵌套参战helper从root修为prev；USM灭亡后比较之前先判断存在。已有存档中的战争与参战国不会因新代码自动重写。
- 西秦三权新增真实周度来源明细。原设计每周重算占比，并非恒定月增；预览计算处理低于40时的派系扶持清理，原实际结算保留。80组边界×4旧占比向量作外部算术核对。
- 帝国人民信心负值减半：基础/战争各25，土地商品化/城市化/每州营产各5，激进派20，破产250；执政IG每个+10不变。起义阈值500与失败0不改。截图的每年-140对应改后-70。
- 新增一次暂缓：暂停正在推进的改革，信心+100，六个月不能重新启动；保存已得改革进度。永久“议止”仍是退出改革的另一行动。“尚未结案”改为“地权革命仍在进行”。
- 共和派创建避免重复add_journal_entry，修正领袖意识形态；和平失败要求实际见过战争，未成功建战时允许重新尝试，防外交过程未进入战争便被吞回。既有起义标记不清零。
- 波斯37个逐州宣称按钮仅显示实际相邻的外国州；执行重验归属、邻接、已有宣称、路线和冷却。同一地区分割时选最大有效外国部分，不能随机抽不相邻的其他地区。原一个月代价及外国干预保留。
- 蜀胜利可复明/大汉；襄樊可复明/共和国；淮国以本宗朱氏复明。共和襄樊有士大夫反对及知识分子、小市民吸引力和政治力量各+25%。结算与旧档补入口只认独立反吴胜利方、USM已灭及全南京所有权。
- 旧明天子先保留/寻找具体活人；本地、全球、流亡池、无所属池依次查询，外国在位君主/继承人不夺取。无可用宗室才创建21岁非历史新角色。宁系阔→作→哲→向→亲→衷；淮系仲→简→靖→迪→先→猷。现有人物姓名不改。新生继承人只检查其父系，避免全世界扫描。已知行辈尽头可复用同辈名字池，不杜撰后续字辈。

## 最新用户存档

只读 latest_test_save.v3，SHA 6d1563547bf2ec4368625e23e3aed25b06352fe90d03aa6cd43ee27ef97711ee；1844.7.13.18。
USM已灭；SIH持有南京但被旧statusquo/settled状态阻断战后结算。朱阔彬、朱作煜仍活在HNA（3146、3147），不是已经被代码删除。淮国本宗君主仍在。
CNE信心180、改革71.6；NRP确曾在1841年建立并活动，盛京/辽南在同年5月回到CNE。存档不能独立证明那次消失是正常战败还是旧过早清理；不能声称“从未触发”，也不据此给旧档强制再刷一场起义。

## 外部检查与边界

639项源码/引用/本地化/守卫检查通过；真实stdio MCP3查询通过。Tiger相对父交付553项为551项，零新增诊断。Standards与Spec最终复查均零未解决发现。全局遗留诊断没有被清零或掩盖。
人口、历史领土、建筑数据和资源未改；主MOD用户日本文案另存并保留。没有引擎运行验收，旧战争的参战阵营不自动修复。

## 继续工作：印度

印度实施已获明确授权，下一批独立候选继续，不把研究当实现。原始方案、24项生命周期与20261103 native-implementation-contract.md、yuanshan-tianzhu-lore.md为依据。
顺序：MUG有效历史/旧英国链兼容→分阶段改革与土邦→法国合作→社会共同体→逐州反吴起义→统一后治理及南明设司。
远山在南非，需实际取得当地领土后设立；天竺只划拨USM实有印度部分，保留TRA和第三国。1936人物/军备/疆界不能倒灌1836。市场以真实产销订单共享，禁止军需库存采购机制。所有内容继续外部检查，游戏由用户测试。
'''
write(R/'release-notes.md',notes);write(R/'work-state.md',notes)
issue='''# 24 日志反馈、战后结算与宗室延续

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: STATIC_PASS
Evidence: [详细断点与交付记录](<'''+(R/'release-notes.md').as_posix()+'''>)

## Result

11项反馈及缺失宗室后继已实施。639检查、MCP3、Tiger零新增、双轴复核收口。未启动游戏；旧档结算恢复与无宗室后继未取得引擎验收。合并结果以报告main-merge.json为准。印度已授权，下一候选继续。
'''
write(C/'.scratch/debug-release/issues/24-feedback-restoration.md',issue)
p=C/'.scratch/debug-release/map.md';write(p,read(p)+'\n## 最新：反馈收口与宗室延续（2026-11-03）\n\n[24 日志与战后结算](issues/24-feedback-restoration.md)：波斯条件/逐州相邻宣称、按钮反馈、西秦周度明细、信心减耗与一次暂缓、共和起义实际战争守卫、明吴倒计时、蜀襄淮结局及宗室补生完成外部检查。未开游戏；印度实施进入下一候选。\n')
# Independent skill-file backup before updating scoped references.
for rel in ['references/journal-text-contract.md','references/syntax-and-routing.md','references/active-work.md']:
 p=S/rel;q=R/'skill-before'/rel
 if not q.exists():q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
p=S/'references/journal-text-contract.md';s=read(p);s+='''
## 按钮预览与周期占比：2026-11-03实际反馈

禁止滥用custom_tooltip不等于删除变量效果提示。按钮可见/可用条件不保证effect预览受同样条件约束；执行内的if在预览时可能展开内部缺值，或已设置标记使效果消失。把真实守卫留在hidden_effect，外层用简短custom_tooltip说明不可原生呈现的变量、路线与一次性期限，配show_as_tooltip显示真实modifier/law/treasury；不得重复同一收益。验证实际执行AST及提示两面。

国家变量完成条件没有本地化时，只包装对应单项条件，勿用全局伪造country_var_*翻译或把无关门槛合成一个勾叉。建筑用bt引用时核对实际定义键，别名不保证可作scope：本轮error.log证明building_textile_mills失败，而building_textile_mill正确。先查同类JE/events/decisions完整链条，再决定用全国累计还是单座建筑；两者不能为显示漂亮而互换。

占比条每周重算不是每月固定增量。原生weekly_progress应解释新目标减旧值，并纳入同周期扶持撤销，再由既有单一写入者绝对同步；只读预览不得改变持久变量。依据：原生00_ip4_victoria_progress_bars与本轮QE1三权来源/80组边界报告。

证据：WORK/reports/persia-journal-ui-20261103/release-notes.md、sources.json、button-feedback-other-review.md、qe1-court-progress-research.md。未做引擎验收。
''';write(p,s)
p=S/'references/syntax-and-routing.md';write(p,read(p)+'''
## 宗室延续与无所属角色

需要恢复人物时先查已保存身份，再查本国、every/any_character、流亡池及void，确认存活与owner；exile/void不得先无保护比较owner。移出外国在位ruler/heir须有明确剧情授权，不能将同姓当作身份。只有确定缺少可用活人且作者授权时，create_character创建新角色，不能重用旧历史template当复活。行辈/支系单独记录，淮系不能混宁系；已有姓名不回写，新出生只查自己的父系，不能为每个国家的出生扫描全球。on_created保存新角色后验证其owner，再立为君主；一次结算/创建锁避免重复刷人。当前原版法国、日本及巴西来源见WORK/reports/persia-journal-ui-20261103/ming-successor-generation.md。
''')
p=S/'references/active-work.md';write(p,read(p)+'\n## 当前（2026-11-03）：反馈修复完成外部检查，印度进入实施\n\n主项目任务24与WORK/reports/persia-journal-ui-20261103/release-notes.md为最新断点；候选43个玩法/文本文件，639检查/MCP3/Tiger零新增，未开游戏。主MOD合入与Git结果以main-merge.json/git-delivery.json为准。作者主MOD日本改稿必须保留。下一步按WORK/reports/india-development-20261103/native-implementation-contract.md与yuanshan-tianzhu-lore.md落实印度及两司；研究不等于玩法实现。\n')
print('Records prepared; skill rules updated with source evidence.')
