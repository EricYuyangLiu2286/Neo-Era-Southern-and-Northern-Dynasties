"""Mine n-grams over-represented in agent prose vs author original and vanilla.
python3 -I mine.py corpora.json
"""
import json, re, sys, math
from collections import Counter

CODE = re.compile(r'\[[^\]]*\]|\$[^$]*\$|#[A-Za-z_]+[ ;]?|#!|@[a-z_]+!|\\n')
CJK = re.compile(r'[一-鿿]')


def clean(v):
    return CODE.sub(' ', v)


def is_prose(v):
    c = clean(v)
    return len(CJK.findall(c)) >= 12


def load(path):
    d = json.load(open(path, encoding='utf-8'))
    author = [v for vs in d['author'].values() for v in vs if is_prose(v)]
    vanilla = [v for v in d['vanilla'].values() if is_prose(v)]
    agent = [r['value'] for r in d['current'] if r['status'] in ('agent_new', 'agent_changed') and is_prose(r['value'])]
    return author, vanilla, agent


def ngrams(texts, n):
    c = Counter()
    for t in texts:
        for seg in re.findall(r'[一-鿿]+', clean(t)):
            for i in range(len(seg) - n + 1):
                c[seg[i:i + n]] += 1
    return c


def chars(texts):
    return sum(len(CJK.findall(clean(t))) for t in texts)


if __name__ == '__main__':
    author, vanilla, agent = load(sys.argv[1])
    ca, cv, cg = chars(author), chars(vanilla), chars(agent)
    print('prose entries: author', len(author), 'vanilla', len(vanilla), 'agent', len(agent))
    print('CJK chars: author', ca, 'vanilla', cv, 'agent', cg)
    for n in (2, 3, 4):
        A, V, G = ngrams(author, n), ngrams(vanilla, n), ngrams(agent, n)
        scored = []
        for g, k in G.items():
            if k < 25:
                continue
            rg = k / cg * 1e4
            ra = (A[g] + 0.5) / ca * 1e4
            rv = (V[g] + 0.5) / cv * 1e4
            ratio = rg / max(ra, rv)
            scored.append((ratio * math.log(k), g, k, A[g], V[g], ratio))
        scored.sort(reverse=True)
        print(f'--- n={n}')
        for s, g, k, a, v, r in scored[:70]:
            print(f'{g}\t{k}\t{a}\t{v}\tx{r:.1f}')
