import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import locedit
repo=sys.argv[1]; base=sys.argv[2]; sub=sys.argv[3] if len(sys.argv)>3 else ''
os.environ['LOC_LANG']='simp_chinese'
zh=locedit.index_repo(repo)
os.environ['LOC_LANG']='english'
en=locedit.index_repo(repo)
# keys changed in zh vs base
names=subprocess.run(['git','-C',repo,'diff','--name-only',base,'--','localization/simp_chinese'],capture_output=True,text=True).stdout.split()
keys=[]
for f in names:
    old=subprocess.run(['git','-C',repo,'show',f'{base}:{f}'],capture_output=True).stdout.decode().lstrip('﻿')
    o={}
    for l in old.splitlines():
        m=locedit.LINE.match(l)
        if m:o[m.group(2)]=m.group(4)
    for k,(p,n,v) in zh.items():
        if os.path.relpath(p,repo)==f and o.get(k)!=v: keys.append(k)
missing=[k for k in keys if k not in en]
print('changed zh',len(keys),'missing en',len(missing),missing[:20],file=sys.stderr)
for k in keys:
    if sub and sub not in os.path.basename(zh[k][0]): continue
    if k in en:
        print(f"## {k}  [{os.path.basename(en[k][0])}]\n  ZH: {zh[k][2]}\n  EN: {en[k][2]}")
