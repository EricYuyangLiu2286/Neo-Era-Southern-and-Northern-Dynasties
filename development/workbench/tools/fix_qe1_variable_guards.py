from qin_persia_context import W,M,G,read,write,sha,man,dump,parse
import shutil
R=W/'reports/qe1-variable-20261103';C=W/'exports/qe1-variable-20261103-a'
B=W/'backups/pre-change-qe1-variable-guards-20261103T002508Z/mod'
assert not C.exists()
before=man(M);assert before==man(B)
shutil.copytree(M,C)
rel='common/script_values/nesnd_qe1_identity.txt';s=read(C/rel);tree=parse(s)
names=['nesnd_qe1_unity_war','nesnd_qe1_uprising_low_unity','nesnd_qe1_uprising_war','nesnd_qe1_uprising_deprivation']
edits=[]
for name in names:
    n=tree.get(name);assert n.scalar('value')=='0'
    # Keep the existing branches and all numerical amounts; guard their evaluation.
    old=s[n.start:n.end];inner=old[old.index('if ='):old.rfind('}')].strip()
    var='nesnd_qe1_war_months' if name=='nesnd_qe1_unity_war' else 'nesnd_qe1_unity'
    new=name+' = {\n\tvalue = 0\n\tif = {\n\t\tlimit = { has_variable = '+var+' }\n\t\t'+inner+'\n\t}\n}'
    edits.append((n.start,n.end,new))
for start,end,new in sorted(edits,reverse=True):s=s[:start]+new+s[end:]
write(C/rel,s)

rel='common/journal_entries/nesnd_qe1_identity.txt';s=read(C/rel)
for threshold in (25,50):
    old='trigger = { var:nesnd_qe1_unity < '+str(threshold)+' }'
    new='''trigger = {
                trigger_if = { limit = { has_variable = nesnd_qe1_unity } var:nesnd_qe1_unity < '''+str(threshold)+''' }
                trigger_else = { always = no }
            }'''
    assert s.count(old)==1;s=s.replace(old,new)
old='complete = { nesnd_qe1_unity_live = yes var:nesnd_qe1_uprising >= 100 }'
new='''complete = {
        nesnd_qe1_unity_live = yes
        trigger_if = { limit = { has_variable = nesnd_qe1_uprising } var:nesnd_qe1_uprising >= 100 }
        trigger_else = { always = no }
    }'''
assert s.count(old)==1;s=s.replace(old,new);write(C/rel,s)
assert man(M)==before
sources=[('common/script_values/je_values.txt','271–278'),('common/journal_entries/05_danubian_federation.txt','29, 225–235'),('common/scripted_effects/00_victoria_ip3_scripted_effects.txt','128'),('common/script_values/ep2_japan_values.txt','183–197'),('common/scripted_progress_bars/scripted_progress_bars.md','22–23')]
dump(R/'native-sources.json',{'game':'1.13.11','build':24799966,'sources':[{'path':str(G/p),'lines':lines,'sha256':sha(G/p)} for p,lines in sources]})
dump(R/'baseline.json',{'backup':str(B),'candidate':str(C),'main_files':before,'commit':'c1463da95111e3ec2369c174c86f37803adbbdce','changed':[p for p,v in man(C).items() if before.get(p)!=v],'game_started_by_agent':False})
print('Candidate prepared: four source-value branches and three JE predicates guarded; main unchanged.')
