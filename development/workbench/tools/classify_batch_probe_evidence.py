"""Small global-runner adapter over qa_batch_probe.py's actual collector output."""
from pathlib import Path
import json,hashlib,argparse
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def classify(candidate,collector_report):
    candidate=Path(candidate).resolve();collector_report=Path(collector_report)
    if not collector_report.is_file():return {'status':'NOT_RUN','engine_verified':False,'reason':'No actual collector report supplied'}
    r=json.loads(collector_report.read_text('utf-8-sig'));mp=Path(r['manifest']);m=json.loads(mp.read_text('utf-8-sig'))
    actual={f.relative_to(candidate).as_posix():sha(f) for f in sorted(candidate.rglob('*')) if f.is_file()}
    match=actual==m.get('candidate_manifest');bind=r.get('binding',{})
    integrity={'manifest_unchanged':sha(mp)==r.get('manifest_sha256'),'candidate_exact_manifest_match':match,
               'run_unchanged':bool(bind.get('run')) and Path(bind['run']).is_file() and sha(Path(bind['run']))==bind.get('run_sha256'),
               'reported_logs_unchanged':all(Path(x['path']).is_file() and sha(Path(x['path']))==x['sha256'] for x in r.get('input_files_oldest_first',[]))}
    usable=all(integrity.values()) and bool(bind.get('verified'))
    status='PASS' if usable and r.get('status')=='OBSERVED_PASS' and r.get('engine_verified') else ('FAIL' if usable and r.get('status')=='FAIL' else 'NOT_RUN')
    return {'status':status,'engine_verified':status=='PASS','candidate':str(candidate),'collector_report':str(collector_report),
            'collector_report_sha256':sha(collector_report),'collector_status':r.get('status'),'binding':bind,'integrity':integrity,
            'coverage':r.get('required_cases',[]),'passed_cases':r.get('passed_cases',[]),
            'reason':'Only the explicitly named native predicates are covered' if status=='PASS' else ('Bound native predicate failure observed' if status=='FAIL' else 'No complete current-candidate bound execution evidence; missing, stale, partial or skipped output is not a pass'),
            'boundary':'NOT_RUN is a runner evidence status, not proof the game never executed; does not cover all events, UI, economy or map navigation.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--candidate',type=Path,required=True);p.add_argument('--collector-report',type=Path,required=True);p.add_argument('--out',type=Path);a=p.parse_args();r=classify(a.candidate,a.collector_report)
    if a.out:
        w=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench').resolve()
        if not a.out.resolve().is_relative_to(w):raise ValueError('Output outside WORK')
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,ensure_ascii=False,indent=2),'utf-8')
    print(json.dumps(r,ensure_ascii=False));raise SystemExit(1 if r['status']=='FAIL' else 0)
