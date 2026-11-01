"""Verified full MOD backup outside all active mod directories."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, argparse, re
from catalog import MOD, WORK, version

def manifest(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--label',default='update');ap.add_argument('--status',choices=['pre-change','candidate','checkpoint','accepted'],default='pre-change');ap.add_argument('--evidence',type=Path);ap.add_argument('--source',type=Path,default=MOD);args=ap.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+',args.label):raise ValueError('Label must contain letters, numbers, underscores or hyphens')
    source=args.source.resolve()
    if source!=MOD.resolve() and not source.is_relative_to((WORK/'exports').resolve()):
        raise ValueError('Backup source must be the main MOD or an isolated workbench export')
    if not ((source/'descriptor.mod').is_file() or (source/'.metadata/metadata.json').is_file()):
        raise ValueError('Backup source must have descriptor.mod or .metadata/metadata.json')
    target=(WORK/'backups'/(args.status+'-'+args.label+'-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))).resolve()
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
