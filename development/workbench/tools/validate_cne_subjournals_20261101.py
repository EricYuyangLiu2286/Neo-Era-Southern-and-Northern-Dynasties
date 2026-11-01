"""Use WORK/tools/mcp-venv/Scripts/python.exe. Source tooling only; no game process."""
from pathlib import Path
import sys,json,hashlib,subprocess,collections,difflib,asyncio,re
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts');from pdx import parse
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');C=W/'exports/cne-reform-subjournals-20261101-a';M=W/'backups/pre-change-cne-reform-subjournals-20261101T222906Z/mod';R=W/'reports/cne-reform-subjournals-20261101'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def shape(n):return (n.key,n.op,n.value,tuple(shape(c) for c in n.children or []))
def indent(s):
 depth=0;out=[]
 for line in s.splitlines():
  t=line.strip()
  if not t:out.append('');continue
  code='';quoted=False;escaped=False
  for ch in t:
   if escaped:escaped=False;continue
   if ch=='\\' and quoted:escaped=True;continue
   if ch=='"':quoted=not quoted;continue
   if not quoted:
    if ch=='#':break
    code+=ch
  leading=len(code)-len(code.lstrip('}'));out.append('\t'*max(0,depth-leading)+t);depth+=code.count('{')-code.count('}')
 assert depth==0;return '\n'.join(out)+'\n'
for rel in ['common/scripted_effects/nesnd_cne_programs.txt','common/scripted_triggers/nesnd_cne_programs.txt','events/nesnd_cne_funding.txt']:
 p=C/rel;s=p.read_text('utf-8-sig');out=indent(s);assert shape(parse(out))==shape(parse(s));p.write_bytes(b'\xef\xbb\xbf'+out.encode())
for label,root in [('red',M),('green',C)]:subprocess.run([sys.executable,'-X','utf8',str(W/'tools/check_cne_subjournals_20261101.py'),str(root),label],check=True)
diff=[];changes=[]
for p in C.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(C).as_posix();q=M/rel
 if not q.exists() or sha(p)!=sha(q):
  changes.append({'file':rel,'before':sha(q) if q.exists() else None,'after':sha(p)})
  if p.suffix=='.txt':parse(p.read_text('utf-8-sig'))
  if p.suffix=='.yml':assert p.read_bytes().startswith(b'\xef\xbb\xbf')
  diff.extend(difflib.unified_diff(q.read_text('utf-8-sig').splitlines(True) if q.exists() else [],p.read_text('utf-8-sig').splitlines(True),fromfile='base/'+rel,tofile='candidate/'+rel))
assert all(not x['file'].startswith(('map_data/','common/history/','common/country_definitions/','gfx/','.metadata/')) for x in changes)
# Revised localization keys have one active definition in each language; no competing old rules tooltip.
for lang in ['simp_chinese','english']:
 own=C/f'localization/{lang}/replace/zzzzzz_nesnd_cne_programs_l_{lang}.yml';keys=set(re.findall(r'^ ([\w.]+):',own.read_text('utf-8-sig'),re.M));counts=collections.Counter()
 for p in (C/f'localization/{lang}').rglob('*.yml'):counts.update(k for k in re.findall(r'^ ([\w.]+):',p.read_text('utf-8-sig'),re.M) if k in keys)
 assert all(counts[k]==1 for k in keys),{k:counts[k] for k in keys if counts[k]!=1}
(R/'candidate.diff').write_text(''.join(diff),encoding='utf-8');(R/'changed-files.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
cmd=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game',r'D:/Program Files (x86)/Steam/steamapps/common/Victoria 3','--config',str(W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'),'--json',str(C)]
p=subprocess.run(cmd,capture_output=True);(R/'tiger-raw.json').write_bytes(p.stdout);(R/'tiger-stderr.txt').write_bytes(p.stderr)
a=json.loads(p.stdout.decode('utf-8-sig'));b=json.loads((W/'reports/south-war-collapse-20261101/tiger-raw.json').read_text('utf-8-sig'))
def key(d):return json.dumps({'severity':d.get('severity'),'key':d.get('key'),'message':d.get('message'),'locations':[(x.get('from'),x.get('path'),(x.get('line') or '').strip()) for x in d.get('locations',[])]},ensure_ascii=False,sort_keys=True)
added=[json.loads(x) for x,n in (collections.Counter(map(key,a))-collections.Counter(map(key,b))).items() for _ in range(n)]
out={'counts':dict(collections.Counter(x['severity'] for x in a)),'added':added,'command':cmd,'game_launched':False};(R/'tiger-delta.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print('Tiger:',out['counts'],'added:',len(added));assert not added,added
async def mcp_queries():
 from mcp import ClientSession,StdioServerParameters
 from mcp.client.stdio import stdio_client
 queries=[('common/scripted_triggers/nesnd_cne_programs.txt','nesnd_cne_camp_shaanbei_ready','trigger_if.limit','region_state:CNE'),('common/scripted_triggers/nesnd_cne_programs.txt','nesnd_cne_relief_target_valid','trigger_if.scope:nesnd_cne_funding_state.any_scope_pop.OR','is_in_mild_starvation'),('common/scripted_effects/nesnd_cne_programs.txt','nesnd_cne_register_officer','if.owner.add_to_variable_list','nesnd_cne_reform_officers'),('common/scripted_triggers/nesnd_cne_programs.txt','nesnd_cne_coup_has_succeeded','OR.AND','modifier_government_recently_couped'),('common/script_values/nesnd_cne_programs.txt','nesnd_cne_engines_levels','every_scope_state.every_scope_building.limit','building_motor_industry')]
 rows=[]
 async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize();x=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not x.isError
   for path,symbol,key_path,want in queries:
    x=await session.call_tool('get_structure',{'file_path':path,'symbol':symbol,'key_path':key_path});s='\n'.join(c.text for c in x.content if getattr(c,'type',None)=='text');assert not x.isError and want in s,(symbol,s)
    rows.append({'path':path,'symbol':symbol,'key_path':key_path,'sha256':sha(C/path),'response':s})
 (R/'mcp-queries.json').write_text(json.dumps({'status':'PASS','game_launched':False,'queries':rows},ensure_ascii=False,indent=2),encoding='utf-8');print('MCP: 5 nested source queries PASS')
asyncio.run(mcp_queries())
