from native_extract import G,W,rd,loc,tree
import json,hashlib,collections,re
p=W/'native-inventory.json';d=json.loads(p.read_text(encoding='utf8'))
sources={s['path']:s for s in d['sources']}
def addsource(rel):
 q=G/rel;sources[str(q)]={'path':str(q),'sha256':hashlib.sha256(q.read_bytes()).hexdigest()}
def rows(rel,ids=None):
 t,r=rd(rel);addsource(rel)
 return [{**loc(rel,t,n),'id':n.key,'data':tree(n),'source':t[n.start:n.end]} for n in r.children if n.children is not None and (ids is None or n.key in ids)]
for rel in ['common/journal_entries/00_liberalism.txt','common/journal_entries/00_fascism.txt','common/journal_entries/01_coup.txt','common/journal_entries/03_korea.txt']:
 d['journal_entries']+=rows(rel)
for rel in ['events/liberalism.txt','events/fascism_events.txt','events/coup_events.txt','events/gg_korea_events.txt']:
 if (G/rel).exists():d['events']+=rows(rel)
d['support_definitions']=[]
# Economically activated PMs: all their actual database definitions, preserving order.
pmkeys={pm for v in d['economic_inputs'].values() for b in v.get('buildings',[]) for pm in b['pms']}
pmkeys |= {'pm_no_organization','pm_samurai_training'}
for f in (G/'common/production_methods').glob('*.txt'):
 t,r=rd(f.relative_to(G).as_posix());hits=[n.key for n in r.children if n.key in pmkeys]
 if hits:d['support_definitions']+=rows(f.relative_to(G).as_posix(),hits)
paths=['common/scripted_effects/00_victoria_ep2_scripted_effects.txt','common/scripted_effects/00_victoria_heir_generation.txt','common/scripted_effects/00_sgui_effects.txt','common/scripted_triggers/00_ep2_victoria_scripted_triggers.txt','common/script_values/ep2_japan_values.txt','common/scripted_buttons/ryukyu_rivalry_buttons.txt','common/decisions/japan_decisions.txt','common/decisions/japan_shinto.txt','common/scripted_progress_bars/00_ep2_ryukyu_rivalry_progress_bars.txt','common/company_types/00_companies_japan.txt']
for rel in paths:d['support_definitions']+=rows(rel)
for rel,ids in {
 'common/scripted_effects/00_victoria_royal_successions.txt':['character_japan_ruler_succession_chain_effect','character_japan_imperial_succession_chain_effect'],
 'common/scripted_effects/00_starting_pop_wealth.txt':['effect_starting_pop_wealth_medium'],
 'common/scripted_effects/00_starting_pop_literacy.txt':['effect_starting_pop_literacy_middling'],
 'common/scripted_effects/00_starting_inventions.txt':['effect_starting_technology_tier_4_tech'],
 'common/laws/00_distribution_of_power.txt':['law_bakufu'],
 'common/laws/01_trade_policy.txt':['law_sakoku'],
 'common/laws/00_army_model.txt':['law_warrior_caste'],
 'common/laws/01_education_system.txt':['law_terakoya'],
 'common/laws/00_caste_hegemony.txt':['law_intermediate_edo_system'],
 'common/laws/00_citizenship.txt':['law_subjecthood'],
 'common/country_definitions/00_countries.txt':['JAP']}.items():d['support_definitions']+=rows(rel,ids)
for rel in ['common/on_actions/00_code_on_actions.txt','common/on_actions/00_on_actions_monthly.txt','common/on_actions/00_on_actions_yearly.txt','common/history/countries/jap - japan.txt','common/history/characters/jap - japan.txt','common/history/population/jap - japan.txt','common/history/states/00_states.txt','common/script_values/event_values.txt','common/history/diplomacy/00_subject_relationships.txt','common/history/diplomacy/00_relations.txt','gui/journal_entry_widgets/ep2_japan_widgets.gui']:
 addsource(rel)
# state ownership records: distinguish country/state from whole region potential.
t,r=rd('common/history/states/00_states.txt');r=r.get('STATES')
for st in r.children:
 if st.key[2:] in d['economic_inputs']:
  d['economic_inputs'][st.key[2:]]['state_history']={**loc('common/history/states/00_states.txt',t,st),'owners':[{'country':n.scalar('country'),'state_type':n.scalar('state_type','default'),'province_count':len(n.get('owned_provinces').values())} for n in st.all('create_state')]}
d['sources']=sorted(sources.values(),key=lambda v:v['path'])
# References expose each direct caller, not a guessed execution sequence. Edges retain repeated calls.
byid=collections.defaultdict(list)
allrows=d['journal_entries']+d['events']+d['buttons']+d['support_definitions']
for row in allrows:byid[row['id']].append(row)
edge=[]
for row in allrows:
 t,r=__import__('pdx').read(G/row['path']);n=next(x for x in r.children if x.key==row['id'])
 for x in n.walk():
  target=None;kind=None
  if x.key=='trigger_event':target=x.scalar('id');kind='event'
  elif x.key=='add_journal_entry':target=x.scalar('type');kind='add_je'
  elif x.key=='scripted_button':target=__import__('pdx').unquote(x.value);kind='button'
  elif x.key in byid and x.key!=row['id']:target=x.key;kind='script_call'
  if target:edge.append({'caller':row['id'],'kind':kind,'target':target,**loc(row['path'],t,x),'target_locations':[{k:z[k] for k in ['path','line','end_line']} for z in byid.get(target,[])]})
d['direct_reference_edges']=edge
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print('extended',len(d['journal_entries']),'JEs',len(d['events']),'events',len(d['support_definitions']),'support defs',len(edge),'edges',len(d['sources']),'source files')
