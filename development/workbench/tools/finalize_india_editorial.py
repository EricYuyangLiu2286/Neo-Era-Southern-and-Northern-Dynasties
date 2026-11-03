from india_context import *
p=C/'common/scripted_buttons/nesnd_india_reform.txt';s=read(p)
for k in ['schools','industry']:
 n=parse(s).get('nesnd_india_choose_'+k);part=s[n.start:n.end]
 part=part.replace('possible = { has_technology_researched = academia }','possible = { has_technology_researched = academia custom_tooltip = { text = nesnd_india_priority_cooldown_tt NOT = { has_variable = nesnd_india_priority_cooldown } } }')
 part=part.replace('set_variable = { name = nesnd_india_priority value =','set_variable = { name = nesnd_india_priority_cooldown months = 12 } set_variable = { name = nesnd_india_priority value =')
 # The effect rechecks the same cooldown; AI completes its chosen priority before switching.
 at=part.index('hidden_effect');part=part[:at]+part[at:].replace('nesnd_india_reform_live = yes','nesnd_india_reform_live = yes NOT = { has_variable = nesnd_india_priority_cooldown }',1)
 ai=parse(part).get('nesnd_india_choose_'+k).get('ai_chance');aitxt=part[ai.start:ai.end]
 aitxt=aitxt[:-1]+(' if = { limit = { NOT = { has_variable = nesnd_india_schools_done } } value = 0 }' if k=='industry' else '')+' }'
 part=part[:ai.start]+aitxt+part[ai.end:]
 s=s[:n.start]+part+s[n.end:]
write(p,s)
loc({'nesnd_india_priority_cooldown_tt':('距上次调整改革重点已满一年。','At least a year has passed since the last change of reform priority.')})
# Sources used for all current copy, aligned to the author baseline rather than older AI drafts.
original=W/'backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_country_flavor_text_l_simp_chinese.yml'
text=read(original);sample=[(i+1,line) for i,line in enumerate(text.splitlines()) if 'MUG_FLAVOR_TEXT' in line]
dump(R/'writing-source.json',{'path':str(original),'sha256':sha(original),'samples':sample,'native_english_sources':['game/localization/english/dlc/ep2/*india*','events/india_events/federation_of_india_events.txt'],'game_launched':False})
cnp=C/'localization/simp_chinese/replace/zzzzzzzzzzzzzz_nesnd_india_l_simp_chinese.yml';enp=C/'localization/english/replace/zzzzzzzzzzzzzz_nesnd_india_l_english.yml'
def pairs(p):return dict(re.findall(r'^\s*([\w.\-]+):\d*\s+"(.*)"',read(p),re.M))
zh,en=pairs(cnp),pairs(enp);assert zh.keys()==en.keys()
rows=[]
for k,v in zh.items():
 category='narrative' if k.endswith(('_reason','.d')) or '.d' in k else ('mechanic' if k.endswith(('_tt','_desc','_tooltip')) else 'title_or_label')
 rows.append({'key':k,'chinese':v,'english':en[k],'category':category,'editorial_status':'reviewed','scope':'current effective India localization; exact states/names and actual effect quantities checked separately'})
dump(R/'writing-lines.json',{'files':{str(cnp):sha(cnp),str(enp):sha(enp)},'rows':rows,'engine_verified':False})
write(R/'writing-comparison.md','''# 印度文案对读与返工

作者样本：原始备份ce_country_flavor_text_l_simp_chinese.yml的MUG_FLAVOR_TEXT（第30行、SHA及全文见writing-source.json）。其叙述以过去的政治地位、具体危机、外援选择相承接，保留作者的鲜明判断；不把游戏步骤排成剧情。当前PPT、海军原稿和HOI4只用于设定，不冒称为玩家文字。

|作者特点／原句|初稿或风险|最终处理|
|---|---|---|
|“过去多于未来的国度”，列腐败、鸦片、外国干涉、南方殖民地|将BIC英国兵变改名，或先解释三个开发模块|莫卧儿正文讲旧威望、法国资本与学校工场。避免将王朝出身套到全部印度居民。|
|“进一步倚重法国…乃至自力更生”保留多条政治选择|法国永久无条件援助；依赖指标混同影响力|正文把法国视作有利益的对方；按钮/事件公开四年顾问及真实费用，关系、国库、援助互不冒充。|
|行动者、地区和利益具体|原稿固定“同戴一个王冠”，与本轮共和国按钮冲突|主体改为国家与各省；王朝民望独立为仅君主制日志，共同体在共和国保留。|
|海外设定地区有区别|天竺与远山后续治理两段完全对齐|天竺写港口、村社与本地王公；远山写沿海据点如何深入南非腹地。远山不放到印度。|
|条件各有意义，不用冗长说明替代判定|“持续推进”不展示当地条件；无效大段custom_tooltip|建设用原生独立建筑／市场条件，筹备用具名月度来源。不可见变量、创建国家、一次性成本仍给短tooltip。|
|英文应自然表达政治过程|逐中文逗号翻译、反复重述同一效果|主语转换重新断句。标题和玩家选项短；并入、独立、防御条约、教育顾问区分，拒绝不说已经生效。|

逐条中英文最终文本见writing-lines.json，共'''+str(len(rows))+'''键。机械用语扫描和482项脚本检查另有原始报告；这些并非AI检测器或游戏UI验证。阵营名、时代人物与引用没有新增伪造出处。颜色/数值/国家scope按有效脚本核对，未知引擎显示留待用户实测。
''')
print('Priority oscillation guard and',len(rows),'bilingual editorial rows saved')
