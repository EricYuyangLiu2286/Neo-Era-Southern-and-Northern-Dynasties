"""Source and localization regression checks, not a Victoria 3 execution model."""
from pathlib import Path
from datetime import date,timedelta
import sys,json,hashlib,re,collections,subprocess,difflib,asyncio
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');C=W/'exports/south-feedback-20261101-a';B=W/'backups/pre-change-south-politics-feedback-20261101T175047Z/mod';R=W/'reports/south-feedback-20261101'
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts');from pdx import parse
def shape(n):return (n.key,n.op,n.value,tuple(shape(x) for x in n.children or [])) if n else None
def has(n,key,value):return n is not None and any(x.key==key and x.value==value for x in n.walk())
def checks(root):
 cache={};rows=[]
 def get(rel,*keys):
  if rel not in cache:cache[rel]=parse((root/rel).read_text('utf-8-sig') if (root/rel).exists() else '')
  n=cache[rel]
  for key in keys:n=n.get(key) if n else None
  return n
 def record(name,ok):rows.append({'name':name,'pass':bool(ok)})
 tr='common/scripted_triggers/nesnd_succession_board.txt';ef='common/scripted_effects/nesnd_succession_board.txt';btn='common/scripted_buttons/nesnd_succession_board.txt'
 record('HNA policy identity',has(get(tr,'nesnd_board_fixed_ming_allegiance'),'c:HNA','this'))
 record('HNA policy does not rewrite settled outcomes',has(get(tr,'nesnd_board_fixed_ming_allegiance','NOT'),'has_global_variable','usm_civilwar_occured') and any(has(n,'has_global_variable','nesnd_south_settled') for n in (get(tr,'nesnd_board_fixed_ming_allegiance').all('NOT') if get(tr,'nesnd_board_fixed_ming_allegiance') else [])))
 record('HNA first preview is Ming',has(get('common/script_values/nesnd_succession_board.txt','nesnd_board_stance_value','if','limit'),'nesnd_board_fixed_ming_allegiance','yes') and has(get('common/script_values/nesnd_succession_board.txt','nesnd_board_stance_value','if'),'value','1'))
 record('registration repairs actual allegiance',has(get(ef,'nesnd_board_initialize_country'),'nesnd_board_enforce_allegiance','yes'))
 record('HNA old Wu agreement revoked',has(get(ef,'nesnd_board_enforce_allegiance','if'),'nesnd_south_accord_side_value','2') and has(get(ef,'nesnd_board_enforce_allegiance','if'),'nesnd_south_withdraw_accord','yes'))
 record('AI initial HNA policy',has(get('common/scripted_effects/nesnd_south_political_ai.txt','nesnd_south_ai_initial_stance','if','limit'),'nesnd_board_fixed_ming_allegiance','yes'))
 record('AI review excludes HNA',has(get('common/scripted_effects/nesnd_south_political_ai.txt','nesnd_south_ai_review','if','limit','NOT'),'nesnd_board_fixed_ming_allegiance','yes'))
 record('court cannot choose local stances',has(get(tr,'nesnd_board_can_choose_local_stance'),'c:USM','this') and has(get(tr,'nesnd_board_can_choose_local_stance'),'has_variable','nesnd_ming_court'))
 for stance in ['ming','wu','neutral','autonomy']:
  key='nesnd_board_choose_'+stance
  record(key+' fixed allegiance visibility',has(get(btn,key,'visible'),'nesnd_board_fixed_ming_allegiance','yes'))
  wanted='nesnd_board_can_choose_local_stance' if stance in ['neutral','autonomy'] else 'nesnd_board_can_choose'
  record(key+' execution recheck',has(get(btn,key,'effect','if','limit'),wanted,'yes'))
  if stance in ['neutral','autonomy']:
   record(key+' court visibility',has(get(btn,key,'visible'),'c:USM','this') and has(get(btn,key,'visible'),'has_variable','nesnd_ming_court'))
   record(key+' eligibility',has(get(btn,key,'possible'),wanted,'yes'))
 for key,condition in [('nesnd_south_can_receive_accord','nesnd_board_stance_value'),('nesnd_south_accord_reply_valid','nesnd_south_pending_side_value')]:
  record(key+' fixed allegiance',has(get('common/scripted_triggers/nesnd_south_politics.txt',key,'trigger_if','limit'),'nesnd_board_fixed_ming_allegiance','yes') and has(get('common/scripted_triggers/nesnd_south_politics.txt',key,'trigger_if'),condition,'1'))
 opts=get('events/usm_civilwar_events.txt','usm_civilwar.1').all('option')
 loyal=[o for o in opts if o.scalar('name')=='usm_civilwar.1.1' and o.scalar('default_option')=='yes' and has(o.get('trigger'),'c:HNA','this')]
 wu=[o for o in opts if o.scalar('name')=='usm_civilwar.1.3']
 record('HNA loyal default response',len(loyal)==1)
 record('HNA cannot accept Wu',len(wu)==1 and has(wu[0].get('trigger').get('NOT') if wu[0].get('trigger') else None,'c:HNA','this'))
 je='common/journal_entries/nesnd_succession_board.txt'
 record('global JE involved pin',has(get(je,'nesnd_south_succession_board'),'should_be_pinned_by_default_involved','yes'))
 record('global JE other pin preserved',has(get(je,'nesnd_south_succession_board'),'should_be_pinned_by_default_uninvolved_or_context','yes'))
 timing='common/scripted_effects/nesnd_south_timing.txt';jt='common/journal_entries/ce_usm_the_last_days_of_ming.txt'
 record('single monthly pressure writer',has(get(jt,'ce_usm_conflicts_within','on_monthly_pulse','effect'),'nesnd_south_crisis_month','yes'))
 record('base rate 3 and compact 2.5',has(get('common/script_values/nesnd_south_progress.txt','nesnd_south_base_monthly_pressure','if'),'value','2.5') and has(get('common/script_values/nesnd_south_progress.txt','nesnd_south_base_monthly_pressure','else'),'value','3'))
 record('rate display uses actual accrual value',has(get('common/script_values/nesnd_south_progress.txt','nesnd_south_monthly_pressure_value'),'add','nesnd_south_base_monthly_pressure') and has(get(timing,'nesnd_south_crisis_month'),'add','nesnd_south_base_monthly_pressure'))
 record('case opens July 1837',has(get('common/scripted_triggers/nesnd_chen_security.txt','nesnd_chen_case_possible'),'game_date','1837.7.1'))
 record('1838 case forced through real existing event',has(get(timing,'nesnd_south_crisis_month','if','limit'),'game_date','1838.1.1') and has(get(timing,'nesnd_south_crisis_month','if'),'id','nesnd_chen.2'))
 record('old low pressure cannot block 1838 case',has(get('common/scripted_triggers/nesnd_chen_security.txt','nesnd_chen_case_possible','OR'),'game_date','1838.1.1'))
 record('1839 deadline clamps pressure to 100',has(get(timing,'nesnd_south_enforce_crisis_deadline','if','limit'),'game_date','1839.1.1') and has(get(timing,'nesnd_south_enforce_crisis_deadline','if','clamp_variable'),'min','100'))
 record('deadline does not override completed peace',has(get(timing,'nesnd_south_enforce_crisis_deadline','if','limit'),'has_global_variable','nesnd_south_settled'))
 record('weekly deadline prevents monthly-order stall',has(get(jt,'ce_usm_conflicts_within','on_weekly_pulse'),'nesnd_south_enforce_crisis_deadline','yes'))
 record('accession waits for the case to conclude',has(get(jt,'ce_usm_conflicts_within','complete'),'nesnd_chen_case_concluded','yes'))
 record('Qin survival cannot cause indefinite delay',has(get('common/scripted_triggers/nesnd_south_timing.txt','nesnd_south_accession_window_open'),'game_date','1839.1.1') and has(get(jt,'ce_usm_conflicts_within','complete'),'nesnd_south_accession_window_open','yes'))
 record('pending death blocks auto succession',has(get('common/scripted_triggers/nesnd_south_timing.txt','nesnd_chen_case_concluded','NOT'),'has_variable','nesnd_chen_case_pending_death'))
 record('early accession respects case order',has(get('common/scripted_buttons/nesnd_crisis_buttons.txt','nesnd_early_accession','possible'),'nesnd_chen_case_concluded','yes'))
 intro=get('events/flavorUSM_ce.txt','flavorUSM.1','immediate')
 record('intro no longer resets accumulated pressure',not any(n.key=='set_variable' and n.scalar('name')=='usm_conflicts_within_tracker' for n in intro.walk()))
 chen='common/scripted_effects/nesnd_chen_security.txt'
 for key,amount in [('nesnd_chen_after_death','25'),('nesnd_chen_case_wounded','10'),('nesnd_chen_case_escape','3')]:
  record(key+' preserved pressure gain',has(get(chen,key),'add',amount))
  record(key+' immediate bar sync',has(get(chen,key),'nesnd_refresh_south_display','yes'))
 death=get(chen,'nesnd_chen_after_death');once=[n for n in death.walk() if n.key=='if' and has(n.get('limit'),'has_variable','started_with_chendongyang')]
 record('death gain remains once only',len(once)==1 and has(once[0],'add','25') and has(once[0],'remove_variable','started_with_chendongyang'))
 display=get('common/scripted_effects/nesnd_presentation_effects.txt','nesnd_refresh_south_display','if')
 record('both pressure bars sync safely',has(display.get('limit') if display else None,'exists','scope:nesnd_south_display_country') and has(display,'name','nesnd_south_pressure_bar') and has(display,'name','nesnd_board_pressure_bar'))
 return rows
