"""Save exact independent candidate trees; never touch the source directories."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess

WORK = Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
REPO = WORK / 'projects/nesnd-repository'

def git(*args, source=None):
    command = ['git', '--git-dir', str(REPO/'.git'), '--work-tree', str(source or REPO), *args]
    run = subprocess.run(command, check=True, capture_output=True)
    return run.stdout.decode('utf-8', 'replace').strip()

def manifest(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}

def main():
    assert git('symbolic-ref', '--short', 'HEAD') == 'main'
    assert not git('status','--porcelain'), 'Preserve existing working changes before snapshot import'
    specs = [
        ('batch-debug-20261101-f2','candidate/f2','candidate/f1','f2-pre-player-20261101'),
        ('f2-player-continuation-20261101-a','archive/unselected-player-ack-a','candidate/f2','unselected-player-ack-20261101'),
        ('f2-japan-legacy-20261101-a','archive/unselected-japan-legacy-a','candidate/f2','unselected-japan-legacy-20261101'),
    ]
    records=[]
    try:
        for folder, branch, parent, tag in specs:
            source = (WORK/'exports'/folder).resolve()
            assert source.is_relative_to((WORK/'exports').resolve())
            hashes = manifest(source)
            assert '.metadata/metadata.json' in hashes
            git('branch',branch,parent)
            git('symbolic-ref','HEAD','refs/heads/'+branch)
            git('read-tree','--empty')
            git('add','--force','--all','--','.',source=source)
            paths={x for x in git('ls-files','-z',source=source).split('\0') if x}
            assert paths == set(hashes)
            selection = 'UNSELECTED alternative after user design clarification' if branch.startswith('archive/unselected-') else 'Selected debug baseline; runtime coverage partial'
            git('commit','-m',f'Checkpoint {folder}; {selection}',source=source)
            commit=git('rev-parse','HEAD')
            assert hashes==manifest(source),'Candidate changed during import'
            fingerprint=hashlib.sha256(json.dumps(hashes,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            git('tag','-a',tag,'-m',f'Checkpoint only; not accepted.\n{selection}\nCandidate: {folder}\nFiles: {len(hashes)}\nSHA-256: {fingerprint}')
            records.append({'candidate':str(source),'branch':branch,'parent':parent,'tag':tag,'commit':commit,'files':len(hashes),'fingerprint':fingerprint,'selection':selection,'engine_acceptance':'incomplete'})
    finally:
        git('symbolic-ref','HEAD','refs/heads/main')
        git('read-tree','main')
    assert not git('status','--porcelain')
    out=WORK/'reports'/('git-candidate-checkpoints-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.json')
    out.write_text(json.dumps({'remote_pushed':False,'snapshots':records},indent=2),'utf-8')
    print(json.dumps({'report':str(out),'snapshots':records},ensure_ascii=False,indent=2))

if __name__ == '__main__': main()
