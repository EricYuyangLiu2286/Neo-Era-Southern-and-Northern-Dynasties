from test_commission_gate_behavior import *
# Actual AST control flow; native creation APIs are fault-injected, NOT an engine simulation.
class EffectTrace:
 def __init__(self,w,rootdir=C,create_ok=True,pact_ok=True):
  self.w=w;self.pred=Evaluator(rootdir,w);self.db={};self.trace=[];self.create_ok=create_ok;self.pact_ok=pact_ok
  for p in (rootdir/'common/scripted_effects').glob('*.txt'):
   for n in parse(read(p)).children:self.db[n.key]=n
 def move(self,st,target):
  old=st.a['owner'];old.a['states'].remove(st);target.a['states'].append(st);st.a['owner']=target;st.a['controller']=target;self.trace.append(('transfer',st.a['state_region'].name,old.name,target.name))
 def call(self,k,actor):self.block(self.db[k],actor,actor)
 def block(self,n,o,root,prev=None):
  chain=None
  for x in n.children or []:
   if x.key=='if':
    chain=self.pred.block(x.get('limit'),o,root,prev)
    if chain:self.block(SimpleNamespace(children=[q for q in x.children if q.key!='limit']),o,root,prev)
   elif x.key=='else':
    assert chain is not None
    if not chain:self.block(x,o,root,prev)
    chain=None
   elif x.key=='else_if':
    assert chain is not None
    if not chain:
     yes=self.pred.block(x.get('limit'),o,root,prev)
     if yes:self.block(SimpleNamespace(children=[q for q in x.children if q.key!='limit']),o,root,prev)
     chain=yes
   else:chain=None;self.effect(x,o,root,prev)
 def effect(self,n,o,root,prev):
  k,v=n.key,n.value
  if k=='set_variable':
   name=v or n.scalar('name');o.a.setdefault('vars',set()).add(name);self.trace.append(('set_variable',o.name,name));return
  if k=='remove_variable':o.a.setdefault('vars',set()).discard(v);o.a.setdefault('variable_values',{}).pop(v,None);return
  if k=='remove_modifier':
   assert v in o.a.get('modifiers',set()),('remove absent modifier',o.name,v)
   o.a['modifiers'].remove(v);self.trace.append(('remove_modifier',o.name,v));return
  if k=='create_country':
   self.trace.append(('create_country',n.scalar('tag'),self.create_ok))
   if not self.create_ok:return
   target=Obj('country',n.scalar('tag'),states=[],vars=set(),tech=set(),is_country_alive=True)
   assert target.name not in self.w['countries'];self.w['countries'][target.name]=target
   st=self.pred.scope(n.scalar('state'),o,root,prev);assert st is not None;self.move(st,target);self.block(n.get('on_created'),target,root,o);return
  if k=='create_diplomatic_pact':
   self.trace.append(('create_pact',o.name,n.scalar('country'),self.pact_ok))
   if self.pact_ok:self.pred.scope(n.scalar('country'),o,root,prev).a['overlord']=o
   return
  if k=='set_state_owner':
   target=self.pred.scope(v,o,root,prev);assert target is not None;self.move(o,target);return
  if k=='add_journal_entry':o.a.setdefault('journals',set()).add(n.scalar('type'));return
  if k in ['set_country_type','set_social_hierarchy','copy_laws','activate_law','set_capital','nesnd_commission_inherit_technology']:
   self.trace.append(('native_not_simulated',k,o.name));return
  if k in self.db:self.block(self.db[k],o,root,prev);return
  link=self.pred.scope(k,o,root,prev)
  if link is None:
   if n.op=='?=':return
   raise AssertionError(('unhandled effect',k))
  self.block(n,link,root,o)

def cleanup_cases(rootdir):
 rows=[];mods=['nesnd_india_french_advisers','nesnd_india_french_teachers','nesnd_india_french_engineers','nesnd_india_french_officers']
 for active in [[],mods[:1],mods[:2],[mods[0],mods[2]],[mods[0],mods[3]],mods,mods[2:]]:
  w=world_from_history();o=w['countries']['MUG'];o.a['modifiers']=set(active);r=EffectTrace(w,rootdir)
  try:r.call('nesnd_india_remove_advisers',o);r.call('nesnd_india_remove_advisers',o);ok=not o.a['modifiers'];error=None
  except AssertionError as e:ok=False;error=str(e)
  rows.append({'active':active,'pass':ok,'error':error})
 return rows

def creation_cases():
 from test_commission_boundaries import direct_world,SOUTH
 rows=[]
 for slug,tag,cap in [('tianzhu','TZ1','STATE_MADRAS'),('yuanshan','YU1','STATE_ZULULAND')]:
  for create_ok,pact_ok in [(False,False),(True,False),(True,True)]:
   w=direct_world()
   if slug=='yuanshan':
    for region in SOUTH:captured(w,region)
   original=[(st,st.a['owner'].name) for r in w['regions'].values() for st in r.a['states']]
   trace=EffectTrace(w,create_ok=create_ok,pact_ok=pact_ok);o=w['countries']['USM'];trace.call('nesnd_establish_'+slug+'_commission',o)
   assert ('nesnd_'+slug+'_commission_established' in o.a['vars'])==(create_ok and pact_ok)
   assert all(st.a['owner'].name==owner for st,owner in original if owner!='USM'),('third-party moved',slug)
   transfers=[x for x in trace.trace if x[0]=='transfer']
   if not create_ok:assert not transfers
   elif not pact_ok:assert len(transfers)==2 and transfers[0][1]==cap and transfers[1][1]==cap and all(st.a['owner'].name==owner for st,owner in original)
   else:
    pact_index=next(i for i,x in enumerate(trace.trace) if x[0]=='create_pact')
    assert all(i>pact_index for i,x in enumerate(trace.trace) if x[0]=='transfer' and x[1]!=cap)
    size=len(trace.trace);trace.call('nesnd_establish_'+slug+'_commission',o);assert len(trace.trace)==size
   rows.append({'case':slug,'create_ok':create_ok,'pact_ok':pact_ok,'pass':True,'trace':trace.trace})
 return rows

