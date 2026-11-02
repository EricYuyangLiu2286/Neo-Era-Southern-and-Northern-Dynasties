"""Read-only 1836 history inventory; geography alignment by existing province IDs.
No proportional allocation of vanilla substate pops to a partial footprint.
"""
from pathlib import Path
import sys,json,collections,re,hashlib,subprocess
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');M=W.parent/'mod/Neo-Era Southern and Northern Dynasties';G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game');R=W/'reports/rules-poland-qin-20261102';R.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts');from pdx import parse
def read(p):return p.read_text('utf-8-sig')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def effective(rel,mod=True):
 files={p.name:p for p in (G/rel).glob('*.txt')}
 if mod:files.update({p.name:p for p in (M/rel).glob('*.txt')})
 return [files[k] for k in sorted(files)]
def rows(rel,block,mod=True):
 for p in effective(rel,mod):
  text=read(p);root=parse(text).get(block)
  if root:
   for n in root.children:yield p,text,n
def populations(mod=True):
 out=[]
 for p,text,region in rows('common/history/pops','POPS',mod):
  for state in region.children or []:
   if not state.key.startswith('region_state:'):continue
   for pop in state.all('create_pop'):
    out.append({'region':region.key[2:],'owner':state.key.split(':')[1],'culture':pop.scalar('culture'),'religion':pop.scalar('religion'),'size':int(float(pop.scalar('size','0'))),'source':str(p),'line':text[:pop.start].count('\n')+1})
 return out
def ownership(mod=True):
 out=[]
 for p,text,region in rows('common/history/states','STATES',mod):
  for state in region.all('create_state'):
   provinces=state.get('owned_provinces')
   out.append({'region':region.key[2:],'owner':state.scalar('country','').removeprefix('c:'),'provinces':provinces.values() if provinces else [],'source':str(p),'line':text[:state.start].count('\n')+1})
 return out
def locs():
 d={}
 for root in [G/'localization/simp_chinese',M/'localization/simp_chinese']:
  for p in sorted(root.rglob('*.yml')):
   for m in re.finditer(r'^\s+([A-Za-z0-9_.]+):\s*\d*\s*"(.*)"\s*$',read(p),re.M):d[m.group(1)]=m.group(2)
 return d
loc=locs();owners=ownership();vanillaowners=ownership(False);footprint=set();regions=[]
for row in owners:
 if row['owner']=='QE1':footprint.update(row['provinces']);regions.append(row['region'])
regions=sorted(set(regions));modpops=[r for r in populations() if r['owner']=='QE1'];vanillapops=populations(False)
assert all(r['region'] in regions for r in modpops)
totals=collections.Counter();byregion=collections.defaultdict(collections.Counter)
for r in modpops:totals[r['culture']]+=r['size'];byregion[r['region']][r['culture']]+=r['size']
assert set(regions)==set(byregion),(set(regions)-set(byregion))
# Resolve source-owned primary cultures and current heritage/language/traditions.
defs={}
for p in effective('common/cultures'):
 for n in parse(read(p)).children:defs[n.key.split(':')[-1]]=(n,p)
primary=['ce_laoqin','ce_xiyu','ce_xibei']
def culturemeta(c):
 n,p=defs[c];return {'name':loc.get(c,c),'heritage':n.scalar('heritage'),'language':n.scalar('language'),'traditions':n.get('traditions').values() if n.get('traditions') else [],'definition':str(p)}
meta={c:culturemeta(c) for c in totals}
aligned=[];vp={}
for r in vanillapops:vp.setdefault((r['region'],r['owner']),[]).append(r)
coveredcult=collections.Counter();partialcult=collections.Counter()
for r in vanillaowners:
 ps=set(r['provinces']);hit=ps&footprint
 if not hit:continue
 full=hit==ps
 pops=vp.get((r['region'],r['owner']),[]);counts=collections.Counter()
 for p in pops:counts[p['culture']]+=p['size']
 (coveredcult if full else partialcult).update(counts)
 aligned.append({'vanilla_region':r['region'],'name':loc.get(r['region'],r['region']),'vanilla_owner':r['owner'],'coverage':'full' if full else 'partial','matched_provinces':len(hit),'vanilla_provinces':len(ps),'cultures':dict(counts),'note':'Exact vanilla starting-pop comparator for this whole historical substate' if full else 'Whole vanilla substate listed as contextual reference; population of the intersecting portion is unknown'})
absentfull={c:n for c,n in coveredcult.items() if totals[c]==0};absentpartial={c:n for c,n in partialcult.items() if totals[c]==0 and c not in absentfull}
local_losses=collections.defaultdict(list);alignment_detail=[]
qeowners=[r for r in owners if r['owner']=='QE1']
for original in vanillaowners:
 ps=set(original['provinces']);hit=ps&footprint
 if not hit:continue
 related=[r['region'] for r in qeowners if set(r['provinces'])&hit]
 current_here=set(c for r in related for c in byregion[r])
 original_counts=collections.Counter()
 for pop in vp.get((original['region'],original['owner']),[]):original_counts[pop['culture']]+=pop['size']
 absent=sorted(set(original_counts)-current_here)
 item={'vanilla_region':original['region'],'vanilla_name':loc.get(original['region'],original['region']),'vanilla_owner':original['owner'],'coverage':'full' if hit==ps else 'partial','current_regions':related,'locally_absent_cultures':absent,'vanilla_cultures':dict(original_counts)}
 alignment_detail.append(item)
 if hit==ps:
  for c in absent:local_losses[c].append(item)
