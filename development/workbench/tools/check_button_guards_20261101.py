"""Check real source guards and preserved data; Tiger/MCP do not execute Jomini."""
from pathlib import Path
import sys,json,hashlib,collections,subprocess,difflib,asyncio,re
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
B=W/'backups/pre-change-button-guard-fix-20261101T093152Z/mod';C=W/'exports/button-guards-20261101-a';R=W/'reports/button-guards-20261101'
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse
def shape(n):return (n.key,n.op,n.value,tuple(shape(x) for x in n.children or []))
def checks(root):
 rows=[];cache={}
 def get(path,*keys):
  if path not in cache:cache[path]=parse((root/path).read_text('utf-8-sig'))
  n=cache[path]
  for key in keys:
   n=n.get(key) if n else None
  return n
 def add(name,ok):rows.append({'name':name,'pass':bool(ok)})
 def has(n,key,value):return n is not None and any(x.key==key and x.value==value for x in n.walk())
 def gated(n,key,value):
  branch=n.get('trigger_if') if n else None;fallback=n.get('trigger_else') if n else None
  return branch is not None and has(branch.get('limit'),key,value) and has(fallback,'always','no')
 t='common/scripted_triggers/nesnd_external_triggers.txt'
 for key in ['nesnd_external_target_valid','nesnd_external_any_legal_aid']+['nesnd_external_can_'+x for x in ['offer_money','offer_arms','request_money','request_arms']]:
  add(key,gated(get(t,key),'exists','var:nesnd_external_target'))
 add('reply requester gate',gated(get(t,'nesnd_external_request_valid'),'exists','scope:nesnd_external_requester'))
 n=get(t,'nesnd_external_request_valid','trigger_if','scope:nesnd_external_requester')
 for value in ['var:nesnd_external_pending','var:nesnd_external_target']:add('reply identity '+value,gated(n,'exists',value))
 for value in ['var:nesnd_external_target','var:nesnd_external_requester_sponsor','var:nesnd_external_receiver_sponsor']:
  add('politics '+value,gated(get(t,'nesnd_external_pending_politics_valid'),'exists',value))
 b='common/scripted_buttons/nesnd_external_buttons.txt'
 for action in ['offer_money','offer_arms','request_money','request_arms']:
  add('execute '+action,has(get(b,'nesnd_external_'+action,'effect','if','limit'),'nesnd_external_can_'+action,'yes'))
 for suffix,tag in [('wu','USM'),('sih','SIH'),('hus','HUS'),('fra','FRA')]:
  add('select '+suffix,gated(get(b,'nesnd_external_choose_'+suffix,'possible'),'exists','c:'+tag) and has(get(b,'nesnd_external_choose_'+suffix,'effect','if','limit'),'exists','c:'+tag))
 add('send request target gate',has(get('common/scripted_effects/nesnd_external_effects.txt','nesnd_external_send_request','if','limit'),'nesnd_external_target_valid','yes'))
 add('idle numeric safe getter',(root/'common/script_values/nesnd_external_preview_values.txt').exists() and 'var:nesnd_external_idle_weeks >=' not in (root/b).read_text('utf-8-sig'))
 e='events/nesnd_external_events.txt'
 for num in [2,3,5,6]:
  key='nesnd_external.'+str(num);opt=get(e,key,'option');condition=opt.get('trigger');run=opt.get('if')
  add(key+' eligibility',gated(condition,'nesnd_external_request_valid','yes'))
  add(key+' execution recheck',run and shape(run.get('limit'))[3]==shape(condition)[3] and has(run,'create_treaty',None))
  add(key+' cancellation',has(get(e,key,'cancellation_trigger'),'nesnd_external_request_valid','yes'))
  add(key+' AI guards',all(gated(x.get('trigger'),'exists','scope:nesnd_external_requester') for x in opt.get('ai_chance').all('modifier')))
  decline=get(e,key).all('option')[1].get('scope:nesnd_external_requester')
  add(key+' decline identity',decline and has(decline.get('if'),'exists','var:nesnd_external_pending') and has(decline,'var:nesnd_external_pending','root'))
 for rel,key,scope in [
  ('common/scripted_effects/nesnd_presentation_effects.txt','nesnd_refresh_land_display','nesnd_land_display_country'),
  ('common/scripted_effects/nesnd_presentation_effects.txt','nesnd_refresh_south_display','nesnd_south_display_country'),
  ('common/scripted_effects/nesnd_tenasserim.txt','nesnd_ten_display','nesnd_ten_display_country'),
  ('common/scripted_effects/nesnd_phi_finance.txt','nesnd_phi_display','nesnd_phi_display_country')]:
  n=get(rel,key);guard=n.get('if');all_bars=[x for x in n.walk() if x.key=='set_bar_progress'];safe_bars=[x for x in guard.walk() if x.key=='set_bar_progress'] if guard else []
  add(key,guard and has(guard.get('limit'),'exists','scope:'+scope) and len(all_bars)==len(safe_bars)==2)
 for key in ['nesnd_ten_healthy','nesnd_ten_can_build','nesnd_ten_can_train']:
  add(key,gated(get('common/scripted_triggers/nesnd_tenasserim.txt',key),'exists','s:STATE_TENASSERIM.region_state:DEI'))
 add('ten IG boundary',gated(get('common/scripted_triggers/nesnd_tenasserim.txt','nesnd_ten_can_compromise'),'exists','ig:ig_landowners'))
 add('JAP predicate boundary',gated(get('common/scripted_triggers/nesnd_japan.txt','nesnd_japan_can_send'),'exists','c:JAP') and has(get('common/scripted_triggers/nesnd_japan.txt','nesnd_japan_can_send','trigger_if','c:JAP'),'is_country_alive','yes'))
 add('JAP effect boundary',has(get('common/scripted_buttons/nesnd_japan.txt','nesnd_japan_send_terms','effect','if','limit'),'nesnd_japan_can_send','yes'))
 f='common/scripted_buttons/ce_french_empire_je_buttons.txt';key='ce_french_republican_hit_unity'
 add('French identical candidate sets',shape(get(f,key,'possible','any_interest_group'))[3]==shape(get(f,key,'effect','random_interest_group','limit'))[3])
 return rows
