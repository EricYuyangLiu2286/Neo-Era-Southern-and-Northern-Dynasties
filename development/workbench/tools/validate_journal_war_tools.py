from journal_war_context import *
import asyncio,subprocess
async def mcp():
    from mcp import ClientSession,StdioServerParameters
    from mcp.client.stdio import stdio_client
    qs=[]
    async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
        async with ClientSession(r,w) as session:
            await session.initialize();res=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not res.isError
            for path,symbol,key,want in [
                ('common/scripted_progress_bars/nesnd_japan_absolute_counters.txt','nesnd_eastern_readiness_bar','max_value','3'),
                ('common/journal_entries/nesnd_india_core.txt','nesnd_india_industry','should_be_pinned_by_default_uninvolved_or_context','True'),
                ('common/journal_entries/zzzz_nesnd_hus_native_monarchy.txt','REPLACE:je_abolish_monarchy','complete.nesnd_native_abolish_monarchy_eligible','True'),
                ('common/scripted_effects/nesnd_south_holdouts.txt','nesnd_south_court_collapse','if.if.c:USM.annex_as_civil_war','nesnd_court_fallen'),
                ('common/scripted_effects/nesnd_south_holdouts.txt','nesnd_holdout_reopen_war','if.if.scope:nesnd_holdout_new_play.add_escalation','90')]:
                args={'file_path':path,'symbol':symbol,'key_path':key};res=await session.call_tool('get_structure',args)
                body='\n'.join(x.text for x in res.content if getattr(x,'type',None)=='text');assert not res.isError and want in body,(args,body)
                qs.append({'query':args,'response':body,'sha256':sha(C/path)})
    dump(R/'mcp-final.json',{'status':'PASS','queries':qs,'engine_verified':False});print('MCP PASS',len(qs))
def tiger(phase):
    target=B if phase=='baseline' else C
    cmd=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game',str(G.parent),'--config',str(W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'),'--json',str(target)]
    with (R/f'tiger-{phase}.json').open('wb') as out,(R/f'tiger-{phase}.stderr.txt').open('wb') as err:p=subprocess.run(cmd,stdout=out,stderr=err)
    dump(R/f'tiger-{phase}-run.json',{'command':cmd,'returncode':p.returncode,'source_files':man(target),'game_launched':False});print('Tiger',phase,'complete',p.returncode)
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='mcp':asyncio.run(mcp())
    elif mode in ['baseline','candidate']:tiger(mode)
    elif mode=='compare':
        def sig(x):return x['severity'],x['key'],x['message'],tuple((z.get('path'),(z.get('line') or '').strip()) for z in x['locations'])
        old={sig(x) for x in json.loads(read(R/'tiger-baseline.json'))}
        added=[x for x in json.loads(read(R/'tiger-candidate.json')) if sig(x) not in old]
        dump(R/'tiger-added.json',added)
        print('Added diagnostics',len(added))
        for x in added:print(x['severity'],x['key'],x['message'],x['locations'][:1])
        sys.exit(bool(added))
