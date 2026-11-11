"""Compare same-path files in the main MOD with vanilla (clausewitz, jomini, game, dlc) and rewrite the override list.

python scripts/vanilla_overrides.py [--out <dir>]
Writes vanilla-overrides.md and baseline.json to --out (default WORK/reports/<date>-vanilla-overrides).
Review, then copy the .md over lookup/vanilla-overrides.md.
Generalised from WORK/reports/2026-11-08-vanilla-overrides/manifest.py.
"""
import argparse, hashlib, json
from collections import defaultdict
from datetime import date
from pathlib import Path
from catalog import MOD, WORK, GAME, version

INTRO = ('本表用于复查整文件覆盖。新增、撤回同路径覆盖，或完成版本迁移时，按主 MOD 实际加载目录与本机原版重新比对，并同步技能副本。'
         '独立文件中的 `REPLACE:` 按覆盖的定义另行比对；例如秀全的通用选人条件对应 '
         '`common/scripted_triggers/00_ep2_victoria_scripted_triggers.txt` 中的 `character_is_valid_for_events`。')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path)
    ap.add_argument('--mod', type=Path, default=MOD)
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
    lines = ['# 主 MOD 修改的原版文件', '',
             f'对照 Victoria 3 {v["version"]}，Steam build {v["build"]}。文件夹从 MOD 根目录或原版 `game/` 起算，拼上文件名即可定位双方文件。',
             '', INTRO, '']
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
                      'changed': sum(map(len, sections['changed'].values()))}, ensure_ascii=False))


if __name__ == '__main__':
    main()
