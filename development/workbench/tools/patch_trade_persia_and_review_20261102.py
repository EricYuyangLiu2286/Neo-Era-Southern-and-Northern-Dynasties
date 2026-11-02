from maintenance_20261102_context import *
import re
# CNE conditional prose must not treat optional-scope absence as affirmative.
p=C/'common/scripted_triggers/nesnd_cne_programs.txt';write(p,read(p)+'''nesnd_cne_republic_is_fighting = {
 trigger_if = { limit = { exists = c:NRP exists = c:CNE } c:NRP = { has_war_with = c:CNE } }
 trigger_else = { always = no }
}
nesnd_cne_confidence_is_waning = {
 trigger_if = { limit = { has_variable = nesnd_cne_confidence } var:nesnd_cne_confidence < 750 }
 trigger_else = { always = no }
}
''')
p=C/'common/journal_entries/nesnd_cne_confidence.txt';s=read(p).replace('c:NRP ?= { has_war_with = root }','nesnd_cne_republic_is_fighting = yes').replace('has_variable = nesnd_cne_confidence var:nesnd_cne_confidence < 750','nesnd_cne_confidence_is_waning = yes');write(p,s)
p=C/'common/scripted_triggers/nesnd_poland_repairs.txt';s=read(p).replace('nesnd_poland_can_issue_ultimatum = {','nesnd_poland_can_issue_ultimatum = {\n c:KRA ?= { is_subject = no is_diplomatic_play_committed_participant = no }',1).replace('owner = {\n   NOR','owner = {\n   is_at_war = no\n   NOR',1).replace('state_region = { has_claim_by = c:KRA }','has_claim_by = c:KRA');write(p,s)
replace_def('common/scripted_triggers/nesnd_poland_repairs.txt','nesnd_poland_existing_successor','''nesnd_poland_existing_successor = {
 trigger_if = { limit = { exists = c:POL } c:POL = { is_subject = no num_incorporated_states >= 3 } }
 trigger_else_if = { limit = { exists = c:PLC } c:PLC = { is_subject = no num_incorporated_states >= 3 } }
 trigger_else = { always = no }
}''')
# Both possible successors must be evaluated independently; existence of an
# unqualified POL must not hide an eligible PLC.
replace_def('common/scripted_triggers/nesnd_poland_repairs.txt','nesnd_poland_existing_successor','''nesnd_poland_existing_successor = {
 OR = { nesnd_poland_existing_pol = yes nesnd_poland_existing_plc = yes }
}
nesnd_poland_existing_pol = {
 trigger_if = { limit = { exists = c:POL } c:POL = { is_subject = no num_incorporated_states >= 3 } }
 trigger_else = { always = no }
}
nesnd_poland_existing_plc = {
 trigger_if = { limit = { exists = c:PLC } c:PLC = { is_subject = no num_incorporated_states >= 3 } }
 trigger_else = { always = no }
}''')
p=C/'common/scripted_triggers/nesnd_poland_repairs.txt';write(p,read(p)+'''nesnd_poland_many_claims = {
 trigger_if = { limit = { has_global_variable = ce_polish_claim_state_count } global_var:ce_polish_claim_state_count >= 3 }
 trigger_else = { always = no }
}
''')
p=C/'common/scripted_progress_bars/ce_poland_progress_bars.txt';s=read(p);tree=parse(s)
for n in sorted([x for x in tree.walk() if x.key=='limit' and any(a.key=='global_var:ce_polish_claim_state_count' and a.op=='>=' and a.value=='3' for a in x.children or [])],key=lambda n:n.start,reverse=True):s=s[:n.start]+'limit = { nesnd_poland_many_claims = yes }'+s[n.end:]
write(p,s)
# Values use their actual units: country influence capacity; direct relation points.
modpaths=list((C/'common/static_modifiers').glob('*.txt'))
changed=[]
for p in modpaths:
 s=read(p);tree=parse(s);out=s
 for n in tree.children[::-1]:
  if n.key=='nesnd_supply_envoys':out=out[:n.start]+s[n.start:n.end].replace('country_influence_add = -15','country_influence_add = -100')+out[n.end:];changed.append(n.key)
  if n.get('country_influence_add') and n.scalar('country_influence_add')=='25' and 'supply' in n.key:
   out=out[:n.start]+s[n.start:n.end].replace('country_influence_add = 25','country_influence_add = 100')+out[n.end:];changed.append(n.key)
 if out!=s:write(p,out)
assert 'nesnd_supply_envoys' in changed and len(changed)==2,changed
p=C/'common/scripted_buttons/nesnd_supply_buttons.txt';s=read(p).replace('influence >= 15','influence >= 100')
tree=parse(s)
# One 3-month reply must fit inside its 4-month request lock, including 7-day travel.
for n in sorted([x for x in tree.walk() if x.key=='set_variable' and x.scalar('name')=='nesnd_supply_pending'],key=lambda x:x.start,reverse=True):
 body=s[n.start:n.end];body=re.sub(r'days\s*=\s*30','months = 4',body);s=s[:n.start]+body+s[n.end:]
write(p,s)
p=C/'events/nesnd_supply_events.txt';s=read(p);n=parse(s).get('nesnd_supply.1');rel=next(x for x in n.walk() if x.key=='change_relations')
replacement='''if = { limit = { NOT = { has_variable = nesnd_supply_first_contact_rewarded } }
 set_variable = nesnd_supply_first_contact_rewarded
 change_relations = { country = root value = 25 }
}''';s=s[:rel.start]+replacement+s[rel.end:];write(p,s)
# Historical relation only: no recurring script that re-subjugates a later independent Persia.
p=C/'common/history/diplomacy/ce_subject_relationships.txt';s=read(p);n=next(x for x in parse(s).walk() if x.key=='c:QE1');s=s[:n.end-1]+'''\n if = { limit = { exists = c:PER } create_diplomatic_pact = { country = c:PER type = tributary } }
 set_variable = nesnd_qe1_per_relation_v1
'''+s[n.end-1:];write(p,s)
p=C/'common/history/treaties/ce_historical_treaties.txt';s=read(p);tree=parse(s);treaty=next(x for x in tree.walk() if x.key=='create_treaty' and x.scalar('name')=='treaty_name_state_of_persia_protectorate')
article=next(x for x in treaty.walk() if x.scalar('article')=='defensive_pact');s=s[:article.start]+s[article.end:];write(p,s)
# Update the existing text definitions; don't add a second explanatory effect line.
for lang in ['simp_chinese','english']:
 for p in (C/f'localization/{lang}').rglob('*.yml'):
  s=read(p);out=s
  for m in re.finditer(r'^ (nesnd_supply[^:]*):.*$',s,re.M):
   line=m.group(0);key=m.group(1);new=line
   if key=='nesnd_supply_accept_tt':new=f' {key}:0 "'+('建立通商联络。' if lang=='simp_chinese' else 'Establish commercial contact.')+'"'
   elif key=='nesnd_supply_invitation_tt':new=f' {key}:0 "'+('商使将在七日后抵达；本次使团任期六个月。' if lang=='simp_chinese' else 'The envoys arrive in seven days and serve for six months.')+'"'
   else:
    if ('15' in line and ('影响力' in line or 'influence' in line.lower())):new=new.replace('15','100')
    if ('25' in line and ('影响力' in line or 'influence' in line.lower())):new=new.replace('25','100')
   if new!=line:out=out.replace(line,new)
  if out!=s:write(p,out)
print('Trade capacity scaled; one-time relation bonus; Persia tributary history; review guard fixes written')
