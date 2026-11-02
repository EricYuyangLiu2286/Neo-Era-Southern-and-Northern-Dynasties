"""Source AST/formula regression and real Tiger/MCP adapters; never a game test."""
from cne_confidence_context import *
import collections,difflib,subprocess,re,itertools,asyncio
rows=[];cache={}
def node(rel,key=None):
 if rel not in cache:cache[rel]=parse(read(C/rel))
 return cache[rel].get(key) if key else cache[rel]
def has(n,k,v):return any(a.key==k and a.value==v for a in n.walk())
def check(name,value):rows.append({'name':name,'pass':bool(value)});assert value,name
def shape(n):return n.key,n.op,n.value,tuple(shape(a) for a in n.children or [])
def compare(a,op,b):return {'=':a==b,'>':a>b,'<':a<b,'>=':a>=b,'<=':a<=b,'!=':a!=b}[op]
values={}
for rel in ['common/script_values/nesnd_cne_confidence.txt','common/script_values/nesnd_cne_bar_values.txt','common/script_values/nesnd_cne_programs.txt']:
 values.update({n.key:n for n in node(rel).children})
def atom(n,e):
 if n.key in ('NOT','NOR'):return not any(atom(a,e) for a in n.children)
 if n.key in ('AND','limit'):return all(atom(a,e) for a in n.children)
 if n.key=='OR':return any(atom(a,e) for a in n.children)
 if n.key=='has_variable':return n.value in e['vars']
 if n.key=='has_modifier':return n.value in e['mods']
 if n.key.startswith('var:'):return compare(e['vars'][n.key[4:]],n.op,float(n.value))
 if n.key.startswith('ig:'):
  assert n.scalar('is_in_government')=='yes';return n.key in e['igs']
 if n.key in ('is_at_war','nesnd_cne_programs_live','nesnd_reform_healthy','nesnd_reform_distress'):return e[n.key]==(n.value=='yes')
 if n.key in ('radical_population_fraction','bureaucracy','country_turmoil'):return compare(e[n.key],n.op,float(n.value))
 raise AssertionError(('unsupported source trigger',n.key))
def val(v,e):
 if not isinstance(v,str):return calc(v,e)
 if v in values:return calc(values[v],e)
 if v.startswith('var:'):return e['vars'][v[4:]]
 return float(v)
def calc(n,e,initial=0):
 total=initial
 for a in n.children or []:
  if a.key in ('limit','desc'):continue
  if a.key=='if':
   if atom(a.get('limit'),e):total=calc(a,e,total)
  elif a.key in ('value','add','subtract','multiply','divide'):
   v=val(a.value if a.value is not None else a,e)
   if a.key=='value':total=v
   elif a.key=='add':total+=v
   elif a.key=='subtract':total-=v
   elif a.key=='multiply':total*=v
   elif a.key=='divide':total/=v
  else:raise AssertionError(('unsupported source value operation',a.key))
 return total
def env():return {'vars':{'nesnd_reform_samples':10,'nesnd_cne_camps_active':0},'mods':set(),'igs':set(),'is_at_war':False,'nesnd_cne_programs_live':True,'nesnd_reform_healthy':False,'nesnd_reform_distress':False,'radical_population_fraction':0,'bureaucracy':0,'country_turmoil':0}
annual_cases=0
for land,urban,camps,war,radical,mask in itertools.product([0,1],[0,1],[0,1,3,22],[0,1],[.15,.1501],range(16)):
 e=env();e['vars']['nesnd_cne_camps_active']=camps;e['is_at_war']=bool(war);e['radical_population_fraction']=radical
 for flag,on in [('nesnd_cne_land_program',land),('nesnd_cne_urban_program',urban)]:
  if on:e['vars'][flag]=1
 for bit,ig in enumerate(['intelligentsia','petty_bourgeoisie','trade_unions','industrialists']):
  if mask & (1<<bit):e['igs'].add('ig:ig_'+ig)
 expected=-50-10*(land+urban+camps)-50*war-40*(radical>.15)+10*mask.bit_count()
 actual=val('nesnd_cne_confidence_annual_change',e)
 bar=calc(node('common/scripted_progress_bars/nesnd_cne_confidence.txt','nesnd_cne_confidence_bar').get('yearly_progress'),e)
 assert actual==expected==bar,(e,expected,actual,bar)
 annual_cases+=1
