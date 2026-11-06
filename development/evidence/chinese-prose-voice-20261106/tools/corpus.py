"""Build three Chinese corpora: author original (tag), vanilla, current agent text.

Usage: python3 -I corpus.py <repo> <vanilla_loc_dir> <out_json>
"""
import json, os, re, subprocess, sys, unicodedata

KEY_RE = re.compile(r'^\s*([A-Za-z0-9_.\-]+):\d*\s*"(.*)"\s*(#.*)?$')
TAG = 'original-20261030'


def parse_text(text):
    out = []
    if text.startswith('﻿'):
        text = text[1:]
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith('#') or s.startswith('l_'):
            continue
        m = re.match(r'^\s*([A-Za-z0-9_.\-]+):\d*\s*"(.*)$', line)
        if not m:
            continue
        rest = m.group(2)
        # value ends at last quote on the line
        idx = rest.rfind('"')
        val = rest[:idx] if idx >= 0 else rest
        out.append((m.group(1), val, n))
    return out


def git(repo, *args):
    return subprocess.run(['git', '-C', repo, *args], capture_output=True, check=True).stdout


def tag_files(repo):
    names = git(repo, 'ls-tree', '-r', '--name-only', TAG).decode().splitlines()
    return [n for n in names if n.startswith('localization/simp_chinese/') and n.endswith('.yml')]


PUNCT = set('，。；：、？！“”‘’（）《》—…·,.;:?!()"\' \\n')


def norm_punct(v):
    v = v.replace('\\n', '')
    return ''.join(ch for ch in v if ch not in PUNCT and not unicodedata.category(ch).startswith('P') and not ch.isspace())


def main(repo, vdir, out):
    author = {}  # key -> list of (file, value, line)
    for f in tag_files(repo):
        txt = git(repo, 'show', f'{TAG}:{f}').decode('utf-8', 'replace')
        for k, v, n in parse_text(txt):
            author.setdefault(k, []).append((f, v, n))

    cur = {}
    root = os.path.join(repo, 'localization/simp_chinese')
    for dp, _, fs in os.walk(root):
        for fn in fs:
            if not fn.endswith('.yml'):
                continue
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, repo)
            txt = open(p, encoding='utf-8-sig').read()
            for k, v, n in parse_text(txt):
                cur.setdefault(k, []).append((rel, v, n))

    vanilla = {}
    for dp, _, fs in os.walk(vdir):
        for fn in fs:
            if fn.endswith('.yml'):
                p = os.path.join(dp, fn)
                for k, v, n in parse_text(open(p, encoding='utf-8-sig', errors='replace').read()):
                    vanilla[k] = v

    rows = []
    for k, defs in cur.items():
        for (f, v, n) in defs:
            avals = [a[1] for a in author.get(k, [])]
            if v in avals:
                status = 'author_verbatim'
            elif not avals:
                status = 'agent_new'
            elif any(norm_punct(a) == norm_punct(v) for a in avals):
                status = 'punct_only'
            else:
                status = 'agent_changed'
            rows.append({'key': k, 'file': f, 'line': n, 'value': v, 'status': status,
                         'author_value': avals[0] if avals else None, 'dup': len(defs)})

    data = {
        'author': {k: [d[1] for d in v] for k, v in author.items()},
        'author_files': {k: [d[0] for d in v] for k, v in author.items()},
        'vanilla': vanilla,
        'current': rows,
    }
    json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
    from collections import Counter
    print('author keys', len(author), 'vanilla keys', len(vanilla), 'current defs', len(rows))
    print(Counter(r['status'] for r in rows))
    print('dup keys in current:', sum(1 for k, v in cur.items() if len(v) > 1))


if __name__ == '__main__':
    main(*sys.argv[1:4])
