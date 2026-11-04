import asyncio,json
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
W=Path(r"D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench");R=W/"reports/canon-route-execution-20261104";cfg=json.loads((R/"batch-c2-test-config.json").read_text())
async def main():
 report={"engine_run":False,"calls":[]}
 async with stdio_client(StdioServerParameters(command=str(W/"tools/mcp-venv/Scripts/paradox-script-mcp.exe"))) as (reader,writer):
  async with ClientSession(reader,writer) as session:
   report["initialize"]=(await session.initialize()).model_dump(mode="json");report["schema"]=(await session.list_tools()).model_dump(mode="json")
   calls=[("init_game",{"game_directory":cfg["snapshot"],"game_type":"vic3"})]
   for path,symbol in [
    ("common/scripted_effects/nesnd_civic_routes.txt","nesnd_c2_monthly"),
    ("common/scripted_effects/nesnd_civic_characters.txt","nesnd_c2_character_monthly"),
    ("common/scripted_triggers/nesnd_civic_routes.txt","nesnd_italy_country"),
    ("common/journal_entries/nesnd_civic_routes.txt","nesnd_c2_italy_foundations"),
    ("common/script_values/nesnd_civic_routes.txt","nesnd_c2_weekly_quote")]:calls.append(("get_structure",{"file_path":path,"symbol":symbol}))
   for name,args in calls:
    result=await session.call_tool(name,args);report["calls"].append({"tool":name,"args":args,"result":result.model_dump(mode="json")})
    print(name,args.get("symbol","init"),"ERROR" if result.isError else "OK",flush=True)
 (Path(cfg["run"])/"mcp-c2.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
asyncio.run(main())
