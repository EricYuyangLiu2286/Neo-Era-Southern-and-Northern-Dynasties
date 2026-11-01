# 综合A真实新局基线

run014437，原生1836.1.1暂停档，99,561,728字节，SHA-256 `9b4de7f764cb5e1e28e77c5aea76337651dd69e24ffbb6390941d2c1819f9982`。存档实际seed `1873443562`；UI checksum `995d` 由root记录。root声明流程NewGame→Sandbox→USM、无QA状态夹具/走时/经济命令。冻结MOD逐SHA匹配run来源清单。

| 对象 | 实际ID / 所属 | 基线事实 |
|---|---|---|
| 玩家 | player0 → USM730 | 保存时仍玩USM |
| 林汉涵 | 3153 / USM730 | 现有general/politician/IG leader，无死亡记录，不是ruler |
| 陈东阳 | 3148 / USM730 | 现有politician/IG leader，无死亡记录 |
| 郑沁 | 3150 / USM730 | 现有general/politician/IG leader，无死亡记录 |
| 日本君主 | 3446 / JAP17 | 国家ruler实际指针为丰臣秀治3446；储君3447 |
| 日本关系 | pact60 | USM730→JAP17，tributary |
| 日本领土 | JAP12个state | JTK735/JIM736只有预登记国家record，各0state、无ruler，不代表已释放 |

USM已存在 `started_with_chendongyang=true`。压力变量尚未序列化，**不能记作实测0**；此时intro尚未执行，`ce_usm_conflicts_within` JE记录0，所选相关USM活跃JE0。相关实际DP0、war记录0，`usm_civilwar_occured` global未设置。

这是之后判断同一人物、加压顺序及真实外交博弈/战争的前档，仅记录基线，剧情验收仍未运行。精确字段见 `sequence-snapshot.json`；入口来源、文件绑定和摘要见 `baseline-summary.json`。
