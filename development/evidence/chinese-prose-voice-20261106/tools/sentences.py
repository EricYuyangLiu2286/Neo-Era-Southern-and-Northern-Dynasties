"""Sentence-level mining: openings, endings, and frames. Narrative fields only for agent.
python3 -I sentences.py corpora.json repo
"""
import json, re, sys, os
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mine import clean, is_prose
from fields import index, classify

NARR = {'事件正文', '事件选项', '日志正文', '按钮说明', '日志状态/目标', '修正说明', '其他说明', '通知', '决议'}


def sents(v):
    t = clean(v)
    for s in re.split(r'[。！？]|\s{2,}', t):
        s = re.sub(r'^[\s，、“”]+', '', s).strip()
        if len(re.findall(r'[一-鿿]', s)) >= 4:
            yield s


def main(cp, repo):
    d = json.load(open(cp, encoding='utf-8'))
    ix = index(repo)
    agent = [(r['key'], r['value']) for r in d['current'] if r['status'] in ('agent_new', 'agent_changed')
             and is_prose(r['value']) and classify(r['key'], ix) in NARR]
    author = [(k, v) for k, vs in d['author'].items() for v in vs if is_prose(v)]
    vanilla = [(k, v) for k, v in d['vanilla'].items() if is_prose(v)]
    print('agent narrative entries', len(agent))
    for name, fn in (('open2', lambda s: s[:2]), ('end3', lambda s: s[-3:]), ('end2', lambda s: s[-2:])):
        G = Counter(fn(s) for _, v in agent for s in sents(v))
        A = Counter(fn(s) for _, v in author for s in sents(v))
        V = Counter(fn(s) for _, v in vanilla for s in sents(v))
        tg, ta, tv = sum(G.values()), sum(A.values()), sum(V.values())
        print('---', name, 'sentences', tg, ta, tv)
        sc = []
        for g, k in G.items():
            if k < 10:
                continue
            r = (k / tg) / max((A[g] + .5) / ta, (V[g] + .5) / tv)
            sc.append((r * k ** .5, g, k, A[g], V[g]))
        for _, g, k, a, v in sorted(sc, reverse=True)[:30]:
            print(f'{g}\t{k}\t{a}\t{v}')


main(*sys.argv[1:3])
