# 帝国人民的信心与地权革命收尾

用户最新规格，2026-11-01。父版本 bbe7ebe；主MOD改动前完整备份 pre-change-cne-confidence-20261101T235300Z。不开游戏，静态工具不冒充引擎。

## 顺序

1. 子日志入口：分开一次性数据初始化与可恢复运行标记。开场事件先设v3，月度孤儿清理可清running，旧init因v3存在不修复，三个子日志遂不可达。源码守卫重放已得到RED。父JE实际存在时补齐三个项目和信心JE；terminal_pending/完成后不复活，不清零旧进度。
2. 信心：初始1000；每年固定-50，处于战争额外-50，激进派严格大于15%额外-40；知识分子、小市民、工会、实业家每个在政府+10。每个运行项目每年额外-10；土地、城市各算一个，每个正在整顿营产的州各算一个。采用年度消耗，非每月扣10；暂停停止持续消耗。破产惩罚出现时一次-500，惩罚存续不重复扣；离开惩罚后再破产可再扣。保留当前值，不因重载/重建JE补满。
3. 父JE：信心<=0、失去君主制、实际爆发引擎revolution/secession、政变成功或旧极端危机均走失败清理。普通脚本共和派战争不使用dp_revolution/dp_secession，所以500起义本身不立即令土改失败。排除同帧成功。
4. 500阈值共和派起义（一次）：三组等权，仅转移CNE实际拥有的州。组A晋中、晋北、陕北、漠南；组B辽东、吉林；组C山东、河间、燕京。新NRP（原版/主MOD无此tag）。如所有组均无CNE领土，保持待触发，不能抢外国领土。跳过500直接到0仍只触发一次起义，然后父JE失败。
5. 共和派共和国、有限初始陆军、无新增海军；双边吞并诉求的专用外交博弈。先确保博弈存在再开放和平失败判定。重建大汉共和邦JE：战争期间占领CNE至少80%州（只计NRP控制，不算其他敌人的占领）→吞并CNE→change_tag CNE→共和国与新名称；CNE被吞并后的通常战胜路线同样变身。停战且CNE仍存→共和派JE失败，由CNE吞并。吞并后领取尚未由CNE或其附属拥有的湖南、湖北、四川州之声索。战争结算可独立于改革终止继续。
6. 文案：主状态列出“土地商品化”“国家城市化”“结束营产制度”，使用用户指定“在牧皇的伟大构想下，帝国提出了以下三项革命目标……”语意。信心正文用大革命、共和国愿望、流亡者与开蒙运动叙事；数值规则放状态/条件。

## 原版依据

- GAME/common/journal_entries/journal_entries.md：自动激活需shown+possible；add_journal_entry显式添加跳过它们；country scope、invalid、脉冲。入口缺陷不是“所有JE都必须显式添加”，而是自锁标记；显式补齐同时提供旧档迁移。
- GAME/events/american_civil_war/acw_je_events.txt:125起：战争JE显式添加，目标country持久绑定；00_acw_entries.txt:90战胜后处理。美国起义依赖原生革命系统，本次按用户区分改用独立tag+普通定制战争，不复制原生革命标志。
- GAME/events/soi_events/00_ep1_kazakh_events.txt:65起：create_country/origin/state→法律/IG→create_military_formation（5+5陆军）→claim。本次仅创建有限陆军，不改变原有CNE历史OOB。
- GAME/common/history/diplomatic_plays/00_carlist_war.txt：war=yes、annex_as_civil_war=yes；GAME/events/british_raj_events.txt:276：反向annex_country诉求；00_sepoy_mutiny_scripted_effects.txt：已存在博弈检查→创建→检查并设置诉求。
- GAME/common/on_actions/00_code_on_actions.txt:5156/5523原生革命/分离开始，root原国家，target起义国；dp_revolution/dp_secession实际战争判定另作旧档补检。
- GAME/common/journal_entries/00_abolish_monarchy.txt使用country_has_monarchy_law（包括变体）。源MOD3702225772/ce_cne_land_draft.txt旧版有civil_war_progress>=.90失效，最新请求改为真正爆发后失败，不提前在筹备期终止。

## 验证

需要源码入口RED/GREEN、年度公式边界、破产一次性、500一次性、0失败、所有终局清理、NRP不继承运行/人物debuff、三组仅CNE州、双边吞并及停战不遗留、胜者改tag/声索、Tiger差分、MCP实际查询、平行Standards/Spec审查。发布前快照并三方合入；主包排除工具和QA。实机交给用户。


## 2026-11-02追加要求与最终适配

- 进度条按法国实例采用原生monthly/yearly明细。国家变量保留为存档/事件状态；同一JE脉冲按同一脚本值结算一次后绝对同步。信心年度结算从父JE移到信心JE，以遵守原生同JE执行次序。信心原生goal_add_value不是总上限；改用1000上限的scriptedbar。
- 删除玩家文本中的子项目、原规则、继续决定等开发口吻，地方失序名称统一；发布前逐句检查写入NESND技能硬约束。旧“内阁与失序±0.25”提示在父版本没有对应effect，已撤去该假提示，保留既有七项实际月度失序来源，未增添那段虚构计算。
- 开始按钮已有州存在检查，暂停按钮缺失，22州一并补齐。父JE有效时，on_state_owner_change/on_state_created清理失去的州，次日隐藏事件撤销其对应国家/人物惩罚；每周补查，保留其他州。部分割地只清外方state，保留CNE剩余部分的政策。延迟事件再次检查父JE有效，终局不重新施加效果。
- 恢复源MOD num_states<4 的invalid条件，并阻止不足4州时成功或继续推进。
- 独立审查修正NRP军队使用ROOT=CNE首都的错误，保存NRP scope供部队使用；缺国家/变量与同步预览增加分支守卫。random_list使用本机trigger权重条件，非旧式factor。
- 1024年度组合、128月度失序组合校验共享公式，259旧子日志回归；MCP布尔序列化为True，不是源码yes，查询断言按真实返回类型修正。全部属于外部源码证据。


最终审查补充：州回调ROOT为state，内战/博弈谓词改用明确国家对象；NRP普通战争关闭annex_as_civil_war，脚本采用annex_with_incorporation，来源GAME/events/canada_australia_events.txt:66与engine effects.log。新失败原因使用对应叙事通知，旧极端危机的选项不删。所有源码输出以最终候选及main-merge记录为准。

起义地区可用性还要求帝国保有组外领土，避免一次分出全部余州、尚未开战便因CNE不存在自动获得共和国胜利；无可用组时保留未起义状态，不抢外国州。
