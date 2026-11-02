from pathlib import Path
import sys,json,hashlib,re,collections
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts');import pdx
G=Path(r'D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game');W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-research-20261102')
d=json.loads((W/'native-inventory.json').read_text(encoding='utf8'));p=W/'native-japan.md';s=p.read_text(encoding='utf8')
new=['','补充整州资源/土地细项（仍为state_region潜力，非JAP当前开发量）：','','| 州 | 金/林/渔/鲸上限 | 可发现资源 | 耕作种类与州特性 |','|---|---|---|---|']
for st,e in d['economic_inputs'].items():
 r=e['resources'];cap={k:int(v) for z in r['capped'] for k,v in z.items()};dis=[]
 for rr in r['discoverable']:
  dis.append(', '.join(str(x['key'])+'='+str(x['value']) for x in rr['children']))
 new.append('| '+st+' | '+' / '.join(str(cap.get(k,0)) for k in ['building_gold_mine','building_logging_camp','building_fishing_wharf','building_whaling_station'])+' | '+('; '.join(dis) or '未显式定义')+' | '+', '.join(r['arable_resources'])+'；特性 '+(', '.join(r['traits']) or '无显式特性')+' |')
new+=['','文化/宗教create_pop输入合计（未填写religion表示该条未显式指定，不擅自归为某信仰）：','','| 文化 | 显式宗教 | 人口 |','|---|---|---:|']
counts=collections.Counter((r['culture'],r['religion']) for e in [])
for e in d['economic_inputs'].values():
 for r in e['pops']:counts[r['culture'],r['religion']]+=int(r['size'])
for (c,r),n in counts.items():new.append('| '+c+' | '+(r or '未显式指定')+f' | {n:,} |')
new.append('')
s=s.replace('所有权来源计算方法：','\n'.join(new)+'\n所有权来源计算方法：')
p.write_text(s,encoding='utf8')
# Verify source hashes stayed stable; key numerical invariants are extraction checks, not game tests.
checks=[]
for rec in d['sources']:
 current=hashlib.sha256(Path(rec['path']).read_bytes()).hexdigest()
 if current!=rec['sha256']:checks.append(rec['path'])
assert not checks, checks
hist=d['economic_inputs'];pop=sum(int(r['size']) for e in hist.values() for r in e['pops']);levels=sum(r['ownership_levels'] for e in hist.values() for r in e.get('buildings',[]));army=sum(int(u['count']) for f in d['formations'] for u in f['units'])
assert (pop,levels,army)==(32545935,141,58)
assert len([r for r in d['events'] if '/japan_events/' in r['path'] or r['path']=='events/meiji_restoration.txt'])==124
assert len(d['character_templates'])==112
# Verify every local GAME anchor exists and line falls in file.
anchors=re.findall(r'\]\(<(D:/Program Files \(x86\)/Steam/steamapps/common/Victoria 3/game/.*?):(\d+)>\)',s)
for pp,line in anchors:
 q=Path(pp);assert q.exists(),pp
 assert int(line)<=len(q.read_text(encoding='utf-8-sig').splitlines()),(pp,line)
record={'status':'RESEARCH_SOURCE_VERIFIED','game':'1.13.11','build':'24799966','source_count':len(d['sources']),'hash_changes':checks,'game_file_links_checked':len(anchors),'native_JAP_create_pop_total':pop,'historical_ownership_levels':levels,'formation_irregular_units':army,'native_japan_events':124,'character_templates':112,'game_run':False,'report_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(W/'native-research-verification.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(record))
