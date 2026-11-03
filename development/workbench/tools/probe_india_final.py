from india_context import *
import asyncio
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
async def main():
 rows=[]
 async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize();res=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not res.isError
   for path,symbol,key,want in [
    ('common/country_definitions/nesnd_commissions.txt','TZ1','country_type','colonial'),
    ('common/script_values/nesnd_india_core.txt','nesnd_india_case_stage_value','if.limit','nesnd_india_case_stage'),
    ('common/journal_entries/nesnd_india_uprising.txt','nesnd_india_revolt_war','fail.NOT','nesnd_india_revolt_won'),
    ('common/scripted_effects/nesnd_india_uprising.txt','nesnd_india_circars_create_play','clear_saved_scope','india_case_backer'),
    ('common/scripted_triggers/nesnd_india_core.txt','nesnd_india_industry_ready','OR.0.country_has_building_type_levels','bt:building_coal_mine'),
    ('common/scripted_progress_bars/nesnd_india_core.txt','nesnd_india_contact_bar','monthly_progress.add.0','nesnd_india_case_organisation'),
    ('common/journal_entries/nesnd_india_core.txt','nesnd_india_dynasty_journal','immediate','nesnd_india_sync_dynasty')]:
    args={'file_path':path,'symbol':symbol,'key_path':key};res=await session.call_tool('get_structure',args);body='\n'.join(x.text for x in res.content if getattr(x,'type',None)=='text');assert not res.isError and want in body,(args,body);rows.append({'query':args,'response':body,'sha256':sha(C/path)})
 dump(R/'mcp-final.json',{'status':'PASS','queries':rows,'engine_verified':False});print('MCP PASS',len(rows))
asyncio.run(main())