before,after=checks(B),checks(C);assert all(x['pass'] for x in after),[x for x in after if not x['pass']]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def man(root):return {p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file()}
bm,cm=man(B),man(C);changed=[p for p,h in cm.items() if bm.get(p)!=h];assert not(set(bm)-set(cm))
for rel,h in bm.items():
 if rel.startswith(('map_data/','common/history/','gfx/','common/character_templates/')) or rel=='.metadata/metadata.json':assert cm[rel]==h,rel
for p in (C/'common').rglob('*.txt'):parse(p.read_text('utf-8-sig'))
for p in (C/'events').rglob('*.txt'):parse(p.read_text('utf-8-sig'))
for rel in changed:
 if rel.endswith('.yml'):
  p=C/rel;raw=p.read_bytes();assert raw.startswith(b'\xef\xbb\xbf');s=raw.decode('utf-8-sig');lang='simp_chinese' if '/simp_chinese/' in rel else 'english';assert s.startswith('l_'+lang+':')
  seen=set()
  for line in s.splitlines()[1:]:
   if not line.strip() or line.lstrip().startswith('#'):continue
   match=re.fullmatch(r'\s*([^\s:]+):\d*\s+"(?:[^"\\]|\\.)*"\s*',line);assert match,(rel,line[:100]);assert match[1] not in seen,(rel,match[1]);seen.add(match[1])