def modifier_guards(rootdir,mutate=False):
 bad=[];sites=0
 def walk(n,guards):
  nonlocal sites
  if n.key=='remove_modifier':
   sites+=1
   if n.value not in guards:bad.append((path.name,n.start,n.value))
   return
  if n.key=='limit':return
  g=set(guards)
  if n.key=='if':
   lim=n.get('limit')
   if lim:g.update(x.value for x in lim.children if x.key=='has_modifier' and x.op=='=')
  if n.key and (n.key.startswith(('scope:','var:','c:','s:')) or n.key in ['owner','root','prev','every_scope_state','every_country','random_scope_state']):g=set()
  for child in n.children or []:walk(child,g)
 for folder in ['scripted_buttons','scripted_effects']:
  for path in (rootdir/'common'/folder).glob('nesnd_india*.txt'):
   t=parse(read(path))
   if mutate and path.name=='nesnd_india_diplomacy.txt' and folder=='scripted_effects':
    fn=t.get('nesnd_india_remove_advisers');first=next(x for x in fn.children if x.key=='if');fn.children[fn.children.index(first)]=first.get('remove_modifier')
   for fn in t.children:walk(fn,set())
 return {'sites':sites,'unguarded':bad}

def lost_india_fixture():
 w=world_from_history();o=w['countries']['MUG'];partner=w['countries']['FRA']
 for name in list(w['regions']):
  if any(st.a['owner'] is o for st in w['regions'][name].a['states']):captured(w,name,'FRA')
 region=Obj('state_region','STATE_OUTSIDE_INDIA',states=[]);w['regions'][region.name]=region
 other=Obj('strategic_region','region_elsewhere');w['strategic']={'region_elsewhere':other,'region_north_india':Obj('strategic_region','region_north_india'),'region_south_india':Obj('strategic_region','region_south_india')}
 st=Obj('state','outside:MUG',state_region=region,owner=o,controller=o,region=other,state_population=100000)
 region.a['states']=[st];o.a['states'].append(st)
 o.a['mods_before']={'nesnd_india_french_advisers','nesnd_india_french_teachers'};o.a['modifiers']=set(o.a['mods_before'])
 o.a['vars'].update(['nesnd_india_adviser_partner','nesnd_india_adviser_patron','nesnd_india_aid_lock'])
 o.a['variable_values']={'nesnd_india_adviser_partner':partner,'nesnd_india_adviser_patron':partner}
 return w,o

def geographic_exit(rootdir):
 w,o=lost_india_fixture();trace=EffectTrace(w,rootdir)
 on=parse(read(rootdir/'common/on_actions/nesnd_india_core.txt')).get('nesnd_india_maintenance')
 reached=trace.pred.block(on.get('trigger'),o,o)
 if reached:trace.call('nesnd_india_diplomacy_maintenance',o)
 monthly_clear=not o.a['modifiers'] and not any(k in o.a['vars'] for k in ['nesnd_india_adviser_partner','nesnd_india_adviser_patron'])
 w,o=lost_india_fixture();trace=EffectTrace(w,rootdir)
 je=parse(read(rootdir/'common/journal_entries/nesnd_india_diplomacy.txt')).get('nesnd_india_foreign')
 trace.block(je.get('on_invalid'),o,o)
 return {'monthly_dispatch_reachable':reached,'monthly_clears_advisers':monthly_clear,'journal_exit_clears_advisers':not o.a['modifiers'],'aid_lock_preserved': 'nesnd_india_aid_lock' in o.a['vars']}

if __name__=='__main__':
 before=cleanup_cases(B);after=cleanup_cases(C);create=creation_cases();guards=modifier_guards(C);mutant=modifier_guards(C,True)
 geo_before=geographic_exit(B);geo_after=geographic_exit(C)
 assert not geo_before['monthly_clears_advisers'] and not geo_before['journal_exit_clears_advisers']
 assert all(geo_after.values())
 status='PASS' if any(not x['pass'] for x in before) and all(x['pass'] for x in after+create) and not guards['unguarded'] and mutant['unguarded'] else 'FAIL'
 dump(R/'effect-boundaries.json',{'status':status,'geographic_exit_before':geo_before,'geographic_exit_after':geo_after,'cleanup_before':before,'cleanup_after':after,'creation_failure_injection':create,'same_scope_modifier_guard_audit':guards,'removed_guard_negative_control':mutant,'scope':'Actual AST control flow with fault-injected native API results; no engine callback or population simulation','engine_verified':False})
 print(status,len(after),'cleanup sequences',len(create),'creation scenarios',guards['sites'],'guarded removal sites')