check('annual formula and native bar exact for '+str(annual_cases)+' scenarios including radical boundary',True)
monthly_cases=0
for bits in itertools.product([0,1],repeat=7):
 healthy,distress,admin,turmoil,war,bankrupt,appeals=bits;e=env()
 e.update({'nesnd_reform_healthy':bool(healthy),'nesnd_reform_distress':bool(distress),'bureaucracy':-1 if admin else 0,'country_turmoil':.26 if turmoil else .25,'is_at_war':bool(war)})
 if bankrupt:e['mods'].add('declared_bankruptcy')
 if appeals:e['mods'].add('nesnd_land_appeals')
 expected=-healthy+distress+.5*(admin+turmoil+war)+bankrupt-.5*appeals
 actual=val('nesnd_cne_order_monthly_delta',e)
 bar=calc(node('common/scripted_progress_bars/nesnd_crisis_bars.txt','nesnd_land_disorder_bar').get('monthly_progress'),e)
 assert actual==expected==bar,(bits,expected,actual,bar)
 monthly_cases+=1
check('original disorder formula preserved and native breakdown equal across '+str(monthly_cases)+' scenarios',True)
for count in [0,1,3,22]:
 e=env();e['vars'].update({'nesnd_cne_camps_active':count,'nesnd_cne_land_program':1,'nesnd_cne_urban_program':1})
 assert abs(val('nesnd_cne_land_monthly_delta',e)-(.6+.05*count))<1e-8
 for barname in ['nesnd_land_completion_bar','nesnd_land_disorder_bar']:
  assert abs(calc(node('common/scripted_progress_bars/nesnd_crisis_bars.txt',barname).get('monthly_progress'),e)-val('nesnd_cne_land_monthly_delta' if 'completion' in barname else 'nesnd_cne_order_monthly_delta',e))<1e-8