def loc(root,lang):
 d={};files=list((root/'localization'/lang).rglob('*.yml'))
 for p in sorted(files,key=lambda p:('replace' in p.parts,p.name)):
  for m in re.finditer(r'(?m)^\s*([^\s:]+):\d*\s+"(.*)"\s*$',p.read_text('utf-8-sig')):d[m[1]]=m[2]
 return d
zh,en=loc(C,'simp_chinese'),loc(C,'english');assert zh['nesnd_supply_preparations']=='脆弱的贸易' and en['nesnd_supply_preparations']=='Fragile Trade'
for key in ['nesnd_chen_case_concluded_tt']+['nesnd_supply_status_jobs_'+tag for tag in ['hna','sih','gng','hus']]:assert key in zh and key in en,key
assert '每周更新' not in zh['nesnd_south_succession_board_status']
assert '检查大学' not in zh['nesnd_supply_status_jobs'] and '检查工具厂' not in zh['nesnd_supply_status_jobs_sih']
assert '0.4' not in zh['nesnd_south_pressure_detail_tt'] and '1839' in zh['nesnd_south_pressure_detail_tt']
for key in ['nesnd_south_succession_board_reason','nesnd_supply_preparations_reason','nesnd_supply_hus_preparations_reason']:
 assert '\\n\\n' in zh[key] and '\\\\n' not in zh[key]
 for value in [zh[key],en[key]]:assert value.count('[')==value.count(']'),key
