from commission_context import *
checks=[]
def ck(k,v):checks.append({'name':k,'pass':bool(v)})
def has(n,k,v=None,op=None):return any(x.key==k and (v is None or x.value==v) and (op is None or x.op==op) for x in n.walk())
# Effective native+MOD military paths, preserving every repeated unit declaration.
paths={}
for folder in [G,C]:
 for p in (folder/'common/history/military_formations').glob('*.txt'):paths[p.name.lower()]=p
units=[]
for p in paths.values():
 for n in parse(read(p)).walk():
  if n.key=='c:MUG':
   for q in n.walk():
    if q.key=='combat_unit':units.append({'path':str(p),'count':q.scalar('count'),'type':q.scalar('type')})
ck('Actual effective MUG declarations total40',sum(int(x['count']) for x in units)==40)
ck('Native3 really loaded',any('05_military_formations_india.txt' in x['path'] for x in units) and sum(int(x['count']) for x in units if '05_military_formations_india.txt' in x['path'])==3)
ck('Author new37 really loaded',sum(int(x['count']) for x in units if 'nesnd_mughal_armies.txt' in x['path'])==37)
# Literal recruitment comparator and same-branch guard, not just a string's existence.
effects=parse(read(C/'common/scripted_effects/nesnd_india_uprising.txt'))
for fn in [n for n in effects.children if n.key and n.key.endswith('_launch')]:
 def walk(n,zero_guard=False):
  if n.key=='if':zero_guard=zero_guard or (n.get('limit') is not None and has(n.get('limit'),'army_size','1','<'))
  if n.key=='create_military_formation':ck(fn.key+' zero-army ancestor',zero_guard)
  for ch in n.children or []:
   if ch.key!='limit':walk(ch,zero_guard)
 walk(fn)
# Exact admission callable shared by decisions, buttons and execution; entry shared by JE/initializer.
trig=parse(read(C/'common/scripted_triggers/nesnd_commissions.txt'));exp=parse(read(C/'common/scripted_triggers/nesnd_commission_expansion.txt'))
for slug,tag in [('tianzhu','TZ1'),('yuanshan','YU1')]:
 key='nesnd_'+slug+'_commission_ready'
 decision=parse(read(C/'common/decisions/nesnd_commissions.txt')).get('nesnd_establish_'+slug)
 button=parse(read(C/'common/scripted_buttons/nesnd_commissions.txt')).get('nesnd_establish_'+slug+'_button')
 effect=parse(read(C/'common/scripted_effects/nesnd_commissions.txt')).get('nesnd_establish_'+slug+'_commission')
 ck(slug+' decision same predicate',has(decision.get('possible'),key,'yes','='))
 ck(slug+' button same predicate',has(button.get('possible'),key,'yes','='))
 ck(slug+' execution guarded before all mutations',len(effect.children)==1 and effect.children[0].key=='if' and has(effect.children[0].get('limit'),key,'yes','='))
 ck(slug+' root-independent realm helpers',not any(n.value=='root' for h in ['nesnd_commission_owner_in_realm','nesnd_commission_indian_prince'] for n in exp.get(h).walk()))
 ck(slug+' late technology',has(trig.get(key),'has_technology_researched','civilizing_mission'))
 ready=trig.get(key);ck(slug+' seed population positive',any(n.key=='state_population' and n.op=='>' and n.value=='0' for n in ready.walk()))
# Bound all handover states to USM; transferring direct subjects' land is never a side effect of counting them.
allowed=json.loads(read(R/'implemented.json'))
fn=parse(read(C/'common/scripted_effects/nesnd_commissions.txt')).get('nesnd_establish_tianzhu_commission');transfers=[]
def transfer_walk(n,scope_key=None):
 if n.key and n.key.startswith('s:'):scope_key=n.key
 if n.key=='set_state_owner' and n.value=='c:TZ1':transfers.append(scope_key)
 for ch in n.children or []:transfer_walk(ch,scope_key)
transfer_walk(fn)
ck('Tianzhu cedes24 explicit USM pieces after seed',len(transfers)==24 and all(x.endswith('.region_state:USM') for x in transfers))
ck('Handover includes all new Indian conquests',set(x[2:].split('.')[0] for x in transfers)==set(allowed['tianzhu_transfer'])-{'STATE_MADRAS'})
finite=parse(read(C/'common/journal_entries/nesnd_commissions.txt')).get('nesnd_tianzhu_governance');permanent=parse(read(C/'common/journal_entries/nesnd_india_core.txt')).get('nesnd_india_usm')
ck('Suppression is unique permanent entry',len(finite.all('scripted_button'))==0 and len(permanent.all('scripted_button'))==6)
bm,cm=man(B),man(C);changed={p:h for p,h in cm.items() if bm.get(p)!=h}
ck('No previous data deleted',not bm.keys()-cm.keys())
ck('Historical population/buildings/maps/characters unchanged',not any(p.startswith(('map_data/','gfx/','common/history/','common/character_templates/')) for p in changed))
ck('Main still preserved pending merge',man(M)==bm)
for report in ['boundary-cases.json','effect-boundaries.json','request-boundaries.json','mcp-final.json']:ck(report,json.loads(read(R/report))['status']=='PASS')
ck('No new Tiger diagnostics',not json.loads(read(R/'tiger-added.json')))
status='STATIC_PASS' if all(x['pass'] for x in checks) else 'FAIL';dump(R/'contract-validation.json',{'status':status,'checks':checks,'effective_MUG_units':units,'files':changed,'engine_verified':False});print(status,len(checks),[x['name'] for x in checks if not x['pass']])
