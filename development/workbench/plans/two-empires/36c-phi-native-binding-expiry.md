# 36c — PHI 原生钱款到期与控制器交接

最新状态：C5已在真实游戏完成未改订现金A的自然到期正例，见下节。用户最新要求停止新增内容，当前只debug与总结；没有据此新增经济、剧情或地图设计。

## C5实际到期结果（1837.5.9.6）

run20261031T224458Z，根从控制器完整的May1档自然走时，USM玩家、PHI AI。实际保存 `大明联邦_1837_05_09_A_expiry_C5.v3`，SHA `1e00d426b424a4a2bc51b982f5fc5c55e9490b4eeab68d6f4ad486c0907dd7bc`。原约33554442已在1837.5.8死亡，withdrawn_countries为USM730；PHI finish_reason1，无native_amendment；active、typed、term、retry marker与USM五个镜像字段清除；正式`.9`/`.15`无剩余任务。PHI周收入槽11、USM周支出槽15均为0，旧8700钱款已停止。

QA独立tracked_treaty仍能读到dead数据库中的旧对象，但`target_in_country_list=0`。**数据库仍有记录不等于合同仍生效**，必须同时读取dead_objects/国家条约列表。实际冻结的effects/events/script_values SHA均与A7一致。

原生日志155条：冷启动153、载旧C4名称的missing-mod提示1、22:49:26无脚本定位的GameStateAccess原生assertion1；none类型错误0。已归档 `evidence/phi-c5-expiry-logs-20261031T225426Z`。这条assertion在既有自然局也出现，缺乏因果证据，既不归咎用户，也不掩饰为无错。验收范围只覆盖这次未改订现金A的到期路径；真实改约、提前撤约、亡国、战争、旧retry命中新serial等负例仍未因此认证。

证据 `evidence/phi-A-expiry-May9-c5-224458.json`、`phi-A-expiry-c5-actual-result.json`，工具 `audit_phi_expiry_boundary.py`、`record_phi_c5_expiry_result.py`。后一工具读取真实原约死亡与双边预算、冻结文件SHA并保存原始日志，不模拟事件执行。后续纯海域debug候选E1逐字节保留C5全部脚本。

### 原生提前退出负例：同日付款停止，控制器待正常复核

同run根重新加载May1，实际打开原生广州宣言、退出并确认；UI展示恶名+5/关系−10，预算约−38.1k→−29.4k，未推进时间。存档 `大明联邦_1837_05_01_A_withdraw_C5.v3` 的原约33554442已在1837.5.1死亡、USM为withdrawn_country；PHI收入槽11和USM支出槽15立即为0。此时模块active/typed及双方镜像仍在，finish_reason0，term剩6，正式`.9`仍排6天。

当前代码没有原生withdraw即时清理回调；收尾由正常PHI月度或正式`.9`复核完成。依据May1队列预测May7的`.9`转入PHI_month首个not-live分支并写reason4，不能承诺单走1天生产控制器就清理。QA变量当时仍为上次采样缓存，应与真实death_date/双边预算区分。数据 `evidence/phi-A-withdraw-May1-c5-224458.json`。

随后根以速度III正常推进，没有再作政策、建设或事件选择；实际暂停于May24并点只读sample，保存 `大明联邦_1837_05_24_A_interrupted_C5.v3`，SHA `c5e1c486c28f54460fe9a5e92c319069dd6346772735a0e0b61fa43d8ca9c987`。**这项提前退出负例现已实际收口**：finish_reason4；active、typed、term、retry marker及USM五镜像全清；无native_amendment；`.9/.15`均无任务；双方8700槽仍为0。原约记录已GC，QA target_exists/in_country_list=0（remaining=-1是不可读默认），与May1原生死亡证据衔接。没有保存精确清理日，不能把预测May7改写为已观测May7。

日志156条=153冷+两次旧候选名载档提示+先前同一原生GameStateAccess断言；此次撤约后走时没有新增脚本报错，none=0。原文归档 `evidence/phi-c5-interrupted-logs-20261031T230503Z`，数据 `phi-A-interrupted-May24-c5-224458.json` 与 `phi-A-interrupted-c5-actual-result.json`。该路径证明正式到期任务/周期监测能识别已丢失原约并按中断收尾；没有独立区分付款方月度先运行的单独触发时序，也不代替改约、战争、亡国、替换serial负例。

## 已证实的问题

