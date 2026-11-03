from india_context import *
# Native source only; safety repairs do not rebalance achieved gameplay.
def wrap_tail(rel,fn,needle,conditions):
 p=C/rel;s=read(p);n=parse(s).get(fn);pos=s.index(needle,n.start,n.end)
 parent=min([x for x in n.walk() if x.children is not None and x.vstart<pos<x.vend],key=lambda x:x.vend-x.vstart)
 tail=s[pos:parent.vend-1];write(p,s[:pos]+'if = { limit = { '+conditions+' }\n'+tail+'\n}\n'+s[parent.vend-1:])
wrap_tail('common/scripted_effects/nesnd_india_diplomacy.txt','nesnd_india_clear_request','var:nesnd_india_request_partner = {','exists = scope:india_request_cleanup_owner')
wrap_tail('common/scripted_effects/nesnd_india_uprising.txt','nesnd_india_contact_release_sponsor','var:nesnd_india_case_sponsor = {','exists = scope:india_cleanup_region')
p=C/'common/scripted_effects/nesnd_india_uprising.txt';s=read(p)
# Stable case eligibility is distinct from transient capacity to advance/launch.
s=s.replace('var:nesnd_india_case_sponsor = { nesnd_india_uprising_strength = yes }','var:nesnd_india_case_sponsor = { nesnd_india_empire = yes }')
# Aborted case does not receive the survived-war award.
s=s.replace('c:IR1 ?= { set_variable = nesnd_india_revolt_resolved }','c:IR1 ?= { set_variable = nesnd_india_revolt_resolved }')
for i,region in enumerate(['CIRCARS','KURNOOL','MADRAS','MYSORE','TRAVANCORE','GUJARAT'],1):
 tag='IR'+str(i);fn='nesnd_india_'+region.lower()+'_create_play';n=parse(s).get(fn);s=s[:n.vstart+1]+'\n clear_saved_scope = india_case_backer\n'+s[n.vstart+1:]
 # first resolved call belongs to stage4 abort, second to actual previously registered DP end.
 n=parse(s).get('nesnd_india_'+region.lower()+'_maintain');part=s[n.start:n.end];needle=f'c:{tag} ?= {{ set_variable = nesnd_india_revolt_resolved }}';assert part.count(needle)==2
 part=part.replace(needle,f'c:{tag} ?= {{ set_variable = nesnd_india_revolt_failed set_variable = nesnd_india_revolt_resolved }}',1)
 part=part.replace(needle,f'c:{tag} ?= {{ set_variable = nesnd_india_revolt_negotiation_ended set_variable = nesnd_india_revolt_resolved }}',1)
 s=s[:n.start]+part+s[n.end:]
write(p,s)
# Newly saved region/original-owner aliases and original-province comparisons guarded in each callback.
for region in ['CIRCARS','KURNOOL','MADRAS','MYSORE','TRAVANCORE','GUJARAT']:
 fn='nesnd_india_'+region.lower()+'_maintain';rel='common/scripted_effects/nesnd_india_uprising.txt'
 wrap_tail(rel,fn,'if = { limit = { var:nesnd_india_case_state = { owner = scope:india_case_region','exists = scope:india_case_region')
 wrap_tail(rel,fn,'if = { limit = { has_variable = nesnd_india_case_original_provinces','has_variable = nesnd_india_case_original_provinces')
 wrap_tail(rel,fn,'s:STATE_'+region+'.region_state:IR'+str(['CIRCARS','KURNOOL','MADRAS','MYSORE','TRAVANCORE','GUJARAT'].index(region)+1)+' = { set_state_owner','exists = scope:india_case_original_owner')
# Keep active case accessible through temporary military/legitimacy setbacks.
p=C/'common/scripted_triggers/nesnd_india_uprising.txt';s=read(p);n=parse(s).get('nesnd_india_uprising_available');old=s[n.start:n.end]
new='''nesnd_india_uprising_available = { nesnd_india_empire = yes OR = { has_variable = nesnd_india_contact_region AND = { nesnd_india_uprising_strength = yes OR = { '''+' '.join('nesnd_india_'+r.lower()+'_target = yes' for r in ['CIRCARS','KURNOOL','MADRAS','MYSORE','TRAVANCORE','GUJARAT'])+' } } } }'
s=s[:n.start]+new+s[n.end:]
s=s.replace('var:nesnd_india_case_sponsor = { in_default = no','var:nesnd_india_case_sponsor = { nesnd_india_uprising_strength = yes in_default = no');write(p,s)
# Pause is a stable state; no upkeep or progression until an explicit resume.
p=C/'common/scripted_effects/nesnd_india_uprising.txt';s=read(p);needle='change_variable = { name = nesnd_india_case_progress add = nesnd_india_case_monthly }';assert needle in s
s=s.replace(needle,'''if = { limit = { nesnd_india_case_stage_value = 1 NOT = { nesnd_india_case_can_advance = yes } }
 set_variable = { name = nesnd_india_case_stage value = 2 }
 var:nesnd_india_case_sponsor ?= { remove_modifier = nesnd_india_contact_cost }
}
'''+needle)
# Stage2 accessibility survives sponsor weakness; restarting requires real local viability.
write(p,s)
p=C/'common/scripted_buttons/nesnd_india_uprising.txt';s=read(p)
for n in sorted([x for x in parse(s).children if x.key.endswith(('_pause','_resume'))],key=lambda n:n.start,reverse=True):
 part=s[n.start:n.end].replace('nesnd_india_uprising_strength = yes','nesnd_india_empire = yes')
 if n.key.endswith('_resume'):
  region=n.key.removeprefix('nesnd_india_').removesuffix('_resume').upper()
  condition=f'''nesnd_india_uprising_strength = yes in_default = no NOT = {{ has_modifier = declared_bankruptcy }} is_at_war = no
 s:STATE_{region} = {{ trigger_if = {{ limit = {{ exists = var:nesnd_india_case_state }} var:nesnd_india_case_state = {{ nesnd_india_case_unrest = yes }} }} trigger_else = {{ always = no }} }}'''
  part=part.replace('possible = { always = yes }','possible = { '+condition+' }')
  # Same resume condition in execution's limit.
  pos=part.index('hidden_effect =');before,after=part[:pos],part[pos:];after=after.replace('limit = {','limit = { '+condition+' ',1);part=before+after
 s=s[:n.start]+part+s[n.end:]
