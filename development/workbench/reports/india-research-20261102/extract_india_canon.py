import sys, json, hashlib, re, importlib.util
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
spec=importlib.util.spec_from_file_location('ooxml', 'C:/Users/Eric Liu/.codex/skills/beiming-biography/scripts/extract_ooxml.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
src=Path('D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世')
out=Path(__file__).parent
rows=[]; manifest=[]
for p in src.iterdir():
    if p.suffix.lower() not in ['.docx','.pptx']: continue
    records=m.extract(p)
    sha=hashlib.sha256(p.read_bytes()).hexdigest()
    manifest.append({'path':str(p),'sha256':sha,'records':len(records)})
    rows.extend({'source':str(p),'sha256':sha,**r} for r in records)
(out/'canon-original-reread.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'canon-source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
pat=re.compile('印度|天竺|莫卧|蒙兀|Mughal|种姓|婆罗门|达利特|孟加拉|古吉拉特|马哈拉施特拉|章西|尼赫鲁|甘地|旁遮普|Hind',re.I)
hits=[r for r in rows if pat.search(r['text'])]
(out/'india-original-matches.json').write_text(json.dumps(hits,ensure_ascii=False,indent=2),encoding='utf-8')
for r in hits:
    print(Path(r['source']).name, 'slide '+str(r['slide']) if 'slide' in r else r['part'], 'p'+str(r['paragraph']), r['text'])
print('FILES',len(manifest),'ROWS',len(rows),'MATCHES',len(hits))
