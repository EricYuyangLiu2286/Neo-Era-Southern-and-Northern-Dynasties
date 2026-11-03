from commission_context import *
data=json.loads(read(R/'native-starting-regions.json'));mainland=data['mainland_regions'];princes=data['living_princes']
prince_regions=[row['region'] for row in data['rows'] if any(st['tag'] in princes for st in row['states'])]
heartlands=['STATE_DELHI','STATE_AGRA','STATE_BIHAR','STATE_WEST_BENGAL','STATE_EAST_BENGAL','STATE_BOMBAY']
south=['STATE_CAPE_COLONY','STATE_EASTERN_CAPE','STATE_NORTHERN_CAPE','STATE_ZULULAND','STATE_VRYSTAAT','STATE_TRANSVAAL']
transfer=mainland+['STATE_CEYLON','STATE_INDIAN_OCEAN_TERRITORY']
def group(key,names):return key+' = { OR = { '+' '.join('this = s:'+x for x in names)+' } }\n'
extra=group('nesnd_tianzhu_mainland_region',mainland)+group('nesnd_tianzhu_princely_region',prince_regions)+group('nesnd_tianzhu_mughal_heartland',heartlands)+group('nesnd_tianzhu_transfer_region',transfer)+group('nesnd_yuanshan_target_region',south)
extra+='''# Country scope; only actual ownership and a direct subject relationship count.
nesnd_commission_owner_in_realm = {
 is_country_alive = yes
 OR = {
  this = root
  AND = {
   trigger_if = { limit = { is_subject = yes exists = overlord } overlord = root }
   trigger_else = { always = no }
  }
 }
}
# Region scope: outer any_state_region counts each region once, even when several members share it.
nesnd_commission_region_controlled = {
 any_scope_state = { state_population > 0 is_largest_state_in_region = yes owner = { nesnd_commission_owner_in_realm = yes } }
}
# Full legal ownership excludes a Mughal or third-country remainder; occupation is insufficient.
nesnd_commission_region_fully_controlled = {
 any_scope_state = { state_population > 0 }
 NOT = { any_scope_state = { NOT = { owner = { nesnd_commission_owner_in_realm = yes } } } }
}
nesnd_commission_indian_prince = {
 OR = { '''+' '.join('c:'+t+' ?= this' for t in princes)+''' }
 is_country_alive = yes
 trigger_if = { limit = { is_subject = yes exists = overlord } overlord = root }
 trigger_else = { always = no }
 any_scope_state = { state_population > 0 state_region = { nesnd_tianzhu_mainland_region = yes } }
}
'''
for slug,reg in [('tianzhu','nesnd_tianzhu_transfer_region'),('yuanshan','nesnd_yuanshan_target_region')]:
 extra+=f'''nesnd_{slug}_commission_entry = {{
 nesnd_{slug}_commission_available = yes
 has_technology_researched = civilizing_mission
 any_state_region = {{ {reg} = yes nesnd_commission_region_controlled = yes }}
}}
'''
write(C/'common/scripted_triggers/nesnd_commission_expansion.txt',extra)
replace_node('common/scripted_triggers/nesnd_commissions.txt','nesnd_tianzhu_region','nesnd_tianzhu_region = { state_region = { nesnd_tianzhu_transfer_region = yes } }')
for slug,capital,count,reg in [('tianzhu','MADRAS',12,'nesnd_tianzhu_mainland_region'),('yuanshan','ZULULAND',4,'nesnd_yuanshan_target_region')]:
 rest=''
 if slug=='tianzhu':rest='''
 custom_tooltip = { text = nesnd_tianzhu_princes_required_tt
  OR = {
   any_country = { count >= 3 nesnd_commission_indian_prince = yes }
   any_state_region = { count >= 3 nesnd_tianzhu_princely_region = yes nesnd_commission_region_fully_controlled = yes }
  }
 }
 custom_tooltip = { text = nesnd_tianzhu_mughal_required_tt
  any_state_region = { count >= 2 nesnd_tianzhu_mughal_heartland = yes nesnd_commission_region_fully_controlled = yes }
 }
'''
 text=f'''nesnd_{slug}_commission_ready = {{
 hidden_trigger = {{ nesnd_{slug}_commission_available = yes NOT = {{ has_variable = nesnd_{slug}_commission_cooldown }} }}
 is_subject = no is_at_war = no is_active_in_diplomatic_play = no
 has_technology_researched = democracy
 has_technology_researched = civilizing_mission
 custom_tooltip = {{ text = nesnd_{slug}_regions_required_tt
  any_state_region = {{ count >= {count} {reg} = yes nesnd_commission_region_controlled = yes }}
 }}
 {rest}
 any_scope_state = {{ state_region = s:STATE_{capital} state_population > 0 any_scope_building = {{ is_building_type = building_port level >= 1 }} }}
 any_scope_state = {{ nesnd_{slug}_region = yes any_scope_building = {{ is_building_type = building_government_administration level >= 1 }} }}
}}'''
 replace_node('common/scripted_triggers/nesnd_commissions.txt','nesnd_'+slug+'_commission_ready',text)
 # Shared entry for country startup, inactive display, actual addition, buttons, and decisions.
 for rel in ['common/journal_entries/nesnd_commissions.txt','common/scripted_effects/nesnd_india_core.txt']:
  p=C/rel;s=read(p);s=s.replace('nesnd_'+slug+'_commission_available = yes any_scope_state = { nesnd_'+slug+'_region = yes }','nesnd_'+slug+'_commission_entry = yes');write(p,s)
 for rel in ['common/decisions/nesnd_commissions.txt','common/scripted_buttons/nesnd_commissions.txt']:
  p=C/rel;s=read(p).replace('nesnd_'+slug+'_commission_available = yes','nesnd_'+slug+'_commission_entry = yes');write(p,s)
 rel='common/journal_entries/nesnd_commissions.txt';p=C/rel;s=read(p);n=parse(s).get('nesnd_'+slug+'_commission').get('invalid');s=s[:n.start]+f'invalid = {{ NOT = {{ has_variable = nesnd_{slug}_commission_established }} NOT = {{ nesnd_{slug}_commission_entry = yes }} }}'+s[n.end:];write(p,s)
