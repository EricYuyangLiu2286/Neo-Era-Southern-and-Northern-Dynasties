"""Exercise live Mod predicates and the migration worker. No engine or save edits."""
import ast
import copy
import json
import math
import operator
import sys
from itertools import product
from pathlib import Path

from_root = Path.cwd()
reports = from_root.parents[1] / 'nesnd-workbench/reports'
sys.path.insert(0, str(Path.home() / '.codex/skills/nesnd-victoria3/scripts'))
from pdx import read

def load(rel):
    return read(from_root / rel)[1]

checks = []
def check(label, result):
    assert result, label
    checks.append(label)

# Execute the actual scripted region trigger on realistic split states.
region_test = load('common/scripted_triggers/nesnd_ottoman_recovery.txt').get('nesnd_ottoman_claim_target')
cost = float(load('common/script_values/nesnd_ottoman_recovery.txt').scalar('nesnd_ottoman_claim_cost'))
def predicate(node, world, current, prev=None):
    children = node.children or []
    def all_of():
        return all(predicate(item, world, current, prev) for item in children)
    name = node.key
    if name in ('nesnd_ottoman_claim_target', 'limit'):
        if children and children[0].key == 'trigger_if':
            conditional, fallback = children
            if predicate(conditional.get('limit'),world,current,prev):
                return all(predicate(n,world,current,prev) for n in conditional.children if n.key!='limit')
            return predicate(fallback.children[0],world,current,prev)
        return all_of()
    if name=='exists':return world['exists']
    if name=='always':return node.value=='yes'
    if name=='NOT':return not all_of()
    if name=='c:TUR' and children:
        return all(predicate(n,world,'TUR',current) for n in children)
    if name=='is_country_alive':return world['exists']
    if name=='has_claim':
        assert node.value=='prev' and prev==world['region']
        return world['claimed']
    if name=='nesnd_ottoman_enthusiasm_value':
        assert node.op=='>=' and node.value=='nesnd_ottoman_claim_cost'
        return world['points']>=cost
    if name=='any_scope_state':
        return any(all(predicate(n,world,st,current) for n in children) for st in current)
    if name=='any_neighbouring_state':
        return any(all(predicate(n,world,st,current) for n in children) for st in current['adj'])
    if name=='owner':
        if not children:return current['owner']==node.value.removeprefix('c:')
        return all(predicate(n,world,current['owner'],current) for n in children)
    if name in ('c:TUR','c:EGY'):return current==name[2:]
    if name=='trigger_if':
        return (not predicate(node.get('limit'),world,current,prev) or
                all(predicate(n,world,current,prev) for n in children if n.key!='limit'))
    if name=='is_subject':return current not in world['subjects']
    raise ValueError(name)

def eligible(states,claimed=False,points=25,subjects=(),exists=True):
    region=[dict(owner=o,adj=[{'owner':x} for x in neighbors]) for o,neighbors in states]
    world=dict(exists=exists,region=region,claimed=claimed,points=points,subjects=subjects)
    return predicate(region_test,world,region)
buttons=load('common/scripted_buttons/nesnd_ottoman_claims.txt')
purchase=load('common/scripted_effects/nesnd_ottoman_recovery.txt').get('nesnd_ottoman_purchase_claim')
check('purchase rechecks the selected state before it can debit enthusiasm',purchase.get('if').get('limit').get('s:$STATE$').scalar('nesnd_ottoman_claim_target')=='yes')
for button in buttons.children:
    state_key='STATE_'+button.key.removeprefix('nesnd_ottoman_claim_').upper()
    check(button.key+' visibility and purchase use the same concrete target',
          button.get('visible').get('s:'+state_key).scalar('nesnd_ottoman_claim_target')=='yes' and
          button.get('effect').get('hidden_effect').get('nesnd_ottoman_purchase_claim').scalar('STATE')==state_key)
for own,adj,claimed,points,dep in product(['TUR','PER','EGY'],[False,True],[False,True],[0,24,25,100],[False,True]):
    exp=own!='TUR' and adj and not claimed and points>=25 and not (own=='EGY' and dep)
    check(f'{own}, adjacent {adj}, claimed {claimed}, enthusiasm {points}, subject Egypt {dep}',
          eligible([(own,['TUR'] if adj else ['PER'])],claimed,points,['EGY'] if dep else [])==exp)
check('noncontiguous split: eligible foreign piece must itself border Turkey',
      not eligible([('EGY',['TUR']),('PER',['RUS'])],subjects=['EGY']))
check('split foreign piece borders a directly owned Ottoman state',eligible([('TUR',[]),('PER',['TUR'])]))
check('Turkey has ceased to exist',not eligible([('PER',['TUR'])],exists=False))

# Reuse the project fixture that interprets actual ordered move effects. Import the
# VM class only, as the 1.13 suite also runs expectations for the old JE layout.
vm_source=reports/'diaspora-39/independent_accounting_tests.py'
tree=ast.parse(vm_source.read_text('utf-8-sig'))
vm_node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='VM')
effects=load('common/scripted_effects/nesnd_diaspora.txt')
namespace=dict(E=effects,copy=copy,math=math,operator=operator)
exec(compile(ast.Module(body=[vm_node],type_ignores=[]),str(vm_source),'exec'),namespace)
VM=namespace['VM']
for total,due,size,actual,expected in [(100000,98000,500000,None,10000),(100000,2000,500000,None,2000),(7,7,5,None,1),(100000,90000,400,0,0),(100000,90000,400,37,37)]:
    vm=VM()
    vm.g['nesnd_diaspora_total']=total
    vm.b['nesnd_diaspora_batch_bar']=100
    check(f'movement total {total}, due {due}, pop {size}, observed {actual}',vm.transfer(size,due,actual)==(expected,expected))
    check('only a real transfer resets the batch',vm.b['nesnd_diaspora_batch_bar']==(0 if expected else 100))
vm=VM();vm.g.update(nesnd_diaspora_open=True,nesnd_diaspora_total=100000,nesnd_diaspora_remaining=98000)
vm.b['nesnd_diaspora_batch_bar']=98
vm.run(effects.get('nesnd_diaspora_week'))
check('route changes at 98 retain preparation and outstanding population',
      vm.chosen==1 and vm.b['nesnd_diaspora_batch_bar']==98 and vm.g['nesnd_diaspora_remaining']==98000)
journal=load('common/journal_entries/nesnd_diaspora.txt').get('nesnd_diaspora')
check('all viewers can see the registered ongoing campaign',journal.get('should_show_when_not_involved').scalar('has_global_variable')=='nesnd_diaspora_open')
check('only original participants receive participation status',journal.get('should_be_involved').get('OR').scalar('nesnd_diaspora_receiver')=='yes')
outcomes=journal.all('outcome')
condition=outcomes[0].get('trigger').get('custom_tooltip').get('trigger_if')
check('successful outcome requires no outstanding measured debt, globally and in each surviving source',
    len(outcomes)==2 and outcomes[1].get('trigger').get('custom_tooltip').scalar('nesnd_diaspora_no_refuge')=='yes' and condition.get('global_var:nesnd_diaspora_remaining').op=='<=' and
    condition.scalar('global_var:nesnd_diaspora_remaining')=='0' and
    condition.get('NOT').get('any_country').scalar('nesnd_diaspora_can_depart')=='yes')
Path(__file__).with_name('results.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),'utf8')
print(len(checks),'checks passed',len(buttons.children),'Ottoman buttons')
