from regional_context import *
import asyncio
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
async def run():
 rows=[]
 async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize();reply=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not reply.isError
   for path,symbol,key,want in [
    ('common/journal_entries/nesnd_regional_development.txt','nesnd_rg_pru','scripted_progress_bar','nesnd_rg_work'),
    ('common/scripted_triggers/nesnd_regional_development.txt','nesnd_rg_tur_entry','has_variable','sick_man_complete'),
    ('common/scripted_triggers/nesnd_regional_development.txt','nesnd_rg_usa_entry','has_law','law_slavery_banned'),
    ('common/scripted_progress_bars/nesnd_regional_development.txt','nesnd_rg_work','max_value','12'),
    ('common/scripted_effects/nesnd_regional_development.txt','nesnd_rg_reward','if.add_modifier.months','60'),
    ('common/journal_entries/nesnd_regional_development.txt','nesnd_rg_peu','timeout','5475'),
    ('common/static_modifiers/nesnd_regional_development.txt','nesnd_rg_provincial_schools','state_education_access_add','0.05')]:
    args={'file_path':path,'symbol':symbol,'key_path':key};reply=await session.call_tool('get_structure',args);body='\n'.join(x.text for x in reply.content if getattr(x,'type',None)=='text')
    assert not reply.isError and want in body,(args,body);rows.append({'query':args,'response':body,'sha256':sha(C/path)})
 dump(R/'mcp-final.json',{'pass':True,'queries':rows,'engine_verified':False});print('MCP PASS',len(rows))
asyncio.run(run())
