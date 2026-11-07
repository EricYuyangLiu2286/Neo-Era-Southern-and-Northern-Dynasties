# 69 附：「追认圣徒」事件图作图说明

给作图的人或代理（Claude 等）。目前事件用原版视频 `southamerica_christianity` 占位。

## 一、交付规格

| 项 | 要求 |
|---|---|
| 尺寸 | **1700 × 1200**（原版事件视频的帧尺寸；比例 17:12，接近 4:3 横幅） |
| 交稿格式 | PNG（或高质量 JPG），不小于 1700 × 1200；比例不同会被居中裁切 |
| 游戏内格式 | DDS BC3/DXT5，由下面的脚本转换，不用手转 |
| 文件名 | `gfx/event_pictures/nesnd_xiuquan_saint.dds` |
| 构图注意 | 事件窗口右侧有渐隐遮罩（原版 `gui/eventwindow.gui` 的 `fade_horizontal_right`），主体放在左侧与中部，右侧约 1/5 只放背景 |

## 二、先研究原版风格（给作图代理的步骤）

1. 原版事件图是 Bink 视频（`.bk2`），本机没有解码器，不要去读。改看同一美术团队的静态画：
   - 原版加载画面：`D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/gfx/loadingscreens/victoria3_load_0.dds` 到 `_7.dds`
   - 本 MOD 已有的中国题材事件图：主 MOD `gfx/event_pictures/event_ce_mordern_chinese_1.dds` 到 `_9.dds`
2. 用 Pillow 转成 PNG 再看（只读原文件，输出放草稿目录）：

   ```python
   from PIL import Image
   from pathlib import Path
   out = Path("<草稿目录>/refs"); out.mkdir(parents=True, exist_ok=True)
   for f in [*Path(r"D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/gfx/loadingscreens").glob("victoria3_load_*.dds"),
             *Path(r"D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/gfx/event_pictures").glob("event_ce_mordern_chinese_*.dds")]:
       im = Image.open(f); im.load()
       im.convert("RGB").resize((im.width // 3, im.height // 3)).save(out / (f.stem + ".png"))
   ```
3. 逐张记下：光源方向与色温、笔触粗细（远景是否只用色块）、人物比例与面部细节程度、饱和度范围、暗部颜色、画面边缘的处理。写成 5–8 条风格要点，作画时逐条对照。
4. 画完后，与参考图并排缩到同一大小再看一遍：明暗反差、饱和度、笔触是否像同一套画。不像就改，不只调色。

## 三、画面设想

**时间与地点**：19 世纪晚期，华南丘陵乡间，阴天转晴的傍晚。

**主体**：一座新坟和旁边的小屋。坟前立着石头十字架，十字架底部仍靠着最早那根已经发黑的木十字架。小屋门口坐着、躺着几个等候救治的人：缠着绷带的旧伤兵、抱孩子的妇人。

**人群**：坟前一群前来祭奠的人，衣着是本世界线的明式汉服（交领、宽袖、短褐、斗笠），不留辫。有人手里拿着不同样式的十字架或念珠：一个拉丁十字、一个东方式的十字、一个带圆环的十字。这是「信仰被各自理解」的暗示，不要做成对称排列，要像随手带来的。

**远处**：山谷和树林，一条小路通向远方。路上有两位穿黑色长袍的西洋教士（教廷调查员）正在走来，手里拿着簿册。

**不画**：洪秀全本人（他已经去世）；光环、天使、神迹光束；现代建筑；清式辫子与马蹄袖。

## 四、作图提示词

中文：

> 19世纪写实学院派油画，维多利亚时代历史画风格，厚涂笔触，暖褐与灰绿色调，柔和的傍晚侧光。华南丘陵乡间的一座新坟，坟前立着一座简朴的石头十字架，底部倚着一根发黑的旧木十字架。坟旁一间土墙瓦顶小屋，门口有缠绷带的伤兵和抱着孩子的妇人在等候。坟前十余名穿明式交领汉服、短褐、戴斗笠的中国乡民在祭奠，有人手持不同样式的十字架和念珠。远景是起伏的山谷与树林，一条小路上两名黑袍西洋教士拿着簿册走来。画面肃穆、安静，主体偏左，右侧留背景。无光环，无天使，无辫子，无文字。

English:

> 19th-century academic oil painting, realistic Victorian history-painting style, visible impasto brushwork, warm umber and muted grey-green palette, soft low evening side-light. A fresh grave in the hill country of southern China, marked by a plain stone cross with a blackened old wooden cross leaning at its base. Beside it a small mud-walled, tile-roofed house; bandaged veterans and a woman holding a child wait at its door. In front of the grave a dozen Chinese villagers in Ming-style cross-collared robes, short work tunics and conical straw hats pay their respects; a few hold crosses and rosaries of different shapes. In the distance, rolling valleys and woods; on a path two Western priests in black cassocks approach carrying ledgers. Solemn and quiet mood, main subject left of centre, right side kept to background. No halos, no angels, no queues (pigtails), no text.

## 五、接入游戏

交稿后运行（工作台脚本，会先在 `reports/2026-11-07-xiuquan-saint/art/` 生成 DDS 并回读核对，再复制进主 MOD，并把事件的占位视频改成这张图；改前自动备份事件文件）：

```
python "D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/tools/install_xiuquan_event_image.py" <原图路径>
```

只想先看转换结果、不改 MOD：加 `--dry-run`。