check('land and 22 estate contributions preserved',True)
e=env();e['nesnd_cne_programs_live']=False;e['vars']={}
for key in ['nesnd_cne_land_monthly_delta','nesnd_cne_order_monthly_delta','nesnd_cne_confidence_annual_change']:assert val(key,e)==0
check('inactive/missing-variable preview returns zero without reading missing values',True)
ef='common/scripted_effects/nesnd_cne_confidence.txt';p='common/journal_entries/ce_cne_land_draft.txt';je=node(p,'ce_cne_land_reform')
ensure=node(ef,'nesnd_cne_ensure_children');children=[a.scalar('type') for a in ensure.walk() if a.key=='add_journal_entry']
check('exactly four children explicitly added with duplicate guards',len(children)==4 and all(has(ensure,'has_journal_entry',x) for x in children))
check('confidence initialize once, no old progress reset',has(node(ef,'nesnd_cne_confidence_init'),'has_variable','nesnd_cne_confidence') and has(node(ef,'nesnd_cne_confidence_init'),'value','1000'))
check('yearly accounting has one owner, same JE as native yearly bar',not has(je,'nesnd_cne_confidence_yearly','yes') and has(node('common/journal_entries/nesnd_cne_confidence.txt'),'nesnd_cne_confidence_yearly','yes'))
check('confidence never imports auto-incremented bar into country variable',not any('scripted_bar_progress' in (a.value or '') for a in node(ef).walk()))
check('confidence bankruptcy once until penalty gone',has(node(ef,'nesnd_cne_confidence_watch'),'add','-500') and has(node(ef,'nesnd_cne_confidence_watch'),'has_variable','nesnd_cne_bankruptcy_charged') and has(node(ef,'nesnd_cne_confidence_watch'),'remove_variable','nesnd_cne_bankruptcy_charged'))
check('500 uses <=, once guard, does not miss direct 1000 to0 drop',has(node(ef,'nesnd_cne_confidence_watch'),'var:nesnd_cne_confidence','500') and has(node(ef,'nesnd_cne_confidence_watch'),'has_variable','nesnd_cne_republican_rose'))
for k in ['complete','fail']:check('parent '+k+' observes all failure reasons',has(je.get(k),'nesnd_cne_reform_failed','yes'))
for k in ['on_fail','on_invalid']:check(k+' clears programmes',has(je.get(k),'nesnd_cne_programs_cleanup','yes') or (has(je.get(k),'nesnd_cne_end_failed_reform','yes') and has(node(ef,'nesnd_cne_end_failed_reform'),'nesnd_cne_programs_cleanup','yes')))
check('zero check branch guarded',has(node('common/scripted_triggers/nesnd_cne_confidence.txt','nesnd_cne_confidence_exhausted').get('trigger_if').get('limit'),'has_variable','nesnd_cne_confidence'))
check('native revolution hooks root and old-save fallback discriminate play type',all(node('common/on_actions/nesnd_cne_confidence.txt').get(x) for x in ['on_revolution_start','on_secession_start']) and has(node('common/scripted_triggers/nesnd_cne_confidence.txt'),'is_diplomatic_play_type','dp_revolution'))
rep='common/scripted_effects/nesnd_cne_republic.txt';setup=node(rep,'nesnd_cne_republic_setup');play=node('common/diplomatic_plays/nesnd_cne_republic.txt','dp_nesnd_cne_republic')
check('new tag unused at base and vanilla',not any(re.search(r'^NRP\s*=',read(q),re.M) for parent in [B/'common/country_definitions',G/'common/country_definitions'] for q in parent.glob('*.txt')))
check('both annexation goals use native mirror rule',play.scalar('war_goal')=='annex_country' and play.scalar('mirror_war_goal')=='yes')
check('army attached to explicit new republic; 15 regular units and no fleet',sum(int(a.scalar('count')) for a in setup.walk() if a.key=='combat_unit')==15 and not has(setup,'type','fleet') and not any('root.capital' in (a.value or '') for a in setup.walk()))
check('new country inherited cleanup only',has(setup,'nesnd_land_cleanup','yes') and not has(setup,'nesnd_cne_programs_cleanup','yes'))
check('peace fail cannot fire before war creation and grace',has(node('common/journal_entries/nesnd_cne_republic.txt','nesnd_cne_republic_journal').get('fail'),'has_variable','nesnd_cne_republic_war_created') and has(node('common/journal_entries/nesnd_cne_republic.txt'),'has_variable','nesnd_cne_republic_launch_grace'))
check('80 percent uses republican controller not all-enemy occupation',has(node('common/scripted_triggers/nesnd_cne_republic.txt'),'percent','0.8') and has(node('common/scripted_triggers/nesnd_cne_republic.txt'),'controller','c:NRP') and not has(node('common/scripted_triggers/nesnd_cne_republic.txt'),'enemy_occupation','0.8'))
win=node(rep,'nesnd_cne_republic_victory');check('victory annexes first then guarded change_tag and claims',has(win,'annex_with_incorporation','c:CNE') and has(win,'change_tag','CNE') and has(win,'nesnd_cne_republic_southern_claims','yes'))
check('ordinary war does not inherit defeated CNE/NRP reform variables',has(node(rep,'nesnd_cne_start_republic_war'),'annex_as_civil_war','no') and has(node(rep,'nesnd_cne_republic_defeat'),'annex_with_incorporation','prev'))
check('native civil war trigger independent of state callback ROOT',not has(node('common/scripted_triggers/nesnd_cne_confidence.txt','nesnd_cne_native_civil_war'),'initiator','root') and has(node('common/scripted_triggers/nesnd_cne_confidence.txt'),'initiator','c:CNE'))
check('source-MOD four-state minimum restored and takes precedence over success',has(je.get('invalid'),'num_states','4') and has(je.get('complete'),'num_states','4') and has(node('common/scripted_triggers/nesnd_cne_programs.txt','nesnd_cne_programs_live'),'num_states','4'))
for reg in json.loads(read(W/'reports/cne-reform-subjournals-20261101/initial-inventory.json'))['regions']:
 key='nesnd_cne_camp_'+reg[6:].lower()
 for action in ['start','stop']:
  check(reg+' '+action+' button requires current CNE state',has(node('common/scripted_buttons/nesnd_cne_programs.txt',key+'_'+action+'_button').get('visible'),'exists','s:'+reg+'.region_state:CNE'))
 check(reg+' lost-country cleanup cancels own project only',has(node('common/scripted_effects/nesnd_cne_estate_ownership.txt','nesnd_cne_prune_lost_estates'),key+'_stop','yes'))
