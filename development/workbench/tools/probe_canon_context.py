from canon_prose_context import *
import asyncio
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    before=man(E);rows=[]
    tests=[
        ('events/nesnd_crisis_events.txt','nesnd_crisis.30','desc.first_valid','nesnd_crisis.30.local'),
        ('events/nesnd_crisis_events.txt','nesnd_crisis.30','immediate.ordered_scope_state','nesnd_land_petition_state'),
        ('common/scripted_buttons/nesnd_south_accords.txt','nesnd_south_offer_accord','desc.first_valid','nesnd_federal_compact_button_alt_desc'),
        ('common/scripted_triggers/nesnd_per_campaign.txt','nesnd_per_aid_live','trigger_if.NOT','has_war_with'),
        ('events/nesnd_per_campaign.txt','nesnd_per.4','desc.first_valid','nesnd_per.4.d_unavailable'),
        ('events/nesnd_south_accords.txt','nesnd_south_accords.20','trigger.nesnd_south_ming_peace_ready','True'),
    ]
    async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
        async with ClientSession(r,w) as session:
            await session.initialize()
            result=await session.call_tool('init_game',{'game_directory':str(E),'game_type':'vic3'});assert not result.isError
            for path,symbol,key,want in tests:
                args={'file_path':path,'symbol':symbol,'key_path':key}
                result=await session.call_tool('get_structure',args)
                body='\n'.join(n.text for n in result.content if getattr(n,'type',None)=='text')
                assert not result.isError and want in body,(args,body)
                rows.append({'query':args,'response':body,'source_sha':sha(E/path)})
    assert before==man(E)
    dump(R/'mcp-source-queries.json',{'status':'PASS','queries':rows,'candidate_unchanged':True,'game_launched':False,'engine_verified':False})
    print('Six actual MCP source queries passed; no engine execution.')
asyncio.run(main())
