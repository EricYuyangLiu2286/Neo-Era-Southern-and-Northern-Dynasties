from cne_native_context import *
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
                ('common/script_values/nesnd_cne_confidence.txt','nesnd_cne_conf_delay','if.if.add.floor','True'),
                ('events/poland_events.txt','poland_events.1','trigger.always','False'),
                ('events/zanzibar_events.txt','zanzibar.1','cancellation_trigger.always','True'),
                ('common/journal_entries/zzzz_nesnd_native_error_bans.txt','REPLACE:je_splitting_oman','invalid.always','True'),
                ('common/naval_battle_conditions/00_naval_battle_conditions.txt','naval_condition_cyclone','possible.always','False')]:
                args={'file_path':path,'symbol':symbol,'key_path':key};res=await session.call_tool('get_structure',args)
                body='\n'.join(x.text for x in res.content if getattr(x,'type',None)=='text')
                assert not res.isError and want in body,(args,body)
                queries.append({'query':args,'response':body,'sha256':sha(C/path)})
    dump(R/'mcp-final.json',{'status':'PASS','queries':queries,'engine_verified':False});print('MCP PASS',len(queries))

def tiger(phase):
    target=W/'exports/cne-native-tiger-control-20261103' if phase=='control' else C
    cmd=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game',str(G.parent),'--config',str(W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'),'--json',str(target)]
    with (R/f'tiger-{phase}.json').open('wb') as out,(R/f'tiger-{phase}.stderr.txt').open('wb') as err:p=subprocess.run(cmd,stdout=out,stderr=err)
    dump(R/f'tiger-{phase}-run.json',{'command':cmd,'returncode':p.returncode,'source_files':man(target),'game_launched':False});print('Tiger',phase,'complete',p.returncode)

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='mcp':asyncio.run(mcp_check())
    elif mode in ('control','candidate'):tiger(mode)
    elif mode=='compare':
        def sig(x):return x['severity'],x['key'],x['message'],tuple((z.get('path'),(z.get('line') or '').strip()) for z in x['locations'])
        old={sig(x) for x in json.loads(read(R/'tiger-control.json'))}
        added=[x for x in json.loads(read(R/'tiger-candidate.json')) if sig(x) not in old]
        dump(R/'tiger-added.json',added);print('Added diagnostics',len(added))
        for x in added:print(x['severity'],x['key'],x['message'])
        sys.exit(bool(added))