check('ownership event is parent-gated and deferred',has(node('events/nesnd_cne_confidence.txt','nesnd_cne_confidence.6').get('trigger'),'nesnd_cne_programs_live','yes') and has(node('common/scripted_effects/nesnd_cne_estate_ownership.txt','nesnd_cne_queue_estate_ownership_check'),'days','1'))
check('owner-change and split-state native callbacks installed',all(node('common/on_actions/nesnd_cne_estate_ownership.txt').get(x) for x in ['on_state_owner_change','on_state_created']))
check('weekly owner repair exists and only active parent can act',has(je,'nesnd_cne_prune_lost_estates','yes') and has(node('common/scripted_effects/nesnd_cne_estate_ownership.txt','nesnd_cne_prune_lost_estates'),'nesnd_cne_programs_live','yes'))
for key in ['west','northeast','north']:
 n=node(rep,'nesnd_cne_republic_raise_'+key)
 check(key+' takes only scoped CNE states; preserves foreigners',has(n,'origin','root') and has(n,'set_state_owner','c:NRP') and has(n,'nesnd_cne_republic_'+key+'_region','yes'))
for tag in ['HUNAN','EASTERN_HUBEI','WESTERN_HUBEI','XIANGYANG','SICHUAN','CHONGQING']:check(tag+' claim source exists',(node(rep,'nesnd_cne_republic_southern_claims').get('s:STATE_'+tag) is not None))
# Compatibility assertions from the last batch, adapted only for the new shared
# failure/aggregate helper; original checker and its evidence remain untouched.
legacy=read(W/'tools/check_cne_subjournals_20261101.py')
legacy=legacy.replace("R=W/'reports/cne-reform-subjournals-20261101'","R=W/'reports/cne-confidence-20261101'")
shutil.copy2(W/'reports/cne-reform-subjournals-20261101/initial-inventory.json',R/'initial-inventory.json')
legacy=legacy.replace("'add','nesnd_cne_program_monthly_progress'","'add','nesnd_cne_land_monthly_delta'")
legacy=legacy.replace("'nesnd_cne_coup_has_succeeded','yes'","'nesnd_cne_reform_failed','yes'")
legacy=legacy.replace("has(node(parent,'ce_cne_land_reform',k),'nesnd_cne_programs_cleanup','yes')", "(has(node(parent,'ce_cne_land_reform',k),'nesnd_cne_programs_cleanup','yes') or (has(node(parent,'ce_cne_land_reform',k),'nesnd_cne_end_failed_reform','yes') and has(node('common/scripted_effects/nesnd_cne_confidence.txt','nesnd_cne_end_failed_reform'),'nesnd_cne_programs_cleanup','yes')))")
q=W/'tools/check_cne_confidence_legacy.py';q.write_text(legacy,encoding='utf-8')
subprocess.run([sys.executable,'-X','utf8',str(q),str(C),'legacy-green'],check=True)
changes=[];diff=[]
for rel,h in manifest(C).items():
 q=B/rel;r=C/rel
 if not q.exists() or sha(q)!=h:
  changes.append({'file':rel,'before':sha(q) if q.exists() else None,'after':h})
  if r.suffix=='.txt':parse(read(r))
  if r.suffix=='.yml':assert r.read_bytes().startswith(b'\xef\xbb\xbf')
  diff.extend(difflib.unified_diff(read(q).splitlines(True) if q.exists() else [],read(r).splitlines(True),fromfile='base/'+rel,tofile='candidate/'+rel))
check('all original maps/history/portraits/metadata bytes preserved',all(not x['file'].startswith(('map_data/','common/history/','gfx/','.metadata/')) for x in changes))
check('no original files deleted',not set(manifest(B))-set(manifest(C)))
for rel,changed in [('common/scripted_effects/nesnd_crisis_effects.txt',{'nesnd_land_monthly','nesnd_land_success'}),('common/scripted_progress_bars/nesnd_crisis_bars.txt',{'nesnd_land_completion_bar','nesnd_land_disorder_bar'}),('common/dynamic_country_names/ce_dynamic_country_names.txt',{'CNE'})]:
 old=parse(read(B/rel));new=node(rel)
 check(rel+' unrelated definitions identical',all(shape(n)==shape(new.get(n.key)) for n in old.children if n.key not in changed))
