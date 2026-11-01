"""Guard the remaining literal modifier removals in production scripts, preserving source spans."""
from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse,replace_spans
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
C=W/'exports/release-logfix-20261101-a';rows=[]
for sub in ('common/scripted_buttons','common/scripted_effects','events','common/journal_entries','common/decisions'):
 for f in (C/sub).rglob('*.txt'):
  s=f.read_text('utf-8-sig');edits=[]
  def walk(n,parents):
   if n.key=='remove_modifier' and n.value:
    guarded=any(a.key=='if' and a.get('limit') and any(x.key=='has_modifier' and x.value==n.value for x in a.get('limit').walk()) for a in parents)
    if not guarded:
     assert all(c.isalnum() or c=='_' for c in n.value), 'Review dynamic modifier names separately'
     edits.append((n.start,n.end,'if = { limit = { has_modifier = '+n.value+' } '+s[n.start:n.end]+' }'))
     rows.append({'file':f.relative_to(C).as_posix(),'line':s[:n.start].count('\n')+1,'modifier':n.value})
   for c in n.children or []:walk(c,parents+[n])
  walk(parse(s),[])
  if edits:
   fixed=replace_spans(s,edits);parse(fixed);f.write_text(fixed,encoding='utf-8-sig')
(W/'reports/logfix-release-20261101/modifier-cleanup.json').write_text(json.dumps({'repairs':rows,'meaning':'Same-scope conditional removal; present modifier removal unchanged, absent modifier is already the required end state.'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'unguarded_before':len(rows),'files':len({r['file'] for r in rows})}))
