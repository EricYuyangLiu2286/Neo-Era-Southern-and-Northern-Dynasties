import asyncio,json
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');R=W/'reports/canon-route-execution-20261104'
cfg=json.loads((R/'batch-c-repair4-test-config.json').read_text('utf-8'));out=Path(cfg['run'])
async def main():
 report={'scope':'actual stdio MCP on fixed C snapshot','calls':[],'game_launched':False}
 server=W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'
 async with stdio_client(StdioServerParameters(command=str(server))) as (reader,writer):
  async with ClientSession(reader,writer) as session:
   report['initialize']=(await session.initialize()).model_dump(mode='json')
   report['schema']=(await session.list_tools()).model_dump(mode='json')
   calls=[('init_game',{'game_directory':cfg['snapshot'],'game_type':'vic3'}),
          ('get_structure',{'file_path':'common/scripted_effects/nesnd_egypt_independence.txt','symbol':'nesnd_egypt_settle_dependence'}),
          ('get_structure',{'file_path':'common/scripted_triggers/nesnd_canon_diplomacy.txt','symbol':'nesnd_canon_current_request_valid'}),
          ('get_structure',{'file_path':'common/scripted_triggers/nesnd_egypt_independence.txt','symbol':'nesnd_egypt_protected_fact'}),
          ('get_structure',{'file_path':'events/nesnd_canon_diplomacy.txt','symbol':'nesnd_canon_diplomacy.1'}),
          ('get_structure',{'file_path':'common/scripted_triggers/nesnd_canon_diplomacy.txt','symbol':'nesnd_canon_reply_valid'}),
          ('get_structure',{'file_path':'common/scripted_triggers/nesnd_europe_america.txt','symbol':'nesnd_austrian_intervention_ready'}),
          ('get_structure',{'file_path':'common/scripted_effects/nesnd_europe_america.txt','symbol':'nesnd_usa_press_west'}),
          ('get_structure',{'file_path':'common/journal_entries/nesnd_egypt_independence.txt','symbol':'nesnd_egypt_investment_accounts'})]
   for name,args in calls:
    r=await session.call_tool(name,args);v=r.model_dump(mode='json')
    report['calls'].append({'tool':name,'args':args,'result':v})
    print(name,'ERROR' if r.isError else 'OK',args.get('symbol','init'))
    if r.isError:report['status']='FAIL_TOOL';break
   else:report['status']='QUERY_COMPLETED_NOT_ENGINE_VALIDATION'
 (out/'mcp-c-owned.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
asyncio.run(main())
