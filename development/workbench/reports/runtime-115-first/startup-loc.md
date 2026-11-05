# 1.15 启动本地化兼容修复

启动分组 `WORK/reports/migration-115/startup-data/whole-debug-diagnostic-blocks.json` 实有33个简中参数转义诊断，其中32项由主MOD定义。32个英文同键也使用了相同的未转义参数。

两语的法国日志6键、吴朝统一战争1键、埃及1键和东洲社会等级24键中，仅将引号包裹的概念参数从 `$key$` 改为 `$key|q$`。原版 `localization/simp_chinese/alerts_l_simp_chinese.yml` 的 `alert_major_formable_possible_name` 示范相同用法。本批八份冻结文件按改动反向替换后，与全部写前字节吻合。

考纳斯沿用本体立陶宛地区的ID 153和相同的城镇、港口、农场、矿山、伐木场五个省份坐标。MOD `common/scripted_effects/00_dynamic_state_names_europe.txt:187,190,1752` 将 `STATE_KAUNAS` 路由至立陶宛的俄语/波兰语命名效果，生成的键以KAUNAS为前缀。`script-review-first-snapshot/error.5.log` 记录俄语五键，波兰语五键来自同一函数的另一条可达分支。每种显示语言在既有 `ce_hub_names` 文件各追加十个别名，直接引用本体对应的 `HUB_NAME_STATE_LITHUANIA_*` 翻译。两份地图文件的原字节均为冻结文件的完整前缀。

四个王党修正由原版 `modifiers_l_*` 定义。mult引用add，add再引用 `political_movements_l_*` 的运动名。运动名调用原版 `common/customizable_localization/victoria_custom_loc.txt` 中的两个 `COUNTRY.GetCustom` 条目。主MOD没有覆盖相关键、函数或同路径脚本，也未找到直接产生该错误的MOD脚本/UI引用。`CONSTRUCTION_QUEUE_DESC_ITEM` 的原版英语WEEKS_LEFT参数已加q，原版中文尚缺。上述五项均按授权保留原版归属。

本批共改10文件，84个语言/键组合，其中64处单参数修正、20个新据点别名。全MOD双语索引逐键唯一，20个别名目标在对应语言的原版均唯一。所有文件具UTF-8 BOM。冻结后其他子批继续修改同文件的其他内容；最终验证分别核对本批冻结前后字节以及当前工作树84个目标键，保留并行修改。详见 `startup-loc-validation.json` 与 `startup-loc.diff`。独立写前备份为 `WORK/backups/pre-change-startup-loc115-20261105T174041Z/mod`。上述为游戏外验证，未启动游戏、未提交Git。
