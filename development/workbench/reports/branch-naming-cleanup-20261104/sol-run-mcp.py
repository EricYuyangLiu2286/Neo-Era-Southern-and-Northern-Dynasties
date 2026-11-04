import asyncio,json,hashlib
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');R=W/'reports/branch-naming-cleanup-20261104';C=W/'exports/maintenance-current';B=W/'backups/pre-change-maintenance-pre-cleanup-20261104T213001Z/mod'
async def main():
 report={'candidate_manifest_sha256':hashlib.sha256((R/'candidate-freeze.json').read_bytes()).hexdigest(),'calls':[]}
 async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'))) as (reader,writer):
  async with ClientSession(reader,writer) as s:
   report['initialize']=(await s.initialize()).model_dump(mode='json');report['tools']=(await s.list_tools()).model_dump(mode='json')
   calls=[]
   for label,root in [('B',B),('C',C)]:
    calls.append((label,'init_game',{'game_directory':str(root),'game_type':'vic3'}))
    calls.append((label,'get_structure',{'file_path':'common/scripted_effects/nesnd_small_states.txt','symbol':'nesnd_small_monthly'}))
    calls.append((label,'get_structure',{'file_path':'common/scripted_triggers/nesnd_qe1_campaign.txt','symbol':'nesnd_qe1_economic_victory'}))
    calls.append((label,'get_structure',{'file_path':'common/dynamic_country_names/00_dynamic_country_names.txt','symbol':'HNA'}))
   for label,name,args in calls:
    response=await s.call_tool(name,args);raw=response.model_dump(mode='json');report['calls'].append({'root':label,'tool':name,'arguments':args,'response':raw});print(label,name,'error=',response.isError)
 report['status']='FAIL' if any(x['response'].get('isError') for x in report['calls']) else 'PROTOCOL_PASS'
 (R/'sol-mcp-repair1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(report['status'])
asyncio.run(main())
