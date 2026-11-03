from observer_logfix_context import *
from pdx import effective_files
import subprocess,asyncio

async def mcp_check():
    from mcp import ClientSession,StdioServerParameters
    from mcp.client.stdio import stdio_client
    queries=[]
    async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
        async with ClientSession(r,w) as session:
            await session.initialize()
            res=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not res.isError
            for path,symbol,key,want in [
                ('events/nesnd_external_events.txt','nesnd_external.2','cancellation_trigger.NOT','nesnd_external_request_valid'),
                ('common/scripted_effects/nesnd_qe1_fracture.txt','nesnd_qe1_setup_civil_challenger','create_character.ideology','ideology_jingoist_leader'),
                ('common/journal_entries/zzzz_nesnd_india_native.txt','REPLACE:je_uneasy_raj','should_be_involved.always','False'),
                ('common/scripted_effects/nesnd_ming_royal_refuge.txt','nesnd_ming_mark_retained_royals','if.if.0.limit.trigger_if.limit.exists','nesnd_ming_claimant_ref')]:
                args={'file_path':path,'symbol':symbol,'key_path':key}
                res=await session.call_tool('get_structure',args)
                body='\n'.join(x.text for x in res.content if getattr(x,'type',None)=='text')
                assert not res.isError and want in body,(args,body)
                queries.append({'query':args,'response':body,'sha256':sha(C/path)})
    dump(R/'mcp-final.json',{'status':'PASS','queries':queries,'engine_verified':False});print('MCP PASS',len(queries))

def tiger(phase):
    target=B if phase=='baseline' else C
    cmd=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game',str(G.parent),'--config',str(W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'),'--json',str(target)]
    with (R/f'tiger-{phase}.json').open('wb') as out,(R/f'tiger-{phase}.stderr.txt').open('wb') as err:
        p=subprocess.run(cmd,stdout=out,stderr=err)
    dump(R/f'tiger-{phase}-run.json',{'command':cmd,'returncode':p.returncode,'source_files':man(target),'game_launched':False})
    print('Tiger complete',phase,p.returncode)

if __name__=='__main__':
    if sys.argv[1]=='mcp':asyncio.run(mcp_check())
    elif sys.argv[1] in ('baseline','candidate'):tiger(sys.argv[1])
    elif sys.argv[1]=='compare':
        def sig(x):return x['severity'],x['key'],x['message'],tuple((z.get('path'),(z.get('line') or '').strip()) for z in x['locations'])
        old={sig(x) for x in json.loads(read(R/'tiger-baseline.json'))}
        added=[x for x in json.loads(read(R/'tiger-candidate.json')) if sig(x) not in old]
        dump(R/'tiger-added.json',added)
        print('Added Tiger diagnostics',len(added))
        for x in added:print(x['severity'],x['key'],x['message'])
        sys.exit(bool(added))
