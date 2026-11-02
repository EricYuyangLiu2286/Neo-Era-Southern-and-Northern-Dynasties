from pathlib import Path
import zipfile, json, hashlib, base64, zlib, urllib.parse, re, html
from xml.etree import ElementTree as ET
OUT=Path(__file__).parent
P=Path('D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/计划文件（相关项目）')
records=[]
src=P/'Japanese map brief.docx'
with zipfile.ZipFile(src) as z:
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    ps=[{'p':i+1,'text':''.join(t.text or '' for t in p.findall('.//w:t',ns))} for i,p in enumerate(ET.fromstring(z.read('word/document.xml')).findall('.//w:p',ns))]
    images=[x for x in z.namelist() if x.startswith('word/media/')]
    for name in images:
        (OUT/('japan-map-brief-'+Path(name).name)).write_bytes(z.read(name))
    records.append({'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'paragraphs':ps,'embedded_images':images})
src=P/'Japanese Mission Overhual.drawio'
root=ET.fromstring(src.read_bytes())
diagrams=[]
for diagram in root.findall('diagram'):
    graph=diagram.find('mxGraphModel')
    if graph is None:
        payload=(diagram.text or '').strip()
        if payload.startswith('<'): graph=ET.fromstring(payload)
        else: graph=ET.fromstring(urllib.parse.unquote(zlib.decompress(base64.b64decode(payload),-15).decode()))
    cells=[]
    for cell in graph.findall('.//mxCell'):
        raw=cell.get('value','')
        text=html.unescape(re.sub('<[^>]+>', '\n', raw))
        text='\n'.join(x.strip() for x in text.splitlines() if x.strip())
        cells.append({'id':cell.get('id'),'value':text,'source':cell.get('source'),'target':cell.get('target'),'geometry':cell.find('mxGeometry').attrib if cell.find('mxGeometry') is not None else None})
    diagrams.append({'diagram_id':diagram.get('id'),'name':diagram.get('name'),'cells':cells})
records.append({'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'diagrams':diagrams})
(OUT/'japan-plans-original-reread.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
lines=[]
for r in records:
    lines.extend([r['source'],r['sha256']])
    if 'paragraphs' in r:
        lines.extend(f"[p{p['p']}] {p['text']}" for p in r['paragraphs'])
        lines.append('Embedded images: '+str(r['embedded_images']))
    for d in r.get('diagrams',[]):
        lines.append('Diagram: '+str(d['name']))
        lines.extend(f"[cell {c['id']}] {c['value']}" for c in d['cells'] if c['value'])
        names={c['id']:c['value'] for c in d['cells']}
        lines.extend(f"[edge {c['id']}] {names.get(c['source'],'(unattached)')} ({c['source']}) -> {names.get(c['target'],'(unattached)')} ({c['target']})" for c in d['cells'] if c['source'] or c['target'])
(OUT/'japan-plans-full-text.txt').write_text('\n'.join(lines),encoding='utf-8')
manifest=json.loads((OUT/'source-manifest.json').read_text(encoding='utf-8'))
for r in records:
    manifest=[m for m in manifest if m['path']!=r['source']]
    manifest.append({'path':r['source'],'sha256':r['sha256'],'bytes':Path(r['source']).stat().st_size})
(OUT/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Extracted plan sources: '+str(len(records)))