oldrepo=W/'projects/nesnd-repository';oldrows=[]
files=subprocess.check_output(['git','ls-tree','-r','--name-only','f18b6c4','common/history/pops'],cwd=oldrepo).decode().splitlines()
for rel in files:
 if not rel.endswith('.txt'):continue
 text=subprocess.check_output(['git','show','f18b6c4:'+rel],cwd=oldrepo).decode('utf-8-sig');root=parse(text).get('POPS')
 if not root:continue
 for region in root.children:
  for state in region.all('region_state:QE1'):
   for pop in state.all('create_pop'):oldrows.append((pop.scalar('culture'),int(pop.scalar('size','0'))))
oldtotals=collections.Counter()
for c,n in oldrows:oldtotals[c]+=n
total=sum(totals.values());heritages=collections.Counter()
for c,n in totals.items():heritages[meta[c]['heritage']]+=n
data={'version':'1.13.11','build':'24799966','scope':'1836 scripted starting sizes, not live save population','current_total':total,'current_cultures':dict(totals),'current_culture_meta':meta,'primary_cultures':primary,'primary_population':sum(totals[c] for c in primary),'primary_share':sum(totals[c] for c in primary)/total,'heritages':dict(heritages),'states':{r:{'name':loc.get(r,r),'cultures':dict(byregion[r]),'size':sum(byregion[r].values())} for r in regions},'vanilla_covered_substates':aligned,'local_alignment':alignment_detail,'local_culture_losses':dict(local_losses),'absent_current_but_present_fully_covered_vanilla':absentfull,'absent_only_partial_reference':absentpartial,'vanilla_full_footprint_cultures':dict(coveredcult),'original_f18b6c4_qe1_totals':dict(oldtotals),'original_to_current_culture_set_removed':sorted(set(oldtotals)-set(totals)),'original_to_current_culture_set_added':sorted(set(totals)-set(oldtotals)),'source_pop_rows':modpops,'input_hashes':{str(p):sha(p) for p in effective('common/history/pops')+effective('common/history/states')},'game_launched':False}
(R/'qin-culture-inventory.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# 西秦1836文化清单与原版对照','',f'当前QE1直接领土：{len(regions)}州，脚本初始人口合计{total:,}；三种主流文化占{data["primary_share"]:.2%}。这里是create_pop.size合计，不是运行存档。','', '|文化|代码|初始人口|份额|主流|heritage|','|---|---|---:|---:|---|---|']
for c,n in totals.most_common():lines.append(f'|{loc.get(c,c)}|{c}|{n:,}|{n/total:.2%}|'+('是' if c in primary else '否')+f'|{meta[c]["heritage"]}|')
lines+=['','## 当前全境不再有人口、但原版完整对应地区存在的文化','','这是开局人口组缺席，不等于文化数据库定义被删除，也不能仅凭聚合差额证明它们一对一转成了西域汉羌。','', '|文化|代码|完整对应原版人口组规模|','|---|---|---:|']
for c,n in sorted(absentfull.items(),key=lambda x:-x[1]):lines.append(f'|{loc.get(c,c)}|{c}|{n:,}|')
lines+=['','## 地区内消失、但别处仍可能保留的文化','','以下只列原版substate被QE1完全覆盖的地理组。现版跨旧州的新州若仍有该文化，不冒称该文化从对应片区消失；因此此表宁可漏列，也不把无法定位的群体归到某片土地。','', '|文化|原版地区（现版对应州）|','|---|---|']
for c,items in sorted(local_losses.items(),key=lambda x:-len(x[1])):
 lines.append('|'+loc.get(c,c)+' `'+c+'`|'+ '；'.join(i['vanilla_name']+'（'+ '、'.join(loc.get(r,r) for r in i['current_regions'])+'）' for i in items)+'|')
lines+=['','## 地理对齐方法','','以QE1历史owned_provinces集合映射原版create_state的省份集合。完全覆盖的原版substate可作整组比较；部分覆盖只列文化背景，不按面积比例编造该片土地的文化人口。新拆州经省份ID对齐，不按州名猜测。','',f'完全覆盖{sum(r["coverage"]=="full" for r in aligned)}组，部分覆盖{sum(r["coverage"]=="partial" for r in aligned)}组。部分覆盖独有缺席候选：'+('、'.join(loc.get(c,c) for c in absentpartial) or '无')+'。','','## 最初MOD与现版','','原始f18b6c4至现版文化集合删去：'+('、'.join(data['original_to_current_culture_set_removed']) or '无')+'；新增：'+('、'.join(data['original_to_current_culture_set_added']) or '无')+'。人口总量差异及逐州分组保存在JSON，地图拆州不等于删除原始文化。','','## 逐州','', '|州|总数|文化分布|','|---|---:|---|']
for r in regions:lines.append(f'|{loc.get(r,r)} `{r}`|{sum(byregion[r].values()):,}|'+ '；'.join(f'{loc.get(c,c)} {n:,}' for c,n in byregion[r].most_common())+'|')
lines+=['','逐create_pop来源路径/行号及各输入SHA见qin-culture-inventory.json。']
(R/'qin-cultures.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({k:data[k] for k in ['current_total','current_cultures','primary_share','heritages','absent_current_but_present_fully_covered_vanilla','absent_only_partial_reference','original_to_current_culture_set_removed','original_to_current_culture_set_added']},ensure_ascii=False))
