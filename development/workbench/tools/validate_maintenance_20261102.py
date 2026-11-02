"""Source/AST regression; optional real MCP protocol queries. Not an engine test."""
from maintenance_20261102_context import *
import collections,difflib,re,itertools,asyncio
rows=[];cache={}
def node(rel,key=None,root=C):
 k=(str(root),rel)
 if k not in cache:cache[k]=parse(read(root/rel))
 return cache[k].get(key) if key else cache[k]
def has(n,k,v=None):return any(a.key==k and (v is None or a.value==v) for a in n.walk())
def check(label,ok):rows.append({'name':label,'pass':bool(ok)});assert ok,label
def shape(n):return (n.key,n.op,n.value,tuple(shape(a) for a in n.children or []))
mb,mc=man(B),man(C);changed=sorted(r for r in mc if mb.get(r)!=mc[r]);check('main is unchanged from parent backup',man(M)==mb);check('no file deletions',not set(mb)-set(mc))
diff=[]
for rel in changed:
 if rel.endswith(('.txt','.yml','.md')):
  diff.extend(difflib.unified_diff(read(B/rel).splitlines(True) if (B/rel).exists() else [],read(C/rel).splitlines(True),fromfile='base/'+rel,tofile='candidate/'+rel))
 if rel.endswith('.txt'):check('changed source parses '+rel,bool(node(rel)))
 if rel.endswith('.yml'):check('localization BOM/header '+rel,(C/rel).read_bytes().startswith(b'\xef\xbb\xbf') and read(C/rel).startswith('l_'+('simp_chinese' if 'simp_chinese' in rel else 'english')+':'))
check('no map/pop/building/portrait changes',not any(r.startswith(('map_data/','gfx/','common/history/pops/','common/history/buildings/','common/genes/','common/ethnicities/')) for r in changed))
check('all dedicated Japan files exact bytes',all(mb[r]==mc[r] for r in mb if any(x in r.lower() for x in ['japan','jap_'])))
# All non-Poland definitions in mixed legacy files remain byte-independent AST equal.
for rel in ['common/on_actions/ce_code_on_actions.txt','common/journal_entries/ce_usm_the_last_days_of_ming.txt']:
 a,b=node(rel,root=B),node(rel);ed=[]
 for x in a.children:
  y=b.get(x.key)
  if not y or shape(x)!=shape(y):ed.append(x.key)
 dump(R/('mixed-'+Path(rel).stem+'.json'),{'changed_definitions':ed})
 if 'usm' in rel:check('only original parent USM JE mount changed',len(ed)==1 and not any('jap' in x.lower() for x in ed))

tr='common/scripted_triggers/nesnd_cne_programs.txt';foundation=node(tr,'nesnd_cne_urban_foundation')
check('urban foundation no wrapper',not has(foundation,'custom_tooltip'))
expected={'building_iron_mine':25,'building_coal_mine':40,'building_steel_mill':10,'building_tooling_workshop':30,'building_motor_industry':6,'building_logging_camp':60,'building_shipyard':12}
found={a.scalar('target')[3:]:int(a.scalar('value')) for a in foundation.all('country_has_building_type_levels')}
check('seven national industrial totals individually native',found==expected)
city=node(tr,'nesnd_cne_urban_centres_ready').get('any_scope_state');check('cities count5 and level5 separated',city.scalar('count')=='5' and city.get('state_has_building_type_levels').scalar('value')=='5' and not has(city,'country_has_building_type_levels'))
start=node(tr,'nesnd_cne_program_can_start');branch=start.get('trigger_if');check('start caution AI-only',branch.get('limit').scalar('is_ai')=='yes' and has(branch,'nesnd_cne_ai_program_safe','yes') and not start.get('bureaucracy'))
for key in ['nesnd_reform_can_invest','nesnd_reform_can_relieve']:
 n=node('common/scripted_triggers/nesnd_cne_reform.txt',key);check(key+' caution inside AI branch',n.get('trigger_if').get('limit').scalar('is_ai')=='yes' and not n.get('bureaucracy') and not n.get('NOT') is None)
check('USM has one mounted envoy action',sum(1 for p in (C/'common/journal_entries').glob('*.txt') for a in parse(read(p)).walk() if a.key=='scripted_button' and a.value in {'nesnd_federal_compact_button','nesnd_south_offer_accord'})==1)
check('confidence status guarded and conditional',has(node('common/journal_entries/nesnd_cne_confidence.txt'),'nesnd_cne_republic_is_fighting','yes') and has(node('common/journal_entries/nesnd_cne_confidence.txt'),'nesnd_cne_confidence_is_waning','yes'))
check('CNE confidence/economy runtime formulas untouched',all(mc[r]==mb[r] for r in mb if r.startswith(('common/script_values/nesnd_cne_confidence','common/script_values/nesnd_cne_bar_values','common/scripted_effects/nesnd_cne_confidence','common/scripted_effects/nesnd_cne_republic'))))

