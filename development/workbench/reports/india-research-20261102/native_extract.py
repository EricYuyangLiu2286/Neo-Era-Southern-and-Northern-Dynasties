from pathlib import Path
import sys,json,hashlib
from collections import Counter
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
import pdx
G=Path(r'D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
W=Path(__file__).parent
def read(rel): return pdx.read(G/rel)
def loc(t,n): return [t.count('\n',0,n.start)+1,t.count('\n',0,n.end)+1]
def obj(rel,key,fields=None):
 t,r=read(rel)
 for n in r.children:
  if n.key==key:
   if fields:
    for c in n.children or []:
     if c.key in fields: print(f'{rel}:{loc(t,c)}\n'+t[c.start:c.end])
   else: print(f'{rel}:{loc(t,n)}\n'+t[n.start:n.end])
def lines(rel,a,b):
 for i,l in enumerate((G/rel).read_text(encoding='utf-8-sig').splitlines(),1):
  if a<=i<=b: print(f'{i}: {l}')
if __name__=='__main__':
 if sys.argv[1]=='obj': obj(sys.argv[2],sys.argv[3],sys.argv[4:])
 elif sys.argv[1]=='lines': lines(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
 elif sys.argv[1]=='index':
  paths=list(G.glob('events/india_events/*.txt'))
  paths += [p for p in G.glob('common/journal_entries/*.txt') if p.name.startswith('04_') or p.name=='00_east_indies.txt']
  rels=['events/british_raj_events.txt','events/bic_breakup.txt','events/east_indies_events.txt','common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt','common/scripted_progress_bars/00_sepoy_mutiny_progress_bars.txt','common/scripted_buttons/04_india_buttons.txt','common/scripted_buttons/04_indian_famines_buttons.txt','common/script_values/india_values.txt','common/decisions/india_decisions.txt','common/decisions/british_raj_decisions.txt','common/history/countries/bic - british east india company.txt','common/history/characters/bic - britishindia.txt','common/history/population/bic - british east india company.txt','common/history/pops/10_india.txt','common/history/buildings/10_india.txt','common/history/military_formations/05_military_formations_india.txt','common/character_templates/country_bic.txt','common/character_templates/indian_princely_states.txt','common/social_hierarchies/00_social_hierarchies.txt','common/social_classes/01_british_indian_caste_system.txt','common/laws/00_caste_hegemony.txt','common/political_movements/03_pan_national_movements.txt','common/scripted_effects/00_starting_pop_literacy.txt','common/scripted_effects/00_starting_pop_wealth.txt','common/country_definitions/00_countries.txt','common/religions/religion.txt','common/history/global/00_global.txt']
  rels += ['common/on_actions/00_code_on_actions.txt','common/on_actions/00_on_actions_yearly.txt','common/on_actions/00_on_actions_monthly.txt','common/scripted_effects/00_victoria_scripted_effects.txt','common/static_modifiers/content_304_modifiers.txt','common/interest_groups/00_devout.txt','common/political_movements/04_national_movements.txt','common/political_movements/04_country_specific_ideological_movements.txt','common/history/countries/mug - mughals.txt','common/history/characters/mug - mughals.txt','common/law_groups/00_laws.txt','common/scripted_progress_bars/00_victoria_progress_bars.txt','common/scripted_triggers/00_scripted_triggers.txt','common/scripted_triggers/00_victoria_scripted_triggers.txt','common/scripted_lists/victoria_scripted_lists.txt']
  paths+= [G/r for r in rels if (G/r).exists()]
  entries=[]
  for p in sorted(set(paths)):
   t,r=pdx.read(p)
   entries.append({'file':p.relative_to(G).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'lines':len(t.splitlines()),'objects':[{'id':n.key,'lines':loc(t,n)} for n in r.children if n.children is not None]})
  result={'version':'1.13.11','build':'24799966','scope':'All top-level objects in selected native India-related files; descriptive analysis is selected, not all events exhaustively traced.','parser':'pdx.py ordered duplicate-preserving','files':entries}
  (W/'native-india-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
  for e in entries:
   if e['file'].startswith(('events/','common/journal_entries/')): print(e['file']+': '+', '.join(f"{n['id']}@{n['lines'][0]}-{n['lines'][1]}" for n in e['objects']))
 elif sys.argv[1]=='quantify':
  religions={}; culture_files=[]
  for p in G.glob('common/cultures/*.txt'):
   t,r=pdx.read(p)
   for n in r.children:
    if n.children is not None and n.scalar('religion'): religions[n.key]=n.scalar('religion'); culture_files.append(p)
  pops=[]; buildings=[]; sources=set(culture_files)
  for section,key,out in [('pops','create_pop',pops),('buildings','create_building',buildings)]:
   for p in G.glob(f'common/history/{section}/*.txt'):
    t,r=pdx.read(p)
    for holder in r.children:
     for state in holder.children or []:
      for rs in state.children or []:
       if rs.key!='region_state:BIC': continue
       for n in rs.all(key):
        rec={'file':p.relative_to(G).as_posix(),'lines':loc(t,n),'state_region':state.key}
        if key=='create_pop':
         rec.update(culture=n.scalar('culture'),religion=n.scalar('religion') or religions.get(n.scalar('culture'),'UNRESOLVED'),religion_explicit=n.scalar('religion') is not None,pop_type=n.scalar('pop_type','unspecified'),size=int(n.scalar('size','0')))
        else:
         owners=[]
         for own in n.all('add_ownership'):
          for who in own.children or []:
           owners.append({'kind':who.key,'country':who.scalar('country'),'type':who.scalar('type'),'levels':int(who.scalar('levels','0')),'region':who.scalar('region')})
         rec.update(building=n.scalar('building'),explicit_level=n.scalar('level'),ownership_level_sum=sum(x['levels'] for x in owners),owners=owners,pms=n.get('activate_production_methods').values() if n.get('activate_production_methods') else [])
        out.append(rec); sources.add(p)
  stats={}
  for field in ['culture','religion','pop_type','state_region']:
   c=Counter()
   for p in pops:c[p[field]]+=p['size']
   stats[field]=dict(c.most_common())
  b=Counter(); owners=Counter(); explicit=Counter()
  for r in buildings:
   b[r['building']]+=r['ownership_level_sum']
   explicit[r['building']]+=int(r['explicit_level'] or 0)
   for own in r['owners']:owners[own['country']]+=own['levels']
  result={'scope':'Full GAME/common/history/pops and buildings explicit region_state:BIC blocks; excludes subjects, dynamic initialization, auto-generated subsistence/urban centers. Population size inputs are not measured runtime totals. Building level count uses sum of repeated add_ownership entries, not number of create_building blocks.','population_input_total':sum(p['size'] for p in pops),'population_records':len(pops),'population_by':stats,'building_records':len(buildings),'building_ownership_level_total':sum(b.values()),'building_by':dict(b.most_common()),'ownership_country_levels':dict(owners),'pops':pops,'buildings':buildings,'sources':[{'file':p.relative_to(G).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(sources)]}
  result['explicit_building_levels']=dict((k,v) for k,v in explicit.items() if v)
  formations=[]
  for p in G.glob('common/history/military_formations/*.txt'):
   t,r=pdx.read(p)
   for h in r.children:
    for c in h.children or []:
     if c.key!='c:BIC':continue
     for n in c.all('create_military_formation'):
      units=Counter()
      for unit in n.all('combat_unit'):units[unit.scalar('type')]+=int(unit.scalar('count','0'))
      formations.append({'name':n.scalar('name'),'type':n.scalar('type'),'file':p.relative_to(G).as_posix(),'lines':loc(t,n),'unit_counts':dict(units)})
  result['military_formations']=formations
  (W/'native-india-inputs.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
  print(json.dumps({k:v for k,v in result.items() if k not in ['pops','buildings','sources']},ensure_ascii=False,indent=2))
