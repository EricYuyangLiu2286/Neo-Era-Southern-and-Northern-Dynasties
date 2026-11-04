from qin_persia_context import W,M,G,S,D,read,write,sha,man,dump,parse,shape
from pathlib import Path
import json,shutil,subprocess,sys
B=W/'backups/pre-change-regional-expansion-20261104T032336Z/mod'
C=W/'exports/regional-expansion-20261104-a'
R=W/'reports/regional-expansion-20261104'
PARENT='b374be519fe71a7c8bfca48b18d94645b0151766'
if __name__=='__main__':
 assert man(B)==man(M)
 assert not C.exists()
 shutil.copytree(B,C);R.mkdir(parents=True,exist_ok=True)
 shutil.copy2(W.parent/'logs/error.log',R/'error-before.log')
 dump(R/'baseline.json',{'parent':PARENT,'files':man(B),'log_sha256':sha(R/'error-before.log'),'engine_verified':False})
 print('Candidate copied:',len(man(C)))
