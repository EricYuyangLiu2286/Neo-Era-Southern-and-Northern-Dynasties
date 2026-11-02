from pathlib import Path
import re,json,hashlib
M=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties')
W=M.parent.parent/'nesnd-workbench'
C=W/'exports/japan-development-20261102-a'
B=W/'backups/pre-update-20261030T233944Z/mod'
R=W/'reports/canon-prose-20261102'
rx=re.compile(r'^\s*([^\s:#]+):\s*(?:\d+\s*)?"(.*)"\s*$')
def readloc(root,lang):
    all={}; eff={}
    for p in sorted((root/'localization'/lang).rglob('*.yml'),key=lambda p:('replace' in p.parts,p.name,str(p))):
        for ln,s in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
            m=rx.match(s)
            if not m: continue
            k,v=m.groups(); row={'text':v,'file':str(p.relative_to(root)).replace('\\','/'),'line':ln,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
            all.setdefault(k,[]).append(row);eff[k]=row
    return all,eff
Z,zh=readloc(M,'simp_chinese');E,en=readloc(M,'english');_,old=readloc(B,'simp_chinese');_,candidate_en=readloc(C,'english')
fnparts=('ce_usm_events','nesnd_succession_board','nesnd_south_journal_ui','nesnd_chen_security','nesnd_ming_court','nesnd_south_politics','nesnd_south_peace_gates','nesnd_south_feedback','nesnd_court_followup','nesnd_external_l','nesnd_supply_l','nesnd_usm_local_authority')
prefixes=('nesnd_hna_','nesnd_huguang_','nesnd_federal_','nesnd_court_protection','nesnd_wu_','nesnd_foreign_','nesnd_refugee_','nesnd_maritime_','nesnd_japan_reorganization','nesnd_early_accession','nesnd_south_','ce_usm_','flavorUSM.','usm_civilwar.','nesnd_crisis.10.','nesnd_crisis.11.','nesnd_crisis.20.','nesnd_crisis.21.','nesnd_crisis.40.','nesnd_crisis.41.','nesnd_protect_chen')
keys=[k for k,r in zh.items() if any(s in r['file'] for s in fnparts) or k.startswith(prefixes)]
scripts=[]
for folder in ('common','events','gui'):
    for p in (M/folder).rglob('*'):
        if p.suffix in ('.txt','.gui'):scripts.append((str(p.relative_to(M)).replace('\\','/'),p.read_text(encoding='utf-8-sig',errors='replace')))
refs={k:[] for k in keys}
keyset=set(keys)
for file,txt in scripts:
    for ln,s in enumerate(txt.splitlines(),1):
        s=s.split('#')[0]
        for tok in re.findall(r'[\w.]+',s):
            if tok in keyset and len(refs[tok])<12:refs[tok].append(f'{file}:{ln}')
inventory={k:{'zh':zh[k],'en':en.get(k),'baseline_zh':old.get(k),'candidate_en':candidate_en.get(k),'all_zh':Z[k],'all_en':E.get(k,[]),'refs':refs[k]} for k in keys}
(R/'usm-inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
print('keys',len(inventory),'files',len(set(zh[k]['file'] for k in keys)))