write(p,s)
# Failed partial creation cannot complete a victory JE; outcomes mutually exclusive.
p=C/'common/journal_entries/nesnd_india_uprising.txt';s=read(p);s=s.replace('complete = { custom_tooltip = { text = nesnd_india_revolt_resolved_tt has_variable = nesnd_india_revolt_resolved } num_states >= 1 }','complete = { custom_tooltip = { text = nesnd_india_revolt_resolved_tt has_variable = nesnd_india_revolt_negotiation_ended NOT = { has_variable = nesnd_india_revolt_failed } } num_states >= 1 }\n fail = { has_variable = nesnd_india_revolt_failed }');write(p,s)
# Absolute bar sync reads the current country captured at call time, never an unrelated global root.
sync=''
for name,var,je,bar in [('schools','nesnd_india_schools_months_value','nesnd_india_schools','nesnd_india_schools_bar'),('industry','nesnd_india_industry_months_value','nesnd_india_industry','nesnd_india_industry_bar'),('dynasty','nesnd_india_dynasty','nesnd_india_society','nesnd_india_dynasty_bar'),('community','nesnd_india_community','nesnd_india_society','nesnd_india_community_bar'),('contact','nesnd_india_contact_progress','nesnd_india_uprising','nesnd_india_contact_bar')]:
 sync+=f'''nesnd_india_sync_{name} = {{
 save_scope_as = india_display_country
 if = {{ limit = {{ exists = scope:india_display_country has_journal_entry = {je} }}
  je:{je} = {{ set_bar_progress = {{ name = {bar} value = scope:india_display_country.{var} }} }}
 }}
}}
'''
 for rel in ['common/scripted_effects/nesnd_india_core.txt','common/scripted_effects/nesnd_india_uprising.txt']:
  p=C/rel;s=read(p);nodes=[n for n in parse(s).walk() if n.key=='je:'+je and n.get('set_bar_progress') and n.get('set_bar_progress').scalar('name')==bar]
  for n in sorted(nodes,key=lambda n:n.start,reverse=True):s=s[:n.start]+f'nesnd_india_sync_{name} = yes'+s[n.end:]
  write(p,s)
append('common/scripted_effects/nesnd_india_core.txt',sync)
p=C/'common/journal_entries/nesnd_india_core.txt';s=read(p)
for name in ['schools','industry']:
 n=parse(s).get('nesnd_india_'+name).get('immediate');s=s[:n.vend-1]+f' nesnd_india_sync_{name} = yes '+s[n.vend-1:]
n=parse(s).get('nesnd_india_society');s=s[:n.vend-1]+' immediate = { nesnd_india_initialize = yes nesnd_india_sync_dynasty = yes nesnd_india_sync_community = yes }\n'+s[n.vend-1:];write(p,s)
p=C/'common/journal_entries/nesnd_india_uprising.txt';s=read(p);n=parse(s).get('nesnd_india_uprising');s=s[:n.vend-1]+' immediate = { nesnd_india_sync_contact = yes }\n'+s[n.vend-1:];write(p,s)
# Contact start/end and suppression update the sponsor's visible bar immediately.
p=C/'common/scripted_effects/nesnd_india_uprising.txt';s=read(p);s=s.replace('remove_variable = nesnd_india_contact_region remove_modifier = nesnd_india_contact_cost','remove_variable = nesnd_india_contact_region remove_modifier = nesnd_india_contact_cost nesnd_india_sync_contact = yes')
for slug in ['circars','kurnool','madras','mysore','travancore','gujarat']:
 n=parse(s).get('nesnd_india_'+slug+'_start');s=s[:n.vend-1]+' nesnd_india_sync_contact = yes\n'+s[n.vend-1:]
write(p,s)
p=C/'common/scripted_buttons/nesnd_india_uprising.txt';s=read(p)
for n in sorted([n for n in parse(s).children if n.key.endswith('_suppress')],key=lambda n:n.start,reverse=True):
 part=s[n.start:n.end];region=[x for x in n.walk() if x.key and x.key.startswith('s:STATE_')][-1]
 part=part[:region.vend-1-n.start]+' var:nesnd_india_case_sponsor ?= { nesnd_india_sync_contact = yes } '+part[region.vend-1-n.start:]
 s=s[:n.start]+part+s[n.end:]
write(p,s)
# New aid buttons expose native recipient benefits, without requiring the requested effect to execute in preview.
p=C/'common/scripted_buttons/nesnd_india_diplomacy.txt';s=read(p)
for k,mod in [(1,'teachers'),(2,'engineers'),(3,'officers')]:
 n=parse(s).get('nesnd_india_request_'+str(k)).get('effect');s=s[:n.vstart+1]+f'\n show_as_tooltip = {{ add_modifier = {{ name = nesnd_india_french_{mod} months = 48 }} add_modifier = {{ name = nesnd_india_french_advisers months = 48 }} }}\n'+s[n.vstart+1:]
write(p,s)
print('Second review corrections applied')
