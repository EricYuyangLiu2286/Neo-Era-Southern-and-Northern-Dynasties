from commission_context import *
import asyncio
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
async def main():
 rows=[]
 async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize();res=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not res.isError
   for path,symbol,key,want in [
    ('common/scripted_triggers/nesnd_commissions.txt','nesnd_tianzhu_commission_ready','custom_tooltip.1.any_state_region','12'),
    ('common/scripted_triggers/nesnd_commission_expansion.txt','nesnd_commission_owner_in_realm','trigger_if.limit.exists','c:USM'),
    ('common/scripted_triggers/nesnd_commissions.txt','nesnd_yuanshan_commission_ready','custom_tooltip.1.any_state_region','4'),
    ('common/journal_entries/nesnd_india_diplomacy.txt','nesnd_india_foreign','on_invalid','nesnd_india_remove_advisers'),
    ('common/scripted_triggers/nesnd_commission_expansion.txt','nesnd_tianzhu_commission_entry','has_technology_researched','civilizing_mission')]:
    args={'file_path':path,'symbol':symbol,'key_path':key};res=await session.call_tool('get_structure',args);body='\n'.join(x.text for x in res.content if getattr(x,'type',None)=='text');assert not res.isError and want in body,(args,body);rows.append({'query':args,'response':body,'sha256':sha(C/path)})
 dump(R/'mcp-final.json',{'status':'PASS','queries':rows,'engine_verified':False});print('MCP PASS',len(rows))
asyncio.run(main())
