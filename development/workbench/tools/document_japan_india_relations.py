from qin_persia_context import W, M, S, man, sha, read, write, dump, G
from pathlib import Path
import json, subprocess

R = W / 'reports/japan-india-plan-revision-20261102'
B = W / 'backups/pre-change-japan-india-plan-relations-20261102T165000Z/mod'
parent = 'd2a7f302322eef2bb868bb6c6e0625f55b2d55b5'
repo = W / 'projects/nesnd-repository'
before = man(B)
assert man(M) == before
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip() == parent
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()

source_checks, updated_plans = [], []
for f in R.glob('*sources.json'):
    sources = json.loads(read(f))['sources']
    entries = sources if isinstance(sources, list) else [dict(v, path=k) for k,v in sources.items()]
    for e in entries:
        p = Path(e['path'])
        current = sha(p)
        rec = {'manifest':f.name,'path':str(p),'read_sha256':e['sha256'],'current_sha256':current}
        if current != e['sha256']:
            assert p in [W/'plans/two-empires/20261102-japan-development-design.md',W/'plans/two-empires/20261102-india-development-design.md'], str(p)
            updated_plans.append(rec)
        else:
            source_checks.append(rec)

write(R/'review-resolution.md', '''# 修订审查处理

2026-11-02；审查对象为两份方案和共同生命周期，未执行游戏代码。

|研究审查|处理|
|---|---|
|法国：旧王朝标记可能盖过可靠现任身份|印度第十二节改为现行法律、可靠唯一当朝证据优先；摄政与社会君主制另判，旧旗标不改写当前王朝|
|印度：筹备成熟即完成会提前清掉发难数据|第十/十三节明确成熟仍进行，战争案件接收身份后才结束联络子项|
|印度：永久无目标不能无限暂停|第十三节区分临时不足、目标已自主、全转第三国与USM灭亡；部分转属保留剩余合法目标|
|印度：整合状态不是殖民关系的替代条件|第十节明确USM部分已整合印度州仍可属于设计目标|
|日本：旧宗主收费和商业条约不应一起清掉|共同L12和日本第十节区分贡赋、项目费用与真实条约；变政检查存续，非自动解约|
|日本：无朝鲜领土仍可能存在外交议题|拆治理与交涉入口；失地只关治理子项|
|日本：避免扩大修改已有战争链|实施顺序改为对齐JIM、复核既有战争接口，保留已确定崩溃/恢复|
|日本：旧JAP统治者林迁移并非普通军官转国|保存实例、合法接任、JIM天皇/摄政承载与部分迁移状态；不复活/复制/抢回人物|
|共同：建国后博弈失败造成部分执行|补L23及限次重试、精确返还/第三方变动收尾；未证接口不交付该分支|

来源报告保留研究时SHA；父代理并行修改的两份计划单列为预期差异，游戏/MOD/旧资料来源必须不变。24项是未来实现验收场景，不能称为24项已通过的游戏测试。
''')
write(R/'release-notes.md', '''# 日本修订3、印度修订2与共同生命周期

本轮落实五项方案修改意见，仅文档与任务入口；未改玩法、未启动游戏。

- 印度：新增逐地区联络/筹备/策动南部USM起义链。进入条件为摆脱殖民宗属或具备足够能力；地区按钮、USM回应、实际战争及战后地方自主闭环，起义不自动归赞助者。
- 土邦：审计范围43个有组织本地国家中42个无开局宗属声明，TRA为USM傀儡；另4个decentralized排除普通模板。独立国守土/结盟，属国自治/独立，各国自己的选择纳入MUG/FRA/USM博弈。
- 法国：法律优先、当朝身份其次；波拿巴/奥尔良/波旁、共和及其他政府分别影响政策议题与AI权重。原报价、待答复请求、已签条约和摄政分别处理。
- 日本：宗属、明吴政治承诺、市场/条约、实际战争分开；USM明/吴仍可能同TAG，CNE也有政权继承。影响供给、建设、独立统一、朝鲜交涉和团结，不抹去已建产业与人口文化。
- 共用：24类异常场景，入口、暂停、成功、失败、失效、阶段交接、后继、对象迁移及清理责任写明。建国但博弈失败也纳入；无游戏验收声明。

主方案：WORK/plans/two-empires/20261102-india-development-design.md（修订2）、20261102-japan-development-design.md（第十节修订3）。共同执行契约：20261102-japan-india-lifecycle.md。

三份有源码引用的研究、来源SHA和各自修订审查保存在本目录；处理记录为review-resolution.md。数值和新接口尚待实施时核准，当前原有游戏机制保持。日本/印度原先研究与历史版本均保留。
''')

issue = M/'.scratch/debug-release/issues/20-japan-india-relations-plan.md'
assert not issue.exists()
write(issue, '''# 日本、印度方案：宗属关系与完整结算

Record: decision
Type: research
Status: resolved
Assignee: root
Blocked by: none

## Question

将南印度起义、印度土邦自主、法国政体政策、日本宗属影响和各种失败/失效条件纳入两份开发方案。

## Answer

两份方案已修订，共同生命周期列24类未来验收场景。三项原始源码研究与独立复核已完成，发现的设计缺口已回填。详见[交付说明](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-india-plan-revision-20261102/release-notes.md>)。

resolved仅指研究/方案修改完成；没有实现新日志、人口转换或战争，没有启动游戏。
''')
def append(p, text):
    write(p, read(p).rstrip()+'\n\n'+text.strip()+'\n')
