"""Render markdown tables for the step-1 issue.
python3 -I render.py stats.json rows.json out.md
"""
import json, sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mine import clean

st = json.load(open(sys.argv[1], encoding='utf-8'))
rows = json.load(open(sys.argv[2], encoding='utf-8'))
allp = st['top'] + st['rest']
by = {p['label']: p for p in allp}
# Curated: drop two common words whose excess over vanilla is small; add two user-named constructions.
drop = {'已经', '处置／处理'}
add = ['“，……也须/也要/也将……”补述', '既……也／又']
top = [p for p in st['top'] if p['label'] not in drop] + [by[a] for a in add]
top.sort(key=lambda p: -p['rg'] / max(p['ra'], p['rv'], .2) * p['g'] ** .5)
out = []
c = st['chars']
out.append(f"语料（去掉动态代码后的汉字数）：代理叙事 {c['agent_narr']:,} 字 / {st['entries']['agent_narr']} 条；"
           f"作者原作 {c['author']:,} 字 / {st['entries']['author']} 条；原版 {c['vanilla']:,} 字 / {st['entries']['vanilla']} 条。"
           "每格为“出现次数（每万字）”。\n")
out.append('|#|词或句式|代理|作者原作|原版|代理命中键数|代理例键|')
out.append('|---:|---|---:|---:|---:|---:|---|')
for i, p in enumerate(top, 1):
    ex = '、'.join(f'`{k}`' for k in p['ex'][:3])
    out.append(f"|{i}|{p['label']}|{p['g']}（{p['rg']:.1f}）|{p['a']}（{p['ra']:.1f}）|{p['v']}（{p['rv']:.1f}）|{p['gk']}|{ex}|")
out.append('\n已知例子的当前计数：\n')
out.append('|句式|代理|作者原作|原版|代理例键|')
out.append('|---|---:|---:|---:|---|')
for p in st['known']:
    ex = '、'.join(f'`{k}`' for k in p['ex'][:3]) or '—'
    out.append(f"|{p['label']}|{p['g']}（{p['rg']:.1f}）|{p['a']}（{p['ra']:.1f}）|{p['v']}（{p['rv']:.1f}）|{ex}|")
json.dump([p['rx'] for p in top], open(os.path.join(os.path.dirname(sys.argv[3]), 'top30-regex.json'), 'w'), ensure_ascii=False)

# per-file
toprx = [re.compile(p['rx']) for p in top]
from collections import Counter, defaultdict
pf = defaultdict(Counter)
for r in rows:
    f = r['file'].replace('localization/simp_chinese/', '')
    k = pf[f]
    k['total'] += 1
    if r['status'] in ('author_verbatim', 'punct_only'):
        k['author'] += 1
    elif r['status'] == 'author_revision':
        k['rev'] += 1
    elif r['status'] == 'author_revision_then_agent':
        k['rev2'] += 1
    elif r['status'] == 'pending_confirm':
        k['pending'] += 1
    else:
        k['agent'] += 1
    if r['scope'] == 'narr':
        k['narr'] += 1
        if any(x.search(clean(r['value'])) for x in toprx):
            k['hit'] += 1
    elif r['scope'] == 'mech_dev':
        k['mech'] += 1
    if r['status'] == 'pending_confirm' and r['field'] != '名称类':
        k['pend_text'] += 1
out.append('\n|文件|键数|作者原文（含仅标点差异）|作者改稿（保护）|作者改稿后又被改|代理写或改|其中叙事字段|叙事字段命中前30项|机制提示带开发口吻|待确认文件的文本键|')
out.append('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
T = Counter()
for f in sorted(pf, key=lambda f: -(pf[f]['hit'] + pf[f]['pend_text'])):
    k = pf[f]
    T.update(k)
    if k['agent'] + k['rev'] + k['rev2'] + k['pending'] == 0:
        continue
    out.append(f"|`{f}`|{k['total']}|{k['author']}|{k['rev']}|{k['rev2']}|{k['agent']}|{k['narr']}|{k['hit']}|{k['mech']}|{k['pend_text']}|")
out.append(f"|**合计**|{T['total']}|{T['author']}|{T['rev']}|{T['rev2']}|{T['agent']}|{T['narr']}|{T['hit']}|{T['mech']}|{T['pend_text']}|")
skipped = [f for f in pf if pf[f]['agent'] + pf[f]['rev'] + pf[f]['rev2'] + pf[f]['pending'] == 0]
out.append(f"\n其余 {len(skipped)} 个文件全部与原作逐字相同或仅差标点，不列。")

rev2 = [r for r in rows if r['status'] == 'author_revision_then_agent']
out.append('\n作者改稿后又被代理改动的键（' + str(len(rev2)) + '）：' + '、'.join(f"`{r['key']}`" for r in rev2))
open(sys.argv[3], 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
