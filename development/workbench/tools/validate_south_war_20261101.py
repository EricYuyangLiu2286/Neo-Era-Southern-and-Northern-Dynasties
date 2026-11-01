from pathlib import Path
import sys,json,hashlib,subprocess,collections,asyncio,difflib
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');C=W/'exports/south-war-collapse-20261101-a';M=W.parent/'mod/Neo-Era Southern and Northern Dynasties';R=W/'reports/south-war-collapse-20261101'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def indent(s):
 depth=0;out=[]
 for line in s.splitlines():
  t=line.strip()
  if not t:out.append('');continue
  code='';quote=False;escape=False
  for c in t:
   if escape:escape=False;continue
   if c=='\\' and quote:escape=True;continue
   if c=='"':quote=not quote;continue
   if not quote:
    if c=='#':break
    code+=c
  leading=len(code)-len(code.lstrip('}'));out.append('\t'*max(0,depth-leading)+t);depth+=code.count('{')-code.count('}')
 assert depth==0;return '\n'.join(out)
for rel,keys in [('events/usm_civilwar_events.txt',['usm_civilwar.5','usm_civilwar.8','usm_civilwar.9']),('common/journal_entries/ce_usm_the_last_days_of_ming.txt',['ce_usm_suppress_rebellion','ce_usm_restoration_of_ming','ce_usm_acheive_revolution','ce_usm_cw_japanese_interest'])]:
 p=C/rel;b=p.read_bytes();s=b.decode('utf-8-sig');tree=parse(s)
 for n in sorted([tree.get(k) for k in keys],key=lambda n:n.start,reverse=True):s=s[:n.start]+indent(s[n.start:n.end])+s[n.end:]
 p.write_bytes((b'\xef\xbb\xbf' if b.startswith(b'\xef\xbb\xbf') else b'')+s.encode())
subprocess.run([sys.executable,'-X','utf8',str(W/'tools/check_south_war_20261101.py'),str(M),'red'],check=True)
subprocess.run([sys.executable,'-X','utf8',str(W/'tools/check_south_war_20261101.py'),str(C),'green'],check=True)
changed=[];diff=[]
for p in C.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(C).as_posix();q=M/rel
 if not q.exists() or sha(p)!=sha(q):
  changed.append({'file':rel,'before':sha(q) if q.exists() else None,'after':sha(p)})
  if p.suffix=='.txt':parse(p.read_text('utf-8-sig'))
  if p.suffix=='.yml':assert p.read_bytes().startswith(b'\xef\xbb\xbf')
  diff.extend(difflib.unified_diff(q.read_text('utf-8-sig').splitlines(True) if q.exists() else [],p.read_text('utf-8-sig').splitlines(True),fromfile='base/'+rel,tofile='candidate/'+rel))
assert all(not x['file'].startswith(('map_data/','common/history/pops/','common/history/buildings/','common/history/characters/','common/country_definitions/','common/history/countries/')) for x in changed)
(R/'candidate.diff').write_text(''.join(diff),encoding='utf-8');(R/'changed-files.json').write_text(json.dumps(changed,ensure_ascii=False,indent=2),encoding='utf-8')
cmd=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game',r'D:/Program Files (x86)/Steam/steamapps/common/Victoria 3','--config',str(W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'),'--json',str(C)]
p=subprocess.run(cmd,capture_output=True);(R/'tiger-raw.json').write_bytes(p.stdout);(R/'tiger-stderr.txt').write_bytes(p.stderr)
a=json.loads(p.stdout.decode('utf-8-sig'));b=json.loads((W/'reports/south-feedback-20261101/tiger-raw.json').read_text('utf-8-sig'))
def key(d):return json.dumps({'severity':d.get('severity'),'key':d.get('key'),'message':d.get('message'),'locations':[(x.get('from'),x.get('path'),(x.get('line') or '').strip()) for x in d.get('locations',[])]},ensure_ascii=False,sort_keys=True)
added=[json.loads(x) for x,n in (collections.Counter(map(key,a))-collections.Counter(map(key,b))).items() for _ in range(n)]
delta={'counts':dict(collections.Counter(x['severity'] for x in a)),'added':added,'command':cmd,'game_launched':False};(R/'tiger-delta.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2),encoding='utf-8');print('Tiger',delta['counts'],'added',len(added));assert not added,added
async def mcp_queries():
 from mcp import ClientSession,StdioServerParameters
 from mcp.client.stdio import stdio_client
 queries=[('events/usm_civilwar_events.txt','usm_civilwar.5','trigger','nesnd_south_capital_defeat'),('common/scripted_triggers/nesnd_war_collapse.txt','nesnd_japan_two_centres_lost','s:STATE_KANTO.any_scope_state.controller','has_war_with'),('common/on_actions/nesnd_war_collapse.txt','nesnd_record_wu_defeat','effect.if.limit','tag_WUU_var'),('common/journal_entries/ce_usm_the_last_days_of_ming.txt','ce_usm_suppress_rebellion','fail.NOT','nesnd_south_defeat_resolution_pending')]
 rows=[]
 async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize();result=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not result.isError
   for path,symbol,key_path,want in queries:
    result=await session.call_tool('get_structure',{'file_path':path,'symbol':symbol,'key_path':key_path});s='\n'.join(x.text for x in result.content if getattr(x,'type',None)=='text');assert not result.isError and want in s,(symbol,s)
    rows.append({'path':path,'symbol':symbol,'key_path':key_path,'sha256':sha(C/path),'response':s})
 (R/'mcp-queries.json').write_text(json.dumps({'status':'PASS','game_launched':False,'queries':rows},ensure_ascii=False,indent=2),encoding='utf-8');print('MCP: 4 nested source queries PASS')
asyncio.run(mcp_queries())
