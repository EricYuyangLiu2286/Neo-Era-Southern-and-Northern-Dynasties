from qin_persia_context import *
import asyncio
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
async def main():
 before=man(C);out=[]
 queries=[
 ('common/scripted_progress_bars/nesnd_qe1_agendas.txt','nesnd_qe1_balance_bar','min_value','-50'),
 ('common/scripted_triggers/nesnd_qe1_campaign.txt','nesnd_qe1_army_ready','trigger_if.limit','nesnd_qe1_barracks_snapshot_done'),
 ('common/scripted_effects/nesnd_qe1_identity.txt','nesnd_qe1_convert_selected_cohort',None,'(3 items)'),
 ('common/journal_entries/nesnd_qe1_identity.txt','nesnd_qe1_uprising_journal','possible','nesnd_qe1_uprising_awakened'),
 ('common/scripted_effects/nesnd_per_campaign.txt','nesnd_per_settle_future','if.limit','nesnd_per_future_eligible'),
 ('common/script_values/nesnd_per_campaign.txt','nesnd_per_future_delta','if.value','2'),
 ('common/laws/nesnd_qe1_laws.txt','law_nesnd_qe1_proportional_representation','group','lawgroup_distribution_of_power'),
 ('common/on_actions/nesnd_qin_persia.txt','on_game_started_after_lobby','on_actions','(1 items)')]
 async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize();q=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not q.isError
   for rel,symbol,key,want in queries:
    args={'file_path':rel,'symbol':symbol}
    if key:args['key_path']=key
    q=await session.call_tool('get_structure',args);s='\n'.join(x.text for x in q.content if getattr(x,'type',None)=='text');assert not q.isError and want in s,(args,s)
    out.append({'query':args,'source_sha256':sha(C/rel),'response':s})
 assert man(C)==before
 dump(R/'mcp-queries.json',{'status':'PASS','queries':out,'candidate_unchanged':True,'game_launched':False,'engine_verified':False})
 print('MCP source protocol queries PASS:',len(out))
asyncio.run(main())
