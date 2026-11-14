"""Static scans for load-time and description-time errors that Toolkit does not report.

Three checks over the main MOD (read only):
  bom    script or localisation file without UTF-8 BOM (engine: "should be in utf8-bom encoding")
  color  visible journal outcome with a trigger but no color (engine: "outcome N has no color")
  anyeq  any_* whose body, after expanding scripted triggers and dropping custom_tooltip blocks,
         compares against the iterated object, e.g. c:X ?= this (engine: "Scope dependent values
         in localization inside an any trigger"), reached from a place that generates descriptions:
         button/decision/journal possible, visible journal outcome trigger, event option trigger.

The anyeq check is a text scan. A hit is a risk to review, not proof of an error: it fires only
when the condition is actually described in the UI.

    python scripts/static_lints.py [--checks bom,color,anyeq] [--out report.json]
"""
import argparse
import json
import re
from pathlib import Path

from catalog import MOD

BOM = b'\xef\xbb\xbf'
BOM_DIRS = ['common', 'events', 'localization']
BOM_SKIP = ['common/coat_of_arms/']  # vanilla mixes BOM here and the engine does not warn
CMP = re.compile(r'c:\w+\s*\?=\s*this\b|\bthis\s*\?=\s*c:\w+|\bthis\s*=\s*scope:\w+|\bthis\s*=\s*c:\w+')


def text(p):
    return p.read_bytes().decode('utf-8', errors='replace').lstrip('\ufeff')


def block(t, i):
    """Return (start, end) of the brace block whose '{' is at or after i."""
    j = t.index('{', i) + 1
    d, k = 1, j
    while d and k < len(t):
        c = t[k]
        if c == '#':
            k = t.find('\n', k)
            if k < 0:
                break
            continue
        d += {'{': 1, '}': -1}.get(c, 0)
        k += 1
    return j, k - 1


def line_of(t, i):
    return t.count('\n', 0, i) + 1


def check_bom():
    out = []
    for d in BOM_DIRS:
        for p in (MOD / d).rglob('*'):
            if p.suffix not in ('.txt', '.yml') or not p.is_file():
                continue
            rel = p.relative_to(MOD).as_posix()
            if any(rel.startswith(s) for s in BOM_SKIP):
                continue
            if not p.read_bytes().startswith(BOM):
                out.append({'file': rel})
    return out


def outcomes(t):
    for m in re.finditer(r'\boutcome\s*=\s*\{', t):
        j, k = block(t, m.start())
        yield m.start(), t[j:k]


def visible_with_trigger(ob):
    fl = re.search(r'\bflags\s*=\s*\{([^}]*)\}', ob)
    flags = fl.group(1) if fl else ''
    return 'hidden' not in flags and 'timeout' not in flags and re.search(r'\btrigger\s*=', ob)


def check_color():
    out = []
    for p in (MOD / 'common/journal_entries').glob('*.txt'):
        t = text(p)
        for pos, ob in outcomes(t):
            if visible_with_trigger(ob) and not re.search(r'\bcolor\s*=', ob):
                out.append({'file': p.relative_to(MOD).as_posix(), 'line': line_of(t, pos)})
    return out


def strip_tooltips(body):
    out, i = [], 0
    for m in re.finditer(r'\bcustom_tooltip\s*=\s*\{', body):
        if m.start() < i:
            continue
        j, k = block(body, m.start())
        out.append(body[i:m.start()])
        i = k + 1
    out.append(body[i:])
    return ''.join(out)


def load_triggers():
    defs = {}
    for p in (MOD / 'common/scripted_triggers').glob('*.txt'):
        t = text(p)
        for m in re.finditer(r'^(\w+)\s*=\s*\{', t, re.M):
            j, k = block(t, m.start())
            defs[m.group(1)] = (p.relative_to(MOD).as_posix(), line_of(t, m.start()), t[j:k])
    return defs


def check_anyeq():
    defs = load_triggers()
    dep_memo = {}

    def depends(body, seen):
        body = strip_tooltips(body)
        if CMP.search(body):
            return True
        for n in set(re.findall(r'\b(\w+)\s*=\s*yes\b', body)):
            if n in defs and n not in seen:
                if n not in dep_memo:
                    dep_memo[n] = depends(defs[n][2], seen | {n})
                if dep_memo[n]:
                    return True
        return False

    def bare_any(body, where, seen):
        body = strip_tooltips(body)
        hits = []
        for m in re.finditer(r'\b(any_\w+)\s*=\s*\{', body):
            j, k = block(body, m.start())
            if depends(body[j:k], seen):
                hits.append((m.group(1), where))
        for n in set(re.findall(r'\b(\w+)\s*=\s*yes\b', body)):
            if n in defs and n not in seen:
                f, ln, b = defs[n]
                hits += bare_any(b, f'{f}:{ln} ({n})', seen | {n})
        return hits

    sources = []
    for sub, key in [('common/scripted_buttons', 'possible'), ('common/decisions', 'possible'), ('common/journal_entries', 'possible')]:
        for p in (MOD / sub).glob('*.txt'):
            t = text(p)
            for m in re.finditer(r'\b' + key + r'\s*=\s*\{', t):
                j, k = block(t, m.start())
                sources.append((p, t, m.start(), key, t[j:k]))
    for p in (MOD / 'common/journal_entries').glob('*.txt'):
        t = text(p)
        for pos, ob in outcomes(t):
            if visible_with_trigger(ob):
                tm = re.search(r'\btrigger\s*=\s*\{', ob)
                j, k = block(ob, tm.start())
                sources.append((p, t, pos, 'outcome', ob[j:k]))
    for p in (MOD / 'events').rglob('*.txt'):
        t = text(p)
        for m in re.finditer(r'\boption\s*=\s*\{', t):
            j, k = block(t, m.start())
            tm = re.search(r'\btrigger\s*=\s*\{', t[j:k])
            if tm:
                a, b = block(t, j + tm.start())
                sources.append((p, t, m.start(), 'option trigger', t[a:b]))
    out, seen_keys = [], set()
    for p, t, pos, kind, body in sources:
        src = f'{p.relative_to(MOD).as_posix()}:{line_of(t, pos)}'
        for it, where in bare_any(body, src, frozenset()):
            key = (src, it, where)
            if key not in seen_keys:
                seen_keys.add(key)
                out.append({'source': src, 'kind': kind, 'iterator': it, 'at': where})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--checks', default='bom,color,anyeq')
    ap.add_argument('--out', type=Path)
    a = ap.parse_args()
    fns = {'bom': check_bom, 'color': check_color, 'anyeq': check_anyeq}
    res = {c: fns[c]() for c in a.checks.split(',')}
    for c, items in res.items():
        print(f'{c}: {len(items)}')
        for x in items[:30]:
            print('  ', ' '.join(str(v) for v in x.values()))
        if len(items) > 30:
            print(f'   ... {len(items) - 30} more')
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(res, ensure_ascii=False, indent=2), 'utf-8')


if __name__ == '__main__':
    main()
