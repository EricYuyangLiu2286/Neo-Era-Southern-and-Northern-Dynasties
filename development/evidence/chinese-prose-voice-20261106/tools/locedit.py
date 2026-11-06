"""Dump / apply / check helpers for hand-written localization rewrites.

dump  <repo> <rows.json> <file-substring> [all]   print in-scope keys of one file with current text
apply <repo> <edits.json>                          edits.json = {"key": "new value", ...}; writes in place,
                                                   stores originals in edits-orig/ beside edits.json
check <repo> <base-ref>                            per-key token comparison of every changed key vs base-ref
"""
import json, os, re, subprocess, sys
from collections import Counter

LINE = re.compile(r'^(\s*)([A-Za-z0-9_.\-]+)(:\d*\s*)"(.*)"(\s*(#.*)?)$')
MECH_DEV = re.compile(r'此项|本项|本次|相关|推进|子项目|子日志|原规则|按原|继续决定|核验|重新累计|口径|事务随')


def load_file(path):
    raw = open(path, 'rb').read()
    return raw.decode('utf-8')


def index_repo(repo):
    out = {}
    root = os.path.join(repo, 'localization/simp_chinese')
    for dp, _, fs in os.walk(root):
        for f in fs:
            if f.endswith('.yml'):
                p = os.path.join(dp, f)
                for n, line in enumerate(load_file(p).lstrip('﻿').splitlines()):
                    m = LINE.match(line)
                    if m:
                        out[m.group(2)] = (p, n, m.group(4))
    return out


def in_scope(r):
    st, f, fn = r['status'], r['field'], os.path.basename(r['file'])
    if fn == 'nesnd_qin_persia_l_simp_chinese.yml':
        return False
    if st not in ('agent_new', 'agent_changed', 'pending_confirm'):
        return False
    if f == '名称类':
        return False
    if f in ('提示/条件', '进度条'):
        return bool(MECH_DEV.search(r['value']))
    return True


def dump(repo, rows_path, sub, show_all=False):
    rows = json.load(open(rows_path, encoding='utf-8'))
    idx = index_repo(repo)
    n = 0
    for r in rows:
        if sub not in r['file']:
            continue
        if not show_all and not in_scope(r):
            continue
        cur = idx.get(r['key'], (None, None, r['value']))[2]
        mark = '*' if cur != r['value'] else ' '
        print(f"{mark}[{r['field']}] {r['key']}\n    {cur}")
        n += 1
    print(f'-- {n} keys')


TOK = [
    ('bracket', re.compile(r'\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]')),
    ('dollar', re.compile(r'\$[^$\s]+\$')),
    ('fmt', re.compile(r'#[A-Za-z_]+(?::[^ ]+)?')),
    ('close', re.compile(r'#!')),
    ('icon', re.compile(r'@[A-Za-z_0-9]+!')),
    ('num', re.compile(r'\d+(?:[.,]\d+)*%?')),
    ('cnnum', re.compile(r'(?:[零二三四五六七八九十百千万两半]|一(?=[零二三四五六七八九十百千]))[零一二三四五六七八九十百千万两半]*(?=[个年月周日天次级艘名人万成%])')),
    ('newline', re.compile(r'\\n')),
]


def tokens(v):
    rest = v
    out = {}
    for name, rx in TOK:
        found = rx.findall(rest)
        out[name] = Counter(found)
        if name in ('bracket', 'dollar'):
            rest = rx.sub(' ', rest)
    return out


def apply(repo, edits_path):
    edits = json.load(open(edits_path, encoding='utf-8'))
    idx = index_repo(repo)
    origdir = os.path.join(os.path.dirname(os.path.abspath(edits_path)), 'edits-orig')
    os.makedirs(origdir, exist_ok=True)
    origf = os.path.join(origdir, os.path.basename(edits_path))
    orig = json.load(open(origf, encoding='utf-8')) if os.path.exists(origf) else {}
    byfile = {}
    for k, v in edits.items():
        if k not in idx:
            print('MISSING KEY', k)
            continue
        if '"' in v.replace('\\"', ''):
            print('UNESCAPED QUOTE', k)
            continue
        byfile.setdefault(idx[k][0], []).append(k)
    problems = 0
    for path, keys in byfile.items():
        raw = open(path, 'rb').read()
        bom = raw.startswith(b'\xef\xbb\xbf')
        text = raw.decode('utf-8')
        if bom:
            text = text[1:]
        nl = '\r\n' if '\r\n' in text else '\n'
        lines = text.split(nl)
        for k in keys:
            n = idx[k][1]
            m = LINE.match(lines[n])
            assert m and m.group(2) == k, (path, n, k)
            old = m.group(4)
            orig.setdefault(k, old)
            t0, t1 = tokens(orig[k]), tokens(edits[k])
            for name in ('bracket', 'dollar', 'fmt', 'close', 'icon', 'num'):
                if t0[name] != t1[name]:
                    print(f'TOKEN MISMATCH {k} {name}: {dict(t0[name] - t1[name])} -> {dict(t1[name] - t0[name])}')
                    problems += 1
            if t0['cnnum'] != t1['cnnum']:
                print(f'cn-number change {k}: {dict(t0["cnnum"])} -> {dict(t1["cnnum"])}')
            lines[n] = f'{m.group(1)}{k}{m.group(3)}"{edits[k]}"{m.group(5)}'
        out = nl.join(lines)
        open(path, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + out.encode('utf-8'))
    json.dump(orig, open(origf, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'applied {sum(len(v) for v in byfile.values())} keys in {len(byfile)} files; token problems {problems}')


def check(repo, base):
    names = subprocess.run(['git', '-C', repo, 'diff', '--name-only', base, '--', 'localization/simp_chinese'],
                           capture_output=True, text=True).stdout.split()
    bad, changed, perfile = [], 0, Counter()
    for f in names:
        old = subprocess.run(['git', '-C', repo, 'show', f'{base}:{f}'], capture_output=True).stdout
        new = open(os.path.join(repo, f), 'rb').read()
        hdr = []
        for label, raw in (('old', old), ('new', new)):
            hdr.append((raw.startswith(b'\xef\xbb\xbf'), raw.decode('utf-8').lstrip('﻿').splitlines()[0].strip()))
        if hdr[0] != hdr[1]:
            bad.append((f, 'HEADER/BOM', hdr))
        def kv(raw):
            d, dup = {}, []
            for line in raw.decode('utf-8').lstrip('﻿').splitlines():
                m = LINE.match(line)
                if m:
                    if m.group(2) in d:
                        dup.append(m.group(2))
                    d[m.group(2)] = m.group(4)
            return d, dup
        o, _ = kv(old)
        nw, dup = kv(new)
        if dup:
            bad.append((f, 'DUP', dup))
        if set(o) != set(nw):
            bad.append((f, 'KEYSET', sorted(set(o) ^ set(nw))))
        for k in nw:
            if k in o and o[k] != nw[k]:
                changed += 1
                perfile[f] += 1
                t0, t1 = tokens(o[k]), tokens(nw[k])
                for name in ('bracket', 'dollar', 'fmt', 'close', 'icon', 'num'):
                    if t0[name] != t1[name]:
                        bad.append((f, k, name, dict(t0[name] - t1[name]), dict(t1[name] - t0[name])))
    print(json.dumps({'changed_keys': changed, 'per_file': perfile, 'problems': bad}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'dump':
        dump(sys.argv[2], sys.argv[3], sys.argv[4], len(sys.argv) > 5)
    elif cmd == 'apply':
        apply(sys.argv[2], sys.argv[3])
    elif cmd == 'check':
        check(sys.argv[2], sys.argv[3])