这是一项脚本错误。正式十二个月计时已结束时，原生条约可能仍显示一个绑定日。A5 及以前把 `remaining_binding_period > 0` 和“原约确实被改订”放进同一 OR，随即删除模块保存的条约身份与双方镜像，却没有终止仍在履行的原生钱款。条约越过绑定期以后继续存在；绑定期本身不等于自动撤约。

本轮证据来自 `runtime/profiles/20261031T214835Z`，冻结综合 C4，PHI A5；源游戏 1.13.11/build24799966。根实际加载同一五月十二日已签约存档，USM 为玩家，PHI 为 AI；未手动撤约、改约、政策或建设。QA 只读监测使用保存的真实 typed treaty，不修改生产状态。所有日期以原生存档为准，不以截图观察到但未及时暂停的日期代替。

|原生日期|QA remaining|生产 term／正式 .9 剩余|生产状态|原约与钱款|
|---|---:|---|---|---|
|1837.5.1|7|6／6|active，typed33554442，双方镜像仍在|8700、原绑定360|
|1837.5.7|1|都已不在|active/typed/镜像清除；native_amendment=true；finish_reason=0|同一条约33554442、同一条款33554443仍在|
|1837.5.9.18|0|都已不在|仍丢失控制器|原约仍在，账目8700仍保留|
|1837.5.22|0|都已不在|仍丢失控制器|原约仍在；双方更新的收支仍包含8700|

原条约生效时间为 1836.5.12.12。精确的内部取整原因未从引擎源码证实，不能把“半日取整”当确定机制。足够确定的是：脚本 timer 和实际 binding getter 相差一天，5月7日错误分支确实发生；5月9日与5月22日没有正常撤约。

May7 实名是 `大明联邦_1837_05_07大明联邦_1837_05_07_A_boundary.v3`；May9 是 `大明联邦_1837_05_09_A_after.v3`。不存在已保存的精确 May6 或 May8 样本。May7/May9 均为暂停后人工点只读 QA sample 再保存。May1、May22 和边界解析入口见：

- `evidence/phi-A-expiry-May1-214835.json`
- `evidence/phi-A-expiry-May7-May9-214835.json`
- `evidence/phi-A-expiry-May22-214835.json`
- `tools/audit_phi_expiry_boundary.py`

四档 PHI weekly_income 索引11、USM weekly_expenses 索引15都是8700。May9与May7其他预算缓存/国库相同，不能据此计算这两天实际结算；May22账目已经更新而钱款仍在，是持续错误的补证。QA `owned_unamended=0` 发生在生产 typed 指针已被清之后，不表示原生条款真的被改了。

## A6 修复范围

独立候选 `exports/phi-imperial-service-20261031-a6`，精确父 A5。只改 effects、events、script_values 和 metadata。A5 的安全 proposal serial、A4 的2月/1月提案期限、四个现金/原生金额、AI选择、军队交割、贡赋/免役规则、原生改约钩子和地域历史全部保留。

控制流：

1. 受跟踪的条约仍存在，但单条款、原始 binding、支付方向或精确 quote 不再匹配：按原设计交还原生外交，不撤用户改订的条约。
2. 条约身份与内容全匹配，原生 `remaining_binding_period > 0`：保留 active、typed、quote、original_binding、USM 镜像。捕获当前 contract serial 和真实 typed treaty，安排 hidden `.15` 在一天后复查。
3. `.15` 必须同时匹配 PHI、active、现 contract serial、已保存 serial、现 typed treaty、已保存 typed treaty。只有这个匹配事件才能清掉自己的待复查 marker。不同 serial 或不同条约的旧事件不触动后约。
4. 仍有绑定天数就再排一天；归零才按已有 withdraw 撤下本模块未改订的唯一钱款条约，finish_reason=1，清理镜像并给正常到期通知。

两天短 marker 防止收款国月度、付款国月度和正式 `.9` 在同日重复排复查；marker 本身不作为 `.15` 的有效性条件，避免变量与事件计时顺序引发第二个边界错误。完整 active cleanup 会清它。独立 capture 不依赖原始 `.9` 才有的 scope，因此付款国月度切回 PHI 也可进入同一 helper。

contract serial 的读取采用 numeric default0 + has_variable 守卫。typed treaty 采用 exists 和真实 scope，绝不以0伪造实体。`hidden_effect` 不被当成求值屏障。

## 静态结果和备份

