from qin_persia_context import W,read,sha,dump
import asyncio
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
C=W/'exports/qe1-variable-20261103-a';R=W/'reports/qe1-variable-20261103'
async def main():
    rows=[]
    async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
        async with ClientSession(r,w) as session:
            await session.initialize();res=await session.call_tool('init_game',{'game_directory':str(C),'game_type':'vic3'});assert not res.isError
            for path,symbol,key,want in [
                ('common/script_values/nesnd_qe1_identity.txt','nesnd_qe1_unity_war','if.limit','nesnd_qe1_war_months'),
                ('common/script_values/nesnd_qe1_identity.txt','nesnd_qe1_uprising_low_unity','if.limit','nesnd_qe1_unity'),
                ('common/script_values/nesnd_qe1_identity.txt','nesnd_qe1_uprising_war','if.limit','nesnd_qe1_unity'),
                ('common/script_values/nesnd_qe1_identity.txt','nesnd_qe1_uprising_deprivation','if.limit','nesnd_qe1_unity'),
                ('common/journal_entries/nesnd_qe1_identity.txt','nesnd_qe1_uprising_journal','complete.trigger_if','nesnd_qe1_uprising')]:
                args={'file_path':path,'symbol':symbol,'key_path':key}
                res=await session.call_tool('get_structure',args);body='\n'.join(x.text for x in res.content if getattr(x,'type',None)=='text')
                assert not res.isError and want in body,(args,body)
                rows.append({'query':args,'response':body,'sha256':sha(C/path)})
    dump(R/'mcp.json',{'status':'PASS','queries':rows,'engine_execution':False});print('MCP PASS',len(rows),'queries')
asyncio.run(main())
