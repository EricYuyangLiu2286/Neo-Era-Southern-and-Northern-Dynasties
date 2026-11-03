from qin_persia_context import W,M,G,read,sha,man,dump,parse,shape
import subprocess,json,asyncio
R=W/'reports/qe1-variable-20261103';C=W/'exports/qe1-variable-20261103-a'
B=W/'backups/pre-change-qe1-variable-guards-20261103T002508Z/mod'
checks=[]
def check(name,ok):checks.append({'name':name,'pass':bool(ok)})
rel='common/script_values/nesnd_qe1_identity.txt';old=parse(read(B/rel));new=parse(read(C/rel))
selected={'nesnd_qe1_unity_war':'nesnd_qe1_war_months','nesnd_qe1_uprising_low_unity':'nesnd_qe1_unity','nesnd_qe1_uprising_war':'nesnd_qe1_unity','nesnd_qe1_uprising_deprivation':'nesnd_qe1_unity'}
for a in old.children:
    b=new.get(a.key)
    if a.key in selected:
        guard=b.get('if')
        check(a.key+' guards the correct variable',guard.get('limit').scalar('has_variable')==selected[a.key])
        check(a.key+' absent variable yields zero',b.scalar('value')=='0' and len(b.children)==2)
        check(a.key+' existing-variable calculation unchanged',[shape(x) for x in a.children if x.key!='value']==[shape(x) for x in guard.children if x.key!='limit'])
    else:check(a.key+' unchanged',shape(a)==shape(b))
rel2='common/journal_entries/nesnd_qe1_identity.txt';jo=parse(read(B/rel2));jn=parse(read(C/rel2))
for name in ['nesnd_qe1_unity_journal','nesnd_qe1_uprising_journal']:
    a,b=jo.get(name),jn.get(name)
    modified='status_desc' if name=='nesnd_qe1_unity_journal' else 'complete'
    check(name+' other fields unchanged',[shape(x) for x in a.children if x.key!=modified]==[shape(x) for x in b.children if x.key!=modified])
    branchlist=b.get('status_desc').get('first_valid').all('triggered_desc') if modified=='status_desc' else [b]
    for i,item in enumerate(branchlist):
        block=item.get('trigger') if modified=='status_desc' else item.get('complete')
        check(name+str(i)+' missing variable false',block.get('trigger_else').scalar('always')=='no')
        expected='nesnd_qe1_unity' if modified=='status_desc' else 'nesnd_qe1_uprising'
        check(name+str(i)+' has-variable branch',block.get('trigger_if').get('limit').scalar('has_variable')==expected)
        original=(a.get('status_desc').get('first_valid').all('triggered_desc')[i].get('trigger') if modified=='status_desc' else a.get('complete'))
        check(name+str(i)+' original comparison unchanged',[shape(x) for x in original.children if x.key.startswith('var:')]==[shape(x) for x in block.get('trigger_if').children if x.key.startswith('var:')])
before,after=man(B),man(C)
check('Only two intended gameplay files changed',sorted(p for p in before.keys()|after.keys() if before.get(p)!=after.get(p))==sorted([rel,rel2]))
check('Main unchanged before delivery',man(M)==before)
check('No source deletion',not before.keys()-after.keys())
for folder in ['common','events']:
    for p in (C/folder).rglob('*.txt'):parse(read(p))
check('All current gameplay script files parse',True)
result={'status':'STATIC_PASS' if all(x['pass'] for x in checks) else 'FAIL','checks':checks,'source_files':{p:after[p] for p in [rel,rel2]},'engine_execution':False}
dump(R/'validation.json',result);print(result['status'],len(checks),'checks', [x['name'] for x in checks if not x['pass']])
assert result['status']=='STATIC_PASS'
