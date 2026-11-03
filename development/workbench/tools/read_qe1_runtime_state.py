from qin_persia_context import W,M,G,read,sha,dump,parse
from save_market_network import sections,records,scalar
import re,collections
R=W/'reports/qe1-variable-20261103'
p=W/'runtime/profiles/20261102T234900Z/save games/autosave.v3'
raw=p.read_bytes();assert raw.startswith(b'SAV');s=raw.decode('utf-8-sig');parts=sections(s)
countries=records(parts['country_manager']);tags={i:scalar(b,'definition') for i,b in countries.items()}
qe=[(i,b) for i,b in countries.items() if tags[i]=='QE1' and scalar(b,'dead','no')!='yes'];assert len(qe)==1
cid,body=qe[0];v=re.search(r'^\tvariables=\{\n(.*?)^\t\}',body,re.M|re.S)
varnode=parse(v[0]).get('variables');variables={}
for n in varnode.get('data').children:
    flag=n.scalar('flag')
    if flag and flag in {'nesnd_qe1_campaign_v1','nesnd_qe1_unity','nesnd_qe1_uprising','nesnd_qe1_war_months','nesnd_qe1_dissolved'}:
        d=n.get('data');variables[flag]={'type':d.scalar('type'),'identity':d.scalar('identity')}
jes=[]
for i,b in records(parts['journal_entry_manager']).items():
    typ=scalar(b,'type','')
    if typ in {'nesnd_qe1_unity_journal','nesnd_qe1_uprising_journal'}:
        jes.append({'id':i,'type':typ,'country_id':scalar(b,'country'),'tag':tags.get(scalar(b,'country')),'active':scalar(b,'active','no'),'dead':scalar(b,'dead','no')})
report={'save':str(p),'sha256':sha(p),'game_date':re.search(r'game_date=(\S+)',s)[1],'QE1_country_id':cid,'QE1_variables':variables,'journal_entries':jes,'source_files_equal_runtime':all(sha(M/rel)==sha(W/'exports/runtime-20261102T234900Z/mod'/rel) for rel in ['common/script_values/nesnd_qe1_identity.txt','common/scripted_progress_bars/nesnd_qe1_identity.txt','common/scripted_effects/nesnd_qe1_agendas.txt'])}
dump(R/'runtime-save-evidence.json',report)
print(report['game_date'],variables)
print('JE records:',len(jes),'active:',[x for x in jes if x['active']=='yes'],'inactive examples:',[x for x in jes if x['active']!='yes'][:6])
print('Readonly save SHA',report['sha256'])
