from qin_persia_build_support import *
from collections import defaultdict
# History cannot be assumed to run after formations. Capture actual initial barracks
# on day two (or the first live maintenance of an old save), exactly once.
p=C/'common/scripted_effects/nesnd_qe1_agendas.txt';s=read(p).replace('set_variable = { name = nesnd_qe1_barracks_goal value = { value = nesnd_qe1_barracks_total add = 25 } }','set_variable = { name = nesnd_qe1_barracks_goal value = 107 }\n set_variable = nesnd_qe1_barracks_snapshot_pending\n trigger_event = { id = nesnd_qe1.90 days = 1 popup = no }')
s+='''
nesnd_qe1_capture_barracks = {
 if = { limit = { nesnd_qe1_country = yes has_variable = nesnd_qe1_barracks_snapshot_pending NOT = { has_variable = nesnd_qe1_barracks_snapshot_done } game_date > 1836.1.1 }
  set_variable = { name = nesnd_qe1_barracks_base value = nesnd_qe1_barracks_total }
  set_variable = { name = nesnd_qe1_barracks_goal value = { value = var:nesnd_qe1_barracks_base add = 25 } }
  set_variable = nesnd_qe1_barracks_snapshot_done
  remove_variable = nesnd_qe1_barracks_snapshot_pending
 }
}
''';write(p,s)
p=C/'events/nesnd_qe1_agendas.txt';write(p,read(p)+'\nnesnd_qe1.90 = { type = country_event hidden = yes trigger = { nesnd_qe1_country = yes has_variable = nesnd_qe1_barracks_snapshot_pending } immediate = { nesnd_qe1_capture_barracks = yes } }\n')
p=C/'common/scripted_effects/nesnd_qin_persia_lifecycle.txt';s=read(p).replace('nesnd_qe1_initialize = yes','nesnd_qe1_initialize = yes\n nesnd_qe1_capture_barracks = yes',1);write(p,s)
p=C/'common/scripted_triggers/nesnd_qe1_campaign.txt';s=read(p).replace('limit = { has_variable = nesnd_qe1_barracks_goal }','limit = { has_variable = nesnd_qe1_barracks_goal has_variable = nesnd_qe1_barracks_snapshot_done }');write(p,s)
# Add valid native-region identity pools for later conquests. Existing36 detailed
# province-matched pools remain authoritative for the custom split states.
mapping=json.loads(read(R/'native-identity-map.json'));rows={x['region']:{**x,'return_pairs':[{**p,'weight':p.get('weight',p['native_reference_population'])} for p in x['pairs']]} for x in mapping['states']}
culture_defs={};native_cultures={}
for root in [G,B]:
 for p in (root/'common/cultures').glob('*.txt'):
  for n in parse(read(p)).children:
   key=n.key.split(':')[-1]
   culture_defs[key]=n
   if root==G:native_cultures[key]=n
effective_files={p.name:p for p in (G/'map_data/state_regions').glob('*.txt')};effective_files.update({p.name:p for p in (C/'map_data/state_regions').glob('*.txt')})
regions={n.key for p in effective_files.values() for n in parse(read(p)).children}
pools=defaultdict(lambda:defaultdict(int));sources=defaultdict(set)
for p in (G/'common/history/pops').glob('*.txt'):
 tree=parse(read(p))
 for region in tree.children[0].children:
  reg=region.key.removeprefix('s:')
  if reg not in regions or reg in rows:continue
  for pop in region.walk():
   if pop.key!='create_pop':continue
   cult=pop.scalar('culture');rel=pop.scalar('religion')
   if cult not in native_cultures or cult not in culture_defs:continue
   traits=culture_defs[cult].get('traditions');ts={a.value or a.key for a in traits.children or []} if traits else set()
   # Return identity uses the full native regional pool. Only assimilation is
   # restricted to non-Sinosphere cultures; these are different user requirements.
   rel=rel or native_cultures[cult].scalar('religion')
   if not rel:continue
   pools[reg][(cult,rel)]+=int(float(pop.scalar('size','0')));sources[reg].add(p.relative_to(G).as_posix())
for reg,pool in pools.items():
 if pool:rows[reg]={'region':reg,'return_pairs':[{'culture':cu,'religion':re,'weight':n} for (cu,re),n in sorted(pool.items()) if n>0],'basis':'native entire-region paired cultural references for future conquests; no ancestry inference','sources':sorted(sources[reg])}
eligible=[x for _,x in sorted(rows.items()) if x['return_pairs']]
p=C/'common/scripted_triggers/nesnd_qe1_identity.txt';s=read(p);n=parse(s).get('nesnd_qe1_decay_state');body='nesnd_qe1_decay_state = { owner = c:QE1 any_scope_pop = { culture = cu:ce_xiyu } OR = { '+' '.join('state_region = s:'+x['region'] for x in eligible)+' } }';write(p,s[:n.start]+body+s[n.end:])
p=C/'common/scripted_effects/nesnd_qe1_identity.txt';s=read(p);n=parse(s).get('nesnd_qe1_select_old_identity');body='nesnd_qe1_select_old_identity = {\n clear_saved_scope = nesnd_qe1_return_culture clear_saved_scope = nesnd_qe1_return_religion\n'
for i,row in enumerate(eligible):
 body+=('if' if i==0 else 'else_if')+f' = {{ limit = {{ state_region = s:{row["region"]} }} random_list = {{\n'
 for pair in row['return_pairs']:body+=f'{pair["weight"]} = {{ cu:{pair["culture"]} = {{ save_scope_as = nesnd_qe1_return_culture }} rel:{pair["religion"]} = {{ save_scope_as = nesnd_qe1_return_religion }} }}\n'
 body+='} }\n'
body+='if = { limit = { exists = scope:nesnd_qe1_return_culture exists = scope:nesnd_qe1_return_religion } nesnd_qe1_convert_selected_cohort = yes }\n}\n'
write(p,s[:n.start]+body+s[n.end:])
dump(R/'future-identity-pools.json',{'states':eligible,'count':len(eligible),'pairs':sum(len(x['return_pairs']) for x in eligible),'assimilation_filter':'non-Sinosphere only','return_filter':'all valid native regional culture/religion pairs','game_launched':False})
print('One-time post-load military snapshot and',len(eligible),'native identity pools generated.')
