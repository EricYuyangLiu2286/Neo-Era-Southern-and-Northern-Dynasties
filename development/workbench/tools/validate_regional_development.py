from regional_context import *
import re,hashlib
bm,cm=man(B),man(C);changed={p:h for p,h in cm.items() if bm.get(p)!=h}
rows=[]
def ck(name,fn):
 try:assert fn();rows.append({'name':name,'pass':True})
 except Exception as e:rows.append({'name':name,'pass':False,'detail':repr(e)})
ck('baseline_history_and_existing_scripts_preserved',lambda:all(cm.get(p)==h for p,h in bm.items() if not p.startswith(('.scratch/','docs/'))))
trees={p:parse(read(C/p)) for p in changed if p.endswith('.txt') and p.startswith(('common/','events/'))}
for p,t in trees.items():
 for n in t.walk():
  if n.key=='icon' and n.value.startswith('gfx/'):
   ck('resource_'+n.value,lambda n=n:(G/n.value.strip('"')).exists() or (C/n.value.strip('"')).exists())
  if n.key=='video':ck('video_'+n.value,lambda n=n:(G/'gfx/event_pictures'/(n.value.strip('"')+'.bk2')).exists())
def db(folder):
 out=set()
 for root in [G,C]:
  for p in (root/folder).glob('*.txt'):out|={n.key for n in parse(read(p)).children}
 return out
regions=db('map_data/state_regions');laws=db('common/laws');buildings=db('common/buildings');technologies=db('common/technology/technologies')
for p,t in trees.items():
 for n in t.walk():
  if n.value and n.value.startswith('s:'):ck('state_'+n.value,lambda n=n:n.value[2:] in regions)
  if n.key=='is_building_type':ck('building_'+n.value,lambda n=n:n.value in buildings)
  if n.key=='has_law':ck('law_'+n.value,lambda n=n:n.value[9:] in laws)
  if n.key=='has_technology_researched':ck('technology_'+n.value,lambda n=n:n.value in technologies)
locale={};textrows=[]
for language in ['simp_chinese','english']:
 p=next((C/'localization'/language/'replace').glob('*nesnd_regional_l_*.yml'))
 ck('bom_'+language,lambda p=p:p.read_bytes().startswith(b'\xef\xbb\xbf'))
 vals={}
 for i,line in enumerate(read(p).splitlines(),1):
  m=re.match(r'^\s*(\S+):0 "(.*)"$',line)
  if m:assert m[1] not in vals;vals[m[1]]=m[2];textrows.append({'language':language,'key':m[1],'text':m[2],'path':p.relative_to(C).as_posix(),'line':i,'sha256':sha(p),'decision':'通过','basis':'writing-comparison.md'})
 locale[language]=vals
ck('bilingual_key_parity',lambda:locale['simp_chinese'].keys()==locale['english'].keys())
ck('no_active_regime_or_status_false_claims',lambda:not any(x in ' '.join(locale['simp_chinese'].values()) for x in ['新公民','宗主之间','王国需要','皇室究竟']))
for p,t in trees.items():
 for n in t.walk():
  if n.key in ['title','desc','name','text'] and n.value and n.value.startswith(('nesnd_rg','nesnd_regional')):ck('loc_'+n.value,lambda n=n:n.value in locale['english'])
ck('all_story_journals_pinned',lambda:all(x.scalar('should_be_pinned_by_default_uninvolved_or_context')=='yes' for x in trees['common/journal_entries/nesnd_regional_development.txt'].children))
ck('no_party_membership_or_forced_laws',lambda:not any(n.key in ['activate_law','party','is_in_party','set_party','add_to_party'] for t in trees.values() for n in t.walk()))
def sig(x):return x['severity'],x['key'],x['message'],tuple((z.get('path'),(z.get('line') or '').strip()) for z in x['locations'])
old={sig(x) for x in json.loads(read(R/'tiger-baseline.json'))};added=[x for x in json.loads(read(R/'tiger-candidate.json')) if sig(x) not in old]
dump(R/'tiger-added.json',added);ck('tiger_no_added_diagnostic',lambda:not added)
dump(R/'writing-keys.json',textrows);dump(R/'structural-checks.json',{'pass':all(x['pass'] for x in rows),'checks':rows,'source_files':cm,'engine_verified':False})
print('Structural PASS',sum(x['pass'] for x in rows),'FAIL',sum(not x['pass'] for x in rows),'Text keys',len(textrows))
for row in rows:
 if not row['pass']:print(row)
for x in added:print(x['message'],x['locations'][:1])
sys.exit(not all(x['pass'] for x in rows))
