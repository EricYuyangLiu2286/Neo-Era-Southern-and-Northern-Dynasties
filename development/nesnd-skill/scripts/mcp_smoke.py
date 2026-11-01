"""Exercise installed MCP over stdio against real game and mod files."""
import asyncio, json
from pathlib import Path
from datetime import datetime, timezone
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from catalog import GAME, MOD, WORK

async def main():
    command=WORK/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'
    report={'utc':datetime.now(timezone.utc).isoformat(), 'server':str(command), 'calls':[]}
    async with stdio_client(StdioServerParameters(command=str(command))) as (reader, writer):
        async with ClientSession(reader,writer) as session:
            result=await session.initialize()
            report['initialize']=result.model_dump(mode='json')
            ts=await session.list_tools()
            report['tools']=ts.model_dump(mode='json')
            calls=[('init_game',{'game_directory':str(GAME),'game_type':'vic3'}),
                   ('get_structure',{'file_path':'common/social_classes/00_default.txt','symbol':'upper_class'}),
                   ('get_structure',{'file_path':'map_data/state_regions/11_east_asia.txt','symbol':'STATE_GUANGDONG'}),
                   ('init_game',{'game_directory':str(MOD),'game_type':'vic3'}),
                   ('get_structure',{'file_path':'events/flavorUSM_ce.txt','symbol':'flavorUSM.1'}),
                   ('get_structure',{'file_path':'common/scripted_progress_bars/ce_poland_progress_bars.txt','symbol':'ce_polish_reconquest_energy_bar'})]
            for name,args in calls:
                result=await session.call_tool(name,args)
                data=result.model_dump(mode='json')
                report['calls'].append({'tool':name,'arguments':args,'result':data})
                print(name, json.dumps(data,ensure_ascii=False)[:700])
                if result.isError or any('Error' in getattr(c,'text','') for c in result.content):
                    report['failure']=True
    dest=WORK/'reports/mcp-smoke.json'
    dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
    print('Report:',dest)
    if report.get('failure'): raise SystemExit(1)
if __name__=='__main__': asyncio.run(main())
