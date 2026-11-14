"""Compare same-path files in the main MOD with vanilla (clausewitz, jomini, game, dlc) and rewrite the override list.

python scripts/vanilla_overrides.py [--out <dir>] [--existing <current vanilla-overrides.md>]
Writes vanilla-overrides.md and baseline.json to --out (default WORK/reports/<date>-vanilla-overrides).
Review, then copy the .md over lookup/vanilla-overrides.md.

Only the three file sections from `## 内容有改动` onward are generated. Everything above that heading in
--existing (title, 何时读 line, intro, hand-written single-key REPLACE tables) is kept verbatim; only the
"对照 Victoria 3 …" version line is refreshed. Paths cited in that hand-written part that exist neither in the
MOD nor in vanilla are printed as warnings, so a renamed vanilla file or deleted MOD file is noticed.
Generalised from WORK/reports/2026-11-08-vanilla-overrides/manifest.py.
"""
import argparse, hashlib, json, re
from collections import defaultdict
from datetime import date
from pathlib import Path
from catalog import MOD, WORK, GAME, version

EXISTING = Path(__file__).resolve().parent.parent / 'lookup' / 'vanilla-overrides.md'
FIRST_GENERATED = '## 内容有改动'
VERSION_LINE = re.compile(r'^对照 Victoria 3 .*$', re.M)
CITED_PATH = re.compile(r'`((?:common|events|gfx|gui|localization|map_data)/[^`]+\.[A-Za-z0-9]+)`')


def manual_head(path, version_line):
    """Hand-written part of the current list: everything before the first generated heading."""
    text = path.read_text('utf-8-sig').replace('\r\n', '\n')
    head, sep, _ = text.partition('\n' + FIRST_GENERATED)
    if not sep:
        raise SystemExit(f'{path}: heading "{FIRST_GENERATED}" not found; refusing to drop hand-written sections')
    if not VERSION_LINE.search(head):
        raise SystemExit(f'{path}: version line "对照 Victoria 3 …" not found')
    return VERSION_LINE.sub(lambda _: version_line, head, count=1).rstrip('\n').split('\n') + ['']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path)
    ap.add_argument('--mod', type=Path, default=MOD)
    ap.add_argument('--existing', type=Path, default=EXISTING)
    a = ap.parse_args()
    out = a.out or WORK / 'reports' / f'{date.today().isoformat()}-vanilla-overrides'
    out.mkdir(parents=True, exist_ok=True)
    root, inst = a.mod, GAME.parent
    layers = [inst / 'clausewitz', inst / 'jomini', GAME] + sorted(d for d in (GAME / 'dlc').iterdir() if d.is_dir())
    sections = defaultdict(lambda: defaultdict(list))
    manifest = {}

    def norm(b):
        return b.removeprefix(b'\xef\xbb\xbf').replace(b'\r\n', b'\n')
    for directory in ('common', 'events', 'gfx', 'gui', 'localization', 'map_data'):
        for p in (root / directory).rglob('*'):
            if not p.is_file():
                continue
            rel = p.relative_to(root)
            sources = [r / rel for r in layers if (r / rel).is_file()]
            if not sources:
                continue
            assert len(sources) == 1, (p, sources)
            src = sources[0]
            x, y = p.read_bytes(), src.read_bytes()
            status = ('equal' if x == y else
                      'format' if p.suffix in ('.txt', '.md', '.gui', '.yml') and norm(x) == norm(y) else 'changed')
            sections[status][rel.parent.as_posix()].append(rel.name)
            manifest[rel.as_posix()] = {'source': src.relative_to(inst).as_posix(),
                                        'vanilla_sha256': hashlib.sha256(y).hexdigest(),
                                        'mod_sha256': hashlib.sha256(x).hexdigest(), 'status': status}
    v = version()
    lines = manual_head(a.existing, f'对照 Victoria 3 {v["version"]}，Steam build {v["build"]}。'
                                    '文件夹从 MOD 根目录或原版 `game/` 起算，拼上文件名即可定位双方文件。')
    warnings = [f'cited path missing in MOD and vanilla: {m}'
                for m in sorted(set(CITED_PATH.findall('\n'.join(lines))))
                if not (root / m).is_file() and not any((r / m).is_file() for r in layers)]
    for w in warnings:
        print('WARNING', w)
    for k, title in [('changed', '内容有改动'), ('format', '仅编码标记或换行有差异'), ('equal', '与原版逐字节相同的同路径副本')]:
        groups = sections[k]
        lines += ['## ' + title + f'（{sum(map(len, groups.values()))} 个）', '', '| 文件夹 | 文件名 |', '| --- | --- |']
        for folder, files in sorted(groups.items(), key=lambda s: s[0].casefold()):
            files = sorted(files, key=str.casefold)
            for i in range(0, len(files), 5):
                lines.append(f'| `{folder}` | ' + '、'.join('`' + n + '`' for n in files[i:i + 5]) + ' |')
        lines.append('')
    (out / 'vanilla-overrides.md').write_text('\n'.join(lines), 'utf-8')
    (out / 'baseline.json').write_text(json.dumps({'game': v, 'files': dict(sorted(manifest.items()))},
                                                  ensure_ascii=False, indent=2), 'utf-8')
    print(json.dumps({'out': str(out), 'version': v, 'files': len(manifest),
                      'changed': sum(map(len, sections['changed'].values())),
                      'kept_from': str(a.existing), 'warnings': len(warnings)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
