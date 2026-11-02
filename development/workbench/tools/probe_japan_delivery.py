from japan_dev_context import *
import asyncio
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    before=man(C);rows=[]
    tests=[
        ('common/journal_entries/nesnd_jp_establishment.txt','nesnd_jp_establish_edo','possible','nesnd_jp_establishment_needed'),
        ('common/scripted_triggers/nesnd_jp_industry.txt','nesnd_jp_affordable_grain','trigger_if.capital','state_goods_pricier'),
        ('common/scripted_triggers/nesnd_supply_triggers.txt','nesnd_supply_diplomacy_ready','OR.trigger_if','participants'),
        ('common/scripted_effects/nesnd_supply_effects.txt','nesnd_supply_clear_partner',None,'nesnd_supply_partner'),
        ('common/scripted_triggers/nesnd_jp_foreign.txt','nesnd_jp_reply_valid','trigger_if.scope:jp_sender','jp_sender_regime'),
        ('common/character_templates/zz_ce_JAP.txt','JAP_toyotomi_heikatsu_alt','on_created','nesnd_jp_heikatsu_ever_created'),
        ('common/script_values/nesnd_jp_development.txt','nesnd_jp_conversion_fraction_jiangnan','divide','culture_percent_state(cu:ce_wuu)'),
        ('common/journal_entries/nesnd_jp_industry.txt','nesnd_jp_arsenals','complete','nesnd_jp_arsenals_ready'),
        ('common/scripted_buttons/nesnd_jp_foreign.txt','nesnd_jp_independence_play','possible.trigger_if','has_truce_with'),
        ('common/scripted_buttons/nesnd_jp_nation.txt','nesnd_jp_protected_ports','desc.first_valid','nesnd_jp_protected_ports_junior_desc'),
    ]
    async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
        async with ClientSession(r,w) as session:
            await session.initialize();x=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not x.isError
            for path,symbol,key,want in tests:
                args={'file_path':path,'symbol':symbol,'key_path':key}
                x=await session.call_tool('get_structure',args)
                body='\n'.join(n.text for n in x.content if getattr(n,'type',None)=='text')
                assert not x.isError and want in body,(args,body)
                rows.append({'query':args,'response':body,'source_sha256':sha(C/path)})
    assert before==man(C)
    dump(R/'mcp-final-queries.json',{'status':'PASS','queries':rows,'candidate_unchanged':True,'game_launched':False,'engine_verified':False})
    print('Ten actual MCP source queries passed; not engine execution.')
asyncio.run(main())
