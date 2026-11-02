# 法国政策修订复查

2026-11-02；只读审查印度方案第十二至十四节与共用生命周期。未改方案、未改玩法、未开游戏。

**结论：1项需要修正文义的实质问题；其余法国政策／请求闭包未发现阻断设计的问题。**

## P2：旧王朝旗标并存不应覆盖明确的当前王朝

位置：[印度方案第十二节第164行](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-india-development-design.md:164>)。“多个旧标记并存……进入明确的其他君主制分支”会把实际在位王朝已能唯一识别的法国误归为其他君主制，丢掉本次要求的差异化政策。

源码依据：MOD 奥尔良、波旁 JE 各自完成时删除 bonapartist_restoration_var 并写本派标记，但没有在该段清另一复辟标记；这是旧旗并存的可能来源，不能把并存本身当作当前王朝不明。[奥尔良完成](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_french_empire.txt:494>)、[波旁完成](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_french_empire.txt:795>)。原版对在位家族的即时判据是 ruler 上的家族标记；MOD 波旁还须兼容 house_bourbon / house_bourbon_leader，不能只用原版 legitimist_leader。[原版家族谓词](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_victoria_scripted_triggers.txt:67>)、[MOD波旁选王](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/ce_french_empire_journal_effects.txt:1169>)。

建议将该句限定为：**当前王朝有可靠且唯一的身份依据时，以它为准，旧标记仅作辅助；只有当当前身份依据缺失或冲突时，才进入其他／未决君主分支。** 摄政应按已登记王朝及经验证的继承关系识别，不能用摄政者个人家族代替。这里记录的是源码兼容风险，没有声称实机已经出现三标记并存。

## 已通过的设计边界

- 第166行明确将各政体印度政策标作提案；共和不等于无条件反殖民，硬条件与 AI 权重分离，没有把研究推论伪装成现有脚本。
- 第178行“原报价仍有效时采用当前政府AI权重”是可行的设计选择。它与研究报告较保守的“一改政策就撤回”属于不同可接受方案，不是源码错误。共用流程第37行的请求身份、执行重核与 L07/L08 覆盖了旧答复误兑现／误清新锁；实施时须将原报价内容及政策资格纳入这个同一判据，保持金额／对象／项目不变。
- 已签条约独立于 JE 和政策重算，binding_period 不是到期；第178行与共用流程第36、39行保持一致，没有授权换政府时删条约。
- 神权与委员会政府设默认分支、FRA灭亡／从属变化、州转属、国家形成、旧档及重复领奖均有收尾场景。具体分类落地仍应沿研究报告使用原版 country_has_monarchy_law 覆盖社会君主制，并落实摄政测试；这是实施核验项，不另列设计阻断。

复查输入 SHA-256：

- 印度方案：`a0cc7d2acbd37f535ecb7a907bcc93676e2fc5add1d92ff468b2a09f492a5a15`
- 共用生命周期：`ec2055acb57ec57369d7c820001753f6a90c1700b190721c7b9cb4835725582f`

来源细节与44项原始源码SHA见[法国政策研究](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-india-plan-revision-20261102/france-regime-policy.md>)及[来源清单](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-india-plan-revision-20261102/france-regime-policy-sources.json>). 本次没有进行新的引擎验证。
