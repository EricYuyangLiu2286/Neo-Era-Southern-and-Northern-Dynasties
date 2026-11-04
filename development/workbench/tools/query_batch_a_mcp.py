from pathlib import Path
import asyncio,json,hashlib,re
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');R=W/'reports/canon-route-execution-20261104'
T=Path(json.loads((R/'batch-a-test-snapshot.json').read_text(encoding='utf-8'))['snapshot'])
SERVER=W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'
QUERIES=[
 ('common/law_groups/nesnd_hus_social_hierarchy.txt','lawgroup_nesnd_hus_social_hierarchy','linked_social_hierarchy',r'nesnd_hus_social_hierarchy'),
 ('common/laws/nesnd_hus_social_hierarchy.txt','law_nesnd_hus_manchu_registration','modifier.country_nesnd_hus_manchu_lower_acceptance_min_add',r'\b80\b'),
 ('common/social_classes/nesnd_hus_social_classes.txt','nesnd_hus_manchu_lower','pop_criteria.culture.nesnd_hus_manchu_class_culture',r'\b(?:yes|True)\b'),
 ('common/on_actions/nesnd_hus_registration.txt','nesnd_hus_hierarchy_law_activated','trigger.owner.NOT.has_variable',r'nesnd_hus_hierarchy_mutating'),
 ('common/laws/nesnd_hus_registration.txt','law_nesnd_hus_hierarchy','is_visible.always',r'\b(?:no|False)\b'),
 ('common/history/countries/HUS.txt','COUNTRIES','c:HUS.nesnd_hus_initialize_hierarchy',r'\b(?:yes|True)\b'),
 ('common/scripted_effects/nesnd_hus_registration.txt','nesnd_hus_sync_cmf_law','active_law:lawgroup_nesnd_hus_social_hierarchy.save_scope_as',r'nesnd_hus_display_law'),
 ('common/scripted_effects/nesnd_native_khanate.txt','nesnd_native_primary_cultures_only','if.if.add_primary_culture',r'cu:siouan'),
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
async def main():
 report={'status':'RUNNING','snapshot':str(T),'server':str(SERVER),'server_sha256':sha(SERVER),'calls':[],'engine_verified':False,'whole_C_checked':False}
 paths=sorted({x[0] for x in QUERIES});report['source_hashes_before']={p:sha(T/p) for p in paths}
 try:
  async with stdio_client(StdioServerParameters(command=str(SERVER),cwd=str(W/'tools'))) as (r,w):
   async with ClientSession(r,w) as session:
    await session.initialize();listed=await session.list_tools();report['tool_schemas']={x.name:x.inputSchema for x in listed.tools}
    result=await session.call_tool('init_game',{'game_directory':str(T),'game_type':'vic3'})
    text='\n'.join(x.text for x in result.content if getattr(x,'type',None)=='text');report['initialization']=text
    if result.isError or 'Initialized vic3:' not in text:raise RuntimeError(('init_game',text))
    for path,symbol,key,pattern in QUERIES:
     args={'file_path':path,'symbol':symbol,'key_path':key};res=await session.call_tool('get_structure',args)
     body='\n'.join(x.text for x in res.content if getattr(x,'type',None)=='text')
     ok=not res.isError and not body.lower().startswith('error') and re.search(pattern,body) is not None
     report['calls'].append({'query':args,'response':body,'pass':ok,'source_sha256':sha(T/path)})
     if not ok:raise RuntimeError(('source_query_failed',args,body))
  report['status']='PASS'
 except Exception as exc:report['status']='FAIL';report['error']=repr(exc)
 report['source_hashes_after']={p:sha(T/p) for p in paths};report['snapshot_sources_unchanged']=report['source_hashes_before']==report['source_hashes_after']
 if not report['snapshot_sources_unchanged']:report['status']='FAIL'
 (R/'batch-a-mcp.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'status':report['status'],'queries':len(report['calls']),'error':report.get('error'),'report':str(R/'batch-a-mcp.json')},ensure_ascii=False))
 return report['status']=='PASS'
if __name__=='__main__':raise SystemExit(0 if asyncio.run(asyncio.wait_for(main(),45)) else 1)