- `tools/build_phi_binding_expiry_a6.py` 保留父文件清单、候选清单和逆 AST 检查；去掉明确的到期/复查变化，其余 AST 全等。
- `tools/review_phi_binding_expiry_a6.py` 核 shared expiry 三个入口、serial/typed 双 guard、标量 getter、父 `.9`/创建回调原样继承。
- Tiger 1035→1035，按诊断内容而非路径/行号比较新增0。不是引擎认证。
- `evidence/phi-binding-expiry-a6.json`、`.diff`、`-tiger-incremental.json`、`-static-review.json`。
- 独立备份 `backups/candidate-phi-binding-expiry-a6-20261031T223448Z`，修改前备份同时间 `pre-change-phi-binding-expiry-a6-*`。没有改主 MOD、C4 冻结或运行文件。

## 真实验收与未证边界

应加载安全复制的 May1 原生档（`evidence/autosaves-214835-A-expiry/index.json`），或重新从真实 A_signed 走时。**不要从已经清身份的 May7/May9/May22 档验证修复**；A6有意不按“相同付款人和金额”反向猜哪一条约属于模块，也不注入控制变量重建过去。

需要实际观察 May7 正剩余绑定天时 active/typed/mirrors仍在，`.15` 排队保存正确 serial/typed；随后原生 remaining0时原约被撤、finish_reason1、钱款槽归零、双方控制器清理，其余条约和贡赋没有被撤。再检查原约不会恢复支付，以及到期后正常新申请使用新 serial。实际改约和更换合同的负例仍要分别执行；静态双 guard不能替代这些游戏过程。

独立只读复审未发现 A6 新增的旧事件/重复事件误动新约路径，但发现一个**继承的中断分类边界**：`payer_month` 的到期分支直接调用 expiry；若原约已经原生提前撤销、收款国尚未完成月审，expiry 最后 else 仍会写 finish_reason1，而不是 PHI_month 会写的 reason4。此时不会撤掉另一个条约，但正常到期回执不准确。根要求本轮一并修复，已另制下节 A7，A6仍封存。

旧 all-AI run211226 的新约50331658是第二次现金A，不能把海军25误称自动选择B。独立B mixed分支已经证明原20条战列舰ID856–875最终归USM，但没有同tick船员存档；其钱款在首份Nov1样本前已经因 concessions 丢失而停止，finish_reason5，不能混成到期测试。这些问题与 A6 到期窄修分开保留。

## A7：付款方发现原约已丢失时的中断分类

`exports/phi-imperial-service-20261031-a7` 精确父 A6，仅 effects 中付款方到期入口的一对 if/else 及 metadata 不同。在 PHI 存活、仍 active、付款方 term 消失的原既有条件下，owned-live 为真则调用相同 A6 expiry；owned-live 为假则交给 `PHI_month` 首个 not-live 分支：finish_reason4、clear_active、通知7。不会进入其后互斥的到期分支，PHI_month 没有回调 payer_month，因此此路径不递归。

原有 PHI 亡国时的 typed mirror 清理完全保留；未到期、不 active、真改约、正剩余绑定日、绑定归零、舰船/政治/金额均未更改。局部逆转唯一新增 if/else 后，付款方 helper AST 与 A6 完全相同；其余脚本字节不变。Tiger1035→1035新增0。静态负例仅证明脚本分支与 guard，不等价原生提前撤约实机测试。

工具为 `build_phi_lost_treaty_a7.py`、`review_phi_lost_treaty_a7.py`；证据 `evidence/phi-lost-treaty-a7.json`、`.diff`、`-static-review.json`；备份 `backups/candidate-phi-lost-treaty-a7-20261031T223807Z`。下一综合版应取 A5→A7 累计差分（共3脚本和metadata），一次冷启同时验证真实绑定到期与原约先丢失的分类。已封存的 A6、运行 C4、主MOD均未修改。

## 采样器与 QA 的限度

每日 QA 动态 debug_log 插值实际全为0，日志里的数字不可用。原生 `nesnd_phi_qa_*` 变量是本报告的数值来源，日期和typed保存均可独立核。运行中QA未热改。

600秒 autosave 采集 session68742已正常完成，232次扫描；May1/Apr1/Mar1均在独立证据目录。该目录按旧B证据 SHA 明确排除同profile旧分支；读前后stat和双SHA稳定才复制。没有仍在后台的这个session。`evidence/autosave-capture-exclusion-regression.json` 记录旧11条回归和新增隔离用例通过；这证明采集工具行为，不证明游戏经济或合同。
