from sweep_context import *
import asyncio
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
async def run():
 rows=[]
 async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize();r=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not r.isError
   for path,symbol,key,want in [
    ('common/scripted_buttons/nesnd_crisis_buttons.txt','nesnd_federal_compact_button','desc','nesnd_south_offer_accord_desc'),
    ('common/scripted_buttons/nesnd_jp_politics.txt','nesnd_jp_inspect_military','effect.show_as_tooltip.add_modifier.months','6'),
    ('common/scripted_buttons/nesnd_per_resources.txt','nesnd_per_industry_grant_button','effect.hidden_effect.if.change_variable.add','-40'),
    ('common/journal_entries/nesnd_per_governance.txt','nesnd_per_governance','scripted_progress_bar','nesnd_per_governance_bar'),
    ('common/static_modifiers/nesnd_usm_western_provinces.txt','nesnd_usm_ming_resistance','country_bureaucracy_investment_cost_factor_mult','0.15'),
    ('common/scripted_triggers/nesnd_usm_western_provinces.txt','nesnd_usm_western_eligible','has_variable','nesnd_usm_western_migrated'),
    ('common/scripted_effects/nesnd_per_campaign.txt','nesnd_per_attempt_claim','if.change_variable.add','-25')]:
    args={'file_path':path,'symbol':symbol,'key_path':key};result=await session.call_tool('get_structure',args)
    body='\n'.join(x.text for x in result.content if getattr(x,'type',None)=='text');assert not result.isError and want in body,(args,body)
    rows.append({'query':args,'response':body,'sha256':sha(C/path)})
 dump(R/'mcp-final.json',{'pass':True,'queries':rows,'engine_verified':False});print('MCP PASS',len(rows))
asyncio.run(run())
