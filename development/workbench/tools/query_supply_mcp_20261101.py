"""Read repaired supply definitions through the existing installed MCP server."""
import asyncio,json,hashlib
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
C=W/'exports/release-logfix-20261101-a'
queries=[('common/scripted_effects/nesnd_supply_effects.txt','nesnd_supply_save_pending_sponsor','if.limit','exists'),('common/scripted_triggers/nesnd_supply_triggers.txt','nesnd_supply_partner_valid','trigger_if.limit','nesnd_supply_partner'),('common/scripted_buttons/nesnd_supply_buttons.txt','nesnd_supply_trade','possible.trigger_if','exists'),('common/script_values/nesnd_supply_preview_values.txt','nesnd_supply_weeks_value','if.limit','has_variable')]
async def main():
 rows=[]
 async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
  async with ClientSession(r,w) as s:
   await s.initialize();listed=await s.list_tools();assert 'get_structure' in [t.name for t in listed.tools]
   init=await s.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not init.isError
   for path,symbol,key_path,want in queries:
    result=await s.call_tool('get_structure',{'file_path':path,'symbol':symbol,'key_path':key_path})
    text='\n'.join(x.text for x in result.content if getattr(x,'type',None)=='text')
    assert not result.isError and want in text,(symbol,text)
    rows.append({'path':path,'symbol':symbol,'sha256':hashlib.sha256((C/path).read_bytes()).hexdigest(),'result':text})
 out=W/'reports/logfix-release-20261101/mcp-supply-query.json';out.write_text(json.dumps({'status':'PASS','engine_execution':False,'queries':rows},ensure_ascii=False,indent=2),encoding='utf-8');print('MCP supply source queries: 4 PASS')
asyncio.run(main())
