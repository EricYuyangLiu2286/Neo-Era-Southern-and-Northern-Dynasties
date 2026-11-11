# 北洋 / 西洋三角贸易：方案稿

日期：2026-11-11　状态：方案，未写脚本　游戏：1.15.0

## 一、内容树（两个日志相同）

```
全局日志（开局由 history/global 挂出，contextless）
├─ 状态量：成交进度 0–100（全局变量，唯一写入者是日志月脉冲；进度条照大流散总进度条的写法从变量同步）
│   每月 +1 基础；参与国中每有一国实行「奴隶贸易」或「殖民地奴隶制」+1；任一参与国实行「商业海军」+3（不叠加）
├─ 当前订单：卖方、迁出州、pop（文化）、目标州、买方；清零时选定，显示在日志正文
├─ 按钮：双向国 买入 / 卖出 / 都不做；只买国 迁入 / 拒绝；只卖国 迁出 / 拒绝（每国一个模式变量）
├─ AI：年脉冲按权重为 AI 参与国重设模式
├─ 结算（周检查，进度 ≥100）：成交 或 失败 → 清零 → 选下一单
└─ 结局：失效一个（hidden 以外的普通失效结局，带说明）
```

进度条存放在全局变量而非 `monthly_progress`，是为了复测时能用控制台一句 `change_global_variable` 加满；正文列出每月增速的三行来源。

## 二、地域与参与国

### 北洋（`geographic_region_nesnd_north_triangle`）

战略区：华北 `region_north_china`、华南 `region_south_china`、东北亚 `region_northeast_asia`、西伯利亚 `region_siberia`、中南半岛 `region_indochina`、南洋 `region_indonesia`、大洋洲 `region_oceania`、太平洋沿岸 `region_pacific_coast`。

依据：SHA 首都山东、CNE 河南（华北）；USM 南京、台湾（华南）；JAP 关西、朝鲜、俄远东鄂霍次克/堪察加/阿穆尔（东北亚）；SHA 的雅库特诸州（西伯利亚）；BUR、SIA、DAI（中南半岛）；DEI 爪哇、PHI 吕宋（南洋）；YN1 昆士兰（大洋洲）；HUS 加利福尼亚（太平洋沿岸）。不含中亚（QE1 伊犁，内陆）、印度、加拿大、大平原。

资格 a 的补充：首都在地域内；**或**为 RUS；**或**拥有南京、粤中（广州）、福建、闽江、浙江、苏北、苏南、皖南、皖北、东京（河内）任一州。

身份：
- 双向：SHA；RUS；主体文化含日本人的国家（JAP，及日本三国中的任何一国）。
- 只买：HUS、YN1；另有首都在太平洋沿岸或大洋洲的其他国家。
- 只卖：其余全部（CNE、USM、台湾、朝鲜、蒙古、东南亚各国、DEI 等）。

### 西洋（`geographic_region_nesnd_west_triangle`）

战略区：西欧 `region_western_europe`（英、法、低地、伊比利亚）、南欧 `region_southern_europe`、北非 `region_north_africa`、西非 `region_west_africa`、赤道非洲 `region_equatorial_africa`（含安哥拉）、南部非洲 `region_southern_africa`、大西洋沿岸 `region_atlantic_coast`、大平原 `region_great_plains`（含路易斯安那、得克萨斯）、中美 `region_central_america`（含加勒比、古巴、墨西哥）、巴西 `region_brazil`、大哥伦比亚 `region_gran_colombia`、拉普拉塔 `region_la_plata`。

依据：大西洋三角的三个角——欧洲港口、几内亚湾至安哥拉的非洲海岸、美洲种植园区；北非巴巴里海岸是白奴的来源与买方。不含东非（桑给巴尔的印度洋贸易）、尼罗河流域（红海与撒哈拉商路）、安第斯（太平洋一侧）、加拿大、北欧、中欧、东欧、巴尔干。

身份（按首都所在战略区）：
- 双向：首都在西欧、南欧（殖民国家：为美洲殖民地买入，卖出本国受歧视的穷人＝契约白奴）；首都在北非（巴巴里诸国：扣押欧洲俘虏，又从撒哈拉以南买入）。
- 只买：首都在美洲各区（USA、BRZ、MEX、得克萨斯等）。
- 只卖：首都在西非、赤道非洲、南部非洲（SOK、DAH、ASH 等）。

### 开局实际参与情况（按开局法律推算，未实机核对）

