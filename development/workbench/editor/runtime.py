"""Launch an immutable candidate in an isolated user directory; archive engine evidence."""
import sys,json,subprocess,hashlib,shutil,time
from pathlib import Path
from datetime import datetime,timezone
from model import WORK,GAME,MOD

def launch(candidate, mode='mod', cache_profile=None, autosave=None, save_manifest=None):
    candidate=Path(candidate).resolve()
    if autosave not in {None, 'monthly'}:raise ValueError('Only the explicit isolated monthly autosave experiment is supported.')
    if candidate!=MOD.resolve() and not candidate.is_relative_to((WORK/'exports').resolve()):raise ValueError('Only the main MOD or workbench exports may be launched.')
    running=subprocess.run(['powershell','-NoProfile','-Command','@(Get-Process victoria3 -ErrorAction SilentlyContinue).Count'],capture_output=True,text=True)
    if running.stdout.strip()!='0':raise RuntimeError('Victoria 3 is already running. Close the current game before starting another candidate.')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');report=WORK/'reports/runtime'/stamp;report.mkdir(parents=True)
    # Never mount the editable working tree: hot reload can combine partially written databases.
    snapshot=WORK/'exports'/('runtime-'+stamp);snapshot.mkdir(parents=True)
    frozen=snapshot/'mod';shutil.copytree(candidate,frozen)
    qa=snapshot/'qa-overlay';shutil.copytree(WORK/'runtime/qa-overlay',qa)
    profile=WORK/'runtime/profiles'/stamp;profile.mkdir(parents=True)
    # Native menu scans saves during startup. Copy explicit, unchanged branch
    # baselines BEFORE spawning the process; copying after launch is too late.
    copied_saves=[]
    if save_manifest:
        manifest=Path(save_manifest).resolve()
        if not manifest.is_relative_to(WORK.resolve()):raise ValueError('Save manifest must be inside WORK')
        requested=json.loads(manifest.read_text('utf-8-sig'))['copies']
        if not requested:raise ValueError('Empty save manifest')
        save_dir=profile/'save games';save_dir.mkdir()
        for entry in requested:
            source=Path(entry['source']).resolve()
            if not source.is_relative_to((WORK/'runtime/profiles').resolve()) or source.suffix.lower()!='.v3':raise ValueError('Only isolated profile v3 baselines may be seeded')
            data=source.read_bytes();digest=hashlib.sha256(data).hexdigest()
            if digest!=entry['sha256']:raise ValueError('Baseline hash changed: '+str(source))
            target=save_dir/source.name
            with target.open('xb') as handle:handle.write(data)
            if hashlib.sha256(target.read_bytes()).hexdigest()!=digest:raise ValueError('Baseline copy mismatch')
            copied_saves.append({'source':str(source),'copy':str(target),'sha256':digest})
    cache_seed=None
    if cache_profile:
        previous=Path(cache_profile).resolve()
        if not previous.is_relative_to((WORK/'runtime/profiles').resolve()) or not (previous/'shadercache').is_dir():
            raise ValueError('Shader cache source must be an existing isolated workbench profile')
        # Only disposable engine-generated shaders. No saves, logs, settings,
        # map cache, histories or third-party source assets are imported.
        shutil.copytree(previous/'shadercache',profile/'shadercache')
        cache_seed=str(previous/'shadercache')
    settings=WORK.parent/'pdx_settings.json'
    if settings.exists():shutil.copy2(settings,profile/settings.name)
    autosave_override=None
    if autosave:
        isolated_settings=profile/'pdx_settings.json'
        data=json.loads(isolated_settings.read_text('utf-8-sig')) if isolated_settings.exists() else {}
        previous_autosave=data.setdefault('game',{}).get('autosave')
        data['game']['autosave']=autosave
        isolated_settings.write_text(json.dumps(data,ensure_ascii=False,indent=2),'utf-8')
        autosave_override={'requested':autosave,'previous':previous_autosave,'profile_only':True,'engine_verified':False,'verification':'Check native settings display and an actual autosave after advancing a month.'}
    mods=[]
    if mode in {'mod','dependency'}:mods.append({'path':r'D:\Program Files (x86)\Steam\steamapps\workshop\content\529340\3704408897'})
    if mode in {'mod','mod-only'}:mods.append({'path':str(frozen)})
    mods.append({'path':str(qa)})
    load={'disabledDLC':[],'enabledUGC':[],'enabledMods':mods}
    (profile/'content_load.json').write_text(json.dumps(load,indent=2),'utf-8')
    hashes={p.relative_to(candidate).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(candidate.rglob('*')) if p.is_file()}
    command=[str(GAME.parent/'binaries/victoria3.exe'),'-debug_mode','-nofilewatcher','-gdpr-compliant','-userdir='+str(profile)]
    run={'candidate':str(candidate),'frozen_candidate':str(frozen),'profile':str(profile),'started_utc':stamp,'mode':mode,'load':load,'command':command,'source_sha256':hashes,'shader_cache_seed':cache_seed,'autosave_override':autosave_override,'scope':'launch-and-archive only; navigation and engine assertions are separate evidence'}
    run['prelaunch_seed_saves']=copied_saves
    (report/'run.json').write_text(json.dumps(run,indent=2),'utf-8')
    print(json.dumps({'report':str(report),'profile':str(profile),'mode':mode}),flush=True)
    try:
        p=subprocess.Popen(command,cwd=GAME.parent/'binaries');p.wait()
    finally:
        if (profile/'logs').exists():shutil.copytree(profile/'logs',report/'logs',dirs_exist_ok=True)
        else:(report/'PROFILE-FAILED.txt').write_text('Isolated profile did not produce logs; do not attribute main-profile logs to this run.','utf-8')
        final={q.relative_to(frozen).as_posix():hashlib.sha256(q.read_bytes()).hexdigest() for q in sorted(frozen.rglob('*')) if q.is_file()}
        (report/'snapshot-integrity.json').write_text(json.dumps({'unchanged':final==hashes}),'utf-8')
    return report

if __name__=='__main__':
    try:print(launch(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else 'mod',sys.argv[3] if len(sys.argv)>3 else None,sys.argv[4] if len(sys.argv)>4 else None,sys.argv[5] if len(sys.argv)>5 else None))
    except Exception as e:
        import tkinter as tk
        from tkinter import messagebox
        root=tk.Tk();root.withdraw();messagebox.showerror('游戏验证未启动',str(e));root.destroy();sys.exit(1)
