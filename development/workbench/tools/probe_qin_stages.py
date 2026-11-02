from qin_stage_context import *
import asyncio
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
async def main():
 before=man(C);rows=[]
 tests=[('common/journal_entries/nesnd_qe1_court.txt','nesnd_qe1_court_journal','possible','nesnd_qe1_court_available'),('common/journal_entries/nesnd_qe1_recovery.txt','nesnd_qe1_recovery_journal','possible','nesnd_qe1_recovery_available'),('common/scripted_triggers/nesnd_qe1_campaign.txt','nesnd_qe1_court_available','has_variable','nesnd_qe1_court_opened'),('common/scripted_triggers/nesnd_qe1_campaign.txt','nesnd_qe1_recovery_available','has_variable','nesnd_qe1_recovery_opened')]
 async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize();x=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not x.isError
   for path,symbol,key,want in tests:
    args={'file_path':path,'symbol':symbol,'key_path':key};x=await session.call_tool('get_structure',args);body='\n'.join(n.text for n in x.content if getattr(n,'type',None)=='text')
    assert not x.isError and want in body,(args,body)
    rows.append({'query':args,'response':body,'source_sha256':sha(C/path)})
 assert man(C)==before
 dump(R/'qin-stage-mcp.json',{'status':'PASS','queries':rows,'candidate_unchanged':True,'engine_verified':False,'game_launched':False})
 print('Four MCP source queries PASS; no game started.')
asyncio.run(main())