before,after=checks(B),checks(C)
assert all(x['pass'] for x in after),[x for x in after if not x['pass']]
assert any(not x['pass'] for x in before)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(root):return {p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file()}
bm,cm=manifest(B),manifest(C);changed=[p for p,h in cm.items() if bm.get(p)!=h and not p.startswith('.scratch/')]
assert not(set(bm)-set(cm))
assert all(p.startswith(('common/scripted_','common/script_values/','events/')) for p in changed)
for path in cm:
 if path.endswith('.txt') and path.startswith(('common/','events/')):parse((C/path).read_text('utf-8-sig'))
for path in bm:
 if path.startswith(('map_data/','common/history/','gfx/','localization/')) or path=='.metadata/metadata.json':assert bm[path]==cm[path],path
# Actual treaty payloads and saved delays/cooldowns remain unchanged.
def payloads(root,rel,key):
 return [shape(n) for n in parse((root/rel).read_text('utf-8-sig')).walk() if n.key==key]
assert payloads(B,'events/nesnd_external_events.txt','create_treaty')==payloads(C,'events/nesnd_external_events.txt','create_treaty')
for rel in ['common/scripted_effects/nesnd_external_effects.txt','common/scripted_buttons/nesnd_external_buttons.txt']:
 assert payloads(B,rel,'set_variable')==payloads(C,rel,'set_variable')
assert not [p for p in cm if re.search(r'nesnd_(qa|batch_probe|sequence_qa|f2_qa)|(?:^|/)(?:qa|fixture|probe)[^/]*',p,re.I)]
diff=[]
for p in changed:diff+=list(difflib.unified_diff((B/p).read_text('utf-8-sig').splitlines(True) if (B/p).exists() else [],(C/p).read_text('utf-8-sig').splitlines(True),fromfile='before/'+p,tofile='after/'+p))
(R/'changes.diff').write_text(''.join(diff),encoding='utf-8')
(R/'source-changes.json').write_text(json.dumps({'base':str(B),'candidate':str(C),'changed':changed,'before':bm,'after':cm},ensure_ascii=False,indent=2),encoding='utf-8')
report={'status':'STATIC_PASS','checks':len(after),'before_failures':[x['name'] for x in before if not x['pass']],'after':after,'changed':changed,'data_unchanged':True,'engine_execution':False}
(R/'source-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Source checks:',len(report['before_failures']),'failures -> 0;',len(after),'checks')

cmd=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game','D:/Program Files (x86)/Steam/steamapps/common/Victoria 3','--config',str(W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'),'--json',str(C)]
q=subprocess.run(cmd,capture_output=True);(R/'tiger-raw.json').write_bytes(q.stdout);(R/'tiger-stderr.txt').write_bytes(q.stderr)
raw=json.loads(q.stdout.decode('utf-8-sig'));old=json.loads((W/'reports/logfix-release-20261101/tiger-final-raw.json').read_text('utf-8-sig'))
def norm(d):return json.dumps({'severity':d.get('severity'),'key':d.get('key'),'message':d.get('message'),'locations':[(x.get('from'),x.get('path'),(x.get('line') or '').strip()) for x in d.get('locations',[])]},ensure_ascii=False,sort_keys=True)
added=[json.loads(k) for k,n in (collections.Counter(map(norm,raw))-collections.Counter(map(norm,old))).items() for _ in range(n)]
delta={'counts':dict(collections.Counter(x['severity'] for x in raw)),'added':added,'command':cmd,'engine_execution':False}
(R/'tiger-delta.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2),encoding='utf-8');print('Tiger:',delta['counts'],'added:',len(added))
assert not added,added

async def mcp_queries():
 from mcp import ClientSession,StdioServerParameters
 from mcp.client.stdio import stdio_client
 queries=[('common/scripted_triggers/nesnd_external_triggers.txt','nesnd_external_request_valid','trigger_if.limit','exists'),('common/scripted_effects/nesnd_presentation_effects.txt','nesnd_refresh_land_display','if.limit','exists'),('common/scripted_buttons/nesnd_japan.txt','nesnd_japan_send_terms','effect.if.limit','nesnd_japan_can_send'),('events/nesnd_external_events.txt','nesnd_external.2','cancellation_trigger.NOT','nesnd_external_request_valid')]
 results=[]
 async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize();ts=await session.list_tools();assert 'get_structure' in [t.name for t in ts.tools]
   init=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not init.isError
   for path,symbol,key_path,want in queries:
    response=await session.call_tool('get_structure',{'file_path':path,'symbol':symbol,'key_path':key_path})
    text='\n'.join(x.text for x in response.content if getattr(x,'type',None)=='text')
    assert not response.isError and want in text,(symbol,text)
    results.append({'path':path,'symbol':symbol,'key_path':key_path,'sha256':sha(C/path),'response':text})
 (R/'mcp-queries.json').write_text(json.dumps({'status':'PASS','engine_execution':False,'queries':results},ensure_ascii=False,indent=2),encoding='utf-8');print('MCP: 4 source queries passed')
asyncio.run(mcp_queries())
