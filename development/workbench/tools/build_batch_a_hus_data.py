"""Author approved repetitive HUS database fields and narrow source insertions.

This is an editing tool, not a behavior test. The pre-edit snapshot is under the
batch report; no population files, main MOD files, or game sources are written.
"""
from pathlib import Path
import hashlib
import json
import re

W = Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
C = W / 'exports/canon-route-execution-20261104-a'
G = Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
R = W / 'reports/canon-route-execution-20261104'


def write(rel, text):
    p = C / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8-sig', newline='')


def block_end(text, start):
    depth = 0
    quoted = comment = escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if comment:
            if ch == '\n':
                comment = False
            continue
        if quoted:
            if escape:
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '#':
            comment = True
        elif ch == '"':
            quoted = True
        elif ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return i + 1
    raise ValueError('Unclosed source block')


write('common/law_groups/nesnd_hus_social_hierarchy.txt', '''lawgroup_nesnd_hus_social_hierarchy = {
    law_group_category = power_structure
    ideological_opinion_impact = 0.5
    affected_by_regime_change = no
    linked_social_hierarchy = nesnd_hus_social_hierarchy
    enable = { nesnd_hus_original_country = yes }
    change_allowed_trigger = { always = no }
}
''')
write('common/social_hierarchies/nesnd_hus_social_hierarchy.txt', '''nesnd_hus_social_hierarchy = {
    pop_criteria = { culture = { nesnd_hus_hierarchy_culture = yes } }
}
''')
professions = {
    'upper': 'aristocrats capitalists',
    'middle': 'academics bureaucrats clergymen engineers farmers officers shopkeepers',
    'lower': 'clerks laborers machinists peasants slaves soldiers',
}
classes = []
types = []
for culture in ('han', 'manchu', 'native', 'white'):
    for strata, jobs in professions.items():
        key = f'nesnd_hus_{culture}_{strata}'
        classes.append(f'''{key} = {{
    social_hierarchy = nesnd_hus_social_hierarchy
    strata = {strata}
    allowed_professions = {{ {jobs} }}
    pop_criteria = {{ culture = {{ nesnd_hus_{culture}_class_culture = yes }} }}
}}
''')
        for bound in ('min', 'max'):
            types.append(f'''country_{key}_acceptance_{bound}_add = {{
    decimals = 0
    color = good
    percent = no
    game_data = {{ ai_value = 0 tags = {{ cultural_acceptance }} }}
}}
''')
write('common/social_classes/nesnd_hus_social_classes.txt', '\n'.join(classes))
write('common/modifier_type_definitions/nesnd_hus_social_class_modifiers.txt', '\n'.join(types))

laws = []
for law, promoted, progress, icon in (
    ('four_tier_system', None, -75, 'enforced'),
    ('manchu_registration', 'manchu', -25, 'codified'),
    ('native_registration', 'native', -25, 'codified'),
):
    fields = []
    for culture, bounds in {'han': (80, 100), 'manchu': (60, 79), 'native': (40, 59), 'white': (20, 39)}.items():
        lo, hi = (80, 100) if culture == promoted else bounds
        for strata in professions:
            fields += [f'        country_nesnd_hus_{culture}_{strata}_acceptance_min_add = {lo}',
                       f'        country_nesnd_hus_{culture}_{strata}_acceptance_max_add = {hi}']
    laws.append(f'''law_nesnd_hus_{law} = {{
    group = lawgroup_nesnd_hus_social_hierarchy
    icon = "gfx/interface/icons/law_icons/social_hierarchy_{icon}.dds"
    progressiveness = {progress}
    is_visible = {{ nesnd_hus_original_country = yes }}
    can_enact = {{ always = no }}
    can_impose = {{ always = no }}
    ai_will_do = {{ always = no }}
    modifier = {{
{chr(10).join(fields)}
    }}
    on_activate = {{ nesnd_hus_clear_tiers = yes recalculate_pop_ig_support = yes }}
    on_deactivate = {{ nesnd_hus_clear_tiers = yes recalculate_pop_ig_support = yes }}
}}
''')
write('common/laws/nesnd_hus_social_hierarchy.txt', '\n'.join(laws))
legacy = []
for key in ('law_nesnd_hus_hierarchy', 'law_nesnd_hus_registry_manchu', 'law_nesnd_hus_registry_native'):
    legacy.append(f'''# Read-only save compatibility identity. Reconciler replaces this law on migration.
{key} = {{
    parent = law_cultural_exclusion
    group = lawgroup_citizenship
    icon = "gfx/interface/icons/law_icons/cultural_exclusion.dds"
    progressiveness = -10
    is_visible = {{ always = no }}
    can_enact = {{ always = no }}
    can_impose = {{ always = no }}
    ai_will_do = {{ always = no }}
    on_activate = {{ nesnd_hus_clear_tiers = yes }}
    on_deactivate = {{ nesnd_hus_clear_tiers = yes }}
}}
''')
write('common/laws/nesnd_hus_registration.txt', '\n'.join(legacy))

