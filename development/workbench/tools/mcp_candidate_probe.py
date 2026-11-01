"""Parameterized adapter of the existing mcp_smoke.py: actual read-only stdio calls.
Run with tools/mcp-venv/Scripts/python.exe, not the engine or an emulation.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,asyncio,hashlib,json,re,sys,importlib.metadata
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
SERVER=W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(p):return {f.relative_to(p).as_posix():sha(f) for f in sorted(p.rglob('*')) if f.is_file()}
async def probe(candidate,out):
    report={'adapter':'existing MCP Python SDK / mcp_smoke workflow','candidate':str(candidate),'utc':datetime.now(timezone.utc).isoformat(),'status':'NOT_RUN','engine_verified':False,'calls':[],
            'boundary':'Only protocol availability and candidate source query. Not game execution, semantic validity, event coverage or economy proof.'}
    before=manifest(candidate);report['candidate_manifest_before']=before
    source=candidate/'map_data/state_regions/05_north_america.txt'
    sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
    from pdx import read
    _,tree=read(source);expected=tree.get('STATE_HAWAIIAN_ISLANDS').scalar('naval_exit_id')
    report['query_source']={'path':str(source),'sha256':sha(source),'expected_hawaii_naval_exit':expected}
    try:
        from mcp import ClientSession,StdioServerParameters
        from mcp.client.stdio import stdio_client
    except ImportError as e:report['reason']='MCP SDK unavailable in selected interpreter: '+str(e)
    else:
        if not SERVER.exists():report['reason']='Installed MCP stdio server absent'
        else:
            report['server']={'command':str(SERVER),'sha256':sha(SERVER),'mcp_sdk_version':importlib.metadata.version('mcp')}
            src=W/'tools/paradox-script-mcp/src/paradox_script_mcp/server.py'
            report['server']['source_path']=str(src);report['server']['source_sha256']=sha(src)
            async def calls():
                async with stdio_client(StdioServerParameters(command=str(SERVER),cwd=str(W/'tools'))) as (reader,writer):
                    async with ClientSession(reader,writer) as s:
                        init=await s.initialize();report['calls'].append({'request':{'method':'initialize','params':'existing SDK defaults'},'response':init.model_dump(mode='json')})
                        listed=await s.list_tools();report['calls'].append({'request':{'method':'tools/list','params':{}},'response':listed.model_dump(mode='json')})
                        schemas={t.name:t.inputSchema for t in listed.tools}
                        assert 'init_game' in schemas and 'get_structure' in schemas
                        assert 'game_type' in schemas['init_game']['properties'],'Missing locally repaired vic3 parameter'
                        for name,args in [('init_game',{'game_directory':str(candidate),'game_type':'vic3'}),('get_structure',{'file_path':'map_data/state_regions/05_north_america.txt','symbol':'STATE_HAWAIIAN_ISLANDS'})]:
                            result=await s.call_tool(name,args);data=result.model_dump(mode='json');report['calls'].append({'request':{'method':'tools/call','params':{'name':name,'arguments':args}},'response':data})
                            assert not result.isError,'MCP returned isError'
                            texts='\n'.join(c.text for c in result.content if getattr(c,'type',None)=='text')
                            assert not texts.lower().startswith('error'),texts
                            if name=='init_game':assert 'Initialized vic3:' in texts
                            else:
                                m=re.search(r'naval_exit_id:\s*(\d+)',texts);assert m and m[1]==expected,('Candidate query mismatch',texts)
                                report['observed_hawaii_naval_exit']=m[1]
            try:
                await asyncio.wait_for(calls(),timeout=45);report['status']='PASS'
            except Exception as e:report['status']='FAIL';report['reason']=repr(e)
    after=manifest(candidate);report['candidate_manifest_after']=after;report['candidate_unchanged']=before==after
    if before!=after:report['status']='FAIL';report['reason']='Candidate changed during read-only query'
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
    return {'status':report['status'],'engine_verified':False,'candidate_unchanged':before==after,'report':str(out),'observed_hawaii_naval_exit':report.get('observed_hawaii_naval_exit'),'reason':report.get('reason')}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--candidate',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if not a.out.resolve().is_relative_to(W.resolve()):raise ValueError('Report must stay in WORK')
    r=asyncio.run(probe(a.candidate.resolve(),a.out.resolve()));print(json.dumps(r,ensure_ascii=False));raise SystemExit(1 if r['status']=='FAIL' else 0)
