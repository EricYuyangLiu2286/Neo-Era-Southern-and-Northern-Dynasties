# 地图数据、编码与编辑器操作

> 何时读：动地图前查文件入口、hub/locator/harbor 的编号规则、历史归属块的形状，或操作原生地图编辑器与军队界面。不必读：拆州与经济的判断方法（读 references/map-economy-design.md）。

## 图像与数据入口

- `GAME/map_data/provinces.png`：8192×3616，每个 RGB 对应 province。不改变像素、地形和河流，仅重分组时仍需确认省份连续。
- `heightmap.png`：16384×7232，使用同范围的 2 倍坐标裁切；`rivers.png` 同 province 图尺寸。高度只供判断地形，不把游戏投影像素当平方公里。
- `map_data/state_regions/*.txt`：ID、provinces、city/farm/mine/wood/port、资源、耕地、traits、impassable、prime_land、naval_exit_id。
- `gfx/map/map_object_data/generated_map_object_locators_{city,farm,mine,wood,port}.txt`：instance.id 对应地区数字 ID。本机已用 12 个川陕旧枢纽核对：图像 x≈position.x，图像 y≈3615−position.z。新地区必须有对应 locator；移走原枢纽时也要重定位原地区。不要把字典序首个地块当合格城市。
- `localization/simp_chinese/hub_names_l_simp_chinese.yml` 与 MOD replace：真实枢纽地名。新地名须有地理或设定依据。城市、矿、林、农四个枢纽都需对应地块，不把全部挤到同一点。
- `tools/map_design_audit.py` 生成当前州人口、产业、资源、真实像素面积、province 邻接和 locator 像素归属证据；`map_design_options.py` 生成地理提案图。它们只写 WORK，图像是分析结果，不是引擎验证。

## 历史归属、人口、建筑的形状

```text
STATES = {
    s:STATE_GUANGDONG = {
        create_state = { country = c:USM owned_provinces = { xRRGGBB } }
        add_homeland = cu:han
    }
}
POPS = {
    s:STATE_GUANGDONG = {
        region_state:USM = {
            create_pop = { culture = han religion = confucian size = 10000 }
        }
    }
}
BUILDINGS = {
    s:STATE_GUANGDONG = {
        region_state:USM = {
            create_building = {
                building = "building_government_administration"
                add_ownership = { country = { country = "c:USM" levels = 1 } }
                reserves = 1
                activate_production_methods = { "pm_professional_bureaucrats" "pm_religious_bureaucrats" "pm_horizontal_drawer_cabinets" }
            }
        }
    }
}
```

以上演示当前形状，`xRRGGBB` 是必须换成真实 province 的占位符，不得直接输出。依据 GAME `history/buildings/11_east_asia.txt`，建筑 levels 常在 `add_ownership` 的 owner 内，不能只查 `create_building.level`。金融区/庄园 owner 可能在另一 state，要保留外国投资和跨地区引用的语义。

## 交通网与港口的编号〔1.13.11 实文件；换版本须重新核对〕

`gfx/map/spline_network/spline_network.splnet` 另存交通 anchors/strips；本机文件是二进制，不能当 PDX 文本解析或随意字节替换。土地 hub ID 为 state ID×100 + 类型（city00/farm01/mine02/port03/wood04）；与视觉 locator 的 ID 不是同一编码。新州需要四类交通 anchors、州内连通和可通行相邻州连接；移走旧 hub 的位置后还要处理旧连接。来源为地图作者本人的 [实作指南](https://steamcommunity.com/sharedfiles/filedetails/?id=3165669021)，并由本次真实日志证明必须补做；指南版本较旧，操作以本机编辑器为准。

当前1.13.11实文件的节点约定：陆地port锚点`state_id*100+3`；独立harbor锚点`(1<<23)+state_id*100`；海域锚点同为`(1<<23)+sea_region_id*100`。原广东harbor8438308用type3条带1121027连南海8694208；原CA harbor8421208用type3条带1577219连太平洋8703908。节点编码来自当前原生文件实证，换版本须重新核对，不把经验公式当永久API。海面connection键与端点/条带类型保持原生同形；港口陆地→harbor连接由引擎按对应ID识别，不能用陆地铁路替代。

## 原生编辑器与军队界面操作（1.13.11 实测）

原生编辑器实测（1.13.11）：Spline Strip Tool 在左栏线网图标；右侧地区筛选支持 `|`，清空按钮比全选替换可靠。选择地区后工具提示为 `Automatically place all hub anchors for currently selected territories` 的按钮会按现有 locators 生成节点。右侧 AnchorID 搜索可定位节点，双击输入框原有数字可替换搜索；点结果会把相机聚焦节点。视口右键取得焦点后分次滚轮缩放。**不要修改已有连线的 anchor index**：本轮把 49401 改为 315900 时原生编辑器崩溃（04:10:01，E06D7363）；先另存检查点，解除旧连线／删除重建后再连接，编号应在首次连接前确定。崩溃证据在 WORK/map-projects/spline-authoring-20261031T035657Z；`map_editor_runtime.py <map-project> --resume` 复用隔离工程并先归档旧日志/崩溃，不覆盖证据。

当前原生军队界面：地图旗帜按钮是“战略目标”，房屋旗帜按钮是“驻扎地区”。只有后者显示实际行程天数并发起移动。选中汉中作为战略目标不等于已测试军队移动。暂停/运行可用右上角按钮；键盘快捷键无效时改用可见按钮并核对日期，不能把调用成功当游戏接收到按键。