# The six existing replacements already preserve their native bodies.
p = C / 'common/laws/zzzz_nesnd_hus_citizenship_lock.txt'
s = p.read_text(encoding='utf-8-sig')
s = re.sub(r'(can_impose\s*=\s*\{\s*)nesnd_hus_citizenship_unlocked = yes',
           r'\1scope:target_country = { nesnd_hus_citizenship_unlocked = yes }', s)
write(p.relative_to(C).as_posix(), s)

# Add only the approved attitude block to each effective source object.
plan = (R / 'batch-a-hus-laws-plan.md').read_text(encoding='utf-8')
rows = re.findall(r'^\| `(ideology_[^`]+)` \| (EDO|CIT) \| (\w+) \| (\w+) \| \[([^:]+):', plan, re.M)
diffs = []
for filename in sorted({row[4] for row in rows}):
    rel = 'common/ideologies/' + filename
    src = C / rel if (C / rel).exists() else G / rel
    source_bytes = src.read_bytes()
    s = source_bytes.decode('utf-8-sig')
    edits = []
    for key, mapping, initial, registry, f in rows:
        if f != filename:
            continue
        m = re.search(r'^' + re.escape(key) + r'\s*=\s*\{', s, re.M)
        if not m:
            raise ValueError(f'Missing ideology source {key}')
        end = block_end(s, s.index('{', m.start()))
        body = s[m.start():end]
        if 'lawgroup_nesnd_hus_social_hierarchy' in body:
            raise ValueError('Attitude insertion already present; edit from recorded baseline')
        insertion = f'''\n\tlawgroup_nesnd_hus_social_hierarchy = {{
\t\tlaw_nesnd_hus_four_tier_system = {initial}
\t\tlaw_nesnd_hus_manchu_registration = {registry}
\t\tlaw_nesnd_hus_native_registration = {registry}
\t}}
'''
        edits.append((end - 1, insertion, key, mapping))
    for offset, insertion, _, _ in sorted(edits, reverse=True):
        s = s[:offset] + insertion + s[offset:]
    write(rel, s)
    diffs.append({'path': rel, 'source': src.as_posix(), 'source_sha256': hashlib.sha256(source_bytes).hexdigest(),
                  'operation': 'insert one attitude block before existing object closing brace; no existing source bytes intentionally removed',
                  'insertions': [{'ideology': key, 'mapping': mapping, 'source_char_offset': offset, 'text': insertion} for offset, insertion, key, mapping in edits]})
(R / 'batch-a-native-ideology-edit-manifest.json').write_text(json.dumps(diffs, ensure_ascii=False, indent=2), encoding='utf-8')

# Native GUI: clone one existing Edo header, with only the law-group name changed.
rel = 'gui/culture_panel.gui'
s = (G / rel).read_text(encoding='utf-8-sig')
needle = "GetPlayer.HasSpecialSocialHierarchyLawGroup('lawgroup_edo_social_system')"
at = s.index(needle)
start = s.rfind('\t\t\tacceptance_group_with_law_status = {', 0, at)
end = block_end(s, s.index('{', start))
header = s[start:end].replace('lawgroup_edo_social_system', 'lawgroup_nesnd_hus_social_hierarchy')
write(rel, s[:end] + '\n\n' + header + s[end:])

# Country definition insertion affects only HUS; history retains the native citizenship law.
rel = 'common/country_definitions/ce_countries.txt'
s = (C / rel).read_text(encoding='utf-8-sig')
m = re.search(r'^HUS\s*=\s*\{', s, re.M)
end = block_end(s, s.index('{', m.start()))
s = s[:end-1] + '\tsocial_hierarchy = nesnd_hus_social_hierarchy\n' + s[end-1:]
write(rel, s)
rel = 'common/history/countries/HUS.txt'
s = (C / rel).read_text(encoding='utf-8-sig').replace('activate_law = law_type:law_nesnd_hus_hierarchy', 'activate_law = law_type:law_cultural_exclusion')
at = s.index('\n\t\t# COOP')
s = s[:at] + '\n\t\tnesnd_hus_initialize_hierarchy = yes\n' + s[at:]
write(rel, s)
print('Authored hierarchy, 12 classes, 3 laws, legacy shells, citizenship target guards, ideology insertions, native header and HUS initialization.')
