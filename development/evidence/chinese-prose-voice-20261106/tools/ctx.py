import json,re,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from mine import clean,is_prose
d=json.load(open(sys.argv[1]))
n=int(sys.argv[2])
ag=[(r['key'],clean(r['value'])) for r in d['current'] if r['status'] in('agent_new','agent_changed') and is_prose(r['value'])]
for p in sys.argv[3:]:
    hits=[(k,v) for k,v in ag if re.search(p,v)]
    print('##',p,len(hits))
    for k,v in hits[:n]:
        m=re.search(p,v); i=m.start()
        print('  ',k,'…'+v[max(0,i-40):i+30].replace('\n',' ')+'…')
