from qin_persia_context import W,M,G,S,D,read,write,sha,man,dump,parse,shape
import json,shutil,sys
B=W/'backups/pre-change-observer-logfix-20261103T103900Z/mod'
C=W/'exports/observer-logfix-20261103-a'
R=W/'reports/observer-logfix-20261103'
if __name__=='__main__':
    assert not C.exists()
    assert man(M)==man(B), 'Main changed since backup'
    shutil.copytree(M,C)
    dump(R/'baseline.json',{'parent_commit':'adfc31759b355d33e0f09269822911b367499b53','backup':str(B),'files':man(B),'engine_verified':False})
    print('Candidate created from verified backup')
