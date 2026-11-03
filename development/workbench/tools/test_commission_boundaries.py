from test_commission_gate_behavior import *

MAIN=['STATE_MADRAS','STATE_CIRCARS','STATE_KURNOOL','STATE_MYSORE','STATE_TRAVANCORE','STATE_GUJARAT','STATE_DELHI','STATE_AGRA','STATE_BIHAR','STATE_BOMBAY','STATE_SINDH','STATE_CENTRAL_PROVINCES']
SOUTH=['STATE_ZULULAND','STATE_TRANSVAAL','STATE_VRYSTAAT','STATE_EASTERN_CAPE']
def add_piece(w,name,tag,largest=False,pop=1000):
 r=w['regions'][name];c=w['countries'][tag];st=Obj('state',name+':'+tag,owner=c,controller=c,state_region=r,state_population=pop,is_largest_state_in_region=largest,buildings=[Obj('building','building_port',level=1),Obj('building','building_government_administration',level=1)])
 r.a['states'].append(st);c.a['states'].append(st);return st

def direct_world():
 w=world_from_history()
 for name in list(w['regions']):captured(w,name,'FRA')
 w['countries']['USM'].a['tech'].add('civilizing_mission')
 for name in MAIN:
  captured(w,name)
  if name not in ['STATE_DELHI','STATE_AGRA']:add_piece(w,name,'FRA')
 for tag in ['PAN','HYD','COC']:
  w['countries'][tag].a['overlord']=w['countries']['USM'];add_piece(w,'STATE_KURNOOL',tag)
 return w

def cases():
 rows=[]
 def add(name,w,expected,key='nesnd_tianzhu_commission_ready',actor='USM',global_root=False):rows.append((name,w,key,expected,actor,global_root))
 add('historical_no_expansion',world_from_history(),False)
 w=world_from_history();w['countries']['USM'].a['tech'].add('civilizing_mission');add('research_only_no_expansion',w,False)
 add('12_regions_3_direct_princes_2_heartlands',direct_world(),True)
 add('same_case_startup_without_root',direct_world(),True,global_root=True)
 add('JE_entry_startup_without_root',direct_world(),True,'nesnd_tianzhu_commission_entry',global_root=True)
 w=direct_world();captured(w,'STATE_CENTRAL_PROVINCES','FRA');add('11_regions_even_with_extra_pieces',w,False)
 w=direct_world();captured(w,'STATE_CENTRAL_PROVINCES','FRA');captured(w,'STATE_CEYLON');captured(w,'STATE_INDIAN_OCEAN_TERRITORY');add('islands_do_not_fill_mainland_shortfall',w,False)
 w=direct_world();w['countries']['COC'].a['overlord']=None;add('2_direct_princes',w,False)
 w=direct_world();w['countries']['COC'].a['overlord']=w['countries']['PAN'];add('indirect_subject_is_not_third_direct_prince',w,False)
 w=direct_world();w['countries']['COC'].a['is_country_alive']=False;add('dead_prince_not_counted',w,False)
 w=direct_world();w['countries']['COC'].a['states'][0].a['state_population']=0;add('empty_prince_not_counted',w,False)
 w=direct_world();add_piece(w,'STATE_AGRA','FRA');add('only_one_complete_heartland',w,False)
 w=direct_world();add_piece(w,'STATE_AGRA','FRA').a['controller']=w['countries']['USM'];add('occupation_does_not_complete_heartland',w,False)
 w=direct_world();add_piece(w,'STATE_AGRA','FRA');add_piece(w,'STATE_DELHI','FRA');captured(w,'STATE_RAJPUTANA');captured(w,'STATE_HILL_PUNJAB');add('two_tiny_mughal_enclaves_not_heartlands',w,False)
 w=direct_world();w['regions']['STATE_AGRA'].a['states'][0].a['state_population']=0;add('zero_pop_heartland_does_not_count',w,False)
 w=eligible_world();add('no_princes_survive_conquest_alternative_reachable',w,True)
 w=direct_world();captured(w,'STATE_CENTRAL_PROVINCES','PAN');add('direct_subject_land_counts',w,True)
 w=direct_world();captured(w,'STATE_CENTRAL_PROVINCES','PAN');w['countries']['PAN'].a['overlord']=w['countries']['FRA'];add('subject_leaves_realm_land_and_prince_no_longer_count',w,False)
 for name in ['STATE_MADRAS','STATE_DELHI','STATE_AGRA']:
  w=direct_world();captured(w,name,'FRA');add('lose_'+name,w,False)
 w=direct_world();captured(w,'STATE_MADRAS','PAN');add('subject_capital_cannot_supply_USM_seed',w,False)
 w=direct_world();w['regions']['STATE_MADRAS'].a['states'][0].a['buildings']=[Obj('building','building_government_administration',level=1)];add('missing_seed_port',w,False)
 w=direct_world()
 for st in w['countries']['USM'].a['states']:st.a['buildings']=[b for b in st.a['buildings'] if b.name!='building_government_administration']
 add('missing_USM_administration',w,False)
 for flag in ['nesnd_tianzhu_commission_established','nesnd_tianzhu_commission_cooldown']:
  w=direct_world();w['countries']['USM'].a['vars'].add(flag);add(flag,w,False)
 w=direct_world();w['countries']['TZ1']=Obj('country','TZ1',states=[],vars=set(),is_country_alive=True);add('existing_commission_tag_not_recreated',w,False)
 for flag in ['is_at_war','is_diplomatic_play_initiator','is_diplomatic_play_target','is_diplomatic_play_committed_participant']:
  w=direct_world();w['countries']['USM'].a[flag]=True;add(flag,w,False)
 w=direct_world();w['countries']['USM'].a['overlord']=w['countries']['FRA'];add('founder_is_subject',w,False)
 w=direct_world();w['countries']['USM'].a['tech'].remove('civilizing_mission');add('research_still_required_after_expansion',w,False)
 w=world_from_history();w['countries']['USM'].a['tech'].add('civilizing_mission')
 for r in w['regions'].values():
  for st in r.a['states']:st.a['controller']=w['countries']['USM']
 add('occupation_of_entire_india_does_not_replace_ownership',w,False)
 w=world_from_history();w['countries'].pop('USM');add('missing_USM_is_safe_other_country_context',w,False,actor='FRA',global_root=True)
 for num in [0,1,2,3,4,5,6]:
  w=world_from_history();w['countries']['USM'].a['tech'].add('civilizing_mission')
  for region in (SOUTH+['STATE_CAPE_COLONY','STATE_NORTHERN_CAPE'])[:num]:captured(w,region)
  add('yuanshan_region_count_'+str(num),w,num>=4,'nesnd_yuanshan_commission_ready')
 w=world_from_history();w['countries']['USM'].a['tech'].add('civilizing_mission');w['countries']['PAN'].a['overlord']=w['countries']['USM']
 for i,region in enumerate(SOUTH):captured(w,region,'USM' if i<2 else 'PAN')
 add('yuanshan_own_plus_direct_subject',w,True,'nesnd_yuanshan_commission_ready',global_root=True)
 w=deepcopy(w);w['countries']['PAN'].a['overlord']=w['countries']['FRA'];add('yuanshan_subject_loss',w,False,'nesnd_yuanshan_commission_ready')
 w=world_from_history()
 for region in SOUTH:captured(w,region)
 add('yuanshan_technology_gate',w,False,'nesnd_yuanshan_commission_ready')
 return rows

