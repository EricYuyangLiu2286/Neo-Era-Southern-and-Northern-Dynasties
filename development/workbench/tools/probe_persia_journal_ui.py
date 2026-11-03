from qin_persia_context import W,sha,dump
import asyncio
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
C=W/'exports/persia-journal-ui-20261103-a';R=W/'reports/persia-journal-ui-20261103'
async def main():
    rows=[]
    async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
        async with ClientSession(r,w) as session:
            await session.initialize();res=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not res.isError
            for path,symbol,key,want in [
                ('common/journal_entries/nesnd_per_campaign.txt','nesnd_per_future_journal','complete.custom_tooltip','nesnd_per_future_complete_tt'),
                ('common/scripted_triggers/nesnd_per_campaign.txt','nesnd_per_economy_ready','country_has_building_type_levels.1','bt:building_textile_mill'),
                ('common/scripted_buttons/nesnd_per_campaign.txt','nesnd_per_economy_commit_button','possible','nesnd_per_economy_ready')]:
                args={'file_path':path,'symbol':symbol,'key_path':key};res=await session.call_tool('get_structure',args)
                body='\n'.join(x.text for x in res.content if getattr(x,'type',None)=='text')
                assert not res.isError and want in body,(args,body)
                rows.append({'query':args,'response':body,'sha256':sha(C/path)})
    dump(R/'mcp.json',{'status':'PASS','queries':rows,'engine_verified':False});print('MCP PASS',len(rows))
asyncio.run(main())