- 北洋：未禁奴的只有 HUS（债务奴隶制，买）、USM、DEI、BUR、SIA、DAI（债务奴隶制，卖）、PHI（奴隶贸易，卖）。**SHA、JAP、RUS、CNE、YN1、KOR 开局都是禁止蓄奴**（SHA 写在 `SHA.txt:43`，其余为默认法律），按资格 d 不参与，直到改法。开局约每月 +5，二十个月一单。
- 西洋：FRA、SPA、POR、NET（殖民地奴隶制）与 MOR、TUN、TRI（奴隶贸易）为双向；SOK（奴隶贸易）、DAH、ASH（债务）为卖方；BRZ（奴隶贸易）、USA（遗留奴隶制）为买方；GBR 禁奴不参与。开局约每月 +13，八个月一单。

## 三、资格与人口筛选

参与国（月结判定，同时满足）：
- a 首都在地域内（北洋另有上面的补充）；
- b 在地域内的州里有可买卖人口（见下）；
- c `has_port_country = yes`，或有一个陆上相邻（`is_adjacent_to_country`）、满足 a/b/d/e、本国有港口、未与其交战的国家；
- d 未实行「禁止蓄奴」；
- e 总人口 ≥ **250,000**（SHA 开局约 38 万可过；排除虾夷、兰芳等极小国）。分权国家不参与。

可买卖人口（pop）：职业为佃农、劳工或奴隶；财富 < 10（原版债务奴隶制对财富 ≥10 的人口完全无效，`defines/00_defines.txt:585-588`）；识字率 < 30%（`literacy_rate`）；规模 ≥ 5,000。只取卖方在地域内的州。

文化规则（卖方看全部规则，买方只看主体文化、斯拉夫、日本人三条）：

| | 北洋 | 西洋 |
|---|---|---|
| 所有国家 | 不得卖、买本国主体文化 | 同左 |
| 「儒家文化圈」 | 带 `tradition_sinosphere` 的文化，**除女真（manchu）外**，都不能卖 | 不适用 |
| 例外 | 日本人：任何卖方可卖，日本系国家也可买卖本国日本人；朝鲜人：日本系国家可卖；辽东人：SHA 可卖；台湾原住民（`yuanzhumin`）本就不在文化圈内 | — |
| RUS | 不卖、不买斯拉夫人（东、西、南斯拉夫三种 heritage） | — |
| 卖方额外 | — | 只能卖接受度 < 60 的人口（原版 `enslave_discriminated_farm_workers` 的门槛 `acceptance_status_4`） |

MOD 中带 `tradition_sinosphere` 的文化：华北、辽东、老秦、西北、西域汉羌、巴蜀、荆楚、江南、西南、远南、华夏、客家、闽、粤、日本、朝鲜、越南、苗、彝、壮、女真，及 `nesnd_qe1_conversion_cohort`。琉球在 MOD 中没有此传统。

## 四、成交与失败

**选单**（清零时）：随机取一个模式为「卖」的参与国，在其地域内州中取一个合格 pop；再取一个模式为「买」、不是卖方、未与卖方交战的参与国，在其地域内取一个目标州。目标州须允许奴隶：所有国未禁奴；若为殖民地奴隶制，须是未并入州。另外目标州内不得已有该文化与宗教的非奴隶 pop（原因见下）。

**人数**：取选定 pop 的 10%，以迁出州人口的 1% 与 20,000 人封顶，取整。只搬一个 pop、去一个州。大流散每批上限是总数的十分之一，这里同样按十分之一取，再加州人口封顶防止抽空。

**迁移写法**：`move_partial_pop` 迁到目标州，然后在目标州把该文化、宗教的非奴隶 pop 用 `change_poptype = pop_type:slaves` 改为奴隶（原版 `enslave_discriminated_farm_workers` 的写法）。迁入的人会与目标州同文化同宗教同职业的 pop 合并（大流散脚本已注明），所以选单时要求目标州没有这类非奴隶 pop，才不会把原住户一起改成奴隶。实际搬走人数照大流散的前后计数法核对。

**成交**：
- 卖方（迁出州现所有国）`add_money` = 买方（目标州现所有国）每周固定收入 `fixed_income` × 3（原版 `yearly_gross_income` 即 `fixed_income × 52`）。
- 买方得修正「赊购奴隶」：`state_tax_collection_mult = -0.025`，持续 **913 天**（原版 `short_modifier_time`，2.5 年）。先移除再添加，故不叠加、成交即刷新；两个日志共用这一个修正，同时在两边买入也只扣 2.5%。按税收约占收入六到八成估算，2.5 年约折合 2–2.6 周收入，与卖方所得同一量级。
- 买卖双方各收到一条不弹窗的事件，列出所得与修正。

