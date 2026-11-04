import asyncio,json
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
W=Path(r"D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench");R=W/"reports/canon-route-execution-20261104";cfg=json.loads((R/"batch-a2-test-config.json").read_text())
async def main():
 report={"engine_run":False,"calls":[]}
 async with stdio_client(StdioServerParameters(command=str(W/"tools/mcp-venv/Scripts/paradox-script-mcp.exe"))) as (reader,writer):
  async with ClientSession(reader,writer) as session:
   report["initialize"]=(await session.initialize()).model_dump(mode="json");report["schema"]=(await session.list_tools()).model_dump(mode="json")
   calls=[("init_game",{"game_directory":cfg["snapshot"],"game_type":"vic3"})]
   for path,symbol in [
    ("common/scripted_effects/nesnd_native_khanate.txt","nesnd_khanate_create"),
    ("common/scripted_effects/nesnd_native_khanate.txt","nesnd_khanate_army"),
    ("common/scripted_effects/nesnd_american_restoration.txt","nesnd_restoration_revolt"),
    ("common/scripted_effects/nesnd_a2_manchu_exodus.txt","nesnd_a2_manchu_exodus"),
    ("common/war_goal_types/nesnd_native_americas.txt","wg_nesnd_restoration_settlement"),
    ("common/scripted_effects/nesnd_a2_common.txt","nesnd_a2_barrack_capacity")]:calls.append(("get_structure",{"file_path":path,"symbol":symbol}))
   for name,args in calls:
    result=await session.call_tool(name,args);report["calls"].append({"tool":name,"args":args,"result":result.model_dump(mode="json")})
    print(name,args.get("symbol","init"),"ERROR" if result.isError else "OK",flush=True)
 (Path(cfg["run"])/"mcp-a2.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
asyncio.run(main())