append(M/'.scratch/debug-release/map.md', '''## 最新：日本与印度关系/结算方案（2026-11-02）

[20 关系与生命周期](issues/20-japan-india-relations-plan.md)：印度逐地区起义、土邦自己的自主议程、法国政体政策、日本宗属/明吴承诺和24类异常出口已纳入计划，原始来源与复核已保存。仅文档修改，尚未实施新玩法。''')
append(M/'.scratch/india-development/map.md', '''## 修订2：地区起义、土邦与法国

主方案第十至十三节纳入USM南印度策动、土邦独立/属国分支、法国内政分类与双向选择。共同生命周期覆盖24类异常；来源与复核见[本轮报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-india-plan-revision-20261102/release-notes.md>)。下一批实施仍需先处理基线和共同请求/收尾，尚未写入玩法。''')
append(M/'.scratch/japan-development/map.md', '''## 修订3：宗主与阶段交接

主方案第十节把宗属、明吴立场、条约/市场、实际战争分开，联动建设、统一自主、团结和朝鲜。旧JAP林统治者迁JIM需合法接任与精确人物登记；同市场供给需核接口，不能强制不合法商品条约。共同24类异常场景和源码复核见[本轮报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-india-plan-revision-20261102/release-notes.md>)。仍为方案，既有崩溃/恢复保持。''')
append(W/'plans/two-empires/00-master-plan.md', '''## 2026-11-02 日本/印度关系修订

日本方案第十节修订3、印度第十至十三节修订2及[共同生命周期](20261102-japan-india-lifecycle.md)是最新关系与收尾规格。工作范围仅研究/计划，主MOD玩法不变。证据见WORK/reports/japan-india-plan-revision-20261102/；任务20。''')
append(S/'references/narrative-context.md', '''日本／印度宗属、土邦起义或法国政体分支实施前，读取WORK/plans/two-empires/20261102-japan-development-design.md第十节、20261102-india-development-design.md第十至十三节及20261102-japan-india-lifecycle.md。修订报告在WORK/reports/japan-india-plan-revision-20261102/。它们是设计与源码证据，尚非新玩法；现行政体、当朝身份、现实宗属与承诺分开，不能按显示国名套关系。''')
write(S/'references/active-work.md', '''# 当前交接：日本与印度关系方案修订

Updated: 2026-11-02；基线d2a7f30。[任务20](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/issues/20-japan-india-relations-plan.md>)与[交付说明](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-india-plan-revision-20261102/release-notes.md>)为入口。本轮只改方案/研究/任务文档，游戏未运行。仓库保存记录见同目录delivery-verification.json。

日本第十节修订3：USM明/吴与现实宗属分开，CNE可改朝；供给/条约、独立统一、朝鲜治理/交涉与团结有不同出口。林JIM迁移、三国产业和文化转换仍待实施；旧JAP已任林统治者的存档须单独迁移接任链。

印度修订2：独立或足够强大后逐地区策动；43个有组织本地国家中42个无开局宗属、TRA属USM，另4个decentralized不套普通模板。土邦有自己的守土/自主议程；法国按现行法律及可靠当朝身份分类，旧旗标不能覆盖。补齐筹备→战争交接、永久无目标、部分建国失败和条约收尾。

共用20261102-japan-india-lifecycle.md的24场景是实施验收要求，不是已经通过的游戏测试。原研究与旧方案保留。下一批先处理MUG初始化/人物/军力/公司/BIC绑定和JIM身份接口，再实现阶段与关系，不在开局全开后期JE。西秦上一轮阶段修正保持，当前没有新增玩法合入。
''')
after = man(M)
changed = sorted(rel for rel in after if before.get(rel) != after[rel])
assert len(after) == 671
assert not set(before) - set(after)
assert len(changed) == 4 and all(x.startswith('.scratch/') and x.endswith('.md') for x in changed)
dump(R/'source-and-scope-verification.json', {'baseline':parent,'backup':str(B),'game_version':'1.13.11','build':24799966,
    'unchanged_source_records':source_checks,'expected_revised_plan_records':updated_plans,
    'root_sources':[{'path':str(p),'sha256':sha(p)} for p in [G/'common/journal_entries/journal_entries.md',M/'common/journal_entries/ce_cne_land_draft.txt',M/'common/journal_entries/nesnd_cne_programs.txt',M/'common/journal_entries/nesnd_japan.txt']],
    'main_files':len(after),'main_changes':[{'path':rel,'before':before.get(rel),'after':after[rel]} for rel in changed],
    'gameplay_changed':False,'game_launched':False,'scenario_table':'24 design scenarios; not executed engine tests'})
print(json.dumps({'source_records_unchanged':len(source_checks),'expected_plan_revisions':len(updated_plans),'main_markdown_changes':changed,'gameplay_changed':False}))