**失败**（日志正文显示「上一单失败」及原因，不弹窗；然后清零、选下一单）：
- 无可用成交单：清零时没选出订单，或结算时订单已失效（pop 消失、两国交战、同属一国）；
- 买方没有奴隶制：目标州现所有国已禁奴，或殖民地奴隶制下该州已并入。

## 五、失效

每个日志判定「地域内国家」（满足资格 a、非分权）全部满足以下任一项时失效：已禁止蓄奴；已研究 `human_rights`（人权）；本国无港口。

选 `human_rights` 的理由：它是三代社会科技，修正中带 `country_ban_slavery_no_infamy_bool`（禁奴不再招致恶名）；原版禁奴法的 AI 权重在研究它之后大幅提高，注释原文为“后期强烈倾向废奴”（`laws/02_slavery.txt:86-100`）。四、五代社会科技与奴隶制无关。

## 六、可复用的原版接口

| 用途 | 接口 |
|---|---|
| 贫困 | `is_pop_type`、`wealth`（不用 `strata`：江户、种姓阶序会改变阶层归属） |
| 识字 | `literacy_rate`（pop 可用） |
| 港口 | `has_port_country`；相邻 `is_adjacent_to_country`；交战 `has_war_with` |
| 奴隶制 | `has_law = law_type:law_slavery_banned / law_slave_trade / law_colonial_slavery / law_debt_slavery / law_legacy_slavery`；州 `is_incorporated` |
| 商业海军 | `law_type:law_merchant_navy`（多数沿海国开局即为此法） |
| 文化 | `has_discrimination_trait = tradition_sinosphere / heritage_east_slavic …`、`is_primary_culture_of`、`pop_acceptance` |
| 地域 | 新建两个 geographic region，`is_in_geographic_region` |
| 迁移与转职 | `move_partial_pop`、`change_poptype`；大流散的前后计数法 |
| 收入、税收 | `fixed_income`；`state_tax_collection_mult` |
| 失效科技 | `has_technology_researched = human_rights` |

复用的命名 trigger 约 6 个：地域国家、参与国、可买卖 pop（带卖方/买方参数）、目标州可收奴、订单有效、日志失效。参数 `$KEY$ = north / west` 让两个日志共用同一组 trigger 与 effect。

新增文件：日志、进度条、按钮、trigger、effect、script value、geographic region、static modifier、一个事件文件、history/global 开局挂载、中英本地化。

## 七、与描述的冲突和漏洞（最小改法）

1. **RUS 首都在圣彼得堡**，不在北洋地域。改法：资格 a 对 RUS 按国名放行，交易只取 RUS 在地域内的州。
2. **双向国开局都禁奴**：SHA、JAP、RUS 以及 CNE、YN1 开局均为禁止蓄奴，按资格 d 不参与。改法：照规则不变，改法后自动加入（推荐）；或对列名国家免除 d（但它们作买方时仍会因“没有奴隶制”而失败）。
3. **失效条件的对象**：参与国按定义都未禁奴，“所有参与国都已禁奴”永远不成立。改法：失效按「地域内国家」（只看资格 a）判定。
4. **女真在 MOD 里属儒家文化圈**（`CE_cultures.txt:292` 带 `tradition_sinosphere`），而你要求女真可卖。改法：文化圈定义排除 manchu。顺带确认：苗、彝、壮、越南也带此传统，会被保护；琉球不带，可卖。
5. **殖民地奴隶制**：引擎会解放已并入州的奴隶，“任何形式的奴隶制”在这些州实际无效。改法：殖民地奴隶制只算未并入州。
6. **买方的文化限制**：描述只写了卖方能卖什么。改法：儒家文化圈限制只管卖方；买方只受“不买本国主体文化”和 RUS 斯拉夫限制。
7. **默认模式**：建议所有国家默认「都不做 / 拒绝」，玩家手动开；AI 每年按权重重设一次（奴隶制法律、地主是否执政、是否负债、统治者是否废奴派）。
8. **“显示失败”**：建议只写在日志正文，不弹窗。

## 八、复测（制作完成后细化）

需新开局；或读档后用控制台 `effect add_contextless_journal_entry = nesnd_north_triangle_trade` 手动挂出日志。加满进度：`effect change_global_variable = { name = nesnd_north_trade_progress add = 100 }`，一周内结算。
