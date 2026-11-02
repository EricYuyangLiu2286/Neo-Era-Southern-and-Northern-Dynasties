"""Use installed CWTools LSP, isolated cache; never start the game or edit source."""
from pathlib import Path
import subprocess,threading,queue,json,time,shutil,sys
from urllib.parse import unquote
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
M=Path(sys.argv[1]) if len(sys.argv)>1 else W.parent/'mod/Neo-Era Southern and Northern Dynasties'
E=Path('C:/Users/Eric Liu/.vscode/extensions/tboby.cwtools-vscode-0.10.31')
R=W/'reports/integrity-recheck-20261102';R.mkdir(exist_ok=True,parents=True)
label=sys.argv[2] if len(sys.argv)>2 else 'probe'
cache=W/'tools/cwtools-recheck-cache';cache.mkdir(exist_ok=True)
if not (cache/'vic3').exists():shutil.copytree(E/'.cwtools/vic3',cache/'vic3')
rules=str(cache/'vic3/config')
settings={}
properties=json.loads((E/'package.json').read_text('utf-8'))['contributes']['configuration']['properties']
for key,spec in properties.items():
    dst=settings;parts=key.split('.')
    for part in parts[:-1]:dst=dst.setdefault(part,{})
    dst[parts[-1]]=spec.get('default','' if spec.get('type')=='string' else False)
settings['cwtools'].update(rules_version='manual',rules_folder=rules)
settings['cwtools']['logging']['diagnostic']=True
proc=subprocess.Popen([str(E/'bin/server/win-x64/CWTools Server.exe')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=str(cache),creationflags=subprocess.CREATE_NO_WINDOW)
q=queue.Queue();messages=[]
def reader():
    while True:
        headers={}
        while True:
            line=proc.stdout.readline()
            if not line:return
            if line in [b'\r\n',b'\n']:break
            k,_,v=line.decode(errors='replace').partition(':');headers[k.lower()]=v.strip()
        size=int(headers.get('content-length',0))
        if size:q.put(json.loads(proc.stdout.read(size)))
threading.Thread(target=reader,daemon=True).start()
stderr=[]
def errreader():
    for line in iter(proc.stderr.readline,b''):stderr.append(line.decode(errors='replace'))
threading.Thread(target=errreader,daemon=True).start()
def send(obj):
    b=json.dumps({'jsonrpc':'2.0',**obj}).encode();proc.stdin.write(f'Content-Length: {len(b)}\r\n\r\n'.encode()+b);proc.stdin.flush()
def receive(wait=1):
    try:r=q.get(timeout=wait)
    except queue.Empty:return None
    messages.append(r)
    if 'method' in r and 'id' in r:
        if r['method']=='workspace/configuration':
            values=[]
            for x in r['params']['items']:
                value=settings
                for part in x.get('section','').split('.'):
                    if part:value=value.get(part,{}) if isinstance(value,dict) else {}
                values.append(value)
            send({'id':r['id'],'result':values})
        elif r['method']=='workspace/workspaceFolders':send({'id':r['id'],'result':[{'uri':M.as_uri(),'name':'NESND'}]})
        else:send({'id':r['id'],'result':None})
    return r
target=M/'common/scripted_triggers/nesnd_cne_programs.txt'
send({'id':1,'method':'initialize','params':{'processId':None,'rootUri':M.as_uri(),'rootPath':str(M),'workspaceFolders':[{'uri':M.as_uri(),'name':'NESND'}],'capabilities':{'workspace':{'configuration':True}},'initializationOptions':{'language':'vic3','isVanillaFolder':False,'rulesCache':str(cache),'rules_version':'manual','repoPath':'https://github.com/cwtools/cwtools-vic3-config','diagnosticLogging':True}}})
started=time.monotonic();initialized=False;target_diags=None;last_diag=started;validation_finished=False
try:
    while time.monotonic()-started<45:
        r=receive()
        if not r:
            if proc.poll() is not None:break
            if validation_finished and target_diags is not None and time.monotonic()-started>15 and time.monotonic()-last_diag>5:break
            continue
        if r.get('id')==1 and 'result' in r and not initialized:
            initialized=True
            send({'method':'initialized','params':{}})
            send({'method':'workspace/didChangeConfiguration','params':{'settings':settings}})
            send({'method':'textDocument/didOpen','params':{'textDocument':{'uri':target.as_uri(),'languageId':'vic3','version':1,'text':target.read_text('utf-8-sig')}}})
        if r.get('method')=='textDocument/publishDiagnostics' and unquote(r['params']['uri']).lower()==unquote(target.as_uri()).lower():
            target_diags=r['params']['diagnostics'];last_diag=time.monotonic()
        if r.get('method')=='window/logMessage' and 'Localisation check took' in r['params'].get('message',''):
            validation_finished=True
        if validation_finished and target_diags is not None and time.monotonic()-started>15 and time.monotonic()-last_diag>5:break
    result={'initialized':initialized,'target':str(target),'target_diagnostics':target_diags,'elapsed':time.monotonic()-started,'game_launched':False,'configuration':settings}
    (R/f'cwtools-{label}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
    (R/f'cwtools-{label}-protocol.json').write_text(json.dumps(messages,ensure_ascii=False,indent=2),'utf-8')
    (R/f'cwtools-{label}-stderr.txt').write_text(''.join(stderr),'utf-8')
    print(json.dumps({'initialized':initialized,'target_diagnostics':None if target_diags is None else len(target_diags),'messages':len(messages),'welfare':[x for x in target_diags or [] if 'welfare' in x.get('message','')]}))
finally:
    if proc.poll() is None:proc.terminate()
    proc.wait(timeout=10)
