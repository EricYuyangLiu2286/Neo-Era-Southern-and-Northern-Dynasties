from japan_dev_context import *
import re,datetime

archive=R/'withdrawn-procurement-20261102'
assert not archive.exists()
archive.mkdir()
before=man(C)
shutil.copytree(C,archive/'candidate-before-withdrawal')

def remove_nodes(rel, predicate):
    p=C/rel;s=read(p);nodes=[n for n in parse(s).walk() if predicate(n)]
    # Choose outermost matches so nested ranges cannot be removed twice.
    selected=[]
    for n in sorted(nodes,key=lambda n:(n.start,-n.end)):
        if not any(a.start<=n.start and n.end<=a.end for a in selected):selected.append(n)
    for n in sorted(selected,key=lambda n:n.start,reverse=True):s=s[:n.start]+s[n.end:]
    write(p,s)
    return len(selected)

def kind8(n):
    return any(x.key in {'nesnd_jp_request_kind','nesnd_jp_incoming_kind'} and x.value=='8' for x in n.walk())

rel='common/scripted_effects/nesnd_jp_foreign.txt'
removed=remove_nodes(rel,lambda n:n.key=='if' and n.get('limit') is not None and kind8(n.get('limit')))
# Refusal no longer has outcome-specific variants; accepting replies retain theirs.
p=C/rel;s=read(p);n=parse(s).get('nesnd_jp_refuse_request')
sub=[v for v in n.walk() if v.key=='save_scope_value_as' and v.scalar('name')=='jp_reply_kind']
for v in sorted(sub,key=lambda v:v.start,reverse=True):s=s[:v.start]+s[v.end:]
write(p,s)
rel='common/scripted_triggers/nesnd_jp_foreign.txt'
remove_nodes(rel,lambda n:n.key=='trigger_if' and n.get('limit') is not None and n.get('limit').scalar('nesnd_jp_request_kind')=='8')
p=C/rel;s=read(p).replace('nesnd_jp_request_kind <= 8','nesnd_jp_request_kind <= 7')
s=s.replace('OR = { nesnd_jp_request_kind = 4 nesnd_jp_request_kind = 8 }','nesnd_jp_request_kind = 4')
write(p,s)
rel='events/nesnd_jp_foreign.txt'
remove_nodes(rel,lambda n:(n.key=='triggered_desc' and (n.scalar('desc') or '').endswith('.d8')) or (n.key=='modifier' and n.get('trigger') is not None and kind8(n.get('trigger'))))
p=C/rel;s=read(p);n=parse(s).get('nesnd_jp_foreign.3').get('desc');s=s[:n.start]+'desc = nesnd_jp_foreign.3.d'+s[n.end:]
s=s.replace('OR = { nesnd_jp_incoming_kind = 4 nesnd_jp_incoming_kind = 8 }','nesnd_jp_incoming_kind = 4');write(p,s)
remove_nodes('common/scripted_effects/nesnd_jp_development.txt',lambda n:n.key=='nesnd_jp_ensure_procurement')
remove_nodes('common/scripted_triggers/nesnd_jp_industry.txt',lambda n:n.key=='nesnd_jp_wu_procurement_fulfilled')
remove_nodes('common/journal_entries/nesnd_jp_industry.txt',lambda n:n.key=='scripted_button' and n.value=='nesnd_jp_offer_wu_procurement')

deleted=[]
for folder in ['scripted_triggers','static_modifiers','scripted_effects','journal_entries','scripted_buttons','on_actions','scripted_progress_bars']:
    p=(C/'common'/folder/'nesnd_jp_procurement.txt').resolve()
    assert p.is_relative_to(C.resolve()) and p.is_file(),p
    assert p.name=='nesnd_jp_procurement.txt'
    p.unlink();deleted.append(p.relative_to(C).as_posix())

def rejected(k):
    return (k.startswith('nesnd_jp_procurement') or k.startswith('nesnd_jp_wu_procurement') or k in {'nesnd_jp_wu_supplier_contract','nesnd_jp_wu_buyer_contract','nesnd_jp_offer_wu_procurement','nesnd_jp_offer_wu_procurement_desc','nesnd_jp_foreign.1.d8','nesnd_jp_foreign.2.d8','nesnd_jp_foreign.3.d8'})
removed_loc=[]
for p in (C/'localization').rglob('*.yml'):
    s=read(p);lines=[]
    for line in s.splitlines(True):
        match=re.match(r'\s*([\w.]+):\d*\s*"',line)
        if match and rejected(match[1]):removed_loc.append({'file':str(p.relative_to(C)),'key':match[1]})
        else:lines.append(line)
    if ''.join(lines)!=s:write(p,''.join(lines))

left=[]
for p in [*(C/'common').rglob('*.txt'),*(C/'events').rglob('*.txt'),*(C/'localization').rglob('*.yml')]:
    s=read(p)
    if any(x in s for x in ['nesnd_jp_procurement','nesnd_jp_wu_procurement','nesnd_jp_wu_supplier_contract','nesnd_jp_wu_buyer_contract','nesnd_jp_offer_wu_procurement']):left.append(str(p))
assert not left,left
for rel in ['common/scripted_effects/nesnd_jp_foreign.txt','common/scripted_triggers/nesnd_jp_foreign.txt','events/nesnd_jp_foreign.txt']:
    t=parse(read(C/rel))
    assert not any(n.key in {'nesnd_jp_request_kind','nesnd_jp_incoming_kind'} and n.value=='8' for n in t.walk()),rel
dump(R/'procurement-withdrawal.json',{'user_instruction':'附属国不用采购宗主国军需；VIC3市场不是购买数量然后储存；不要加入类似日志。','archived_before':str(archive/'candidate-before-withdrawal'),'deleted_only_new_candidate_files':deleted,'removed_localization':removed_loc,'remaining_references':left,'main_was_never_modified_by_procurement':not any((M/p).exists() for p in deleted),'preserved':'industry buildings/working production, general development capital assistance, establishment, political identity and preview safety fixes','game_launched':False})
print('Removed procurement: 7 candidate files, all kind-8 paths, modifiers, payments, industry gates and texts. Main never contained it.')
