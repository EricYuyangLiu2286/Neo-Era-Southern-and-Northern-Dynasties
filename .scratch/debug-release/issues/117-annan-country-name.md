# 117 安南将军府地图国名

Record: implementation  
Category: bug  
Status: ready-for-human  
Execution: completed  
Validation: STATIC_PASS

截图中，阿富汗作为西秦属国时地图直接显示脚本键。正式源 common/dynamic_country_names/ce_dynamic_country_names.txt 第 302–303 行引用的国名和形容词，在原作快照与现行中英本地化中均无定义。

作者于 2026-11-23 定名“安南将军府”。在两种语言的 replace/ce_countries 文件中补上 dyn_c_afg_duhufu 和 dyn_c_afg_duhufu_adj。英文沿用同文件波斯将军府 Bosi Protectorate 的国名格式、西秦边地正文所用的 Annan 拼写，写作 Annan Protectorate。

两种语言逐键唯一，BOM 与语言头正确，cliche_check 和 loc_link_check 均零命中。部署 0074c2db1583ecaa503572b86305fff4，三处版本一致，已部署的两文件与正式源逐字节相同。下次启动后以西秦属国身份的 AFG 核对地图与外交界面国名。尚未实机复测。