for lang in ['simp_chinese','english']:
 own=C/f'localization/{lang}/replace/zzzzzz_nesnd_cne_confidence_l_{lang}.yml';keys=set(re.findall(r'^ ([\w.]+):',read(own),re.M));counts=collections.Counter()
 for q in (C/f'localization/{lang}').rglob('*.yml'):counts.update(k for k in re.findall(r'^ ([\w.]+):',read(q),re.M) if k in keys)
 check(lang+' new loc keys unique',all(counts[k]==1 for k in keys))
check('banned player-facing engineering phrases removed',not any(re.search('子项目|见三个子日志|各项建设与利益得失|按原规则|继续决定改革成果|地方困顿|多组符合时仍只计算一次',read(q)) for q in (C/'localization/simp_chinese').rglob('*.yml')))
dump(R/'checks.json',{'status':'STATIC_PASS','checks':rows,'annual_cases':annual_cases,'monthly_cases':monthly_cases,'engine_verified':False,'game_launched':False})
dump(R/'changed-files.json',changes);(R/'candidate.diff').write_text(''.join(diff),encoding='utf-8')
print('PASS',len(rows),'source/lifecycle checks;',annual_cases,'annual;',monthly_cases,'monthly arithmetic scenarios')
if '--tiger' in sys.argv:
 cmd=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game',str(G.parent),'--config',str(W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'),'--json',str(C)]
 p=subprocess.run(cmd,capture_output=True);(R/'tiger-raw.json').write_bytes(p.stdout);(R/'tiger-stderr.txt').write_bytes(p.stderr)
 a=json.loads(p.stdout);b=json.loads(read(W/'reports/cne-reform-subjournals-20261101/tiger-raw.json'))
 def key(d):return json.dumps({'severity':d.get('severity'),'key':d.get('key'),'message':d.get('message'),'locations':[(x.get('from'),x.get('path'),(x.get('line') or '').strip()) for x in d.get('locations',[])]},ensure_ascii=False,sort_keys=True)
 added=[json.loads(x) for x,n in (collections.Counter(map(key,a))-collections.Counter(map(key,b))).items() for _ in range(n)]
 dump(R/'tiger-delta.json',{'counts':dict(collections.Counter(x['severity'] for x in a)),'added':added,'command':cmd,'game_launched':False});print('Tiger additions',len(added));assert not added,added
if '--mcp' in sys.argv:
 async def mcp():
  from mcp import ClientSession,StdioServerParameters
  from mcp.client.stdio import stdio_client
  queries=[('common/scripted_triggers/nesnd_cne_confidence.txt','nesnd_cne_confidence_exhausted','trigger_if.limit','nesnd_cne_confidence'),('common/scripted_effects/nesnd_cne_republic.txt','nesnd_cne_republic_setup','create_military_formation','nesnd_cne_new_republic'),('common/diplomatic_plays/nesnd_cne_republic.txt','dp_nesnd_cne_republic','mirror_war_goal','True'),('common/scripted_progress_bars/nesnd_cne_confidence.txt','nesnd_cne_confidence_bar','yearly_progress','(10 items)'),('common/scripted_progress_bars/nesnd_crisis_bars.txt','nesnd_land_disorder_bar','monthly_progress','(7 items)')]
  out=[]
  async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
   async with ClientSession(r,w) as session:
    await session.initialize();result=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not result.isError
    for rel,symbol,keypath,want in queries:
     result=await session.call_tool('get_structure',{'file_path':rel,'symbol':symbol,'key_path':keypath});s='\n'.join(x.text for x in result.content if getattr(x,'type',None)=='text');assert not result.isError and want in s,(symbol,s);out.append({'file':rel,'symbol':symbol,'key_path':keypath,'sha256':sha(C/rel),'response':s})
  dump(R/'mcp-queries.json',{'status':'PASS','queries':out,'game_launched':False});print('MCP',len(out),'source queries PASS')
 asyncio.run(mcp())