# HNA's special default only changes its valid answer; all original loyalist effects are retained.
old_event=parse((B/'events/usm_civilwar_events.txt').read_text('utf-8-sig')).get('usm_civilwar.1')
new_event=parse((C/'events/usm_civilwar_events.txt').read_text('utf-8-sig')).get('usm_civilwar.1')
original=old_event.all('option')[0]
def effect_payload(o):return [shape(n) for n in o.children if n.key not in ['trigger','default_option']]
loyal=[o for o in new_event.all('option') if o.scalar('name')=='usm_civilwar.1.1'];assert len(loyal)==2 and all(effect_payload(o)==effect_payload(original) for o in loyal)
# Bounded schedule arithmetic only; diplomatic backdown, destroyed participants and player deferral remain game outcomes.
dates={'case_window':'1837-07-01','case_deadline':'1838-01-01','accession_deadline':'1839-01-01','requested_limit':'1840-01-01'}
assert date.fromisoformat(dates['case_deadline'])<date.fromisoformat(dates['accession_deadline'])<date.fromisoformat(dates['requested_limit'])
assert int(parse((C/'common/journal_entries/ce_usm_the_last_days_of_ming.txt').read_text('utf-8-sig')).get('ce_usm_civilwar_journal').scalar('timeout'))==180
diff=[]
for rel in changed:diff+=list(difflib.unified_diff((B/rel).read_text('utf-8-sig').splitlines(True) if (B/rel).exists() else [],(C/rel).read_text('utf-8-sig').splitlines(True),fromfile='before/'+rel,tofile='after/'+rel))
(R/'changes.diff').write_text(''.join(diff),encoding='utf-8')
(R/'source-checks.json').write_text(json.dumps({'status':'STATIC_PASS','tests':len(after),'before_failures':[x['name'] for x in before if not x['pass']],'after':after,'dates':dates,'unchanged_history_maps_characters':True,'game_launched':False,'changed':changed,'before':bm,'after_manifest':cm},ensure_ascii=False,indent=2),encoding='utf-8')
print('Source checks:',len([x for x in before if not x['pass']]),'failures -> 0;',len(after),'checks; paired localization and preserved data PASS')
cmd=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game','D:/Program Files (x86)/Steam/steamapps/common/Victoria 3','--config',str(W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'),'--json',str(C)]
p=subprocess.run(cmd,capture_output=True);(R/'tiger-raw.json').write_bytes(p.stdout);(R/'tiger-stderr.txt').write_bytes(p.stderr)
a=json.loads(p.stdout.decode('utf-8-sig'));b=json.loads((W/'reports/button-guards-20261101/tiger-raw.json').read_text('utf-8-sig'))
def key(d):return json.dumps({'severity':d.get('severity'),'key':d.get('key'),'message':d.get('message'),'locations':[(x.get('from'),x.get('path'),(x.get('line') or '').strip()) for x in d.get('locations',[])]},ensure_ascii=False,sort_keys=True)
added=[json.loads(x) for x,n in (collections.Counter(map(key,a))-collections.Counter(map(key,b))).items() for _ in range(n)]
delta={'counts':dict(collections.Counter(x['severity'] for x in a)),'added':added,'command':cmd,'game_launched':False};(R/'tiger-delta.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2),encoding='utf-8');print('Tiger',delta['counts'],'added',len(added));assert not added,added
async def mcp_queries():
 from mcp import ClientSession,StdioServerParameters
 from mcp.client.stdio import stdio_client
 queries=[('common/scripted_effects/nesnd_south_timing.txt','nesnd_south_crisis_month','if.limit','1838.1.1'),('common/scripted_effects/nesnd_south_timing.txt','nesnd_south_enforce_crisis_deadline','if.clamp_variable','100'),('common/scripted_triggers/nesnd_succession_board.txt','nesnd_board_fixed_ming_allegiance','c:HNA','this'),('common/scripted_effects/nesnd_presentation_effects.txt','nesnd_refresh_south_display','if.je:nesnd_south_succession_board.set_bar_progress','nesnd_board_pressure_bar')]
 rows=[]
 async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize();ts=await session.list_tools();assert 'get_structure' in [t.name for t in ts.tools]
   result=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not result.isError
   for path,symbol,key_path,want in queries:
    result=await session.call_tool('get_structure',{'file_path':path,'symbol':symbol,'key_path':key_path});s='\n'.join(x.text for x in result.content if getattr(x,'type',None)=='text');assert not result.isError and want in s,(symbol,s)
    rows.append({'path':path,'symbol':symbol,'key_path':key_path,'sha256':sha(C/path),'response':s})
 (R/'mcp-queries.json').write_text(json.dumps({'status':'PASS','game_launched':False,'queries':rows},ensure_ascii=False,indent=2),encoding='utf-8');print('MCP: 4 nested source queries PASS')
asyncio.run(mcp_queries())
