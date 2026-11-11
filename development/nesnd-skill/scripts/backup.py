"""Verified backup outside all active mod directories.

Full MOD:   python scripts/backup.py --status pre-change --label <topic>
Some paths: python scripts/backup.py --status pre-change --label <topic> --paths <file or dir> ...
            (paths must lie inside the main MOD or the skills folder; stored as mod/... and skills/...)
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, argparse, re
from catalog import MOD, WORK, version

SKILLS = Path(__file__).resolve().parents[2]  # ...\.codex\skills

def manifest(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}

def partial(args, target):
    """Back up selected files/dirs from the MOD or the skills folder, verified by SHA-256."""
    roots = {'mod': MOD.resolve(), 'skills': SKILLS.resolve()}
    picked = []
    for raw in args.paths:
        p = Path(raw).resolve()
        if not p.exists(): raise FileNotFoundError(p)
        label = next((k for k, r in roots.items() if p.is_relative_to(r)), None)
        if label is None: raise ValueError(f'{p} is outside the main MOD and the skills folder')
        picked.append((label, roots[label], p))
    def files(p): return [p] if p.is_file() else [x for x in sorted(p.rglob('*')) if x.is_file()]
    def snap(): return {f'{l}/{f.relative_to(r).as_posix()}': hashlib.sha256(f.read_bytes()).hexdigest()
                        for l, r, p in picked for f in files(p)}
    before = snap()
    target.mkdir(parents=True, exist_ok=False)
    for label, root, p in picked:
        dst = target/label/p.relative_to(root); dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(p, dst, copy_function=shutil.copy2) if p.is_dir() else shutil.copy2(p, dst)
    copied = {k: hashlib.sha256((target/k).read_bytes()).hexdigest() for k in before}
    if before != snap() or before != copied:
        raise RuntimeError('Backup verification failed or source changed during backup')
    fp = hashlib.sha256(json.dumps(before, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    report = {'paths': [str(p) for _, _, p in picked], 'version': version(), 'status': args.status, 'label': args.label,
              'verified_files': len(before), 'sha256_all': fp, 'sha256': before}
    (target/'manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), 'utf-8')
    print(json.dumps({'backup': str(target), 'verified_files': len(before)}, ensure_ascii=False))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--label',default='update');ap.add_argument('--status',choices=['pre-change','candidate','checkpoint','accepted'],default='pre-change');ap.add_argument('--evidence',type=Path);ap.add_argument('--source',type=Path,default=MOD);ap.add_argument('--paths',nargs='+');args=ap.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+',args.label):raise ValueError('Label must contain letters, numbers, underscores or hyphens')
    target=(WORK/'backups'/(args.status+'-'+args.label+'-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))).resolve()
    if args.paths:
        if args.status=='accepted':raise ValueError('An accepted backup must cover the whole MOD')
        return partial(args, target)
    source=args.source.resolve()
    if source!=MOD.resolve() and not source.is_relative_to((WORK/'exports').resolve()):
        raise ValueError('Backup source must be the main MOD or an isolated workbench export')
    if not ((source/'descriptor.mod').is_file() or (source/'.metadata/metadata.json').is_file()):
        raise ValueError('Backup source must have descriptor.mod or .metadata/metadata.json')
    if not target.is_relative_to(WORK.resolve()) or target.is_relative_to(source):
        raise RuntimeError('Unsafe backup destination')
    before=manifest(source)
    fingerprint=hashlib.sha256(json.dumps(before,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    evidence=json.loads(args.evidence.read_text('utf-8-sig')) if args.evidence else None
    if args.status=='accepted':
        if not evidence or evidence.get('engine_verified') is not True or evidence.get('mod_sha256')!=fingerprint:
            raise ValueError('Accepted backup needs genuine engine evidence for these exact files')
        if not evidence.get('runs') or any(not Path(p).exists() for p in evidence['runs']):raise ValueError('Engine run records are missing')
    target.mkdir(parents=True,exist_ok=False)
    shutil.copytree(source,target/'mod',copy_function=shutil.copy2)
    after=manifest(source); copied=manifest(target/'mod')
    if before!=after or before!=copied:
        raise RuntimeError('Backup verification failed or source changed during backup')
    report={'source':str(source),'backup':str(target/'mod'),'version':version(),'status':args.status,'label':args.label,'verified_files':len(before),'mod_sha256':fingerprint,'sha256':before,'evidence':evidence}
    if args.evidence:shutil.copy2(args.evidence,target/'validation-evidence.json')
    (target/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
    (WORK/'reports/last-backup.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
    print(json.dumps({'backup':str(target/'mod'),'verified_files':len(before)},ensure_ascii=False))
if __name__=='__main__': main()
