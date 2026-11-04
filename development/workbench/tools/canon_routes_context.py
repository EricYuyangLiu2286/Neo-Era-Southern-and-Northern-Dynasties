from qin_persia_context import W,M,G,S,D,read,write,sha,man,dump,parse,shape
from pathlib import Path
import json,shutil,subprocess,sys
B=W/'backups/pre-change-canon-route-execution-20261104T080559Z/mod'
C=W/'exports/canon-route-execution-20261104-a'
R=W/'reports/canon-route-execution-20261104'
PARENT='b94582ecec7b0b6dd5620a184658190157fc1729'
if __name__=='__main__':
 assert man(M)==man(B)
 assert not C.exists()
 shutil.copytree(B,C);R.mkdir(exist_ok=True,parents=True)
 dump(R/'baseline.json',{'parent':PARENT,'source_files':man(B),'engine_verified':False})
 print('Independent candidate:',len(man(C)))
