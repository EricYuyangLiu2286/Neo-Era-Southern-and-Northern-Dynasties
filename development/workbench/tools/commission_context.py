from qin_persia_context import W,M,G,S,D,read,write,sha,man,dump,parse,shape
import json,re,shutil
C=W/'exports/commission-boundaries-20261103-a';R=W/'reports/commission-boundaries-20261103';B=W/'backups/pre-change-commission-boundaries-20261103T074556Z/mod'
def put(rel,s):write(C/rel,s.strip()+'\n')
def replace_node(rel,k,new):
 p=C/rel;s=read(p);n=parse(s).get(k);assert n,(rel,k);write(p,s[:n.start]+new.strip()+s[n.end:])
if __name__=='__main__':
 assert not C.exists();assert man(M)==man(B);shutil.copytree(M,C)
 dump(R/'baseline.json',{'parent_commit':'a06244173fa8a36d97cde42d5bca4068004ece71','files':man(B),'engine_verified':False})
 print('Commission-boundary candidate created')