# Creation transfers the full bounded Indian area, including newly acquired Mughal provinces; princes remain USM subjects.
p=C/'common/scripted_effects/nesnd_commissions.txt';s=read(p);n=parse(s).get('nesnd_establish_tianzhu_commission');part=s[n.start:n.end]
old=['STATE_CIRCARS','STATE_KURNOOL','STATE_MYSORE','STATE_TRAVANCORE','STATE_GUJARAT','STATE_CEYLON','STATE_INDIAN_OCEAN_TERRITORY']
needle='s:STATE_CIRCARS = { nesnd_india_migrate_commission_case = yes }'
more=''.join(f'if = {{ limit = {{ exists = s:{x}.region_state:USM }} s:{x}.region_state:USM = {{ set_state_owner = c:TZ1 }} }}\n' for x in transfer if x not in old+['STATE_MADRAS'])
part=part.replace(needle,more+needle);s=s[:n.start]+part+s[n.end:];write(p,s)
replace_node('common/scripted_triggers/nesnd_india_core.txt','nesnd_india_usm_region','nesnd_india_usm_region = { state_region = { nesnd_tianzhu_transfer_region = yes } }')
# Remove duplicate suppression from the finite reward JE; the permanent provincial JE owns these buttons.
p=C/'common/journal_entries/nesnd_commissions.txt';s=read(p);n=parse(s).get('nesnd_tianzhu_governance');deletes=n.all('scripted_button')
for d in sorted(deletes,key=lambda x:x.start,reverse=True):s=s[:d.start]+s[d.end:]
write(p,s)
# Modifier absence is normal during pause/expiry/read-only cleanup. Guard at the exact modifier-owning scope.
removed=[]
for p in list((C/'common/scripted_effects').glob('nesnd_india*.txt'))+list((C/'common/scripted_buttons').glob('nesnd_india*.txt')):
 s=read(p);nodes=[n for n in parse(s).walk() if n.key=='remove_modifier' and n.value]
 for n in sorted(nodes,key=lambda n:n.start,reverse=True):
  s=s[:n.start]+f'if = {{ limit = {{ has_modifier = {n.value} }} remove_modifier = {n.value} }}'+s[n.end:]
  removed.append({'file':p.relative_to(C).as_posix(),'modifier':n.value})
 if nodes:write(p,s)
