from canon_routes_context import *
import asyncio,collections,subprocess,sys
META=json.loads(read(R/'batch-b-test-snapshot.json'));T=Path(META['snapshot'])

async def mcp_queries():
    from mcp import ClientSession,StdioServerParameters
    from mcp.client.stdio import stdio_client
    before=man(T);rows=[]
    queries=[
        ('common/static_modifiers/nesnd_unity_policies.txt','nesnd_unity_material_expense','country_expenses_add','1'),
        ('common/static_modifiers/nesnd_unity_policies.txt','nesnd_unity_political_assistance','country_legitimacy_base_add','-10'),
        ('common/scripted_effects/nesnd_unity_policies.txt','nesnd_unity_start_material','if.add_modifier[0].months','12'),
        ('common/scripted_effects/nesnd_unity_policies.txt','nesnd_unity_material_monthly_cost','if.every_primary_culture','0.001'),
        ('common/scripted_triggers/nesnd_ottoman_unity.txt','nesnd_ottoman_unity_available','OR','36'),
        ('common/scripted_triggers/nesnd_ottoman_unity.txt','nesnd_ottoman_culture_arab','OR.has_discrimination_trait[2]','heritage_afro_arab'),
        ('common/script_values/nesnd_qe1_identity.txt','nesnd_qe1_unity_laws','add','2 items'),
        ('common/scripted_progress_bars/nesnd_india_core.txt','nesnd_india_community_bar','monthly_progress.add[2].desc','nesnd_unity_lawgroup_citizenship'),
        ('events/nesnd_ottoman_recovery.txt','nesnd_ottoman_recovery.1','trigger.NOT.has_variable','nesnd_ottoman_reform_term'),
        ('common/scripted_triggers/nesnd_ottoman_recovery.txt','nesnd_ottoman_claim_target','trigger_if.c:TUR.NOT[0].has_claim','prev'),
        ('common/static_modifiers/nesnd_ottoman_recovery.txt','nesnd_ottoman_qin_reform','unit_supply_consumption_mult','-0.2'),
        ('common/static_modifiers/nesnd_ottoman_recovery.txt','nesnd_ottoman_qin_reform_success','unit_supply_consumption_mult','-0.25'),
        ('common/static_modifiers/nesnd_ottoman_recovery.txt','nesnd_ottoman_qin_reform_failed','unit_supply_consumption_mult','-0.15'),
    ]
    async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
        async with ClientSession(r,w) as session:
            await session.initialize()
            init=await session.call_tool('init_game',{'game_directory':str(T),'game_type':'vic3'})
            assert not init.isError
            for rel,symbol,key,want in queries:
                args={'file_path':rel,'symbol':symbol,'key_path':key}
                result=await session.call_tool('get_structure',args)
                body='\n'.join(x.text for x in result.content if getattr(x,'type',None)=='text')
                ok=not result.isError and want in body
                if symbol=='nesnd_ottoman_unity_available':
                    ok=ok and 'num_states' in body and '>=' in body
                rows.append({'query':args,'response':body,'source_sha256':sha(T/rel),'pass':ok})
                if not ok:
                    dump(R/'batch-b-mcp.json',{'status':'FAIL_STOP','queries':rows,'snapshot':str(T),'engine_verified':False})
                    raise AssertionError((args,body,want))
    assert man(T)==before
    dump(R/'batch-b-mcp.json',{'status':'PASS','queries':rows,'snapshot':str(T),'unchanged':True,'engine_verified':False})
    print('MCP PASS:',len(rows),'actual protocol queries')

def tiger():
    config=W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'
    runs=[]
    for label,source in [('baseline',B),('snapshot',T)]:
        before=man(source)
        cmd=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game',str(G.parent),'--config',str(config),'--json',str(source)]
        with (R/f'batch-b-tiger-{label}.json').open('wb') as out,(R/f'batch-b-tiger-{label}.stderr.txt').open('wb') as err:
            p=subprocess.run(cmd,stdout=out,stderr=err)
        assert man(source)==before
        runs.append({'source':str(source),'command':cmd,'returncode':p.returncode,'unchanged':True})
    def key(x):
        return (x['severity'],x['key'],x['message'],tuple((n.get('from'),n.get('path'),(n.get('line') or '').strip()) for n in x['locations']))
    baseline=json.loads(read(R/'batch-b-tiger-baseline.json'));current=json.loads(read(R/'batch-b-tiger-snapshot.json'))
    counts=collections.Counter(map(key,baseline));added=[]
    for x in current:
        k=key(x)
        if counts[k]:counts[k]-=1
        else:added.append(x)
    owned=set(META['frozen_files'])|set(META['dependency_files'])
    scoped=[x for x in added if any(str(n.get('path','')).replace('\\','/') in owned for n in x['locations'])]
    result={'status':'DIAGNOSTICS_REQUIRE_CLASSIFICATION','runs':runs,'baseline_count':len(baseline),'snapshot_count':len(current),'all_added_count':len(added),'batch_b_added_count':len(scoped),'batch_b_added':scoped,'all_added':added,'engine_verified':False}
    dump(R/'batch-b-tiger-delta.json',result)
    print('Tiger fixed snapshot diagnostics:',len(current),'added:',len(added),'B-scoped:',len(scoped))
    for (severity,key,message),count in collections.Counter((x['severity'],x['key'],x['message']) for x in scoped).items():
        print(count,severity,key,message)

if __name__=='__main__':
    if sys.argv[1]=='mcp':asyncio.run(mcp_queries())
    elif sys.argv[1]=='tiger':tiger()