pt='common/scripted_triggers/nesnd_poland_repairs.txt';pe='events/ce_poland_events.txt';pb='common/scripted_buttons/ce_poland_scripted_buttons.txt'
ult=[n for n in node(pb).children if has(n.get('possible') or n,'nesnd_poland_can_issue_ultimatum','yes')]
check('ten ultimata',len(ult)==10)
for n in ult:
 check(n.key+' same foreign-state predicate preview/execution',has(n.get('possible'),'nesnd_poland_ultimatum_state','yes') and has(n.get('effect'),'nesnd_poland_ultimatum_state','yes') and not has(n,'owns_entire_state_region') and not any(a.key=='save_scope_as' and a.value=='target_diplo_play_state' for a in n.walk() if False))
 check(n.key+' state, not region, target',any(a.key=='random_scope_state' and has(a,'save_scope_as','target_diplo_play_state') for a in n.walk()))
state=node(pt,'nesnd_poland_ultimatum_state');check('claim check state scoped',has(state,'has_claim_by','c:KRA') and not has(state,'state_region'))
check('unscoped radical selection replaced in two buttons',sum(1 for a in node(pb).walk() if a.key=='random_scope_state' and has(a,'add_radicals_in_state'))==2 and all(a.get('limit') is not None for a in node(pb).walk() if a.key=='random_state'))
for key in ['nesnd_poland_existing_pol','nesnd_poland_existing_plc']:
 n=node(pt,key);check(key+' optional country guarded & 3 incorporated threshold',has(n.get('trigger_if').get('limit'),'exists') and has(n,'is_subject','no') and has(n,'num_incorporated_states','3'))
match=node(pt,'nesnd_poland_matching_pending');check('pending existence nested before equality',match.get('trigger_if').get('limit').scalar('has_variable')=='nesnd_polish_pending_state' and has(match.get('trigger_if').get('trigger_if').get('limit'),'exists','var:nesnd_polish_pending_state'))
for ev in ['ce_poland_events.2','ce_poland_events.7','ce_poland_events.97']:
 n=node(pe,ev);check(ev+' cancellation present',n.get('cancellation_trigger') is not None)
for ev in ['ce_poland_events.10','ce_poland_events.11']:
 n=node(pe,ev);check(ev+' outcome in immediate guarded once',has(n.get('immediate'),'has_variable','nesnd_polish_result_resolved') and has(n.get('immediate'),'set_variable','nesnd_polish_result_resolved'))
 check(ev+' option acknowledgment only',all(a.key in {'name','default_option'} for op in n.all('option') for a in op.children))
effect=node(pe,'ce_poland_events.4').all('option')[0]
# Execute only the actual two bar decrement branches, including the actual else,
# against 101 values each. This checks arithmetic, not game scope scheduling.
seen=0
for guarded in effect.all('if'):
 inner=[x for x in guarded.walk() if x.key=='if' and x.get('limit') and any(a.key.startswith('scripted_bar_progress') or 'scripted_bar_progress' in a.key for a in x.get('limit').walk())]
 for b in inner:
  cond=next(a for a in b.get('limit').walk() if 'scripted_bar_progress' in a.key);delta=next(a.scalar('value') for a in b.walk() if a.key=='add_progress')
  # Else sibling under the same containing JE.
  owner=next(a for a in guarded.walk() if a.children and b in a.children);fallback=owner.children[owner.children.index(b)+1];zero=next(a.scalar('value') for a in fallback.walk() if a.key=='set_bar_progress')
  check('decrement shape native if>=10 elsezero '+str(seen),cond.op=='>=' and cond.value=='10' and delta=='-10' and fallback.key=='else' and zero=='0')
  check('actual AST decrement values0..100 '+str(seen),all((x+float(delta) if x>=float(cond.value) else float(zero))==max(0,x-10) for x in range(101)));seen+=1
check('two actual bar-decrement paths tested',seen==2)
check('claim penalty reads nonnegative count',has(node(pt,'nesnd_poland_many_claims'),'global_var:ce_polish_claim_state_count','3'))
check('new participants added to JE',has(node('common/scripted_effects/nesnd_poland_repairs.txt','nesnd_poland_refresh_participants'),'add_involved_country','prev'))
check('aid saves the actual notifying country',sum(1 for a in node(pb).walk() if a.key=='save_scope_as' and a.value=='ce_strong_power')>=2)

