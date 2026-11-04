"""First frozen A gate: actual ordered trigger AST, including an empty-law-owner fault.

No gameplay writes. A source failure ends the run immediately; remaining phase
work is deliberately NOT_RUN until the coordinator authorizes a repair phase.
"""
from pathlib import Path
from datetime import datetime, timezone
from types import SimpleNamespace
from copy import deepcopy
import hashlib
import json
import sys

W = Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
C = W / 'exports/canon-route-execution-20261104-a'
G = Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
R = W / 'reports/canon-route-execution-20261104'
sys.path.insert(0, 'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse
from test_commission_gate_behavior import Evaluator as Base, Obj


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_report(report):
    (R/'batch-a-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    rows = '\n'.join(f'| {x["name"]} | {x["status"]} | {x.get("detail", "")} |' for x in report['cases'])
    if report['status'] == 'GATE_PASS':
        (R/'batch-a-validation.md').write_text(f'''# Batch A validation — owner gate repaired

Status: **GATE_PASS / REMAINING_TESTS_PENDING**. A-01's actual source callback now rejects an absent owner without a scope error. The original failed report/snapshot remains under `batch-a-validation-red-a01/`.

No gameplay edits occurred during this retest. This executes the actual ordered trigger AST with the existing strict evaluator; it is not an engine callback observation. Current snapshot: `{report['snapshot']}`.

| Case | Result | Evidence |
|---|---|---|
{rows}

The remaining class/law/ideology/lifecycle/UI/MCP/Tiger matrix has not yet run. No whole-candidate fixed SHA or engine pass is claimed.
''', encoding='utf-8')
        return
    body = f'''# Batch A validation — stopped at first failing gate

Status: **{report['status']}**. No gameplay files were changed. No game was launched.

Frozen A scope: `{report['snapshot']}`. The 24 owned files were matched to the edit-phase manifest before copying. Additional candidate and native dependency fingerprints are in [batch-a-test-snapshot.json](batch-a-test-snapshot.json); this does not claim the concurrently edited whole candidate has one fixed SHA.

## Executed gate

The existing strict subset interpreter executes the **actual ordered trigger AST**, preserving operators and eager boolean sibling evaluation. It does not run the game. Unknown nodes or required empty scope links raise errors instead of returning a permissive result. The module's documented rule is that an `exists` sibling does not protect another sibling's scope dereference.

| Case | Result | Evidence |
|---|---|---|
{rows}

## Finding A-01

`common/on_actions/nesnd_hus_registration.txt:{report['callback_line']}` defines the custom law callback with sibling `exists = owner` and mandatory `owner = {{ ... }}` blocks. With a law fixture having no owner, the first sibling evaluates false but the second still resolves the missing scope and raises `unguarded scope`. The normal native callback supplies an owner, so this is an adversarial graceful-failure defect, **not a claim that an ownerless callback was observed in-game**.

The test's positive HUS case and ordinary-country case use the same source AST. Its in-memory optional-owner control returns false cleanly; that control was evaluated before the failing actual AST case and did not modify candidate files. A real repair should put the owner body behind a `trigger_if` existence branch (or equivalent verified optional scope handling), preserving the normal owner semantics.

## Stopped work

Per the coordinator's instruction, testing stopped immediately at A-01. The 12-class/15-profession effective-culture matrix, full law-treatment and ideology preservation assertions, six-law root/target matrix, lifecycle interpreter scenarios, UI datatype/narrow-diff assertions, A-scoped Tiger and MCP queries remain **NOT_RUN in this test phase**. Previous edit/source records are not relabeled as tests.

Repair phase is required before continuing. The next run must bind a new owned-file manifest and rerun this gate before the remaining validation matrix.
'''
    (R/'batch-a-validation.md').write_text(body, encoding='utf-8')


def main():
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    T = W/'validation/runs'/('canon-a-'+stamp)/'mod'
    T.mkdir(parents=True, exist_ok=False)
    owned = json.loads((R/'batch-a-owned-files-sha256.json').read_text(encoding='utf-8'))
    source_rows = []
    for row in owned:
        p = C/row['path']
        data = p.read_bytes()
        if sha(data) != row['sha256']:
            raise RuntimeError('Owned file changed before tests: '+row['path'])
        q = T/row['path']; q.parent.mkdir(parents=True, exist_ok=True); q.write_bytes(data)
        source_rows.append({'path':row['path'], 'source':p.as_posix(), 'snapshot':q.as_posix(), 'sha256':sha(data), 'role':'owned'})
    # Freeze only actual A prerequisites and effective culture/profession/ideology inputs.
    dependencies = {
        'common/country_definitions/nesnd_native_khanate.txt',
        'common/scripted_triggers/nesnd_native_khanate.txt',
        'common/static_modifiers/nesnd_hus_culture_tiers.txt',
        '.metadata/metadata.json', 'descriptor.mod',
    }
    for folder in ('common/cultures', 'common/discrimination_traits', 'common/discrimination_trait_groups', 'common/pop_types', 'common/ideologies'):
        if (C/folder).exists():
            dependencies.update(p.relative_to(C).as_posix() for p in (C/folder).glob('*.txt'))
    owned_paths = {row['path'] for row in owned}
    for rel in sorted(dependencies-owned_paths):
        p=C/rel
        if not p.exists():
            continue
        data=p.read_bytes(); q=T/rel; q.parent.mkdir(parents=True, exist_ok=True); q.write_bytes(data)
        source_rows.append({'path':rel,'source':p.as_posix(),'snapshot':q.as_posix(),'sha256':sha(data),'role':'unchanged_candidate_dependency'})
    game_rows=[]
    for folder in ('common/cultures','common/discrimination_traits','common/discrimination_trait_groups','common/pop_types','common/laws','common/law_groups','common/social_classes','common/social_hierarchies','common/ideologies','common/modifier_type_definitions'):
        for p in sorted((G/folder).glob('*.txt')):
            game_rows.append({'path':p.as_posix(),'sha256':sha(p.read_bytes())})
    meta={'utc':stamp,'snapshot':T.as_posix(),'owned_and_candidate_dependencies':source_rows,'game_dependencies':game_rows,
          'whole_C_fingerprint_claimed':False,'game_launched':False}
    (R/'batch-a-test-snapshot.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    trigger_path=T/'common/scripted_triggers/nesnd_hus_registration.txt'
    on_path=T/'common/on_actions/nesnd_hus_registration.txt'
    trigger_tree=parse(trigger_path.read_text(encoding='utf-8-sig'))
    on_text=on_path.read_text(encoding='utf-8-sig')
    on_tree=parse(on_text)
    actual=on_tree.get('nesnd_hus_hierarchy_law_activated').get('trigger')
    callback_line=on_text.count('\n',0,actual.start)+1

    class Eval(Base):
        def __init__(self, world):
            self.w=world; self.db={n.key:n for n in trigger_tree.children}; self.values={}; self.reads=[]

    hus=Obj('country','HUS',vars={'nesnd_hus_hierarchy_version'},laws=set())
    other=Obj('country','FRA',vars=set(),laws=set())
    world={'countries':{'HUS':hus,'FRA':other},'regions':{},'saved':{}}
    ev=Eval(world)
    report={'status':'RUNNING','snapshot':T.as_posix(),'cases':[], 'findings':[], 'engine_verified':False,'callback_line':callback_line,
            'interpreter':'Existing strict ordered AST evaluator from test_commission_gate_behavior.py; no boolean sibling short-circuit',
            'tested_files':[r for r in source_rows if r['path'] in ('common/scripted_triggers/nesnd_hus_registration.txt','common/on_actions/nesnd_hus_registration.txt')],
            'remaining':['classes/professions/effective cultures','24 bounds and three law treatments','68 ideology source preservation','six ordinary citizenship guards','full lifecycle/old timer/reentrancy','UI source datatypes','MCP','A-scoped Tiger']}
    cases=[
        ('native_law_owner_managed_HUS_is_selected',actual,Obj('law','law_example',owner=hus),True),
        ('native_law_owner_unrelated_country_is_rejected',actual,Obj('law','law_example',owner=other),False),
    ]
    control=deepcopy(actual)
    control.get('owner').op='?='
    cases.append(('in_memory_optional_owner_control_rejects_empty_owner_cleanly',control,Obj('law','law_example'),False))
    cases.append(('actual_callback_empty_owner_rejects_without_scope_fault',actual,Obj('law','law_example'),False))
    for name, ast, law, expected in cases:
        try:
            value=ev.block(ast,law,law)
            if value != expected:
                raise AssertionError(('wrong_result',value,expected))
            report['cases'].append({'name':name,'status':'PASS','detail':f'actual={value}; expected={expected}'})
        except Exception as exc:
            report['cases'].append({'name':name,'status':'FAIL','detail':repr(exc)})
            report['status']='FAIL_STOPPED'
            report['findings'].append({'id':'A-01','priority':'P2','file':'common/on_actions/nesnd_hus_registration.txt','line':callback_line,
                'condition':'law scope has no owner','actual':repr(exc),'expected':'false without resolving missing mandatory owner scope',
                'classification':'strict AST scope-guard contract failure, not observed engine callback failure'})
            write_report(report)
            print(json.dumps({'status':report['status'],'cases':report['cases'],'report':str(R/'batch-a-validation.md')},ensure_ascii=False))
            return 1
    report['status']='GATE_PASS'
    write_report(report)
    return 0


if __name__=='__main__':
    raise SystemExit(main())
