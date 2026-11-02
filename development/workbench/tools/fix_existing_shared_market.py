from japan_dev_context import *
from canon_prose_context import apply_proposals

proposal=json.loads(read(R/'market-model-existing-systems-proposals.json'))
for item in proposal['code_changes']:
    p=C/item['file'];s=read(p);assert s.count(item['find'])==item['count'],item['file']
    replacement=item['replace']
    if item['file'].endswith('nesnd_supply_triggers.txt'):
        replacement=replacement.replace('capital.market = { participants >= 2 }','trigger_if = { limit = { exists = capital.market } capital.market = { participants >= 2 } } trigger_else = { always = no }')
    write(p,s.replace(item['find'],replacement))
texts=proposal['localization']
# Native change_relations/add_modifier already expose these exact values.
# Do not reintroduce the author's rejected double listing in custom tooltips.
for key in ['nesnd_supply_accept_tt','nesnd_supply_invitation_tt']:texts.pop(key,None)
rows=apply_proposals(C,texts,extra_name='zzzzzz_nesnd_jp_final')
dump(R/'market-existing-applied.json',{'texts':texts,'rows':rows,'code_changes':proposal['code_changes'],'editorial_decision':'Keep existing short acceptance/invitation tooltip; native effects already expose +25 relations and -100 influence, so do not duplicate them.','main_changed_yet':False,'game_launched':False})
print('Actual shared-market qualification and contact-only cleanup repaired; no inventory logic introduced.')