def evaluate(mutation=None):
 rows=[]
 for name,w,k,expected,actor,global_root in cases():
  ev=Evaluator(C,w)
  if mutation:mutation(ev.db)
  try:actual=ev.test(k,actor,global_root);error=None
  except AssertionError as err:actual='ERROR';error=str(err)
  rows.append({'name':name,'expected':expected,'actual':actual,'pass':actual==expected,'error':error})
 return rows

def mutate_threshold(db):
 n=next(n for n in db['nesnd_tianzhu_commission_ready'].walk() if n.key=='count' and n.value=='12');n.value='2'
def mutate_inverse_population(db):
 n=next(n for n in db['nesnd_tianzhu_commission_ready'].walk() if n.key=='state_population');n.op='<'
def mutate_global_root(db):
 for k in ['nesnd_commission_owner_in_realm','nesnd_commission_indian_prince']:
  for n in db[k].walk():
   if n.key in ['this','overlord'] and n.value=='c:USM':n.value='root'
def mutate_heartland_remainder(db):
 n=db['nesnd_commission_region_fully_controlled'];n.children=[x for x in n.children if x.key!='NOT']
def mutate_prince_count(db):
 n=next(n for n in db['nesnd_tianzhu_commission_ready'].walk() if n.key=='any_country');n.get('count').value='2'
if __name__=='__main__':
 rows=evaluate();mutants=[]
 for fn in [mutate_threshold,mutate_inverse_population,mutate_global_root,mutate_heartland_remainder,mutate_prince_count]:
  result=evaluate(fn);failed=[x['name'] for x in result if not x['pass']];mutants.append({'mutation':fn.__name__,'detected_by':failed,'pass':bool(failed)})
 status='PASS' if all(x['pass'] for x in rows+mutants) else 'FAIL';dump(R/'boundary-cases.json',{'status':status,'cases':rows,'mutation_negative_controls':mutants,'scope':'Real trigger AST evaluated on explicit static ownership fixtures; NOT game execution','candidate_trigger_files':{p.name:sha(p) for p in (C/'common/scripted_triggers').glob('nesnd_commission*.txt')}});print(status,len(rows),'behavior cases',len(mutants),'mutation controls');print([x for x in rows+mutants if not x['pass']])
