from qin_persia_context import W,M,G,S,D,read,write,sha,man,dump,parse,shape
from pathlib import Path
import sys,json,shutil
B=W/'backups/pre-change-cne-time-native-ban-20261103T124341Z/mod'
C=W/'exports/cne-time-native-ban-20261103-a'
R=W/'reports/cne-time-native-ban-20261103'
PARENT='a70eb1257795372105751b1e257a0a21dc83638e'
EVENTS={'events/poland_events.txt':['poland_events.1','poland_events.2'],'events/zanzibar_events.txt':['zanzibar.1'],'events/movement_events.txt':['movement_events.6'],'events/agitators_events/coup_events.txt':['coup_aftermath_events.1']}
if __name__=='__main__':
    assert not C.exists() and man(M)==man(B)
    shutil.copytree(M,C)
    dump(R/'baseline.json',{'parent':PARENT,'files':man(B),'engine_verified':False})
    print('Candidate created')