sb=node('common/scripted_buttons/nesnd_supply_buttons.txt');pending=[a for a in sb.walk() if a.key=='set_variable' and a.scalar('name') in {'nesnd_supply_pending','nesnd_supply_trade_pending'}]
check('seven pending identities cover travel+reply',len(pending)==7 and all(a.scalar('months')=='4' and not a.get('days') for a in pending))
check('six 100 capacity gates',sum(1 for a in sb.walk() if a.key=='influence' and a.value=='100')==6)
for ev in ['nesnd_supply.1','nesnd_supply.2']:check(ev+' invalid request cancels',node('events/nesnd_supply_events.txt',ev).get('cancellation_trigger') is not None)
contact=node('events/nesnd_supply_events.txt','nesnd_supply.1');check('contact25 only once',any(a.key=='if' and has(a.get('limit') or a,'has_variable','nesnd_supply_first_contact_rewarded') and has(a,'change_relations') and has(a,'value','25') for a in contact.walk()))
check('Persia real tributary history',any(a.key=='create_diplomatic_pact' and a.scalar('country')=='c:PER' and a.scalar('type')=='tributary' for a in node('common/history/diplomacy/ce_subject_relationships.txt').walk()))
check('tributary country type database preserved',all(mc[r]==mb[r] for r in mb if r.startswith('common/subject_types/')))

# Proper multiset comparison preserves repeated diagnostics and ignores shifted line numbers.
a=json.loads(read(R/'tiger-final.json'));b=json.loads(read(W/'reports/cne-confidence-20261101/tiger-raw.json'))
def tkey(d):return json.dumps({'severity':d.get('severity'),'key':d.get('key'),'message':d.get('message'),'locations':[(x.get('from'),x.get('path'),(x.get('line') or '').strip()) for x in d.get('locations',[])]},ensure_ascii=False,sort_keys=True)
added=[json.loads(x) for x,n in (collections.Counter(map(tkey,a))-collections.Counter(map(tkey,b))).items() for _ in range(n)]
removed=sum((collections.Counter(map(tkey,b))-collections.Counter(map(tkey,a))).values())
dump(R/'tiger-delta.json',{'counts':dict(collections.Counter(x['severity'] for x in a)),'baseline_counts':dict(collections.Counter(x['severity'] for x in b)),'added':added,'removed':removed,'game_launched':False})
dump(R/'checks.json',{'status':'STATIC_PASS','checks':rows,'source_arithmetic_cases':202,'engine_verified':False,'game_launched':False})
dump(R/'changed-files.json',changed);(R/'candidate.diff').write_text(''.join(diff),encoding='utf-8')
print(json.dumps({'checks':len(rows),'tiger_added':len(added),'tiger_counts':dict(collections.Counter(x['severity'] for x in a)),'changed_files':len(changed)}))
if added:print(json.dumps(added,ensure_ascii=False,indent=2))
if '--mcp' in sys.argv:
 async def probe():
  from mcp import ClientSession,StdioServerParameters
  from mcp.client.stdio import stdio_client
  queries=[(tr,'nesnd_cne_urban_foundation',None,'country_has_building_type_levels'),(pt,'nesnd_poland_matching_pending','trigger_if.trigger_if.limit','exists'),('common/scripted_effects/nesnd_poland_repairs.txt','nesnd_poland_refresh_participants','if.every_country.scope:journal_entry','add_involved_country'),('events/nesnd_supply_events.txt','nesnd_supply.2','cancellation_trigger.NOT','nesnd_supply_trade_request_valid'),('common/history/diplomacy/ce_subject_relationships.txt','DIPLOMACY','c:QE1','nesnd_qe1_per_relation_v1')];out=[]
  async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
   async with ClientSession(r,w) as sess:
    await sess.initialize();q=await sess.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not q.isError
    for rel,symbol,keypath,want in queries:
     args={'file_path':rel}
     if symbol:args['symbol']=symbol
     if keypath:args['key_path']=keypath
     q=await sess.call_tool('get_structure',args);s='\n'.join(x.text for x in q.content if getattr(x,'type',None)=='text');assert not q.isError and want in s,(rel,s)
     out.append({'file':rel,'sha256':sha(C/rel),'query':args,'response':s})
  dump(R/'mcp-queries.json',{'status':'PASS','queries':out,'game_launched':False});print('MCP source queries PASS',len(out))
 asyncio.run(probe())