# Loss of India's last state must close advisers immediately; a short maintenance fallback reaches old-save residue.
p=C/'common/journal_entries/nesnd_india_diplomacy.txt';s=read(p).replace('on_invalid = { nesnd_india_clear_request = yes }','on_invalid = { nesnd_india_clear_request = yes nesnd_india_remove_advisers = yes }');write(p,s)
p=C/'common/scripted_effects/nesnd_india_diplomacy.txt';s=read(p);n=parse(s).get('nesnd_india_diplomacy_maintenance');s=s[:n.vstart+1]+'''\n if = { limit = { NOT = { nesnd_india_diplomacy_live = yes } } nesnd_india_clear_request = yes nesnd_india_remove_advisers = yes }
'''+s[n.vstart+1:];write(p,s)
p=C/'common/on_actions/nesnd_india_core.txt';s=read(p).replace('nesnd_india_country = yes c:USM ?= this c:YU1 ?= this c:TZ1 ?= this','nesnd_india_country = yes c:USM ?= this c:YU1 ?= this c:TZ1 ?= this has_variable = nesnd_india_request_partner has_variable = nesnd_india_adviser_partner has_modifier = nesnd_india_french_advisers');write(p,s)
# Necessary custom counts are each a separate check, not one large opaque condition.
texts={
'nesnd_tianzhu_regions_required_tt':('本国及直属国控制至少12个印度大陆地区的最大份额；同一地区只计一次。','We and our direct subjects hold the largest state in at least 12 mainland Indian regions. Each region counts once.'),
'nesnd_tianzhu_princes_required_tt':('至少3个印度土邦直属本国，或已完整控制至少3个土邦原辖地区。','At least three Indian princely states are our direct subjects, or we fully control at least three regions formerly held by the princes.'),
'nesnd_tianzhu_mughal_required_tt':('本国及直属国完整控制以下至少2个莫卧儿腹地：德里、阿格拉、比哈尔、东孟加拉、西孟加拉、孟买。','We and our direct subjects fully control at least two Mughal heartland regions: Delhi, Agra, Bihar, East Bengal, West Bengal or Bombay.'),
'nesnd_yuanshan_regions_required_tt':('本国及直属国控制至少4个南非地区的最大份额；同一地区只计一次。','We and our direct subjects hold the largest state in at least four South African regions. Each region counts once.'),
}
for lang,idx in [('simp_chinese',0),('english',1)]:
 p=C/'localization'/lang/'replace'/f'zzzzzzzzzzzzzz_nesnd_india_l_{lang}.yml';s=read(p)
 for k,pair in texts.items():assert not re.search(r'(?m)^\s*'+k+':',s);s+=f' {k}:0 "{pair[idx]}"\n'
 key='nesnd_establish_tianzhu_tt';v=['将本国在印度与相关岛屿的直辖领地划归天竺宣慰司，建立[concept_puppet]关系。各土邦仍直属本国。','Transfer our directly held Indian possessions and associated islands to the Tianzhu Commission as a [concept_puppet]. The princely states remain our direct subjects.'][idx]
 s=re.sub(r'(?m)^(\s*'+key+r':\d*\s+)".*"$',lambda m:m[1]+'"'+v+'"',s);write(p,s)
dump(R/'implemented.json',{'mainland':mainland,'prince_regions':prince_regions,'princes':princes,'mughal_heartlands':heartlands,'south_africa':south,'tianzhu_transfer':transfer,'thresholds':{'tianzhu_regions':12,'princes_or_regions':3,'mughal_heartlands':2,'yuanshan_regions':4},'guarded_modifier_removals':removed,'direct_subjects_retained':True,'engine_verified':False})
print('Expansion gates, bounded transfers and cleanup fixes applied; guarded removal sites',len(removed))
